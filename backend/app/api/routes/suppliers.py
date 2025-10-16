from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...core.database import get_db
from ...schemas.supplier import (
    SupplierCreate, SupplierUpdate, SupplierResponse, SupplierListResponse
)
from ...services.supplier_service import SupplierService
from ..deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=SupplierListResponse)
def get_suppliers(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by name, contact person, or email"),
    order_by: str = Query("id", description="Field to order by (id, name, created_at)"),
    order_desc: bool = Query(False, description="Order descending"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all suppliers with pagination and search"""
    skip = (page - 1) * limit
    result = SupplierService.get_suppliers(
        db,
        skip=skip,
        limit=limit,
        search=search,
        order_by=order_by,
        order_desc=order_desc
    )
    return result


@router.get("/{supplier_id}", response_model=SupplierResponse)
def get_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific supplier by ID"""
    supplier = SupplierService.get_supplier(db, supplier_id=supplier_id)
    if not supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with ID {supplier_id} not found"
        )
    return supplier


@router.post("/", response_model=SupplierResponse, status_code=status.HTTP_201_CREATED)
def create_supplier(
    supplier: SupplierCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create a new supplier"""
    # TODO: Check permission supplier:create
    
    return SupplierService.create_supplier(db, supplier=supplier)


@router.put("/{supplier_id}", response_model=SupplierResponse)
def update_supplier(
    supplier_id: int,
    supplier: SupplierUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update an existing supplier"""
    # TODO: Check permission supplier:update
    
    updated_supplier = SupplierService.update_supplier(
        db, supplier_id=supplier_id, supplier=supplier
    )
    if not updated_supplier:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with ID {supplier_id} not found"
        )
    return updated_supplier


@router.delete("/{supplier_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_supplier(
    supplier_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Delete a supplier"""
    # TODO: Check permission supplier:delete
    
    success = SupplierService.delete_supplier(db, supplier_id=supplier_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Supplier with ID {supplier_id} not found"
        )
    return None

