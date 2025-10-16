from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Location(Base):
    """
    Location model - Represents physical storage locations in the warehouse
    
    Attributes:
        id: Primary key
        code: Unique location code (e.g., 'A1-R2-S3' for Aisle 1, Rack 2, Shelf 3)
        description: Human-readable description (e.g., 'Aisle 1, Rack 2')
        capacity: Maximum units that can be stored
        created_at: Timestamp of creation
    """
    __tablename__ = "locations"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(50), unique=True, index=True, nullable=False)
    description = Column(String(255), nullable=True)
    capacity = Column(Integer, nullable=False, default=100)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    inventory_items = relationship("Inventory", back_populates="location", cascade="all, delete-orphan")
    inbound_items = relationship("InboundShipmentItem", back_populates="location")
    outbound_items = relationship("OutboundOrderItem", back_populates="location")

    def __repr__(self):
        return f"<Location(id={self.id}, code='{self.code}', capacity={self.capacity})>"

