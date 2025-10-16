from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...core.database import get_db
from ...schemas.order import (
    OutboundOrderCreate, OutboundOrderUpdate, OutboundOrderResponse,
    OutboundOrderListResponse, OutboundOrderPick
)
from ...models.outbound_order import OrderStatus
from ...services.order_service import OrderService
from ..deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=OutboundOrderListResponse)
def get_orders(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    customer_name: Optional[str] = Query(None, description="Filter by customer name"),
    status: Optional[OrderStatus] = Query(None, description="Filter by status"),
    order_by: str = Query("id", description="Field to order by"),
    order_desc: bool = Query(False, description="Order descending"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all outbound orders with pagination and filters"""
    skip = (page - 1) * limit
    result = OrderService.get_orders(
        db,
        skip=skip,
        limit=limit,
        customer_name=customer_name,
        status=status,
        order_by=order_by,
        order_desc=order_desc
    )
    return result


@router.get("/{order_id}", response_model=OutboundOrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific order by ID"""
    order = OrderService.get_order(db, order_id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    return order


@router.post("/", response_model=OutboundOrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order: OutboundOrderCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Create a new outbound order
    
    This RESERVES stock for the order items.
    Requires order:create permission.
    """
    # TODO: Check permission order:create
    
    try:
        return OrderService.create_order(
            db,
            order_data=order,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{order_id}", response_model=OutboundOrderResponse)
def update_order(
    order_id: int,
    order: OutboundOrderUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Update an existing order
    
    Cannot update shipped orders.
    """
    # TODO: Check permission order:update
    
    try:
        updated_order = OrderService.update_order(
            db,
            order_id=order_id,
            order_data=order,
            user_id=current_user.id
        )
        if not updated_order:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with ID {order_id} not found"
            )
        return updated_order
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{order_id}/pick", response_model=OutboundOrderResponse)
def pick_order(
    order_id: int,
    pick_data: OutboundOrderPick,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Process picking of an order
    
    This operation:
    - Updates quantities picked
    - Unreserves stock
    - Removes stock from inventory
    - Marks order as packed
    
    Requires order:pick permission.
    This is an ATOMIC operation.
    """
    # TODO: Check permission order:pick
    
    try:
        return OrderService.pick_order(
            db,
            order_id=order_id,
            pick_data=pick_data,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{order_id}/ship", response_model=OutboundOrderResponse)
def ship_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Mark an order as shipped
    
    Order must be in PACKED status.
    Requires order:ship permission.
    """
    # TODO: Check permission order:ship
    
    try:
        return OrderService.ship_order(
            db,
            order_id=order_id,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Delete an order
    
    Only pending orders can be deleted.
    This will UNRESERVE the stock.
    """
    # TODO: Check permission order:delete
    
    try:
        success = OrderService.delete_order(db, order_id=order_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with ID {order_id} not found"
            )
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

