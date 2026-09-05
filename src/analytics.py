import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_data():
    products = pd.read_csv(DATA_DIR / "products.csv")
    stores = pd.read_csv(DATA_DIR / "stores.csv")
    sales = pd.read_csv(DATA_DIR / "sales.csv")
    inventory = pd.read_csv(DATA_DIR / "inventory.csv")

    sales["date"] = pd.to_datetime(sales["date"])

    return products, stores, sales, inventory


# ---------------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------------

def get_dashboard_metrics(products, sales, inventory):

    total_sales = sales["revenue"].sum()

    total_products = products["product_id"].nunique()

    low_stock_count = len(
        inventory[inventory["current_stock"] <= 10]
    )

    best_product_id = (
        sales.groupby("product_id")["quantity"]
        .sum()
        .idxmax()
    )

    best_product_name = products.loc[
        products["product_id"] == best_product_id,
        "product_name"
    ].iloc[0]

    return {
        "total_sales": round(total_sales, 2),
        "total_products": total_products,
        "low_stock_products": low_stock_count,
        "best_selling_product": best_product_name
    }


# ---------------------------------------------------------
# TOP SELLING PRODUCTS
# ---------------------------------------------------------

def get_top_products(products, sales, n=5):

    result = (
        sales.groupby("product_id")
        .agg(
            quantity_sold=("quantity", "sum"),
            revenue=("revenue", "sum")
        )
        .reset_index()
        .merge(products, on="product_id")
        .sort_values("quantity_sold", ascending=False)
        .head(n)
    )

    return result[
        [
            "product_id",
            "product_name",
            "category",
            "quantity_sold",
            "revenue"
        ]
    ]


# ---------------------------------------------------------
# LOW STOCK
# ---------------------------------------------------------

def get_low_stock(products, stores, inventory):

    result = (
        inventory[inventory["current_stock"] <= 10]
        .merge(products, on="product_id")
        .merge(stores, on="store_id")
        .sort_values("current_stock")
    )

    return result[
        [
            "store_name",
            "city",
            "product_name",
            "category",
            "current_stock"
        ]
    ]


# ---------------------------------------------------------
# OVERSTOCK
# ---------------------------------------------------------

def get_overstock(products, stores, inventory):

    result = (
        inventory[inventory["current_stock"] >= 100]
        .merge(products, on="product_id")
        .merge(stores, on="store_id")
        .sort_values("current_stock", ascending=False)
    )

    return result[
        [
            "store_name",
            "city",
            "product_name",
            "category",
            "current_stock"
        ]
    ]


# ---------------------------------------------------------
# STORE SALES
# ---------------------------------------------------------

def get_store_sales(stores, sales):

    result = (
        sales.groupby("store_id")
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum")
        )
        .reset_index()
        .merge(stores, on="store_id")
        .sort_values("total_revenue", ascending=False)
    )

    return result[
        [
            "store_name",
            "city",
            "total_quantity",
            "total_revenue"
        ]
    ]


# ---------------------------------------------------------
# PRODUCT SALES
# ---------------------------------------------------------

def get_product_sales(products, sales):

    result = (
        sales.groupby("product_id")
        .agg(
            total_quantity=("quantity", "sum"),
            total_revenue=("revenue", "sum")
        )
        .reset_index()
        .merge(products, on="product_id")
        .sort_values("total_revenue", ascending=False)
    )

    return result[
        [
            "product_name",
            "category",
            "total_quantity",
            "total_revenue"
        ]
    ]


# ---------------------------------------------------------
# SALES CHANGE
# ---------------------------------------------------------

def get_sales_change(products, sales):

    max_date = sales["date"].max()

    recent_start = max_date - pd.Timedelta(days=13)
    previous_start = recent_start - pd.Timedelta(days=14)
    previous_end = recent_start - pd.Timedelta(days=1)

    recent = sales[
        (sales["date"] >= recent_start) &
        (sales["date"] <= max_date)
    ]

    previous = sales[
        (sales["date"] >= previous_start) &
        (sales["date"] <= previous_end)
    ]

    recent_sales = (
        recent.groupby("product_id")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"revenue": "recent_revenue"})
    )

    previous_sales = (
        previous.groupby("product_id")["revenue"]
        .sum()
        .reset_index()
        .rename(columns={"revenue": "previous_revenue"})
    )

    result = (
        products[["product_id", "product_name", "category"]]
        .merge(recent_sales, on="product_id", how="left")
        .merge(previous_sales, on="product_id", how="left")
        .fillna(0)
    )

    result["change_percent"] = (
        (result["recent_revenue"] - result["previous_revenue"])
        / result["previous_revenue"].replace(0, 1)
    ) * 100

    result["change_percent"] = result["change_percent"].round(2)

    return result.sort_values(
        "change_percent",
        ascending=False
    )


# ---------------------------------------------------------
# ATTENTION ITEMS
# ---------------------------------------------------------

def get_attention_items(products, stores, sales, inventory):

    low_stock = get_low_stock(
        products,
        stores,
        inventory
    )

    sales_change = get_sales_change(
        products,
        sales
    )

    declining_products = sales_change[
        sales_change["change_percent"] < -20
    ].head(5)

    return {
        "low_stock": low_stock,
        "declining_products": declining_products
    }