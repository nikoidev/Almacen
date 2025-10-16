from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


class SupplierBase(BaseModel):
    """Base schema for Supplier"""
    name: str = Field(..., min_length=1, max_length=255, description="Supplier company name")
    contact_person: Optional[str] = Field(None, max_length=255, description="Name of contact person")
    email: Optional[EmailStr] = Field(None, description="Supplier email address")
    phone: Optional[str] = Field(None, max_length=50, description="Supplier phone number")
    address: Optional[str] = Field(None, description="Physical address")


class SupplierCreate(SupplierBase):
    """Schema for creating a new supplier"""
    pass


class SupplierUpdate(BaseModel):
    """Schema for updating an existing supplier"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    contact_person: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=50)
    address: Optional[str] = None


class SupplierResponse(SupplierBase):
    """Schema for supplier response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class SupplierListResponse(BaseModel):
    """Paginated response for supplier list"""
    items: List[SupplierResponse]
    total: int
    page: int
    pages: int
    limit: int


class SupplierInShipment(BaseModel):
    """Simplified supplier schema for nested responses"""
    id: int
    name: str
    contact_person: Optional[str] = None

    class Config:
        from_attributes = True

