"""
Create simple sample databases for testing ingestion
Max 3 tables, 1000 rows each - perfect for students
"""

import sqlite3
import pandas as pd
import json
from pathlib import Path


def create_sample_sqlite():
    """Create a simple SQLite database with 2 tables"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    db_path = data_dir / "sample_inventory.db"

    # Table 1: Products (simple data)
    products_data = {
        'product_id': [1, 2, 3, 4, 5],
        'name': ['Laptop', 'Mouse', 'Keyboard', 'Monitor', 'Headphones'],
        'category': ['Electronics', 'Accessories', 'Accessories', 'Electronics', 'Accessories'],
        'price': [1299.99, 29.99, 79.99, 399.99, 159.99],
        'stock': [15, 50, 30, 8, 25]
    }

    # Table 2: Sales (simple data)
    sales_data = {
        'sale_id': [1, 2, 3, 4, 5],
        'product_id': [1, 2, 1, 3, 4],
        'quantity': [2, 5, 1, 3, 1],
        'date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
        'region': ['North', 'South', 'East', 'West', 'North']
    }

    # Create SQLite database
    conn = sqlite3.connect(db_path)

    products_df = pd.DataFrame(products_data)
    sales_df = pd.DataFrame(sales_data)

    products_df.to_sql('products', conn, index=False, if_exists='replace')
    sales_df.to_sql('sales', conn, index=False, if_exists='replace')

    conn.close()

    print(f"✅ Created SQLite database: {db_path}")
    print(
        f"📊 Tables: products ({len(products_df)} rows), sales ({len(sales_df)} rows)")

    return str(db_path)


def create_sample_json():
    """Create simple JSON data file"""
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)

    # Simple customer data
    customers_data = [
        {"customer_id": 1, "name": "John Smith", "region": "North",
            "orders": 5, "total_spent": 2500.99},
        {"customer_id": 2, "name": "Sarah Johnson",
            "region": "South", "orders": 3, "total_spent": 1850.50},
        {"customer_id": 3, "name": "Mike Davis", "region": "East",
            "orders": 7, "total_spent": 3200.75},
        {"customer_id": 4, "name": "Emily Wilson",
            "region": "West", "orders": 2, "total_spent": 999.99},
        {"customer_id": 5, "name": "Tom Brown", "region": "North",
            "orders": 4, "total_spent": 1750.25}
    ]

    json_path = data_dir / "sample_customers.json"
    with open(json_path, 'w') as f:
        json.dump(customers_data, f, indent=2)

    print(f"✅ Created JSON file: {json_path}")
    print(f"📊 Customer records: {len(customers_data)}")

    return str(json_path)


if __name__ == "__main__":
    print("🗄️ Creating Simple Sample Databases")
    print("=" * 50)
    print("Perfect for students - simple structure, small data")

    # Create SQLite database
    sqlite_path = create_sample_sqlite()

    # Create JSON data
    json_path = create_sample_json()

    print("\n" + "=" * 50)
    print("✅ Sample databases created!")
    print("\nNow you can test:")
    print("1. CSV ingestion with data/sample_sales.csv")
    print(f"2. SQLite ingestion with {sqlite_path}")
    print(f"3. JSON ingestion with {json_path}")
    print("\n💡 All files are small and simple - perfect for learning!")
