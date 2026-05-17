"""
Append synthetic Smart Canteen data from the latest available date up to today.
This script does not delete existing data.
"""

import os
import sys
import random
from datetime import datetime, timedelta, time

sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import SessionLocal
from app.models.models import (
    User,
    MenuItem,
    Order,
    OrderItem,
    SalesAnalytics,
    FoodWastage,
    UserRole,
    OrderStatus,
)

DAY_PATTERNS = {
    0: {"multiplier": 1.3, "name": "Monday"},
    1: {"multiplier": 1.1, "name": "Tuesday"},
    2: {"multiplier": 1.0, "name": "Wednesday"},
    3: {"multiplier": 1.05, "name": "Thursday"},
    4: {"multiplier": 1.2, "name": "Friday"},
    5: {"multiplier": 0.7, "name": "Saturday"},
    6: {"multiplier": 0.5, "name": "Sunday"},
}

HOUR_WEIGHTS = [
    (7, 0.06),
    (8, 0.12),
    (9, 0.08),
    (10, 0.16),
    (11, 0.14),
    (12, 0.13),
    (13, 0.14),
    (14, 0.07),
    (16, 0.04),
    (17, 0.04),
    (18, 0.02),
]


def pick_hour() -> int:
    hours = [h for h, _ in HOUR_WEIGHTS]
    weights = [w for _, w in HOUR_WEIGHTS]
    return random.choices(hours, weights=weights, k=1)[0]


def preferred_categories_for_hour(hour: int):
    if 7 <= hour <= 9:
        return ["breakfast", "beverage"]
    if 10 <= hour <= 11:
        return ["snacks", "beverage"]
    if 12 <= hour <= 14:
        return ["lunch", "dinner", "beverage"]
    return ["snacks", "beverage", "fastfood"]


def pick_items(menu_items, hour: int):
    categories = preferred_categories_for_hour(hour)
    filtered = [m for m in menu_items if m.category in categories]
    pool = filtered if filtered else menu_items
    count = random.randint(1, min(3, len(pool)))
    return random.sample(pool, count)


def daterange(start_date, end_date):
    current = start_date
    while current <= end_date:
        yield current
        current += timedelta(days=1)


def add_orders_and_sales(db: Session, start_date, end_date):
    customers = db.query(User).filter(User.role == UserRole.CUSTOMER).all()
    menu_items = db.query(MenuItem).all()

    if not customers or not menu_items:
        raise RuntimeError("Customers or menu items missing. Seed base data first.")

    orders_created = 0
    analytics_created = 0

    for single_date in daterange(start_date, end_date):
        day_of_week = single_date.weekday()
        day_pattern = DAY_PATTERNS[day_of_week]

        base_orders = random.randint(130, 190)
        orders_for_day = max(40, int(base_orders * day_pattern["multiplier"]))

        for _ in range(orders_for_day):
            hour = pick_hour()
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            order_time = datetime.combine(single_date, time(hour=hour, minute=minute, second=second))

            customer = random.choice(customers)
            status = random.choices(
                [OrderStatus.COMPLETED, OrderStatus.CANCELLED],
                weights=[0.94, 0.06],
                k=1,
            )[0]

            order = Order(
                user_id=customer.user_id,
                order_time=order_time,
                total_price=0,
                status=status,
            )
            db.add(order)
            db.flush()

            total_price = 0
            for item in pick_items(menu_items, hour):
                qty = random.randint(1, 3)
                oi = OrderItem(
                    order_id=order.order_id,
                    item_id=item.item_id,
                    quantity=qty,
                    price_at_order=item.price,
                )
                db.add(oi)
                total_price += item.price * qty

                if status == OrderStatus.COMPLETED:
                    sa = SalesAnalytics(
                        item_id=item.item_id,
                        date=order_time,
                        day_of_week=day_pattern["name"],
                        hour=hour,
                        quantity_sold=qty,
                        revenue=item.price * qty,
                    )
                    db.add(sa)
                    analytics_created += 1

            order.total_price = total_price
            orders_created += 1

        db.commit()

    return orders_created, analytics_created


def add_wastage_for_missing_days(db: Session, start_date, end_date):
    menu_items = db.query(MenuItem).all()
    if not menu_items:
        return 0

    created = 0
    for single_date in daterange(start_date, end_date):
        for item in menu_items:
            exists = db.query(FoodWastage).filter(
                func.date(FoodWastage.date) == single_date,
                FoodWastage.item_id == item.item_id,
            ).first()
            if exists:
                continue

            base = random.randint(60, 220)
            cooked = base
            sold = int(cooked * random.uniform(0.75, 0.95))
            wasted = max(0, cooked - sold)

            record = FoodWastage(
                item_id=item.item_id,
                date=datetime.combine(single_date, time(hour=20, minute=0)),
                cooked_quantity=cooked,
                sold_quantity=sold,
                wasted_quantity=wasted,
            )
            db.add(record)
            created += 1

    db.commit()
    return created


def main():
    db = SessionLocal()
    try:
        today = datetime.now().date()

        max_sales_dt = db.query(func.max(SalesAnalytics.date)).scalar()
        max_wastage_dt = db.query(func.max(FoodWastage.date)).scalar()

        sales_start = (max_sales_dt.date() + timedelta(days=1)) if max_sales_dt else (today - timedelta(days=7))
        wastage_start = (max_wastage_dt.date() + timedelta(days=1)) if max_wastage_dt else sales_start

        print(f"Today: {today}")
        print(f"Latest sales date: {max_sales_dt}")
        print(f"Latest wastage date: {max_wastage_dt}")

        if sales_start > today and wastage_start > today:
            print("No gap found. Data is already up to date.")
            return

        orders_created = 0
        analytics_created = 0
        wastage_created = 0

        if sales_start <= today:
            print(f"Adding orders + sales analytics from {sales_start} to {today}...")
            orders_created, analytics_created = add_orders_and_sales(db, sales_start, today)

        if wastage_start <= today:
            print(f"Adding wastage records from {wastage_start} to {today}...")
            wastage_created = add_wastage_for_missing_days(db, wastage_start, today)

        print("\nDone.")
        print(f"Orders added: {orders_created}")
        print(f"Sales analytics added: {analytics_created}")
        print(f"Wastage records added: {wastage_created}")

    except Exception as exc:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    main()
