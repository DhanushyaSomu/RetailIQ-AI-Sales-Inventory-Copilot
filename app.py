import os
import subprocess
import sys


# ---------------------------------------------------------
# START STREAMLIT WHEN RUNNING: python app.py
# ---------------------------------------------------------

if os.environ.get("RETAILIQ_STREAMLIT") != "1":

    env = os.environ.copy()
    env["RETAILIQ_STREAMLIT"] = "1"

    subprocess.run(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            "app.py",
            "--server.port",
            "8000",
            "--server.headless",
            "true"
        ],
        env=env
    )

    sys.exit()


# ---------------------------------------------------------
# STREAMLIT APPLICATION
# ---------------------------------------------------------

import streamlit as st

from src.analytics import (
    load_data,
    get_dashboard_metrics,
    get_top_products,
    get_low_stock,
    get_overstock,
    get_store_sales,
    get_sales_change
)

from src.gemini import ask_gemini


# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="RetailIQ",
    page_icon="🛍️",
    layout="wide"
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

products, stores, sales, inventory = load_data()


# ---------------------------------------------------------
# DASHBOARD METRICS
# ---------------------------------------------------------

metrics = get_dashboard_metrics(
    products,
    sales,
    inventory
)


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

st.title("🛍️ RetailIQ")

st.subheader(
    "AI Sales & Inventory Copilot"
)

st.write(
    "An AI-powered assistant for retail sales "
    "and inventory analysis."
)


# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

col1, col2, col3, col4 = st.columns(4)


with col1:
    st.metric(
        "Total Sales",
        f"₹{metrics['total_sales']:,.0f}"
    )


with col2:
    st.metric(
        "Products",
        metrics["total_products"]
    )


with col3:
    st.metric(
        "Low Stock",
        metrics["low_stock_products"]
    )


with col4:
    st.metric(
        "Best Seller",
        metrics["best_selling_product"]
    )


st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

st.sidebar.title("RetailIQ")

page = st.sidebar.radio(
    "Navigate",
    [
        "AI Copilot",
        "Sales Analysis",
        "Inventory",
        "Store Performance"
    ]
)


# =========================================================
# AI COPILOT
# =========================================================

if page == "AI Copilot":

    st.header("🤖 AI Copilot")

    st.write(
        "Ask questions about your retail business data."
    )

    question = st.text_input(
        "Ask a question",
        placeholder=(
            "Example: Which products need immediate attention?"
        )
    )


    # -----------------------------------------------------
    # PREPARE BUSINESS CONTEXT
    # -----------------------------------------------------

    top_products = get_top_products(
        products,
        sales
    )

    low_stock = get_low_stock(
        products,
        stores,
        inventory
    )

    overstock = get_overstock(
        products,
        stores,
        inventory
    )

    store_sales = get_store_sales(
        stores,
        sales
    )

    sales_change = get_sales_change(
        products,
        sales
    )


    context = f"""
RETAIL BUSINESS DATA

DASHBOARD
Total Sales: ₹{metrics['total_sales']:,.2f}
Total Products: {metrics['total_products']}
Low Stock Products: {metrics['low_stock_products']}
Best Selling Product: {metrics['best_selling_product']}


TOP SELLING PRODUCTS
{top_products.to_string(index=False)}


LOW STOCK PRODUCTS
{low_stock.to_string(index=False)}


OVERSTOCK PRODUCTS
{overstock.to_string(index=False)}


STORE SALES
{store_sales.to_string(index=False)}


SALES CHANGE
{sales_change.to_string(index=False)}
"""


    # -----------------------------------------------------
    # ASK GEMINI
    # -----------------------------------------------------

    if st.button("Ask Copilot"):

        if not question.strip():

            st.warning(
                "Please enter a question."
            )

        else:

            with st.spinner(
                "RetailIQ is analyzing your data..."
            ):

                try:

                    answer = ask_gemini(
                        question,
                        context
                    )

                    st.success(
                        "Analysis complete"
                    )

                    st.markdown(answer)

                except Exception as e:

                    st.error(
                        f"Gemini API error: {e}"
                    )


# =========================================================
# SALES ANALYSIS
# =========================================================

elif page == "Sales Analysis":

    st.header("📈 Sales Analysis")


    st.subheader(
        "Top Selling Products"
    )

    top_products = get_top_products(
        products,
        sales
    )

    st.dataframe(
        top_products,
        use_container_width=True
    )


    st.subheader(
        "Sales Change"
    )

    sales_change = get_sales_change(
        products,
        sales
    )

    st.dataframe(
        sales_change,
        use_container_width=True
    )


# =========================================================
# INVENTORY
# =========================================================

elif page == "Inventory":

    st.header("📦 Inventory Management")


    st.subheader(
        "⚠️ Low Stock Products"
    )

    low_stock = get_low_stock(
        products,
        stores,
        inventory
    )

    if len(low_stock) > 0:

        st.dataframe(
            low_stock,
            use_container_width=True
        )

    else:

        st.success(
            "No low-stock products found."
        )


    st.subheader(
        "📦 Overstock Products"
    )

    overstock = get_overstock(
        products,
        stores,
        inventory
    )

    if len(overstock) > 0:

        st.dataframe(
            overstock,
            use_container_width=True
        )

    else:

        st.success(
            "No overstock products found."
        )


# =========================================================
# STORE PERFORMANCE
# =========================================================

elif page == "Store Performance":

    st.header("🏪 Store Performance")


    store_sales = get_store_sales(
        stores,
        sales
    )


    st.dataframe(
        store_sales,
        use_container_width=True
    )


    st.subheader(
        "Revenue by Store"
    )


    chart_data = store_sales.set_index(
        "store_name"
    )["total_revenue"]


    st.bar_chart(
        chart_data
    )