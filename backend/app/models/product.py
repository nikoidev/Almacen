from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Product(Base):
    """
    Product model - Represents items in the warehouse catalog
    
    Attributes:
        id: Primary key
        sku: Unique stock keeping unit identifier
        name: Product name
        description: Detailed product description
        category: Product category for grouping (e.g., 'Electronics', 'Clothing')
        price: Unit price
        min_stock_level: Minimum stock threshold for reorder alerts
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    category = Column(String(100), nullable=True, index=True)
    price = Column(Numeric(10, 2), nullable=False, default=0.00)
    min_stock_level = Column(Integer, nullable=False, default=10)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    inventory_items = relationship("Inventory", back_populates="product", cascade="all, delete-orphan")
    inbound_items = relationship("InboundShipmentItem", back_populates="product")
    outbound_items = relationship("OutboundOrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, sku='{self.sku}', name='{self.name}')>"

