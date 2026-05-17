"""
Smart Canteen System - Data Generation Script
Generates 30 days of realistic synthetic data for testing analytics and AI features
"""
import sys
import os
from datetime import datetime, timedelta
import random
from faker import Faker

# Add the app directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.core.database import SessionLocal, engine, Base
from app.models.models import User, MenuItem, Order, OrderItem, SalesAnalytics, FoodWastage, UserRole, OrderStatus
from passlib.context import CryptContext

# Initialize
fake = Faker()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Menu items with realistic details
MENU_ITEMS = [
    {"item_name": "Veg Puff", "price": 15, "category": "snacks"},
    {"item_name": "Samosa", "price": 20, "category": "snacks"},
    {"item_name": "Tea", "price": 10, "category": "beverage"},
    {"item_name": "Coffee", "price": 15, "category": "beverage"},
    {"item_name": "Masala Dosa", "price": 40, "category": "breakfast"},
    {"item_name": "Idli", "price": 25, "category": "breakfast"},
    {"item_name": "Poori", "price": 35, "category": "breakfast"},
    {"item_name": "Veg Sandwich", "price": 30, "category": "fastfood"},
    {"item_name": "Bread Omelette", "price": 35, "category": "fastfood"},
    {"item_name": "Upma", "price": 25, "category": "breakfast"},
    {"item_name": "Lemon Rice", "price": 45, "category": "lunch"},
    {"item_name": "Curd Rice", "price": 40, "category": "lunch"},
    {"item_name": "Veg Biryani", "price": 70, "category": "lunch"},
    {"item_name": "Parotta", "price": 50, "category": "dinner"},
    {"item_name": "Chappathi", "price": 45, "category": "dinner"},
    {"item_name": "Milk", "price": 20, "category": "beverage"},
    {"item_name": "Badam Milk", "price": 30, "category": "beverage"},
    {"item_name": "Egg Puff", "price": 20, "category": "snacks"},
    {"item_name": "Cutlet", "price": 25, "category": "snacks"},
    {"item_name": "Noodles", "price": 60, "category": "fastfood"},
]

# Time-based item preferences
TIME_PREFERENCES = {
    "breakfast": {  # 7:30 AM - 9:30 AM
        "items": ["Masala Dosa", "Idli", "Poori", "Upma"],
        "hours": [7, 8, 9],
        "peak_hour": 8,
    },
    "morning_snack": {  # 10:00 AM - 11:30 AM
        "items": ["Veg Puff", "Samosa", "Tea", "Coffee", "Egg Puff", "Cutlet"],
        "hours": [10, 11],
        "peak_hour": 10,
    },
    "lunch": {  # 12:30 PM - 2:30 PM
        "items": ["Veg Biryani", "Lemon Rice", "Curd Rice", "Parotta", "Chappathi"],
        "hours": [12, 13, 14],
        "peak_hour": 13,
    },
    "evening_snack": {  # 4:30 PM - 6:30 PM
        "items": ["Tea", "Coffee", "Veg Puff", "Samosa", "Cutlet"],
        "hours": [16, 17, 18],
        "peak_hour": 17,
    },
}

# Day-of-week patterns (Monday = 0, Sunday = 6)
DAY_PATTERNS = {
    0: {"multiplier": 1.3, "name": "Monday"},  # Higher demand on Mondays
    1: {"multiplier": 1.1, "name": "Tuesday"},
    2: {"multiplier": 1.0, "name": "Wednesday"},
    3: {"multiplier": 1.05, "name": "Thursday"},
    4: {"multiplier": 1.2, "name": "Friday"},  # Higher demand on Fridays
    5: {"multiplier": 0.7, "name": "Saturday"},  # Lower demand on weekends
    6: {"multiplier": 0.5, "name": "Sunday"},   # Lowest demand on Sundays
}


def hash_password(password: str) -> str:
    """Hash password for secure storage"""
    return pwd_context.hash(password)


