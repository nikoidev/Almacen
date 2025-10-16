from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .supplier import SupplierInShipment
from .product import ProductInInventory
from .location import LocationInInventory


class InboundShipmentItemBase(BaseModel):
    """Base schema for Inbound Shipment Item"""
    product_id: int
    location_id: int
    quantity_expected: int = Field(..., gt=0, description="Expected quantity to receive")


class InboundShipmentItemCreate(InboundShipmentItemBase):
    """Schema for creating a shipment item"""
    pass


class InboundShipmentItemReceive(BaseModel):
    """Schema for receiving a shipment item"""
    product_id: int
    quantity_received: int = Field(..., ge=0, description="Actual quantity received")


class InboundShipmentItemResponse(InboundShipmentItemBase):
    """Schema for shipment item response"""
    id: int
    shipment_id: int
    quantity_received: int
    product: ProductInInventory
    location: LocationInInventory

    class Config:
        from_attributes = True


class InboundShipmentBase(BaseModel):
    """Base schema for Inbound Shipment"""
    supplier_id: int
    expected_at: Optional[datetime] = Field(None, description="Expected arrival date/time")


class InboundShipmentCreate(InboundShipmentBase):
    """Schema for creating a new inbound shipment"""
    items: List[InboundShipmentItemCreate] = Field(..., min_length=1, description="List of items in the shipment")


class InboundShipmentUpdate(BaseModel):
    """Schema for updating an inbound shipment"""
    supplier_id: Optional[int] = None
    expected_at: Optional[datetime] = None
    status: Optional[str] = Field(None, pattern="^(PENDIENTE|EN_PROCESO|COMPLETADO)$")


class InboundShipmentReceive(BaseModel):
    """Schema for receiving/processing a shipment"""
    items: List[InboundShipmentItemReceive] = Field(..., min_length=1, description="Items being received with actual quantities")


class InboundShipmentResponse(InboundShipmentBase):
    """Schema for inbound shipment response"""
    id: int
    status: str
    received_at: Optional[datetime] = None
    created_at: datetime
    supplier: SupplierInShipment
    items: List[InboundShipmentItemResponse] = []

    class Config:
        from_attributes = True


class InboundShipmentListResponse(BaseModel):
    """Paginated response for inbound shipment list"""
    items: List[InboundShipmentResponse]
    total: int
    page: int
    pages: int
    limit: int

