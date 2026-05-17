from datetime import datetime, timedelta
import random

from app.core.database import SessionLocal
from app.models.models import MenuItem, SalesAnalytics


def seed_today_sales(min_new_records: int = 120) -> None:
    db = SessionLocal()
    try:
        now = datetime.now()
        start_of_day = datetime.combine(now.date(), datetime.min.time())
        end_of_day = start_of_day + timedelta(days=1)

        existing_today = db.query(SalesAnalytics).filter(
            SalesAnalytics.date >= start_of_day,
            SalesAnalytics.date < end_of_day,
        ).count()

        target_total = max(existing_today, min_new_records)
        records_to_add = target_total - existing_today

        if records_to_add <= 0:
            print(f"No new rows needed. Today's sales rows already at {existing_today}.")
            return

        menu_items = db.query(MenuItem).filter(MenuItem.available == True).all()  # noqa: E712
        if not menu_items:
            print("No available menu items found. Seed menu data first.")
            return

        peak_hours = [8, 9, 10, 11, 12, 13, 16, 17, 18]
        weights = [4, 5, 8, 9, 8, 7, 5, 6, 4]

        for _ in range(records_to_add):
            item = random.choice(menu_items)
            hour = random.choices(peak_hours, weights=weights, k=1)[0]
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            sold_at = start_of_day.replace(hour=hour, minute=minute, second=second)

            quantity = random.randint(1, 5)
            revenue = float(quantity * item.price)

            db.add(
                SalesAnalytics(
                    item_id=item.item_id,
                    date=sold_at,
                    day_of_week=now.strftime("%A"),
                    hour=hour,
                    quantity_sold=quantity,
                    revenue=revenue,
                )
            )

        db.commit()
        print(
            f"Added {records_to_add} rows for today. "
            f"Today's sales analytics rows: {target_total}."
        )
    finally:
        db.close()


if __name__ == "__main__":
    seed_today_sales()
