import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.models import SalesAnalytics, MenuItem
from typing import List, Dict
from sklearn.ensemble import RandomForestRegressor
import pickle
import os


def prepare_data_for_prediction(db: Session, item_id: int) -> pd.DataFrame:
    """Prepare time series data for an item"""
    # Get last 30 days of data
    start_date = datetime.now() - timedelta(days=30)
    
    results = db.query(
        SalesAnalytics.date,
        SalesAnalytics.day_of_week,
        SalesAnalytics.hour,
        func.sum(SalesAnalytics.quantity_sold).label("quantity")
    ).filter(
        SalesAnalytics.item_id == item_id,
        SalesAnalytics.date >= start_date
    ).group_by(
        SalesAnalytics.date,
        SalesAnalytics.day_of_week,
        SalesAnalytics.hour
    ).all()
    
    if not results:
        return None
    
    # Convert to DataFrame
    data = []
    for r in results:
        data.append({
            "date": r.date,
            "day_of_week": r.day_of_week,
            "hour": r.hour,
            "quantity": r.quantity
        })
    
    df = pd.DataFrame(data)
    return df


def extract_features(df: pd.DataFrame) -> pd.DataFrame:
    """Extract features from time series data"""
    df = df.copy()
    
    # Day of week encoding
    day_mapping = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
        "Friday": 4, "Saturday": 5, "Sunday": 6
    }
    df["day_num"] = df["day_of_week"].map(day_mapping)
    
    # Hour features
    df["is_morning"] = (df["hour"] >= 6) & (df["hour"] < 12)
    df["is_afternoon"] = (df["hour"] >= 12) & (df["hour"] < 17)
    df["is_evening"] = (df["hour"] >= 17) & (df["hour"] < 21)
    
    # Weekend flag
    df["is_weekend"] = df["day_num"].isin([5, 6])
    
    return df


def train_simple_model(df: pd.DataFrame) -> RandomForestRegressor:
    """Train simple Random Forest model"""
    df = extract_features(df)
    
    features = ["day_num", "hour", "is_morning", "is_afternoon", "is_evening", "is_weekend"]
    X = df[features]
    y = df["quantity"]
    
    model = RandomForestRegressor(n_estimators=50, random_state=42, max_depth=5)
    model.fit(X, y)
    
    return model


def predict_demand(db: Session) -> List[Dict]:
    """Predict demand for all items for tomorrow"""
    # Get all menu items
    items = db.query(MenuItem).filter(MenuItem.available == True).all()
    
    predictions = []
    tomorrow = datetime.now() + timedelta(days=1)
    tomorrow_day = tomorrow.strftime("%A")
    
    # Day mapping
    day_mapping = {
        "Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3,
        "Friday": 4, "Saturday": 5, "Sunday": 6
    }
    day_num = day_mapping[tomorrow_day]
    is_weekend = day_num in [5, 6]
    
    for item in items:
        # Get historical data
        df = prepare_data_for_prediction(db, item.item_id)
        
        if df is None or len(df) < 5:
            # Not enough data - use simple average
            avg_query = db.query(
                func.avg(SalesAnalytics.quantity_sold)
            ).filter(
                SalesAnalytics.item_id == item.item_id
            ).scalar()
            
            avg_quantity = int(avg_query or 10)
            predictions.append({
                "item_id": item.item_id,
                "item_name": item.item_name,
                "predicted_quantity": avg_quantity,
                "confidence": 0.5
            })
            continue
        
        try:
            # Train model
            model = train_simple_model(df)
            
            # Predict for different hours (aggregate)
            total_predicted = 0
            for hour in range(6, 21):  # Business hours
                is_morning = 6 <= hour < 12
                is_afternoon = 12 <= hour < 17
                is_evening = 17 <= hour < 21
                
                features = pd.DataFrame([{
                    "day_num": day_num,
                    "hour": hour,
                    "is_morning": is_morning,
                    "is_afternoon": is_afternoon,
                    "is_evening": is_evening,
                    "is_weekend": is_weekend
                }])
                
                pred = model.predict(features)[0]
                total_predicted += max(0, pred)
            
            predictions.append({
                "item_id": item.item_id,
                "item_name": item.item_name,
                "predicted_quantity": int(total_predicted),
                "confidence": 0.75
            })
        
        except Exception as e:
            # Fallback to average
            avg_query = db.query(
                func.avg(SalesAnalytics.quantity_sold)
            ).filter(
                SalesAnalytics.item_id == item.item_id
            ).scalar()
            
            avg_quantity = int(avg_query or 10)
            predictions.append({
                "item_id": item.item_id,
                "item_name": item.item_name,
                "predicted_quantity": avg_quantity,
                "confidence": 0.4
            })
    
    return predictions


def get_peak_hours(db: Session, item_id: int) -> List[int]:
    """Get peak selling hours for an item"""
    results = db.query(
        SalesAnalytics.hour,
        func.sum(SalesAnalytics.quantity_sold).label("total")
    ).filter(
        SalesAnalytics.item_id == item_id
    ).group_by(
        SalesAnalytics.hour
    ).order_by(
        func.sum(SalesAnalytics.quantity_sold).desc()
    ).limit(3).all()
    
    return [r.hour for r in results]
