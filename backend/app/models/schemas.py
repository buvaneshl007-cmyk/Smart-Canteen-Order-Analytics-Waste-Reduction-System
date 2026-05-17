from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    OWNER = "owner"
    CUSTOMER = "customer"


class OrderStatus(str, Enum):
    PENDING = "pending"
    PREPARING = "preparing"
    READY = "ready"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.CUSTOMER


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(UserBase):
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# Menu Item Schemas
class MenuItemBase(BaseModel):
    item_name: str
    price: float
    category: str
    description: Optional[str] = ""
    image_url: Optional[str] = ""
    available: bool = True


class MenuItemCreate(MenuItemBase):
    pass


class MenuItemUpdate(BaseModel):
    item_name: Optional[str] = None
    price: Optional[float] = None
    category: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
    available: Optional[bool] = None


class MenuItemResponse(MenuItemBase):
    item_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True


# Order Schemas
class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    order_item_id: int
    item_id: int
    quantity: int
    price_at_order: float
    menu_item: MenuItemResponse
    
    class Config:
        from_attributes = True


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]


class OrderResponse(BaseModel):
    order_id: int
    user_id: int
    order_time: datetime
    total_price: float
    status: OrderStatus
    order_items: List[OrderItemResponse]
    user: UserResponse
    
    class Config:
        from_attributes = True


class OrderUpdateStatus(BaseModel):
    status: OrderStatus


# Analytics Schemas
class DailySales(BaseModel):
    date: str
    total_revenue: float
    total_orders: int
    items_sold: int


class ItemSalesAnalytics(BaseModel):
    item_id: int
    item_name: str
    total_quantity: int
    total_revenue: float
    peak_hour: int


class WeeklySales(BaseModel):
    day_of_week: str
    total_revenue: float
    total_orders: int


class TimeSales(BaseModel):
    hour: int
    total_orders: int
    total_revenue: float


class PredictionResponse(BaseModel):
    item_id: int
    item_name: str
    predicted_quantity: int
    confidence: float


# Food Wastage Schemas
class FoodWastageCreate(BaseModel):
    item_id: int
    cooked_quantity: int
    sold_quantity: int
    wasted_quantity: int


class FoodWastageResponse(BaseModel):
    wastage_id: int
    item_id: int
    date: datetime
    cooked_quantity: int
    sold_quantity: int
    wasted_quantity: int
    
    class Config:
        from_attributes = True


# AI Assistant Schemas
class AIQuery(BaseModel):
    query: str


class AIResponse(BaseModel):
    response: str
    data: Optional[dict] = None
