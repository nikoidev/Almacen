from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import Optional, Dict, Any
from ..models.product import Product
from ..schemas.product import ProductCreate, ProductUpdate


class ProductService:
    """Service for managing products in the warehouse"""
    
    @staticmethod
    def get_product(db: Session, product_id: int) -> Optional[Product]:
        """Get a product by ID"""
        return db.query(Product).filter(Product.id == product_id).first()
    
    @staticmethod
    def get_product_by_sku(db: Session, sku: str) -> Optional[Product]:
        """Get a product by SKU"""
        return db.query(Product).filter(Product.sku == sku).first()
    
    @staticmethod
    def get_products(
        db: Session,
        skip: int = 0,
        limit: int = 100,
        search: Optional[str] = None,
        category: Optional[str] = None,
        order_by: str = "id",
        order_desc: bool = False
    ) -> Dict[str, Any]:
        """
        Get products with pagination, search, filters, and sorting
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            search: Search term for SKU or name
            category: Filter by category
            order_by: Field to order by (id, sku, name, price, created_at)
            order_desc: Sort in descending order
            
        Returns:
            Dict with items, total, page, pages, limit
        """
        query = db.query(Product)
        
        # Search by SKU or name
        if search:
            search_filter = f"%{search}%"
            query = query.filter(
                or_(
                    Product.sku.ilike(search_filter),
                    Product.name.ilike(search_filter)
                )
            )
        
        # Filter by category
        if category:
            query = query.filter(Product.category == category)
        
        # Get total count before pagination
        total = query.count()
        
        # Sorting
        order_column = getattr(Product, order_by, Product.id)
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
    def create_product(db: Session, product: ProductCreate) -> Product:
        """Create a new product"""
        db_product = Product(
            sku=product.sku,
            name=product.name,
            description=product.description,
            category=product.category,
            price=product.price,
            min_stock_level=product.min_stock_level
        )
        
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def update_product(db: Session, product_id: int, product: ProductUpdate) -> Optional[Product]:
        """Update an existing product"""
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return None
        
        update_data = product.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(db_product, field, value)
        
        db.commit()
        db.refresh(db_product)
        return db_product
    
    @staticmethod
    def delete_product(db: Session, product_id: int) -> bool:
        """Delete a product"""
        db_product = db.query(Product).filter(Product.id == product_id).first()
        if not db_product:
            return False
        
        db.delete(db_product)
        db.commit()
        return True
    
    @staticmethod
    def get_categories(db: Session) -> list[str]:
        """Get all unique product categories"""
        categories = db.query(Product.category).distinct().filter(Product.category.isnot(None)).all()
        return [cat[0] for cat in categories]

