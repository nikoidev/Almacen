from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...core.database import get_db
from ...schemas.product import (
    ProductCreate, ProductUpdate, ProductResponse, ProductListResponse
)
from ...services.product_service import ProductService
from ..deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=ProductListResponse)
def get_products(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    search: Optional[str] = Query(None, description="Search by SKU or name"),
    category: Optional[str] = Query(None, description="Filter by category"),
    order_by: str = Query("id", description="Field to order by (id, sku, name, price, created_at)"),
    order_desc: bool = Query(False, description="Order descending"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all products with pagination, search, and filters"""
    skip = (page - 1) * limit
    result = ProductService.get_products(
        db,
        skip=skip,
        limit=limit,
        search=search,
        category=category,
        order_by=order_by,
        order_desc=order_desc
    )
    return result


@router.get("/categories", response_model=list[str])
def get_product_categories(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all unique product categories"""
    return ProductService.get_categories(db)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific product by ID"""
    product = ProductService.get_product(db, product_id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Create a new product"""
    # Check if SKU already exists
    existing = ProductService.get_product_by_sku(db, sku=product.sku)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with SKU '{product.sku}' already exists"
        )
    
    # TODO: Check permission product:create
    
    return ProductService.create_product(db, product=product)


@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Update an existing product"""
    # Check if SKU is being changed and if new SKU already exists
    if product.sku:
        existing = ProductService.get_product_by_sku(db, sku=product.sku)
        if existing and existing.id != product_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with SKU '{product.sku}' already exists"
            )
    
    # TODO: Check permission product:update
    
    updated_product = ProductService.update_product(db, product_id=product_id, product=product)
    if not updated_product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return updated_product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Delete a product"""
    # TODO: Check permission product:delete
    
    success = ProductService.delete_product(db, product_id=product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return None

