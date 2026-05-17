from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.models.models import Order, OrderItem, MenuItem, User, OrderStatus, SalesAnalytics
from app.models.schemas import OrderCreate, OrderResponse, OrderUpdateStatus
from app.api.auth import get_current_user, get_current_owner

router = APIRouter(prefix="/orders", tags=["Order Management"])


@router.post("/", response_model=OrderResponse)
async def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create new order"""
    if not order_data.items:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Order must contain at least one item"
        )
    
    # Calculate total price and validate items
    total_price = 0
    order_items_data = []
    
    for item in order_data.items:
        menu_item = db.query(MenuItem).filter(MenuItem.item_id == item.item_id).first()
        if not menu_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Menu item {item.item_id} not found"
            )
        
        if not menu_item.available:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"{menu_item.item_name} is not available"
            )
        
        item_total = menu_item.price * item.quantity
        total_price += item_total
        
        order_items_data.append({
            "item_id": item.item_id,
            "quantity": item.quantity,
            "price_at_order": menu_item.price,
            "menu_item": menu_item
        })
    
    # Create order
    new_order = Order(
        user_id=current_user.user_id,
        total_price=total_price,
        status=OrderStatus.PENDING
    )
    db.add(new_order)
    db.flush()
    
    # Create order items and analytics data
    for item_data in order_items_data:
        order_item = OrderItem(
            order_id=new_order.order_id,
            item_id=item_data["item_id"],
            quantity=item_data["quantity"],
            price_at_order=item_data["price_at_order"]
        )
        db.add(order_item)
        
        # Record analytics
        order_time = datetime.now()
        analytics = SalesAnalytics(
            item_id=item_data["item_id"],
            date=order_time,
            day_of_week=order_time.strftime("%A"),
            hour=order_time.hour,
            quantity_sold=item_data["quantity"],
            revenue=item_data["price_at_order"] * item_data["quantity"]
        )
        db.add(analytics)
    
    db.commit()
    db.refresh(new_order)
    
    return new_order


@router.get("/", response_model=List[OrderResponse])
async def get_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get orders (customers see their own, owners see all)"""
    if current_user.role == "owner":
        orders = db.query(Order).order_by(Order.order_time.desc()).all()
    else:
        orders = db.query(Order).filter(
            Order.user_id == current_user.user_id
        ).order_by(Order.order_time.desc()).all()
    
    return orders


@router.get("/live", response_model=List[OrderResponse])
async def get_live_orders(
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get pending and preparing orders (Owner only)"""
    orders = db.query(Order).filter(
        Order.status.in_([OrderStatus.PENDING, OrderStatus.PREPARING])
    ).order_by(Order.order_time.desc()).all()
    
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get specific order"""
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check permission
    if current_user.role != "owner" and order.user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have permission to view this order"
        )
    
    return order


@router.patch("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    order_id: int,
    status_data: OrderUpdateStatus,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Update order status (Owner only)"""
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    order.status = status_data.status
    db.commit()
    db.refresh(order)
    
    return order
