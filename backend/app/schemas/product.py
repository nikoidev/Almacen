from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ProductBase(BaseModel):
    """Base schema for Product"""
    sku: str = Field(..., description="Unique stock keeping unit identifier")
    name: str = Field(..., min_length=1, max_length=255, description="Product name")
    description: Optional[str] = Field(None, description="Detailed product description")
    category: Optional[str] = Field(None, max_length=100, description="Product category")
    price: Decimal = Field(..., ge=0, description="Unit price")
    min_stock_level: int = Field(default=10, ge=0, description="Minimum stock threshold for alerts")


class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating an existing product"""
    sku: Optional[str] = Field(None, description="Unique stock keeping unit identifier")
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    category: Optional[str] = Field(None, max_length=100)
    price: Optional[Decimal] = Field(None, ge=0)
    min_stock_level: Optional[int] = Field(None, ge=0)


class ProductResponse(ProductBase):
    """Schema for product response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Paginated response for product list"""
    items: List[ProductResponse]
    total: int
    page: int
    pages: int
    limit: int


class ProductInInventory(BaseModel):
    """Simplified product schema for nested responses"""
    id: int
    sku: str
    name: str
    category: Optional[str] = None

    class Config:
        from_attributes = True

