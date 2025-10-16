from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, Dict, Any
from ..models.supplier import Supplier
from ..schemas.supplier import SupplierCreate, SupplierUpdate


class SupplierService:
    """Service for managing suppliers"""
    
    @staticmethod
    def get_supplier(db: Session, supplier_id: int) -> Optional[Supplier]:
        """Get a supplier by ID"""
        return db.query(Supplier).filter(Supplier.id == supplier_id).first()
    
    @staticmethod
    def get_supplier_by_name(db: Session, name: str) -> Optional[Supplier]:
        """Get a supplier by name"""
        return db.query(Supplier).filter(Supplier.name == name).first()
    
    @staticmethod
    def get_suppliers(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        order_by: str = "id",
        order_desc: bool = False
    ) -> Dict[str, Any]:
        """
        Get suppliers with pagination, search, and sorting
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search term for name, contact person, or email
            order_by: Field to order by (id, name, created_at)
            order_desc: Sort in descending order
            
        Returns:
            Dict with items, total, page, pages, limit
        """
        query = db.query(Supplier)
        
        # Search by name, contact person, or email
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Supplier.name.ilike(search_filter),
                    Supplier.contact_person.ilike(search_filter),
                    Supplier.email.ilike(search_filter)
                )
            )
        
        # Get total count before pagination
        total = query.count()
        
        # Sorting
        order_column = getattr(Supplier, order_by, Supplier.id)
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
    def create_supplier(db: Session, supplier: SupplierCreate) -> Supplier:
        """Create a new supplier"""
        db_supplier = Supplier(
            name=supplier.name,
            contact_person=supplier.contact_person,
            email=supplier.email,
            phone=supplier.phone,
            address=supplier.address
        )
        
        db.add(db_supplier)
        db.commit()
        db.refresh(db_supplier)
        return db_supplier
    
    @staticmethod
    def update_supplier(db: Session, supplier_id: int, supplier: SupplierUpdate) -> Optional[Supplier]:
        """Update an existing supplier"""
        db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not db_supplier:
            return None
        
        update_data = supplier.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_supplier, field, value)
        
        db.commit()
        db.refresh(db_supplier)
        return db_supplier
    
    @staticmethod
    def delete_supplier(db: Session, supplier_id: int) -> bool:
        """Delete a supplier"""
        db_supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if not db_supplier:
            return False
        
        db.delete(db_supplier)
        db.commit()
        return True

