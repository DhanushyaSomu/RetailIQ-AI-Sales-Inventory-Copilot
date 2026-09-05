from src.analytics import (
    load_data,
    get_dashboard_metrics,
    get_top_products,
    get_low_stock,
    get_overstock,
    get_store_sales,
    get_product_sales,
    get_sales_change,
    get_attention_items
)


products, stores, sales, inventory = load_data()


print("\n========== DASHBOARD ==========")

dashboard = get_dashboard_metrics(
    products,
    sales,
    inventory
)

print(dashboard)


print("\n========== TOP PRODUCTS ==========")

print(
    get_top_products(
        products,
        sales
    )
)


print("\n========== LOW STOCK ==========")

print(
    get_low_stock(
        products,
        stores,
        inventory
    )
)


print("\n========== OVERSTOCK ==========")

print(
    get_overstock(
        products,
        stores,
        inventory
    )
)


print("\n========== STORE SALES ==========")

print(
    get_store_sales(
        stores,
        sales
    )
)


print("\n========== PRODUCT SALES ==========")

print(
    get_product_sales(
        products,
        sales
    ).head(10)
)


print("\n========== SALES CHANGE ==========")

print(
    get_sales_change(
        products,
        sales
    ).head(10)
)


print("\n========== ATTENTION ITEMS ==========")

attention = get_attention_items(
    products,
    stores,
    sales,
    inventory
)

print("\nLow Stock:")
print(attention["low_stock"])

print("\nDeclining Products:")
print(attention["declining_products"])