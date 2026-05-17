from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.models import MenuItem, User
from app.models.schemas import MenuItemCreate, MenuItemUpdate, MenuItemResponse
from app.api.auth import get_current_owner, get_current_user

router = APIRouter(prefix="/menu", tags=["Menu Management"])


@router.get("/", response_model=List[MenuItemResponse])
def get_menu(db: Session = Depends(get_db)):
    """Get all menu items (public)"""
    items = db.query(MenuItem).all()
    return items


@router.get("/{item_id}", response_model=MenuItemResponse)
def get_menu_item(item_id: int, db: Session = Depends(get_db)):
    """Get specific menu item"""
    item = db.query(MenuItem).filter(MenuItem.item_id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    return item


@router.post("/", response_model=MenuItemResponse)
async def create_menu_item(
    item_data: MenuItemCreate,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Create new menu item (Owner only)"""
    new_item = MenuItem(
        item_name=item_data.item_name,
        price=item_data.price,
        category=item_data.category,
        description=item_data.description,
        image_url=item_data.image_url,
        available=item_data.available,
        created_by_owner=current_user.user_id
    )
    
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    
    return new_item


@router.put("/{item_id}", response_model=MenuItemResponse)
async def update_menu_item(
    item_id: int,
    item_data: MenuItemUpdate,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Update menu item (Owner only)"""
    item = db.query(MenuItem).filter(MenuItem.item_id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    # Update fields
    update_data = item_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(item, field, value)
    
    db.commit()
    db.refresh(item)
    
    return item


@router.delete("/{item_id}")
async def delete_menu_item(
    item_id: int,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Delete menu item (Owner only)"""
    item = db.query(MenuItem).filter(MenuItem.item_id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    db.delete(item)
    db.commit()
    
    return {"message": "Menu item deleted successfully"}


@router.patch("/{item_id}/availability")
async def toggle_availability(
    item_id: int,
    available: bool,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Toggle menu item availability (Owner only)"""
    item = db.query(MenuItem).filter(MenuItem.item_id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Menu item not found"
        )
    
    item.available = available
    db.commit()
    
    return {"message": f"Item {'enabled' if available else 'disabled'} successfully"}
