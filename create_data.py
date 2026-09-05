import os
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd


# -----------------------------
# Basic settings
# -----------------------------
random.seed(42)
np.random.seed(42)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


# -----------------------------
# 1. Product data
# -----------------------------
products = [
    ("P001", "Laptop", "Electronics", 55000),
    ("P002", "Wireless Mouse", "Electronics", 1200),
    ("P003", "Keyboard", "Electronics", 1800),
    ("P004", "Headphones", "Electronics", 2500),
    ("P005", "Smartphone", "Electronics", 28000),
    ("P006", "Tablet", "Electronics", 22000),
    ("P007", "Smart Watch", "Electronics", 6500),
    ("P008", "Bluetooth Speaker", "Electronics", 3500),
    ("P009", "USB Cable", "Accessories", 500),
    ("P010", "Power Bank", "Accessories", 1800),

    ("P011", "Backpack", "Fashion", 2200),
    ("P012", "Travel Bag", "Fashion", 3500),
    ("P013", "Sports Shoes", "Fashion", 4200),
    ("P014", "Casual Shoes", "Fashion", 3200),
    ("P015", "T-Shirt", "Fashion", 900),
    ("P016", "Jeans", "Fashion", 1800),
    ("P017", "Jacket", "Fashion", 3500),
    ("P018", "Cap", "Fashion", 600),

    ("P019", "Coffee Maker", "Home", 4500),
    ("P020", "Electric Kettle", "Home", 2200),
    ("P021", "Mixer Grinder", "Home", 5500),
    ("P022", "Air Fryer", "Home", 6500),
    ("P023", "Water Bottle", "Home", 800),
    ("P024", "Lunch Box", "Home", 700),

    ("P025", "Notebook", "Stationery", 250),
    ("P026", "Pen Set", "Stationery", 180),
    ("P027", "Desk Organizer", "Stationery", 450),
    ("P028", "Calculator", "Stationery", 550),
    ("P029", "Sticky Notes", "Stationery", 120),
    ("P030", "File Folder", "Stationery", 150),
]

products_df = pd.DataFrame(
    products,
    columns=["product_id", "product_name", "category", "price"]
)

products_df.to_csv(
    os.path.join(DATA_DIR, "products.csv"),
    index=False
)


# -----------------------------
# 2. Store data
# -----------------------------
stores = [
    ("S001", "Chennai Central", "Chennai"),
    ("S002", "Trichy Main", "Trichy"),
    ("S003", "Coimbatore Mall", "Coimbatore"),
    ("S004", "Madurai Plaza", "Madurai"),
    ("S005", "Salem Point", "Salem"),
]

stores_df = pd.DataFrame(
    stores,
    columns=["store_id", "store_name", "city"]
)

stores_df.to_csv(
    os.path.join(DATA_DIR, "stores.csv"),
    index=False
)


# -----------------------------
# 3. Generate sales data
# -----------------------------
sales_records = []

start_date = date(2026, 8, 1)

# Products with higher normal demand
high_demand = {
    "P001": 2.5,
    "P002": 7,
    "P003": 5,
    "P004": 6,
    "P005": 2.8,
    "P009": 10,
    "P010": 5,
    "P015": 8,
    "P023": 7,
    "P025": 12,
    "P026": 15,
    "P029": 14,
}

for day_number in range(30):

    current_date = start_date + timedelta(days=day_number)

    for store_id, store_name, city in stores:

        for _, product in products_df.iterrows():

            product_id = product["product_id"]

            # Default demand
            base_demand = 3

            # Higher demand for selected products
            if product_id in high_demand:
                base_demand = high_demand[product_id]

            # Weekend sales increase
            if current_date.weekday() >= 5:
                base_demand *= 1.25

            # Create a sales spike for some products
            if product_id in ["P001", "P005", "P015"] and day_number >= 20:
                base_demand *= 1.8

            # Create a sales drop for some products
            if product_id in ["P019", "P021"] and day_number >= 20:
                base_demand *= 0.45

            # Small store variation
            store_factor = {
                "S001": 1.20,
                "S002": 0.90,
                "S003": 1.10,
                "S004": 0.85,
                "S005": 0.75,
            }[store_id]

            demand = base_demand * store_factor

            quantity = np.random.poisson(max(demand, 0.1))

            # Avoid too many zero-sales rows
            if quantity == 0 and random.random() < 0.35:
                quantity = 1

            revenue = quantity * product["price"]

            sales_records.append(
                [
                    current_date,
                    store_id,
                    product_id,
                    quantity,
                    revenue,
                ]
            )


sales_df = pd.DataFrame(
    sales_records,
    columns=[
        "date",
        "store_id",
        "product_id",
        "quantity",
        "revenue",
    ],
)

sales_df.to_csv(
    os.path.join(DATA_DIR, "sales.csv"),
    index=False
)


# -----------------------------
# 4. Generate inventory data
# -----------------------------
inventory_records = []

for store_id, store_name, city in stores:

    for _, product in products_df.iterrows():

        product_id = product["product_id"]

        # Different initial stock based on product
        if product_id in ["P001", "P005", "P006"]:
            initial_stock = random.randint(25, 50)

        elif product_id in ["P009", "P015", "P025", "P026", "P029"]:
            initial_stock = random.randint(80, 150)

        else:
            initial_stock = random.randint(30, 90)

        # Calculate total quantity sold
        total_sold = sales_df[
            (sales_df["store_id"] == store_id)
            & (sales_df["product_id"] == product_id)
        ]["quantity"].sum()

        current_stock = max(initial_stock - total_sold, 0)

        # Intentionally create some low-stock products
        if product_id == "P004" and store_id == "S001":
            current_stock = 3

        if product_id == "P001" and store_id == "S002":
            current_stock = 5

        if product_id == "P005" and store_id == "S003":
            current_stock = 4

        # Intentionally create some overstock
        if product_id == "P019" and store_id == "S004":
            current_stock = 180

        if product_id == "P021" and store_id == "S005":
            current_stock = 160

        inventory_records.append(
            [
                store_id,
                product_id,
                initial_stock,
                int(current_stock),
            ]
        )


inventory_df = pd.DataFrame(
    inventory_records,
    columns=[
        "store_id",
        "product_id",
        "initial_stock",
        "current_stock",
    ],
)

inventory_df.to_csv(
    os.path.join(DATA_DIR, "inventory.csv"),
    index=False
)


# -----------------------------
# 5. Print summary
# -----------------------------
print("\n====================================")
print("RetailIQ Dataset Created Successfully")
print("====================================")

print(f"\nProducts : {len(products_df)}")
print(f"Stores   : {len(stores_df)}")
print(f"Sales rows: {len(sales_df)}")
print(f"Inventory rows: {len(inventory_df)}")

print("\nFiles created inside data/:")
print("1. products.csv")
print("2. stores.csv")
print("3. sales.csv")
print("4. inventory.csv")

print("\nDataset generation completed!")