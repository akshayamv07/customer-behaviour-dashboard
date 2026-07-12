import streamlit as st


def build_sidebar(customer_segments=None, revenue_country=None):
    """
    Build the common sidebar used across all pages.

    Returns:
        dict containing selected filters.
    """

    with st.sidebar:

        st.markdown("## 📊 Customer Analytics")

        st.markdown("---")

        st.success("Navigation")

        st.info(
            """
Use the page selector above to switch dashboards.
"""
        )

        st.markdown("---")

        filters = {}

        # ----------------------------
        # Country Filter
        # ----------------------------

        if revenue_country is not None and not revenue_country.empty:

            countries = sorted(revenue_country["Country"].dropna().unique())

            filters["country"] = st.selectbox(
                "🌍 Country",
                ["All"] + countries
            )

        else:
            filters["country"] = "All"

        # ----------------------------
        # Segment Filter
        # ----------------------------

        if customer_segments is not None and not customer_segments.empty:

            segments = sorted(customer_segments["Segment"].dropna().unique())

            filters["segment"] = st.selectbox(
                "👥 Customer Segment",
                ["All"] + segments
            )

        else:
            filters["segment"] = "All"

        # ----------------------------
        # Churn Filter
        # ----------------------------

        if customer_segments is not None and not customer_segments.empty:

            churn_levels = sorted(
                customer_segments["ChurnRisk"].dropna().unique()
            )

            filters["churn"] = st.selectbox(
                "⚠️ Churn Risk",
                ["All"] + churn_levels
            )

        else:
            filters["churn"] = "All"

        st.markdown("---")

        st.markdown("### 📥 Downloads")

        st.caption(
            "Reports can be downloaded from each dashboard page."
        )

        st.markdown("---")

        st.markdown("### ℹ️ About")

        st.write(
            """
Customer Behaviour Analytics
Version **1.0**

Built using:

- Python
- DuckDB
- Streamlit
- Plotly
- Power BI
- Gemini AI
"""
        )

        st.markdown("---")

        st.caption("© 2026 Akshaya Velumani")

    return filters