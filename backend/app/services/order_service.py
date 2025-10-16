from sqlalchemy.orm import Session
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.outbound_order import OutboundOrder, OutboundOrderItem, OrderStatus
from ..schemas.order import OutboundOrderCreate, OutboundOrderUpdate, OutboundOrderPick
from .inventory_service import InventoryService


class OrderService:
    """
    Service for managing outbound orders (shipping goods to customers)
    """
    
    @staticmethod
    def get_order(db: Session, order_id: int) -> Optional[OutboundOrder]:
        """Get an order by ID"""
        return db.query(OutboundOrder).filter(OutboundOrder.id == order_id).first()
    
    @staticmethod
    def get_orders(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        customer_name: Optional[str] = None,
        status: Optional[OrderStatus] = None,
        order_by: str = "id",
        order_desc: bool = False
    ) -> Dict[str, Any]:
        """
        Get orders with pagination, filters, and sorting
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            customer_name: Filter by customer name (partial match)
            status: Filter by status
            order_by: Field to order by
            order_desc: Sort in descending order
            
        Returns:
            Dict with items, total, page, pages, limit
        """
        query = db.query(OutboundOrder)
        
        # Filter by customer name
        if customer_name:
            search_filter = f"%{customer_name}%"
            query = query.filter(OutboundOrder.customer_name.ilike(search_filter))
        
        # Filter by status
        if status:
            query = query.filter(OutboundOrder.status == status)
        
        # Get total count before pagination
        total = query.count()
        
        # Sorting
        order_column = getattr(OutboundOrder, order_by, OutboundOrder.id)
        if order_desc:
            query = query.order_by(order_column.desc())
        else:
            query = query.order_by(order_column.asc())
        
        # Pagination
        items = query.offset(skip).limit(limit).all()
        
        # Calculate pagination info
        page = (skip // limit) + 1 if limit > 0 else 1
        pages = (total + limit - 1) // limit if limit > 0 else 1
        
        return {
            "items": items,
            "total": total,
            "page": page,
            "pages": pages,
            "limit": limit
        }
    
    @staticmethod
    def create_order(
        db: Session,
        order_data: OutboundOrderCreate,
        user_id: Optional[int] = None
    ) -> OutboundOrder:
        """
        Create a new outbound order with items
        
        This RESERVES stock for the order items.
        Stock is reserved but not removed until picking is completed.
        
        Args:
            db: Database session
            order_data: Order data including items
            user_id: User creating the order
            
        Returns:
            Created OutboundOrder with items
            
        Raises:
            ValueError: If insufficient stock for any item
        """
        try:
            # Create order
            db_order = OutboundOrder(
                customer_name=order_data.customer_name,
                status=OrderStatus.PENDING
            )
            
            db.add(db_order)
            db.flush()  # Get order ID without committing
            
            # Create order items and reserve stock
            for item_data in order_data.items:
                # Reserve stock
                InventoryService.reserve_stock(
                    db,
                    product_id=item_data.product_id,
                    location_id=item_data.location_id,
                    quantity=item_data.quantity_ordered
                )
                
                # Create order item
                db_item = OutboundOrderItem(
                    order_id=db_order.id,
                    product_id=item_data.product_id,
                    location_id=item_data.location_id,
                    quantity_ordered=item_data.quantity_ordered,
                    quantity_picked=0
                )
                db.add(db_item)
            
            db.commit()
            db.refresh(db_order)
            
            # TODO: Add audit log entry
            
            return db_order
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to create order: {str(e)}")
    
    @staticmethod
    def update_order(
        db: Session,
        order_id: int,
        order_data: OutboundOrderUpdate,
        user_id: Optional[int] = None
    ) -> Optional[OutboundOrder]:
        """Update an existing order"""
        db_order = db.query(OutboundOrder).filter(
            OutboundOrder.id == order_id
        ).first()
        
        if not db_order:
            return None
        
        # Cannot update shipped orders
        if db_order.status == OrderStatus.SHIPPED:
            raise ValueError("Cannot update shipped order")
        
        update_data = order_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == "status" and value:
                # Validate status transition
                value = OrderStatus(value)
            setattr(db_order, field, value)
        
        db.commit()
        db.refresh(db_order)
        
        # TODO: Add audit log entry
        
        return db_order
    
    @staticmethod
    def delete_order(db: Session, order_id: int) -> bool:
        """
        Delete an order
        
        Only pending orders can be deleted.
        This will UNRESERVE the stock.
        """
        db_order = db.query(OutboundOrder).filter(
            OutboundOrder.id == order_id
        ).first()
        
        if not db_order:
            return False
        
        if db_order.status != OrderStatus.PENDING:
            raise ValueError("Can only delete pending orders")
        
        try:
            # Unreserve stock for all items
            for item in db_order.items:
                InventoryService.unreserve_stock(
                    db,
                    product_id=item.product_id,
                    location_id=item.location_id,
                    quantity=item.quantity_ordered
                )
            
            db.delete(db_order)
            db.commit()
            return True
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to delete order: {str(e)}")
    
    @staticmethod
    def pick_order(
        db: Session,
        order_id: int,
        pick_data: OutboundOrderPick,
        user_id: Optional[int] = None
    ) -> OutboundOrder:
        """
        Process picking of an order
        
        This is a CRITICAL operation that:
        1. Updates quantities picked in order items
        2. Removes stock from inventory for each item
        3. Unreserves the stock
        4. Marks order status appropriately
        5. All operations are ATOMIC
        
        Args:
            db: Database session
            order_id: Order ID to pick
            pick_data: Data with actual quantities picked per item
            user_id: User performing the picking
            
        Returns:
            Updated order
            
        Raises:
            ValueError: If order not found, already shipped, or validation fails
        """
        db_order = OrderService.get_order(db, order_id)
        
        if not db_order:
            raise ValueError(f"Order {order_id} not found")
        
        if db_order.status == OrderStatus.SHIPPED:
            raise ValueError("Order already shipped")
        
        try:
            # Update order status
            db_order.status = OrderStatus.PICKING
            db.flush()
            
            # Process each item
            for pick_item in pick_data.items:
                # Find the corresponding order item
                order_item = next(
                    (item for item in db_order.items 
                     if item.product_id == pick_item.product_id),
                    None
                )
                
                if not order_item:
                    raise ValueError(
                        f"Product {pick_item.product_id} not found in order"
                    )
                
                # Update quantity picked
                order_item.quantity_picked = pick_item.quantity_picked
                
                # Unreserve the originally reserved quantity
                InventoryService.unreserve_stock(
                    db,
                    product_id=order_item.product_id,
                    location_id=order_item.location_id,
                    quantity=order_item.quantity_ordered
                )
                
                # Remove picked quantity from inventory
                if pick_item.quantity_picked > 0:
                    InventoryService.remove_stock(
                        db,
                        product_id=order_item.product_id,
                        location_id=order_item.location_id,
                        quantity=pick_item.quantity_picked,
                        user_id=user_id
                    )
            
            # Mark order as packed (ready to ship)
            db_order.status = OrderStatus.PACKED
            
            db.commit()
            db.refresh(db_order)
            
            # TODO: Add audit log entry
            
            return db_order
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to pick order: {str(e)}")
    
    @staticmethod
    def ship_order(
        db: Session,
        order_id: int,
        user_id: Optional[int] = None
    ) -> OutboundOrder:
        """
        Mark an order as shipped
        
        Order must be in PACKED status.
        """
        db_order = OrderService.get_order(db, order_id)
        
        if not db_order:
            raise ValueError(f"Order {order_id} not found")
        
        if db_order.status != OrderStatus.PACKED:
            raise ValueError("Order must be packed before shipping")
        
        db_order.status = OrderStatus.SHIPPED
        db_order.shipped_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_order)
        
        # TODO: Add audit log entry
        
        return db_order
    
    @staticmethod
    def get_order_items(
        db: Session,
        order_id: int
    ) -> list[OutboundOrderItem]:
        """Get all items for an order"""
        return db.query(OutboundOrderItem).filter(
            OutboundOrderItem.order_id == order_id
        ).all()

