from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .product import ProductInInventory
from .location import LocationInInventory


class OutboundOrderItemBase(BaseModel):
    """Base schema for Outbound Order Item"""
    product_id: int
    location_id: int
    quantity_ordered: int = Field(..., gt=0, description="Quantity requested in the order")


class OutboundOrderItemCreate(OutboundOrderItemBase):
    """Schema for creating an order item"""
    pass


class OutboundOrderItemPick(BaseModel):
    """Schema for picking an order item"""
    product_id: int
    quantity_picked: int = Field(..., ge=0, description="Actual quantity picked")


class OutboundOrderItemResponse(OutboundOrderItemBase):
    """Schema for order item response"""
    id: int
    order_id: int
    quantity_picked: int
    product: ProductInInventory
    location: LocationInInventory

    class Config:
        from_attributes = True


class OutboundOrderBase(BaseModel):
    """Base schema for Outbound Order"""
    customer_name: str = Field(..., min_length=1, max_length=255, description="Name of the customer/recipient")


class OutboundOrderCreate(OutboundOrderBase):
    """Schema for creating a new outbound order"""
    items: List[OutboundOrderItemCreate] = Field(..., min_length=1, description="List of items in the order")


class OutboundOrderUpdate(BaseModel):
    """Schema for updating an outbound order"""
    customer_name: Optional[str] = Field(None, min_length=1, max_length=255)
    status: Optional[str] = Field(None, pattern="^(PENDIENTE|EN_PICKING|EMPACADO|ENVIADO)$")


class OutboundOrderPick(BaseModel):
    """Schema for performing picking on an order"""
    items: List[OutboundOrderItemPick] = Field(..., min_length=1, description="Items being picked with actual quantities")


class OutboundOrderResponse(OutboundOrderBase):
    """Schema for outbound order response"""
    id: int
    status: str
    created_at: datetime
    shipped_at: Optional[datetime] = None
    items: List[OutboundOrderItemResponse] = []

    class Config:
        from_attributes = True


class OutboundOrderListResponse(BaseModel):
    """Paginated response for outbound order list"""
    items: List[OutboundOrderResponse]
    total: int
    page: int
    pages: int
    limit: int