def create_users(db: Session):
    """Create 1 owner and 50 customers"""
    print("\n📋 Creating users...")
    
    # Check if owner already exists
    existing_owner = db.query(User).filter(User.email == "owner@canteen.com").first()
    if existing_owner:
        print("  ✓ Owner already exists")
        owner = existing_owner
    else:
        # Create owner
        owner = User(
            name="Canteen Owner",
            email="owner@canteen.com",
            password=hash_password("owner123"),
            role=UserRole.OWNER
        )
        db.add(owner)
        db.commit()
        print("  ✓ Created owner account (email: owner@canteen.com, password: owner123)")
    
    # Check existing customers
    existing_customers = db.query(User).filter(User.role == UserRole.CUSTOMER).count()
    if existing_customers >= 50:
        print(f"  ✓ {existing_customers} customers already exist")
        return
    
    # Create 50 customers
    customers_to_create = 50 - existing_customers
    for i in range(customers_to_create):
        customer = User(
            name=fake.name(),
            email=fake.email(),
            password=hash_password("customer123"),
            role=UserRole.CUSTOMER
        )
        db.add(customer)
    
    db.commit()
    print(f"  ✓ Created {customers_to_create} customer accounts")


def create_menu_items(db: Session):
    """Create 20 menu items"""
    print("\n🍽️  Creating menu items...")
    
    existing_count = db.query(MenuItem).count()
    if existing_count >= 20:
        print(f"  ✓ {existing_count} menu items already exist")
        return
    
    owner = db.query(User).filter(User.role == UserRole.OWNER).first()
    
    for item_data in MENU_ITEMS:
        # Check if item already exists
        existing = db.query(MenuItem).filter(
            MenuItem.item_name == item_data["item_name"]
        ).first()
        
        if not existing:
            menu_item = MenuItem(
                item_name=item_data["item_name"],
                price=item_data["price"],
                category=item_data["category"],
                description=f"Delicious {item_data['item_name']}",
                available=True,
                created_by_owner=owner.user_id if owner else 1
            )
            db.add(menu_item)
    
    db.commit()
    print(f"  ✓ Created menu items")


def get_time_slot(hour):
    """Determine which time slot an hour belongs to"""
    if 7 <= hour <= 9:
        return "breakfast"
    elif 10 <= hour <= 11:
        return "morning_snack"
    elif 12 <= hour <= 14:
        return "lunch"
    elif 16 <= hour <= 18:
        return "evening_snack"
    return None


def get_preferred_items_for_time(db: Session, hour: int, day_of_week: int):
    """Get menu items that are popular at a specific time"""
    time_slot = get_time_slot(hour)
    
    if not time_slot:
        # Off-peak hours - return random items
        all_items = db.query(MenuItem).all()
        return random.sample(all_items, min(len(all_items), 3)) if all_items else []
    
    preferred_names = TIME_PREFERENCES[time_slot]["items"]
    is_peak = hour == TIME_PREFERENCES[time_slot]["peak_hour"]
    
    # Get preferred items
    preferred_items = db.query(MenuItem).filter(
        MenuItem.item_name.in_(preferred_names)
    ).all()
    
    if not preferred_items:
        all_items = db.query(MenuItem).all()
        return random.sample(all_items, min(len(all_items), 3)) if all_items else []
    
    # During peak hours, strongly prefer peak items
    if is_peak or random.random() < 0.8:
        return random.sample(preferred_items, min(len(preferred_items), random.randint(1, 3)))
    else:
        # Sometimes mix in other items
        all_items = db.query(MenuItem).all()
        return random.sample(all_items, random.randint(1, 3))


