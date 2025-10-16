from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base


class Supplier(Base):
    """
    Supplier model - Represents vendors/suppliers of products
    
    Attributes:
        id: Primary key
        name: Supplier company name
        contact_person: Name of contact person
        email: Supplier email address
        phone: Supplier phone number
        address: Physical address
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    __tablename__ = "suppliers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    contact_person = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(50), nullable=True)
    address = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    inbound_shipments = relationship("InboundShipment", back_populates="supplier")

    def __repr__(self):
        return f"<Supplier(id={self.id}, name='{self.name}')>"

