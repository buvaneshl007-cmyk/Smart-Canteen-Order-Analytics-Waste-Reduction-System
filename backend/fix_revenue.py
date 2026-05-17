"""
Fix revenue in SalesAnalytics table
"""
from app.core.database import SessionLocal
from app.models.models import SalesAnalytics, MenuItem

db = SessionLocal()

print("Fixing revenue in SalesAnalytics...")

# Get all menu items  with prices
menu_items = {item.item_id: item.price for item in db.query(MenuItem).all()}

# Update all sales analytics records
updated_count = 0
for record in db.query(SalesAnalytics).all():
    if record.item_id in menu_items:
        record.revenue = record.quantity_sold * menu_items[record.item_id]
        updated_count += 1

db.commit()

print(f"[OK] Updated {updated_count} records")

# Verify
from sqlalchemy import func
total_revenue = db.query(func.sum(SalesAnalytics.revenue)).scalar()
print(f"[OK] Total revenue now: Rs.{total_revenue:.2f}")

db.close()
