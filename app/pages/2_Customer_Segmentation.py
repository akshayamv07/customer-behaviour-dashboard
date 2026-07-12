import streamlit as st

from utils import (
    load_customer_segments,
    load_segment_overview,
    currency
)

from charts import (
    bar_chart,
    scatter_chart
)

from sidebar import build_sidebar

st.set_page_config(
    page_title="Customer Segmentation",
    layout="wide"
)

st.title("👥 Customer Segmentation Dashboard")

# ----------------------------------------
# Load Data
# ----------------------------------------

customer_segments = load_customer_segments()
segment_overview = load_segment_overview()

if customer_segments.empty:
    st.error("Customer Segmentation data not found.")
    st.stop()

# ----------------------------------------
# Sidebar
# ----------------------------------------

filters = build_sidebar(
    customer_segments=customer_segments
)

selected_segment = filters["segment"]
selected_churn = filters["churn"]

filtered = customer_segments.copy()

if selected_segment != "All":
    filtered = filtered[
        filtered["Segment"] == selected_segment
    ]

if selected_churn != "All":
    filtered = filtered[
        filtered["ChurnRisk"] == selected_churn
    ]

# ----------------------------------------
# KPI Cards
# ----------------------------------------

st.subheader("Segmentation KPIs")

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Customers",
    len(filtered)
)

c2.metric(
    "Segments",
    filtered["Segment"].nunique()
)

c3.metric(
    "Average Revenue",
    currency(filtered["Monetary"].mean())
)

c4.metric(
    "Average Frequency",
    f"{filtered['Frequency'].mean():.2f}"
)

st.divider()

# ----------------------------------------
# Segment Distribution
# ----------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("📊 Customer Segment Distribution")

    segment_counts = (
        filtered["Segment"]
        .value_counts()
        .reset_index()
    )

    segment_counts.columns = ["Segment", "Customers"]

    st.plotly_chart(
        bar_chart(
            segment_counts,
            x="Segment",
            y="Customers",
            title="Customers by Segment",
            color="Segment",
            text="Customers"
        ),
        use_container_width=True
    )

with right:

    st.subheader("💰 Average Revenue by Segment")

    revenue_segment = (
        filtered
        .groupby("Segment")["Monetary"]
        .mean()
        .reset_index()
    )

    revenue_segment.columns = [
        "Segment",
        "AverageRevenue"
    ]

    st.plotly_chart(
        bar_chart(
            revenue_segment,
            x="Segment",
            y="AverageRevenue",
            title="Average Revenue",
            color="Segment",
            text="AverageRevenue"
        ),
        use_container_width=True
    )

st.divider()

# ----------------------------------------
# Customer Value Distribution
# ----------------------------------------

st.subheader("📈 Customer Value Distribution")

scatter_df = filtered[
    [
        "CustomerID",
        "Recency",
        "Monetary",
        "Segment"
    ]
].dropna()

st.plotly_chart(
    scatter_chart(
        scatter_df,
        x="Recency",
        y="Monetary",
        color="Segment",
        hover="CustomerID",
        title="Customer Value Distribution"
    ),
    use_container_width=True
)

st.divider()

# ----------------------------------------
# Customer Search
# ----------------------------------------

st.subheader("🔍 Customer Search")

customer_search = st.text_input(
    "Search Customer ID"
)

customer_table = filtered.copy()

if customer_search:

    customer_table = customer_table[
        customer_table["CustomerID"]
        .astype(str)
        .str.contains(customer_search)
    ]

st.dataframe(
    customer_table,
    use_container_width=True,
    hide_index=True
)

st.download_button(
    label="📥 Download Filtered Customers",
    data=customer_table.to_csv(index=False),
    file_name="filtered_customers.csv",
    mime="text/csv"
)

st.divider()

st.success(
    f"Showing {len(customer_table)} customer(s)"
)