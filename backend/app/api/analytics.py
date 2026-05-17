from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import List
from datetime import datetime, timedelta
from app.core.database import get_db
from app.models.models import SalesAnalytics, MenuItem, Order, OrderItem
from app.models.schemas import (
    DailySales, ItemSalesAnalytics, WeeklySales, 
    TimeSales, PredictionResponse
)
from app.api.auth import get_current_owner, User
from app.services.ml_service import predict_demand

router = APIRouter(prefix="/analytics", tags=["Analytics"])


@router.get("/daily", response_model=List[DailySales])
async def get_daily_sales(
    days: int = 7,
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get daily sales for the last N days"""
    now = datetime.now()
    end_date = now.date()
    start_date = end_date - timedelta(days=max(days - 1, 0))
    start_datetime = datetime.combine(start_date, datetime.min.time())
    
    results = db.query(
        func.date(SalesAnalytics.date).label("date"),
        func.sum(SalesAnalytics.revenue).label("total_revenue"),
        func.count(func.distinct(SalesAnalytics.id)).label("total_items"),
        func.sum(SalesAnalytics.quantity_sold).label("items_sold")
    ).filter(
        SalesAnalytics.date >= start_datetime
    ).group_by(
        func.date(SalesAnalytics.date)
    ).order_by(
        func.date(SalesAnalytics.date)
    ).all()

    result_by_date = {
        str(r.date): {
            "total_revenue": float(r.total_revenue or 0),
            "total_orders": int(r.total_items or 0),
            "items_sold": int(r.items_sold or 0),
        }
        for r in results
    }

    response = []
    current_date = start_date
    while current_date <= end_date:
        date_key = current_date.isoformat()
        day_data = result_by_date.get(
            date_key,
            {"total_revenue": 0.0, "total_orders": 0, "items_sold": 0},
        )
        response.append(
            {
                "date": date_key,
                "total_revenue": day_data["total_revenue"],
                "total_orders": day_data["total_orders"],
                "items_sold": day_data["items_sold"],
            }
        )
        current_date += timedelta(days=1)

    return response


@router.get("/weekly", response_model=List[WeeklySales])
async def get_weekly_sales(
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get sales by day of week"""
    results = db.query(
        SalesAnalytics.day_of_week,
        func.sum(SalesAnalytics.revenue).label("total_revenue"),
        func.count(func.distinct(SalesAnalytics.id)).label("total_orders")
    ).group_by(
        SalesAnalytics.day_of_week
    ).all()
    
    # Order by weekday
    days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    results_dict = {r.day_of_week: r for r in results}
    
    return [
        {
            "day_of_week": day,
            "total_revenue": float(results_dict[day].total_revenue or 0) if day in results_dict else 0,
            "total_orders": int(results_dict[day].total_orders or 0) if day in results_dict else 0
        }
        for day in days_order
    ]


@router.get("/time", response_model=List[TimeSales])
async def get_hourly_sales(
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get sales by hour of day"""
    results = db.query(
        SalesAnalytics.hour,
        func.count(func.distinct(SalesAnalytics.id)).label("total_orders"),
        func.sum(SalesAnalytics.revenue).label("total_revenue")
    ).group_by(
        SalesAnalytics.hour
    ).order_by(
        SalesAnalytics.hour
    ).all()
    
    result_by_hour = {
        int(r.hour): {
            "total_orders": int(r.total_orders or 0),
            "total_revenue": float(r.total_revenue or 0),
        }
        for r in results
    }

    return [
        {
            "hour": hour,
            "total_orders": result_by_hour.get(hour, {}).get("total_orders", 0),
            "total_revenue": result_by_hour.get(hour, {}).get("total_revenue", 0.0),
        }
        for hour in range(24)
    ]


@router.get("/items", response_model=List[ItemSalesAnalytics])
async def get_item_analytics(
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get analytics by item"""
    results = db.query(
        MenuItem.item_id,
        MenuItem.item_name,
        func.sum(SalesAnalytics.quantity_sold).label("total_quantity"),
        func.sum(SalesAnalytics.revenue).label("total_revenue"),
        func.avg(SalesAnalytics.hour).label("peak_hour")  # Changed from mode() to avg()
    ).join(
        SalesAnalytics, MenuItem.item_id == SalesAnalytics.item_id
    ).group_by(
        MenuItem.item_id, MenuItem.item_name
    ).order_by(
        desc("total_revenue")
    ).all()
    
    return [
        {
            "item_id": r.item_id,
            "item_name": r.item_name,
            "total_quantity": int(r.total_quantity or 0),
            "total_revenue": float(r.total_revenue or 0),
            "peak_hour": int(r.peak_hour or 12)
        }
        for r in results
    ]


@router.get("/predict", response_model=List[PredictionResponse])
async def get_demand_prediction(
    current_user: User = Depends(get_current_owner),
    db: Session = Depends(get_db)
):
    """Get demand prediction for tomorrow"""
    try:
        predictions = predict_demand(db)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")
