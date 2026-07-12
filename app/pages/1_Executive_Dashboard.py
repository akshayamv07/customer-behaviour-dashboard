import streamlit as st
import pandas as pd

from utils import (
    load_dashboard_summary,
    load_monthly_revenue,
    load_revenue_by_country,
    load_revenue_by_segment,
    load_purchase_funnel,
    load_top_customers,
    currency,
    integer
)

from charts import (
    line_chart,
    bar_chart,
    funnel_chart
)

from sidebar import build_sidebar

st.set_page_config(
    page_title="Executive Dashboard",
    layout="wide"
)

st.title("📈 Executive Dashboard")

# -----------------------------
# Load Data
# -----------------------------

summary = load_dashboard_summary()
monthly = load_monthly_revenue()
country = load_revenue_by_country()
segment = load_revenue_by_segment()
funnel = load_purchase_funnel()
top_customers = load_top_customers()

if summary.empty:
    st.error("Dashboard summary could not be loaded.")
    st.stop()

# -----------------------------
# Sidebar Filters
# -----------------------------

filters = build_sidebar(
    revenue_country=country
)

selected_country = filters["country"]

# -----------------------------
# Apply Filters
# -----------------------------

country_filtered = country.copy()

if selected_country != "All":
    country_filtered = country_filtered[
        country_filtered["Country"] == selected_country
    ]

# -----------------------------
# KPI Cards
# -----------------------------

st.subheader("Executive KPIs")

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "💰 Total Revenue",
        currency(summary.loc[0, "TotalRevenue"])
    )

with col2:

    st.metric(
        "👥 Customers",
        integer(summary.loc[0, "TotalCustomers"])
    )

with col3:

    st.metric(
        "🧾 Orders",
        integer(summary.loc[0, "TotalOrders"])
    )

with col4:

    st.metric(
        "🛒 Avg Order Value",
        currency(summary.loc[0, "AverageOrderValue"])
    )

st.divider()

# -----------------------------
# Revenue Trend
# -----------------------------

left, right = st.columns((2, 1))

with left:

    st.plotly_chart(
        line_chart(
            monthly,
            "YearMonth",
            "TotalRevenue",
            "Monthly Revenue Trend"
        ),
        use_container_width=True
    )

with right:

    st.plotly_chart(
        funnel_chart(funnel),
        use_container_width=True
    )

st.divider()

# -----------------------------
# Revenue by Country
# -----------------------------

left, right = st.columns(2)

with left:

    st.subheader("🌍 Revenue by Country")

    display_country = (
        country_filtered
        .sort_values("TotalRevenue", ascending=False)
        .head(10)
    )

    st.plotly_chart(
        bar_chart(
            display_country,
            x="Country",
            y="TotalRevenue",
            title="Top Countries by Revenue",
            color="Country",
            text="TotalRevenue"
        ),
        use_container_width=True
    )

with right:

    st.subheader("📊 Revenue by Segment")

    st.plotly_chart(
        bar_chart(
            segment,
            x="Segment",
            y="TotalRevenue",
            title="Revenue by Customer Segment",
            color="Segment",
            text="TotalRevenue"
        ),
        use_container_width=True
    )

st.divider()

# -----------------------------
# Top Customers
# -----------------------------

st.subheader("🏆 Top 10 Customers")

top_customers_display = top_customers.copy()

top_customers_display["TotalRevenue"] = (
    top_customers_display["TotalRevenue"]
    .map(currency)
)

top_customers_display["TotalQuantity"] = (
    top_customers_display["TotalQuantity"]
    .map(integer)
)

st.dataframe(
    top_customers_display,
    use_container_width=True,
    hide_index=True
)

csv = top_customers.to_csv(index=False).encode("utf-8")

st.download_button(
    label="📥 Download Top Customers",
    data=csv,
    file_name="top_customers.csv",
    mime="text/csv"
)

st.divider()

# -----------------------------
# Executive Summary
# -----------------------------

st.subheader("📋 Executive Summary")

summary_text = f"""
### Business Snapshot

- Total Revenue: **{currency(summary.loc[0, 'TotalRevenue'])}**
- Total Customers: **{integer(summary.loc[0, 'TotalCustomers'])}**
- Total Orders: **{integer(summary.loc[0, 'TotalOrders'])}**
- Average Order Value: **{currency(summary.loc[0, 'AverageOrderValue'])}**

This dashboard provides a high-level overview of customer purchasing behaviour,
revenue trends, sales distribution, and top-performing customers.

Use the other dashboard pages to explore segmentation, retention, and AI-generated
business insights in greater detail.
"""

st.markdown(summary_text)