from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Optional, Dict, Any
from ..models.location import Location
from ..schemas.location import LocationCreate, LocationUpdate


class LocationService:
    """Service for managing warehouse locations"""
    
    @staticmethod
    def get_location(db: Session, location_id: int) -> Optional[Location]:
        """Get a location by ID"""
        return db.query(Location).filter(Location.id == location_id).first()
    
    @staticmethod
    def get_location_by_code(db: Session, code: str) -> Optional[Location]:
        """Get a location by code"""
        return db.query(Location).filter(Location.code == code).first()
    
    @staticmethod
    def get_locations(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        order_by: str = "code",
        order_desc: bool = False
    ) -> Dict[str, Any]:
        """
        Get locations with pagination, search, and sorting
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search term for code or description
            order_by: Field to order by (id, code, capacity, created_at)
            order_desc: Sort in descending order
            
        Returns:
            Dict with items, total, page, pages, limit
        """
        query = db.query(Location)
        
        # Search by code or description
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Location.code.ilike(search_filter),
                    Location.description.ilike(search_filter)
                )
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Sorting
        order_column = getattr(Location, order_by, Location.code)
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
    def create_location(db: Session, location: LocationCreate) -> Location:
        """Create a new location"""
        db_location = Location(
            code=location.code,
            description=location.description,
            capacity=location.capacity
        )
        
        db.add(db_location)
        db.commit()
        db.refresh(db_location)
        return db_location
    
    @staticmethod
    def update_location(db: Session, location_id: int, location: LocationUpdate) -> Optional[Location]:
        """Update an existing location"""
        db_location = db.query(Location).filter(Location.id == location_id).first()
        if not db_location:
            return None
        
        update_data = location.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_location, field, value)
        
        db.commit()
        db.refresh(db_location)
        return db_location
    
    @staticmethod
    def delete_location(db: Session, location_id: int) -> bool:
        """Delete a location"""
        db_location = db.query(Location).filter(Location.id == location_id).first()
        if not db_location:
            return False
        
        db.delete(db_location)
        db.commit()
        return True
    
    @staticmethod
    def get_available_capacity(db: Session, location_id: int) -> int:
        """
        Get available capacity for a location
        Returns: capacity - sum of inventory quantities
        """
        from ..models.inventory import Inventory
        
        location = LocationService.get_location(db, location_id)
        if not location:
            return 0
        
        # Calculate total used capacity
        used_capacity = db.query(func.sum(Inventory.quantity)).filter(
            Inventory.location_id == location_id
        ).scalar() or 0
        
        return location.capacity - used_capacity

