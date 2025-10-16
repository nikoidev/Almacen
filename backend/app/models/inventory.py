from sqlalchemy import Column, Integer, ForeignKey, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Inventory(Base):
    """
    Inventory model - Core table tracking stock levels by product and location
    
    Attributes:
        id: Primary key
        product_id: Foreign key to Product
        location_id: Foreign key to Location
        quantity: Current stock quantity
        reserved_quantity: Stock reserved for pending orders (not yet picked)
        last_updated: Timestamp of last stock update
        
    Constraints:
        - Unique constraint on (product_id, location_id) - one inventory record per product per location
    """
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False, default=0)
    reserved_quantity = Column(Integer, nullable=False, default=0)
    
    last_updated = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    product = relationship("Product", back_populates="inventory_items")
    location = relationship("Location", back_populates="inventory_items")

    # Constraints
    __table_args__ = (
        UniqueConstraint('product_id', 'location_id', name='uix_product_location'),
    )

    @property
    def available_quantity(self):
        """Returns quantity available for picking (total - reserved)"""
        return self.quantity - self.reserved_quantity

    def __repr__(self):
        return f"<Inventory(product_id={self.product_id}, location_id={self.location_id}, qty={self.quantity})>"

