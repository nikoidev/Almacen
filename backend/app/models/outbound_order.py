from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..core.database import Base
import enum


class OrderStatus(str, enum.Enum):
    """Enum for outbound order statuses"""
    PENDING = "PENDIENTE"
    PICKING = "EN_PICKING"
    PACKED = "EMPACADO"
    SHIPPED = "ENVIADO"


class OutboundOrder(Base):
    """
    OutboundOrder model - Represents orders to be shipped out
    
    Attributes:
        id: Primary key
        customer_name: Name of the customer/recipient
        status: Current order status (PENDIENTE, EN_PICKING, EMPACADO, ENVIADO)
        created_at: Timestamp of creation
        shipped_at: Timestamp when order was shipped (nullable until shipped)
    """
    __tablename__ = "outbound_orders"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(255), nullable=False, index=True)
    status = Column(SQLEnum(OrderStatus), nullable=False, default=OrderStatus.PENDING, index=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    shipped_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    items = relationship("OutboundOrderItem", back_populates="order", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<OutboundOrder(id={self.id}, customer='{self.customer_name}', status={self.status})>"


class OutboundOrderItem(Base):
    """
    OutboundOrderItem model - Line items for outbound orders
    
    Attributes:
        id: Primary key
        order_id: Foreign key to OutboundOrder
        product_id: Foreign key to Product
        location_id: Foreign key to Location (where to pick from)
        quantity_ordered: Quantity requested in the order
        quantity_picked: Quantity actually picked (0 until picking is done)
    """
    __tablename__ = "outbound_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("outbound_orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    location_id = Column(Integer, ForeignKey("locations.id"), nullable=False, index=True)
    quantity_ordered = Column(Integer, nullable=False)
    quantity_picked = Column(Integer, nullable=False, default=0)

    # Relationships
    order = relationship("OutboundOrder", back_populates="items")
    product = relationship("Product", back_populates="outbound_items")
    location = relationship("Location", back_populates="outbound_items")

    def __repr__(self):
        return f"<OutboundOrderItem(order_id={self.order_id}, product_id={self.product_id}, ordered={self.quantity_ordered})>"

