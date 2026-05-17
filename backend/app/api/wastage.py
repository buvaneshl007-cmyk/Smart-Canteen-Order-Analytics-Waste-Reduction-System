from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import FoodWastage, MenuItem
from app.models.schemas import FoodWastageCreate, FoodWastageResponse
from app.api.auth import get_current_owner, User

router = APIRouter(prefix="/wastage", tags=["Food Wastage"])


@router.post("/", response_model=FoodWastageResponse)
async def record_wastage(
    wastage_data: FoodWastageCreate,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Record food wastage (Owner only)"""
    # Verify item exists
    item = db.query(MenuItem).filter(MenuItem.item_id == wastage_data.item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    # Create wastage record
    wastage = FoodWastage(
        item_id=wastage_data.item_id,
        cooked_quantity=wastage_data.cooked_quantity,
        sold_quantity=wastage_data.sold_quantity,
        wasted_quantity=wastage_data.wasted_quantity
    )
    
    db.add(wastage)
    db.commit()
    db.refresh(wastage)
    
    return wastage


@router.get("/", response_model=List[FoodWastageResponse])
async def get_wastage_records(
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get all wastage records (Owner only)"""
    records = db.query(FoodWastage).order_by(FoodWastage.date.desc()).all()
    return records


@router.get("/item/{item_id}", response_model=List[FoodWastageResponse])
async def get_item_wastage(
    item_id: int,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get wastage records for specific item"""
    records = db.query(FoodWastage).filter(
        FoodWastage.item_id == item_id
    ).order_by(FoodWastage.date.desc()).all()
    
    return records
