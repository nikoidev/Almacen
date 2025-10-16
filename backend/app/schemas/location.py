from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class LocationBase(BaseModel):
    """Base schema for Location"""
    code: str = Field(..., min_length=1, max_length=50, description="Unique location code (e.g., 'A1-R2-S3')")
    description: Optional[str] = Field(None, max_length=255, description="Human-readable description")
    capacity: int = Field(default=100, ge=1, description="Maximum units that can be stored")


class LocationCreate(LocationBase):
    """Schema for creating a new location"""
    pass


class LocationUpdate(BaseModel):
    """Schema for updating an existing location"""
    code: Optional[str] = Field(None, min_length=1, max_length=50)
    description: Optional[str] = Field(None, max_length=255)
    capacity: Optional[int] = Field(None, ge=1)


class LocationResponse(LocationBase):
    """Schema for location response"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class LocationListResponse(BaseModel):
    """Paginated response for location list"""
    items: List[LocationResponse]
    total: int
    page: int
    pages: int
    limit: int


class LocationInInventory(BaseModel):
    """Simplified location schema for nested responses"""
    id: int
    code: str
    description: Optional[str] = None

    class Config:
        from_attributes = True

