import streamlit as st

from utils import (
    load_customer_segments,
    currency
)

from charts import (
    pie_chart,
    bar_chart,
    scatter_chart
)

from sidebar import build_sidebar

st.set_page_config(
    page_title="Customer Retention",
    layout="wide"
)

st.title("🔄 Customer Retention Dashboard")

# --------------------------------------------------
# Load Data
# --------------------------------------------------

customer_segments = load_customer_segments()

if customer_segments.empty:
    st.error("Customer Segmentation data not found.")
    st.stop()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

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

# --------------------------------------------------
# KPI Cards
# --------------------------------------------------

st.subheader("Retention KPIs")

c1, c2, c3, c4 = st.columns(4)

high_risk = len(
    filtered[
        filtered["ChurnRisk"].isin(
            ["High", "Very High"]
        )
    ]
)

c1.metric(
    "Customers",
    len(filtered)
)

c2.metric(
    "High Risk",
    high_risk
)

c3.metric(
    "Average Recency",
    f"{filtered['Recency'].mean():.1f} Days"
)

c4.metric(
    "Average Frequency",
    f"{filtered['Frequency'].mean():.2f}"
)

st.divider()

# --------------------------------------------------
# Charts
# --------------------------------------------------

left, right = st.columns(2)

with left:

    st.subheader("⚠️ Churn Risk Distribution")

    churn = (
        filtered["ChurnRisk"]
        .value_counts()
        .reset_index()
    )

    churn.columns = [
        "ChurnRisk",
        "Customers"
    ]

    st.plotly_chart(
        pie_chart(
            churn,
            names="ChurnRisk",
            title="Customer Churn Risk"
        ),
        use_container_width=True
    )

with right:

    st.subheader("📊 Average Recency by Segment")

    recency = (
        filtered
        .groupby("Segment")["Recency"]
        .mean()
        .reset_index()
    )

    st.plotly_chart(
        bar_chart(
            recency,
            x="Segment",
            y="Recency",
            title="Average Recency",
            color="Segment",
            text="Recency"
        ),
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# Frequency
# --------------------------------------------------

st.subheader("🛒 Average Purchase Frequency")

frequency = (
    filtered
    .groupby("Segment")["Frequency"]
    .mean()
    .reset_index()
)

st.plotly_chart(
    bar_chart(
        frequency,
        x="Segment",
        y="Frequency",
        title="Average Purchase Frequency",
        color="Segment",
        text="Frequency"
    ),
    use_container_width=True
)

st.divider()

# --------------------------------------------------
# Customer Lifetime Value
# --------------------------------------------------

if "CustomerLifetimeValue" in filtered.columns:

    scatter = filtered[
        [
            "CustomerID",
            "Recency",
            "CustomerLifetimeValue",
            "Segment"
        ]
    ].dropna()

    st.subheader("💎 Customer Lifetime Value")

    st.plotly_chart(
        scatter_chart(
            scatter,
            x="Recency",
            y="CustomerLifetimeValue",
            color="Segment",
            hover="CustomerID",
            title="Customer Lifetime Value vs Recency"
        ),
        use_container_width=True
    )

st.divider()

# --------------------------------------------------
# Download
# --------------------------------------------------

st.download_button(
    "📥 Download Retention Data",
    filtered.to_csv(index=False),
    "retention_data.csv",
    "text/csv"
)

st.success(
    f"Showing {len(filtered)} customer(s)"
)