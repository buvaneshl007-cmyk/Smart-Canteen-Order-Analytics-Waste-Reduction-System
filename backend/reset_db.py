"""
Quick script to reset the MySQL database
"""
import pymysql
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get MySQL password from .env
DATABASE_URL = os.getenv("DATABASE_URL", "")
# Extract password from DATABASE_URL: mysql+pymysql://root:PASSWORD@localhost:3306/smart_canteen
password = DATABASE_URL.split(":")[2].split("@")[0] if ":" in DATABASE_URL else ""

print(f"Connecting to MySQL...")

# Connect to MySQL
connection = pymysql.connect(
    host='localhost',
    user='root',
    password=password,
    database='smart_canteen'
)

try:
    with connection.cursor() as cursor:
        # Drop all tables in correct order (respecting foreign keys)
        tables = [
            'order_items',
            'food_wastage',
            'sales_analytics', 
            'orders',
            'menu_items',
            'users'
        ]
        
        print("Dropping existing tables...")
        for table in tables:
            cursor.execute(f"DROP TABLE IF EXISTS {table}")
            print(f"  ✓ Dropped {table}")
        
        connection.commit()
        print("\n✓ All tables dropped successfully!")
        print("Now restart the backend server to recreate tables with correct schema.\n")
        
finally:
    connection.close()
