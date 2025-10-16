from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, Dict, Any
from datetime import datetime
from ..models.inbound_shipment import InboundShipment, InboundShipmentItem, ShipmentStatus
from ..schemas.shipment import (
    InboundShipmentCreate, InboundShipmentUpdate, InboundShipmentReceive
)
from .inventory_service import InventoryService


class ShipmentService:
    """
    Service for managing inbound shipments (receiving goods from suppliers)
    """
    
    @staticmethod
    def get_shipment(db: Session, shipment_id: int) -> Optional[InboundShipment]:
        """Get a shipment by ID"""
        return db.query(InboundShipment).filter(InboundShipment.id == shipment_id).first()
    
    @staticmethod
    def get_shipments(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        supplier_id: Optional[int] = None,
        status: Optional[ShipmentStatus] = None,
        order_by: str = "id",
        order_desc: bool = False
    ) -> Dict[str, Any]:
        """
        Get shipments with pagination, filters, and sorting
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            supplier_id: Filter by supplier
            status: Filter by status (PENDIENTE, EN_PROCESO, COMPLETADO)
            order_by: Field to order by
            order_desc: Sort in descending order
            
        Returns:
            Dict with items, total, page, pages, limit
        """
        query = db.query(InboundShipment)
        
        # Filter by supplier
        if supplier_id:
            query = query.filter(InboundShipment.supplier_id == supplier_id)
        
        # Filter by status
        if status:
            query = query.filter(InboundShipment.status == status)
        
        # Get total count before pagination
        total = query.count()
        
        # Sorting
        order_column = getattr(InboundShipment, order_by, InboundShipment.id)
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
    def create_shipment(
        db: Session,
        shipment_data: InboundShipmentCreate,
        user_id: Optional[int] = None
    ) -> InboundShipment:
        """
        Create a new inbound shipment with items
        
        Args:
            db: Database session
            shipment_data: Shipment data including items
            user_id: User creating the shipment
            
        Returns:
            Created InboundShipment with items
        """
        # Create shipment
        db_shipment = InboundShipment(
            supplier_id=shipment_data.supplier_id,
            expected_at=shipment_data.expected_at,
            status=ShipmentStatus.PENDING
        )
        
        db.add(db_shipment)
        db.flush()  # Get shipment ID without committing
        
        # Create shipment items
        for item_data in shipment_data.items:
            db_item = InboundShipmentItem(
                shipment_id=db_shipment.id,
                product_id=item_data.product_id,
                location_id=item_data.location_id,
                quantity_expected=item_data.quantity_expected,
                quantity_received=0
            )
            db.add(db_item)
        
        db.commit()
        db.refresh(db_shipment)
        
        # TODO: Add audit log entry
        
        return db_shipment
    
    @staticmethod
    def update_shipment(
        db: Session,
        shipment_id: int,
        shipment_data: InboundShipmentUpdate,
        user_id: Optional[int] = None
    ) -> Optional[InboundShipment]:
        """Update an existing shipment"""
        db_shipment = db.query(InboundShipment).filter(
            InboundShipment.id == shipment_id
        ).first()
        
        if not db_shipment:
            return None
        
        # Cannot update completed shipments
        if db_shipment.status == ShipmentStatus.COMPLETED:
            raise ValueError("Cannot update completed shipment")
        
        update_data = shipment_data.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if field == "status" and value:
                # Validate status transition
                value = ShipmentStatus(value)
            setattr(db_shipment, field, value)
        
        db.commit()
        db.refresh(db_shipment)
        
        # TODO: Add audit log entry
        
        return db_shipment
    
    @staticmethod
    def delete_shipment(db: Session, shipment_id: int) -> bool:
        """
        Delete a shipment
        
        Only pending shipments can be deleted.
        """
        db_shipment = db.query(InboundShipment).filter(
            InboundShipment.id == shipment_id
        ).first()
        
        if not db_shipment:
            return False
        
        if db_shipment.status != ShipmentStatus.PENDING:
            raise ValueError("Can only delete pending shipments")
        
        db.delete(db_shipment)
        db.commit()
        return True
    
    @staticmethod
    def receive_shipment(
        db: Session,
        shipment_id: int,
        receive_data: InboundShipmentReceive,
        user_id: Optional[int] = None
    ) -> InboundShipment:
        """
        Process receiving of a shipment
        
        This is a CRITICAL operation that:
        1. Updates quantities received in shipment items
        2. Adds stock to inventory for each item
        3. Marks shipment as completed
        4. All operations are ATOMIC
        
        Args:
            db: Database session
            shipment_id: Shipment ID to receive
            receive_data: Data with actual quantities received per item
            user_id: User processing the reception
            
        Returns:
            Updated shipment
            
        Raises:
            ValueError: If shipment not found, already completed, or validation fails
        """
        db_shipment = ShipmentService.get_shipment(db, shipment_id)
        
        if not db_shipment:
            raise ValueError(f"Shipment {shipment_id} not found")
        
        if db_shipment.status == ShipmentStatus.COMPLETED:
            raise ValueError("Shipment already completed")
        
        try:
            # Update shipment status
            db_shipment.status = ShipmentStatus.IN_PROGRESS
            db.flush()
            
            # Process each item
            for receive_item in receive_data.items:
                # Find the corresponding shipment item
                shipment_item = next(
                    (item for item in db_shipment.items 
                     if item.product_id == receive_item.product_id),
                    None
                )
                
                if not shipment_item:
                    raise ValueError(
                        f"Product {receive_item.product_id} not found in shipment"
                    )
                
                # Update quantity received
                shipment_item.quantity_received = receive_item.quantity_received
                
                # Add to inventory if quantity received > 0
                if receive_item.quantity_received > 0:
                    InventoryService.add_stock(
                        db,
                        product_id=shipment_item.product_id,
                        location_id=shipment_item.location_id,
                        quantity=receive_item.quantity_received,
                        user_id=user_id
                    )
            
            # Mark shipment as completed
            db_shipment.status = ShipmentStatus.COMPLETED
            db_shipment.received_at = datetime.utcnow()
            
            db.commit()
            db.refresh(db_shipment)
            
            # TODO: Add audit log entry
            
            return db_shipment
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to receive shipment: {str(e)}")
    
    @staticmethod
    def get_shipment_items(
        db: Session,
        shipment_id: int
    ) -> list[InboundShipmentItem]:
        """Get all items for a shipment"""
        return db.query(InboundShipmentItem).filter(
            InboundShipmentItem.shipment_id == shipment_id
        ).all()

