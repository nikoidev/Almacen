from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...core.database import get_db
from ...schemas.inventory import (
    InventoryResponse, InventoryListResponse,
    InventoryAdjust, InventoryMove, LowStockProduct
)
from ...services.inventory_service import InventoryService
from ..deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=InventoryListResponse)
def get_inventory(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    product_id: Optional[int] = Query(None, description="Filter by product"),
    location_id: Optional[int] = Query(None, description="Filter by location"),
    order_by: str = Query("id", description="Field to order by"),
    order_desc: bool = Query(False, description="Order descending"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get inventory records with pagination and filters"""
    skip = (page - 1) * limit
    result = InventoryService.get_inventories(
        db,
        skip=skip,
        limit=limit,
        product_id=product_id,
        location_id=location_id,
        order_by=order_by,
        order_desc=order_desc
    )
    return result


@router.get("/product/{product_id}/stock", response_model=dict)
def get_product_stock(
    product_id: int,
    location_id: Optional[int] = Query(None, description="Specific location"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get stock level for a product (all locations or specific location)"""
    stock_level = InventoryService.get_stock_level(
        db,
        product_id=product_id,
        location_id=location_id
    )
    
    return {
        "product_id": product_id,
        "location_id": location_id,
        "stock_level": stock_level
    }


@router.get("/low-stock", response_model=list[LowStockProduct])
def get_low_stock_products(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get products with stock below minimum level"""
    return InventoryService.get_low_stock_products(db)


@router.post("/adjust", response_model=InventoryResponse)
def adjust_inventory(
    adjust_data: InventoryAdjust,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Manually adjust inventory quantity
    
    Use for corrections, cycle counts, etc.
    Requires inventory:adjust permission.
    """
    # TODO: Check permission inventory:adjust
    
    try:
        result = InventoryService.adjust_stock(
            db,
            adjust_data=adjust_data,
            user_id=current_user.id
        )
        return result
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/move", response_model=dict)
def move_inventory(
    move_data: InventoryMove,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Move stock from one location to another
    
    Operation is atomic - either both succeed or both fail.
    Requires inventory:move permission.
    """
    # TODO: Check permission inventory:move
    
    try:
        from_inv, to_inv = InventoryService.move_stock(
            db,
            move_data=move_data,
            user_id=current_user.id
        )
        return {
            "message": "Stock moved successfully",
            "product_id": move_data.product_id,
            "quantity": move_data.quantity,
            "from_location": {
                "location_id": from_inv.location_id,
                "new_quantity": from_inv.quantity
            },
            "to_location": {
                "location_id": to_inv.location_id,
                "new_quantity": to_inv.quantity
            }
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.get("/{inventory_id}", response_model=InventoryResponse)
def get_inventory_by_id(
    inventory_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific inventory record by ID"""
    inventory = InventoryService.get_inventory(db, inventory_id=inventory_id)
    if not inventory:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory record with ID {inventory_id} not found"
        )
    return inventory

