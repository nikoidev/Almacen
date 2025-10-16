from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .product import ProductInInventory
from .location import LocationInInventory


class InventoryBase(BaseModel):
    """Base schema for Inventory"""
    product_id: int = Field(..., description="Product ID")
    location_id: int = Field(..., description="Location ID")
    quantity: int = Field(..., ge=0, description="Current stock quantity")
    reserved_quantity: int = Field(default=0, ge=0, description="Stock reserved for pending orders")


class InventoryCreate(InventoryBase):
    """Schema for creating a new inventory record"""
    pass


class InventoryUpdate(BaseModel):
    """Schema for updating an existing inventory record"""
    quantity: Optional[int] = Field(None, ge=0)
    reserved_quantity: Optional[int] = Field(None, ge=0)


class InventoryAdjust(BaseModel):
    """Schema for manual inventory adjustment"""
    product_id: int
    location_id: int
    quantity: int = Field(..., description="New quantity (replaces current)")
    reason: Optional[str] = Field(None, max_length=500, description="Reason for adjustment")


class InventoryMove(BaseModel):
    """Schema for moving stock between locations"""
    product_id: int
    from_location_id: int
    to_location_id: int
    quantity: int = Field(..., gt=0, description="Quantity to move")


class InventoryResponse(InventoryBase):
    """Schema for inventory response"""
    id: int
    last_updated: datetime
    product: ProductInInventory
    location: LocationInInventory
    
    @property
    def available_quantity(self) -> int:
        """Calculate available quantity (total - reserved)"""
        return self.quantity - self.reserved_quantity

    class Config:
        from_attributes = True


class InventoryListResponse(BaseModel):
    """Paginated response for inventory list"""
    items: List[InventoryResponse]
    total: int
    page: int
    pages: int
    limit: int


class InventoryByProduct(BaseModel):
    """Inventory grouped by product across all locations"""
    product: ProductInInventory
    total_quantity: int
    total_reserved: int
    total_available: int
    locations: List[InventoryResponse]


class LowStockProduct(BaseModel):
    """Schema for low stock alerts"""
    product_id: int
    product_sku: str
    product_name: str
    min_stock_level: int
    current_stock: int
    difference: int  # How much below minimum

