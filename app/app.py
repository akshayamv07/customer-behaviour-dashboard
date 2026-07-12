import streamlit as st

st.set_page_config(
    page_title="Customer Behaviour Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------
# Sidebar
# ----------------------------

with st.sidebar:

    st.image(
        "https://img.icons8.com/color/96/combo-chart--v1.png",
        width=80
    )

    st.title("Customer Analytics")

    st.markdown("---")

    st.success("Project Status")

    st.write("✅ ETL Pipeline")
    st.write("✅ DuckDB Warehouse")
    st.write("✅ Feature Engineering")
    st.write("✅ Customer Segmentation")
    st.write("✅ AI Insights")
    st.write("✅ Power BI")
    st.write("✅ Streamlit")

    st.markdown("---")

    st.subheader("Technology Stack")

    st.markdown("""
- Python
- Pandas
- DuckDB
- Plotly
- Streamlit
- Scikit-Learn
- Power BI
- Google Gemini AI
""")

    st.markdown("---")

    st.caption("Developed by")
    st.write("**Akshaya Velumani**")

# ----------------------------
# Main Page
# ----------------------------

st.title("📊 Customer Behaviour Analytics Dashboard")

st.markdown("---")

st.markdown("""
## Welcome

This application provides an end-to-end analytics solution for understanding customer purchasing behaviour.

### Modules

- 📈 Executive Dashboard
- 👥 Customer Segmentation
- 🔄 Customer Retention
- 🤖 AI Business Insights

Use the navigation menu on the left to switch between pages.
""")

st.info(
    "Select any page from the sidebar to begin exploring the analytics."
)

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Project Objectives")

    st.markdown("""
- Analyze customer purchase behaviour
- Perform customer segmentation
- Predict churn risk
- Generate executive KPIs
- Create interactive dashboards
- Produce AI-generated insights
""")

with col2:

    st.subheader("Technologies Used")

    st.markdown("""
- Python
- DuckDB
- Pandas
- Scikit-Learn
- Streamlit
- Plotly
- Power BI
- Google Gemini AI
""")

st.markdown("---")

st.success("Project Completion: ~96%")