def generate_orders(db: Session, num_orders=5000):
    """Generate realistic orders over 30 days"""
    print(f"\n📦 Generating {num_orders} orders...")
    
    # Check if orders already exist
    existing_orders = db.query(Order).count()
    if existing_orders >= num_orders:
        print(f"  ✓ {existing_orders} orders already exist")
        return
    
    customers = db.query(User).filter(User.role == UserRole.CUSTOMER).all()
    menu_items = db.query(MenuItem).all()
    
    if not customers:
        print("  ✗ No customers found! Please create users first.")
        return
    
    if not menu_items:
        print("  ✗ No menu items found! Please create menu items first.")
        return
    
    # Generate orders over 30 days
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    orders_created = 0
    analytics_data = []
    
    for _ in range(num_orders):
        # Random date within 30 days
        random_days = random.random() * 30
        order_date = start_date + timedelta(days=random_days)
        day_of_week = order_date.weekday()
        day_pattern = DAY_PATTERNS[day_of_week]
        
        # Determine order hour based on realistic patterns
        time_slot_choice = random.choices(
            ["breakfast", "morning_snack", "lunch", "evening_snack", "other"],
            weights=[0.25, 0.30, 0.30, 0.12, 0.03],  # Weighted distribution
            k=1
        )[0]
        
        if time_slot_choice == "breakfast":
            hour = random.choice([7, 8, 9])
            minute = random.randint(0, 59)
        elif time_slot_choice == "morning_snack":
            hour = random.choice([10, 11])
            minute = random.randint(0, 59)
        elif time_slot_choice == "lunch":
            hour = random.choice([12, 13, 14])
            minute = random.randint(0, 59)
        elif time_slot_choice == "evening_snack":
            hour = random.choice([16, 17, 18])
            minute = random.randint(0, 59)
        else:
            hour = random.choice([9, 15, 19])
            minute = random.randint(0, 59)
        
        order_time = order_date.replace(hour=hour, minute=minute, second=random.randint(0, 59))
        
        # Skip if weekend (lower probability)
        if day_of_week >= 5 and random.random() < 0.6:
            continue
        
        # Create order
        customer = random.choice(customers)
        order = Order(
            user_id=customer.user_id,
            order_time=order_time,
            total_price=0,  # Will calculate
            status=random.choice([OrderStatus.COMPLETED, OrderStatus.COMPLETED, OrderStatus.COMPLETED, OrderStatus.CANCELLED])
        )
        db.add(order)
        db.flush()  # Get order_id
        
        # Add 1-3 items to order
        items_to_add = get_preferred_items_for_time(db, hour, day_of_week)
        total_price = 0
        
        for item in items_to_add:
            # Apply day-of-week multiplier to quantity
            base_quantity = random.randint(1, 3)
            if random.random() < day_pattern["multiplier"] - 1:
                base_quantity += 1
            
            quantity = max(1, base_quantity)
            
            order_item = OrderItem(
                order_id=order.order_id,
                item_id=item.item_id,
                quantity=quantity,
                price_at_order=item.price
            )
            db.add(order_item)
            
            item_total = item.price * quantity
            total_price += item_total
            
            # Record analytics if order is completed
            if order.status == OrderStatus.COMPLETED:
                analytics_data.append({
                    "item_id": item.item_id,
                    "date": order_time,
                    "day_of_week": day_pattern["name"],
                    "hour": hour,
                    "quantity_sold": quantity
                })
        
        order.total_price = total_price
        orders_created += 1
        
        # Commit in batches
        if orders_created % 500 == 0:
            db.commit()
            print(f"  ✓ Created {orders_created} orders...")
    
    db.commit()
    print(f"  ✓ Created {orders_created} orders with realistic time patterns")
    
    # Create sales analytics
    print("\n📊 Creating sales analytics records...")
    for data in analytics_data:
        analytics = SalesAnalytics(
            item_id=data["item_id"],
            date=data["date"],
            day_of_week=data["day_of_week"],
            hour=data["hour"],
            quantity_sold=data["quantity_sold"],
            revenue=0  # Will be calculated from order items
        )
        db.add(analytics)
    
    # Update revenue
    menu_items_dict = {item.item_id: item.price for item in menu_items}
    for analytics in db.query(SalesAnalytics).all():
        analytics.revenue = analytics.quantity_sold * menu_items_dict.get(analytics.item_id, 0)
    
    db.commit()
    print(f"  ✓ Created {len(analytics_data)} sales analytics records")


def generate_food_preparation_data(db: Session):
    """Generate 30 days of food preparation and wastage data"""
    print("\n🍳 Generating food preparation data...")
    
    existing_records = db.query(FoodWastage).count()
    if existing_records > 0:
        print(f"  ✓ {existing_records} preparation records already exist")
        return
    
    menu_items = db.query(MenuItem).all()
    end_date = datetime.now()
    start_date = end_date - timedelta(days=30)
    
    records_created = 0
    
    for single_date in (start_date + timedelta(n) for n in range(31)):
        day_of_week = single_date.weekday()
        day_pattern = DAY_PATTERNS[day_of_week]
        
        for item in menu_items:
            # Base preparation quantity depends on item category
            category = item.category
            if category == "breakfast":
                base_prep = random.randint(80, 150)
            elif category == "lunch":
                base_prep = random.randint(60, 120)
            elif category == "snacks":
                base_prep = random.randint(100, 200)
            elif category == "beverage":
                base_prep = random.randint(150, 300)
            else:
                base_prep = random.randint(50, 100)
            
            # Apply day multiplier
            prepared = int(base_prep * day_pattern["multiplier"])
            
            # Sold quantity (80-95% of prepared on average)
            sold_percentage = random.uniform(0.75, 0.95)
            sold = int(prepared * sold_percentage)
            
            # Some items have predictable high waste
            if item.item_name == "Poori":
                sold_percentage = random.uniform(0.60, 0.75)  # Higher waste
                sold = int(prepared * sold_percentage)
            
            wasted = prepared - sold
            
            wastage = FoodWastage(
                item_id=item.item_id,
                date=single_date,
                cooked_quantity=prepared,
                sold_quantity=sold,
                wasted_quantity=wasted
            )
            db.add(wastage)
            records_created += 1
    
    db.commit()
    print(f"  ✓ Created {records_created} food preparation records (30 days)")


