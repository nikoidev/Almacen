from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class ShipmentStatus(str, enum.Enum):
    """Enum for inbound shipment statuses"""
    PENDING = "PENDIENTE"
    IN_PROGRESS = "EN_PROCESO"
    COMPLETED = "COMPLETADO"


class InboundShipment(Base):
    """
    InboundShipment model - Represents incoming shipments from suppliers
    
    Attributes:
        id: Primary key
        supplier_id: Foreign key to Supplier
        status: Current shipment status (PENDIENTE, EN_PROCESO, COMPLETADO)
        expected_at: Expected arrival date/time
        received_at: Actual receipt date/time (nullable until completed)
        created_at: Timestamp of creation
    """
    __tablename__ = "inbound_shipments"

    id = Column(Integer, primary_key=True, index=True)
    supplier_id = Column(Integer, ForeignKey("suppliers.id"), nullable=False, index=True)
    status = Column(SQLEnum(ShipmentStatus), nullable=False, default=ShipmentStatus.PENDING, index=True)
    expected_at = Column(DateTime(timezone=True), nullable=True)
    received_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relationships
    supplier = relationship("Supplier", back_populates="inbound_shipments")
    items = relationship("InboundShipmentItem", back_populates="shipment", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<InboundShipment(id={self.id}, supplier_id={self.supplier_id}, status={self.status})>"


class InboundShipmentItem(Base):
    """
    InboundShipmentItem model - Line items for inbound shipments
    
    Attributes:
        id: Primary key
        shipment_id: Foreign key to InboundShipment
        product_id: Foreign key to Product
        location_id: Foreign key to Location (where to store the product)
        quantity_expected: Expected quantity to receive
        quantity_received: Actual quantity received (0 until processed)
    """
    __tablename__ = "inbound_shipment_items"

    id = Column(Integer, primary_key=True, index=True)
    shipment_id = Column(Integer, ForeignKey("inbound_shipments.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    quantity_expected = Column(Integer, nullable=False)
    quantity_received = Column(Integer, nullable=False, default=0)

    # Relationships
    shipment = relationship("InboundShipment", back_populates="items")
    product = relationship("Product", back_populates="inbound_items")
    location = relationship("Location", back_populates="inbound_items")

    def __repr__(self):
        return f"<InboundShipmentItem(shipment_id={self.shipment_id}, product_id={self.product_id}, expected={self.quantity_expected})>"

