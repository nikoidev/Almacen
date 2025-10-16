from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional
from ...core.database import get_db
from ...schemas.shipment import (
    InboundShipmentCreate, InboundShipmentUpdate, InboundShipmentResponse,
    InboundShipmentListResponse, InboundShipmentReceive
)
from ...models.inbound_shipment import ShipmentStatus
from ...services.shipment_service import ShipmentService
from ..deps import get_current_active_user

router = APIRouter()


@router.get("/", response_model=InboundShipmentListResponse)
def get_shipments(
    page: int = Query(1, ge=1, description="Page number"),
    limit: int = Query(10, ge=1, le=100, description="Items per page"),
    supplier_id: Optional[int] = Query(None, description="Filter by supplier"),
    status: Optional[ShipmentStatus] = Query(None, description="Filter by status"),
    order_by: str = Query("id", description="Field to order by"),
    order_desc: bool = Query(False, description="Order descending"),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get all inbound shipments with pagination and filters"""
    skip = (page - 1) * limit
    result = ShipmentService.get_shipments(
        db,
        skip=skip,
        limit=limit,
        supplier_id=supplier_id,
        status=status,
        order_by=order_by,
        order_desc=order_desc
    )
    return result


@router.get("/{shipment_id}", response_model=InboundShipmentResponse)
def get_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """Get a specific shipment by ID"""
    shipment = ShipmentService.get_shipment(db, shipment_id=shipment_id)
    if not shipment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shipment with ID {shipment_id} not found"
        )
    return shipment


@router.post("/", response_model=InboundShipmentResponse, status_code=status.HTTP_201_CREATED)
def create_shipment(
    shipment: InboundShipmentCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Create a new inbound shipment
    
    Requires shipment:create permission.
    """
    # TODO: Check permission shipment:create
    
    try:
        return ShipmentService.create_shipment(
            db,
            shipment_data=shipment,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.put("/{shipment_id}", response_model=InboundShipmentResponse)
def update_shipment(
    shipment_id: int,
    shipment: InboundShipmentUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Update an existing shipment
    
    Cannot update completed shipments.
    """
    # TODO: Check permission shipment:update
    
    try:
        updated_shipment = ShipmentService.update_shipment(
            db,
            shipment_id=shipment_id,
            shipment_data=shipment,
            user_id=current_user.id
        )
        if not updated_shipment:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment with ID {shipment_id} not found"
            )
        return updated_shipment
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.post("/{shipment_id}/receive", response_model=InboundShipmentResponse)
def receive_shipment(
    shipment_id: int,
    receive_data: InboundShipmentReceive,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Process receiving of a shipment
    
    This operation:
    - Updates quantities received
    - Adds stock to inventory
    - Marks shipment as completed
    
    Requires shipment:receive permission.
    This is an ATOMIC operation.
    """
    # TODO: Check permission shipment:receive
    
    try:
        return ShipmentService.receive_shipment(
            db,
            shipment_id=shipment_id,
            receive_data=receive_data,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )


@router.delete("/{shipment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shipment(
    shipment_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_active_user)
):
    """
    Delete a shipment
    
    Only pending shipments can be deleted.
    """
    # TODO: Check permission shipment:delete
    
    try:
        success = ShipmentService.delete_shipment(db, shipment_id=shipment_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shipment with ID {shipment_id} not found"
            )
        return None
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )

