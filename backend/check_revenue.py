from app.core.database import SessionLocal
from app.models.models import SalesAnalytics, MenuItem
from sqlalchemy import func

db = SessionLocal()

# Check revenue values
print("Sample revenue values:")
for x in db.query(SalesAnalytics).limit(5).all():
    print(f"  Item {x.item_id}: qty={x.quantity_sold}, revenue={x.revenue}")

total_rev = db.query(func.sum(SalesAnalytics.revenue)).scalar()
print(f"\nTotal revenue in DB: {total_rev}")

# Check menu prices
print("\nMenu item prices:")
for item in db.query(MenuItem).limit(5).all():
    print(f"  {item.item_name}: {item.price}")

db.close()
