from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, Dict, Any, List
from ..models.inventory import Inventory
from ..models.product import Product
from ..models.location import Location
from ..schemas.inventory import (
    InventoryCreate, InventoryUpdate, InventoryAdjust, InventoryMove
)


class InventoryService:
    """
    Core service for inventory management
    
    This is the HEART of the warehouse system.
    All stock operations must go through this service to ensure consistency.
    """
    
    @staticmethod
    def get_inventory(db: Session, inventory_id: int) -> Optional[Inventory]:
        """Get an inventory record by ID"""
        return db.query(Inventory).filter(Inventory.id == inventory_id).first()
    
    @staticmethod
    def get_inventory_by_product_location(
        db: Session,
        product_id: int,
        location_id: int
    ) -> Optional[Inventory]:
        """Get inventory record for a specific product in a specific location"""
        return db.query(Inventory).filter(
            and_(
                Inventory.product_id == product_id,
                Inventory.location_id == location_id
            )
        ).first()
    
    @staticmethod
    def get_inventories(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        product_id: Optional[int] = None,
        location_id: Optional[int] = None,
        order_by: str = "id",
        order_desc: bool = False
    ) -> Dict[str, Any]:
        """
        Get inventory records with pagination and filters
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            product_id: Filter by product
            location_id: Filter by location
            order_by: Field to order by
            order_desc: Sort in descending order
            
        Returns:
            Dict with items, total, page, pages, limit
        """
        query = db.query(Inventory)
        
        # Filter by product
        if product_id:
            query = query.filter(Inventory.product_id == product_id)
        
        # Filter by location
        if location_id:
            query = query.filter(Inventory.location_id == location_id)
        
        # Get total count before pagination
        total = query.count()
        
        # Sorting
        order_column = getattr(Inventory, order_by, Inventory.id)
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
    def get_stock_level(
        db: Session,
        product_id: int,
        location_id: Optional[int] = None
    ) -> int:
        """
        Get total stock level for a product
        
        Args:
            product_id: Product ID
            location_id: Optional location filter (if None, returns total across all locations)
            
        Returns:
            Total quantity available
        """
        query = db.query(func.sum(Inventory.quantity)).filter(
            Inventory.product_id == product_id
        )
        
        if location_id:
            query = query.filter(Inventory.location_id == location_id)
        
        result = query.scalar()
        return result if result else 0
    
    @staticmethod
    def add_stock(
        db: Session,
        product_id: int,
        location_id: int,
        quantity: int,
        user_id: Optional[int] = None
    ) -> Inventory:
        """
        Add stock to inventory
        
        Creates a new inventory record if it doesn't exist,
        or updates the existing one.
        
        Args:
            db: Database session
            product_id: Product ID
            location_id: Location ID
            quantity: Quantity to add (must be positive)
            user_id: User performing the operation (for audit log)
            
        Returns:
            Updated or created Inventory record
            
        Raises:
            ValueError: If quantity is negative or location doesn't have capacity
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        # Check if product exists
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise ValueError(f"Product with ID {product_id} not found")
        
        # Check if location exists and has capacity
        location = db.query(Location).filter(Location.id == location_id).first()
        if not location:
            raise ValueError(f"Location with ID {location_id} not found")
        
        # Get or create inventory record
        inventory = InventoryService.get_inventory_by_product_location(
            db, product_id, location_id
        )
        
        if inventory:
            # Check location capacity
            new_total = inventory.quantity + quantity
            if new_total > location.capacity:
                raise ValueError(
                    f"Location capacity exceeded. "
                    f"Available: {location.capacity - inventory.quantity}, "
                    f"Requested: {quantity}"
                )
            
            inventory.quantity += quantity
        else:
            # Create new inventory record
            if quantity > location.capacity:
                raise ValueError(
                    f"Quantity exceeds location capacity. "
                    f"Capacity: {location.capacity}, Requested: {quantity}"
                )
            
            inventory = Inventory(
                product_id=product_id,
                location_id=location_id,
                quantity=quantity,
                reserved_quantity=0
            )
            db.add(inventory)
        
        db.commit()
        db.refresh(inventory)
        
        # TODO: Add audit log entry
        
        return inventory
    
    @staticmethod
    def remove_stock(
        db: Session,
        product_id: int,
        location_id: int,
        quantity: int,
        user_id: Optional[int] = None
    ) -> Inventory:
        """
        Remove stock from inventory
        
        Args:
            db: Database session
            product_id: Product ID
            location_id: Location ID
            quantity: Quantity to remove (must be positive)
            user_id: User performing the operation (for audit log)
            
        Returns:
            Updated Inventory record
            
        Raises:
            ValueError: If quantity is invalid or insufficient stock
        """
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        
        inventory = InventoryService.get_inventory_by_product_location(
            db, product_id, location_id
        )
        
        if not inventory:
            raise ValueError(
                f"No inventory found for product {product_id} "
                f"at location {location_id}"
            )
        
        available = inventory.quantity - inventory.reserved_quantity
        if quantity > available:
            raise ValueError(
                f"Insufficient stock. "
                f"Available: {available}, Requested: {quantity}"
            )
        
        inventory.quantity -= quantity
        
        db.commit()
        db.refresh(inventory)
        
        # TODO: Add audit log entry
        
        return inventory
    
    @staticmethod
    def move_stock(
        db: Session,
        move_data: InventoryMove,
        user_id: Optional[int] = None
    ) -> tuple[Inventory, Inventory]:
        """
        Move stock from one location to another
        
        This operation is ATOMIC - either both operations succeed or both fail.
        
        Args:
            db: Database session
            move_data: InventoryMove schema with product_id, from/to locations, quantity
            user_id: User performing the operation
            
        Returns:
            Tuple of (from_inventory, to_inventory)
            
        Raises:
            ValueError: If move is invalid
        """
        if move_data.from_location_id == move_data.to_location_id:
            raise ValueError("Source and destination locations must be different")
        
        try:
            # Remove from source (validates stock availability)
            from_inventory = InventoryService.remove_stock(
                db, 
                move_data.product_id, 
                move_data.from_location_id, 
                move_data.quantity,
                user_id
            )
            
            # Add to destination (validates capacity)
            to_inventory = InventoryService.add_stock(
                db,
                move_data.product_id,
                move_data.to_location_id,
                move_data.quantity,
                user_id
            )
            
            # TODO: Add audit log entry
            
            return from_inventory, to_inventory
            
        except Exception as e:
            db.rollback()
            raise ValueError(f"Failed to move stock: {str(e)}")
    
    @staticmethod
    def adjust_stock(
        db: Session,
        adjust_data: InventoryAdjust,
        user_id: Optional[int] = None
    ) -> Inventory:
        """
        Manually adjust stock quantity
        
        Use for corrections, cycle counts, etc.
        This REPLACES the current quantity with the new one.
        
        Args:
            db: Database session
            adjust_data: InventoryAdjust schema
            user_id: User performing the operation
            
        Returns:
            Updated Inventory record
        """
        inventory = InventoryService.get_inventory_by_product_location(
            db,
            adjust_data.product_id,
            adjust_data.location_id
        )
        
        if not inventory:
            # Create new inventory record
            return InventoryService.add_stock(
                db,
                adjust_data.product_id,
                adjust_data.location_id,
                adjust_data.quantity,
                user_id
            )
        
        # Validate new quantity doesn't exceed location capacity
        location = db.query(Location).filter(
            Location.id == adjust_data.location_id
        ).first()
        
        if adjust_data.quantity > location.capacity:
            raise ValueError(
                f"Quantity exceeds location capacity. "
                f"Capacity: {location.capacity}, Requested: {adjust_data.quantity}"
            )
        
        old_quantity = inventory.quantity
        inventory.quantity = adjust_data.quantity
        
        db.commit()
        db.refresh(inventory)
        
        # TODO: Add audit log entry with reason and old/new quantities
        
        return inventory
    
    @staticmethod
    def get_low_stock_products(db: Session) -> List[Dict[str, Any]]:
        """
        Get products with stock below minimum level
        
        Returns:
            List of dicts with product info and stock levels
        """
        # Query products with their total stock
        query = (
            db.query(
                Product.id,
                Product.sku,
                Product.name,
                Product.min_stock_level,
                func.sum(Inventory.quantity).label('current_stock')
            )
            .outerjoin(Inventory, Product.id == Inventory.product_id)
            .group_by(Product.id)
            .having(
                func.coalesce(func.sum(Inventory.quantity), 0) < Product.min_stock_level
            )
        )
        
        results = query.all()
        
        return [
            {
                "product_id": r.id,
                "product_sku": r.sku,
                "product_name": r.name,
                "min_stock_level": r.min_stock_level,
                "current_stock": r.current_stock or 0,
                "difference": r.min_stock_level - (r.current_stock or 0)
            }
            for r in results
        ]
    
    @staticmethod
    def reserve_stock(
        db: Session,
        product_id: int,
        location_id: int,
        quantity: int
    ) -> Inventory:
        """
        Reserve stock for an order (without removing it from inventory)
        
        Used when creating an outbound order - stock is marked as reserved
        until picking is completed.
        """
        inventory = InventoryService.get_inventory_by_product_location(
            db, product_id, location_id
        )
        
        if not inventory:
            raise ValueError("Inventory record not found")
        
        available = inventory.quantity - inventory.reserved_quantity
        if quantity > available:
            raise ValueError(
                f"Insufficient available stock. "
                f"Available: {available}, Requested: {quantity}"
            )
        
        inventory.reserved_quantity += quantity
        
        db.commit()
        db.refresh(inventory)
        
        return inventory
    
    @staticmethod
    def unreserve_stock(
        db: Session,
        product_id: int,
        location_id: int,
        quantity: int
    ) -> Inventory:
        """
        Release reserved stock (e.g., when an order is cancelled)
        """
        inventory = InventoryService.get_inventory_by_product_location(
            db, product_id, location_id
        )
        
        if not inventory:
            raise ValueError("Inventory record not found")
        
        if quantity > inventory.reserved_quantity:
            raise ValueError("Cannot unreserve more than currently reserved")
        
        inventory.reserved_quantity -= quantity
        
        db.commit()
        db.refresh(inventory)
        
        return inventory