def print_summary(db: Session):
    """Print summary statistics"""
    print("\n" + "="*60)
    print("📈 DATA GENERATION SUMMARY")
    print("="*60)
    
    users = db.query(User).count()
    owners = db.query(User).filter(User.role == UserRole.OWNER).count()
    customers = db.query(User).filter(User.role == UserRole.CUSTOMER).count()
    
    menu_items = db.query(MenuItem).count()
    orders = db.query(Order).count()
    order_items = db.query(OrderItem).count()
    analytics = db.query(SalesAnalytics).count()
    wastage = db.query(FoodWastage).count()
    
    print(f"\n👥 Users: {users} total ({owners} owners, {customers} customers)")
    print(f"🍽️  Menu Items: {menu_items}")
    print(f"📦 Orders: {orders}")
    print(f"📋 Order Items: {order_items}")
    print(f"📊 Sales Analytics: {analytics}")
    print(f"🗑️  Wastage Records: {wastage}")
    
    # Top selling items
    print("\n🏆 Top 5 Selling Items:")
    from sqlalchemy import func, desc
    top_items = db.query(
        MenuItem.item_name,
        func.sum(SalesAnalytics.quantity_sold).label("total_sold")
    ).join(
        SalesAnalytics, MenuItem.item_id == SalesAnalytics.item_id
    ).group_by(
        MenuItem.item_name
    ).order_by(
        desc("total_sold")
    ).limit(5).all()
    
    for idx, (name, qty) in enumerate(top_items, 1):
        print(f"  {idx}. {name}: {qty} units")
    
    # Peak hours
    print("\n⏰ Peak Hours:")
    peak_hours = db.query(
        SalesAnalytics.hour,
        func.sum(SalesAnalytics.quantity_sold).label("total")
    ).group_by(
        SalesAnalytics.hour
    ).order_by(
        desc("total")
    ).limit(3).all()
    
    for hour, qty in peak_hours:
        print(f"  {hour}:00 - {qty} items sold")
    
    # Most wasted items
    print("\n🗑️  Top 5 Most Wasted Items:")
    wasted_items = db.query(
        MenuItem.item_name,
        func.sum(FoodWastage.wasted_quantity).label("total_waste")
    ).join(
        FoodWastage, MenuItem.item_id == FoodWastage.item_id
    ).group_by(
        MenuItem.item_name
    ).order_by(
        desc("total_waste")
    ).limit(5).all()
    
    for idx, (name, waste) in enumerate(wasted_items, 1):
        print(f"  {idx}. {name}: {waste} units wasted")
    
    print("\n" + "="*60)
    print("✅ Data generation complete!")
    print("="*60)
    print("\nYou can now:")
    print("  • View analytics dashboards")
    print("  • Test AI assistant queries")
    print("  • Train demand prediction models")
    print("  • Visualize charts and insights")
    print("\n")


def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("🚀 SMART CANTEEN DATA GENERATOR")
    print("="*60)
    print("\nThis script will generate:")
    print("  • 1 Owner + 50 Customers")
    print("  • 20 Menu Items")
    print("  • 5000 Orders")
    print("  • ~10,000 Order Items")
    print("  • 30 Days of Preparation Data")
    print("  • ~5000 Sales Analytics Records")
    print("\n" + "="*60)
    
    response = input("\nProceed with data generation? (yes/no): ")
    if response.lower() not in ['yes', 'y']:
        print("Cancelled.")
        return
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Generate data
        create_users(db)
        create_menu_items(db)
        generate_orders(db, num_orders=5000)
        generate_food_preparation_data(db)
        
        # Print summary
        print_summary(db)
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()
