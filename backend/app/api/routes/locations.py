from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...core.database import get_db
from ...schemas.location import (
    LocationCreate, LocationUpdate, LocationResponse, LocationListResponse
)
from ...services.location_service import LocationService
from ..deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=LocationListResponse)
def get_locations(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by code or description"),
    order_by: str = Query("code", description="Field to order by (id, code, capacity, created_at)"),
    order_desc: bool = Query(False, description="Order descending"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all locations with pagination and search"""
    skip = (page - 1) * limit
    result = LocationService.get_locations(
        db,
        skip=skip,
        limit=limit,
        search=search,
        order_by=order_by,
        order_desc=order_desc
    )
    return result


@router.get("/{location_id}", response_model=LocationResponse)
def get_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific location by ID"""
    location = LocationService.get_location(db, location_id=location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {location_id} not found"
        )
    return location


@router.get("/{location_id}/capacity", response_model=dict)
def get_location_capacity(
    location_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get available capacity for a location"""
    location = LocationService.get_location(db, location_id=location_id)
    if not location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {location_id} not found"
        )
    
    available = LocationService.get_available_capacity(db, location_id=location_id)
    
    return {
        "location_id": location_id,
        "code": location.code,
        "total_capacity": location.capacity,
        "available_capacity": available,
        "used_capacity": location.capacity - available
    }


@router.post("/", response_model=LocationResponse, status_code=status.HTTP_201_CREATED)
def create_location(
    location: LocationCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create a new location"""
    # Check if code already exists
    existing = LocationService.get_location_by_code(db, code=location.code)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Location with code '{location.code}' already exists"
        )
    
    # TODO: Check permission location:create
    
    return LocationService.create_location(db, location=location)


@router.put("/{location_id}", response_model=LocationResponse)
def update_location(
    location_id: int,
    location: LocationUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update an existing location"""
    # Check if code is being changed and if new code already exists
    if location.code:
        existing = LocationService.get_location_by_code(db, code=location.code)
        if existing and existing.id != location_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Location with code '{location.code}' already exists"
            )
    
    # TODO: Check permission location:update
    
    updated_location = LocationService.update_location(
        db, location_id=location_id, location=location
    )
    if not updated_location:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {location_id} not found"
        )
    return updated_location


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_location(
    location_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Delete a location"""
    # TODO: Check permission location:delete
    
    success = LocationService.delete_location(db, location_id=location_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Location with ID {location_id} not found"
        )
    return None

