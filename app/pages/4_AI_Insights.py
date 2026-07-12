import streamlit as st
import os

from utils import load_ai_report

st.set_page_config(
    page_title="AI Business Insights",
    layout="wide"
)

st.title("🤖 AI Business Insights")

st.markdown(
"""
This dashboard presents AI-generated business insights and executive recommendations
based on customer purchasing behaviour and segmentation analysis.
"""
)

st.divider()

# -----------------------------------------------------
# Load AI Report
# -----------------------------------------------------

report = load_ai_report()

if report is None:

    st.error("AI Executive Report not found.")

    st.info(
        """
Generate the report first by running:

python src/ai_insights.py
"""
    )

    st.stop()

st.success("AI Executive Report Loaded Successfully")

st.divider()

# -----------------------------------------------------
# Executive Summary
# -----------------------------------------------------

st.subheader("📋 Executive Report")

st.markdown(report)

st.divider()

# -----------------------------------------------------
# Downloads
# -----------------------------------------------------

st.subheader("📥 Download Report")

st.download_button(
    label="Download AI Executive Report",
    data=report,
    file_name="AI_Executive_Report.md",
    mime="text/markdown"
)

st.divider()

# -----------------------------------------------------
# Quick Insights
# -----------------------------------------------------

st.subheader("📌 Key Business Focus Areas")

col1, col2 = st.columns(2)

with col1:

    st.info("""
### Customer Retention

Focus on reducing churn among High and Very High risk customers through
targeted engagement campaigns.
""")

    st.info("""
### Loyalty Growth

Move Regular customers into Loyal and Champion segments
using personalized offers.
""")

with col2:

    st.info("""
### Revenue Optimization

Increase customer lifetime value through upselling,
cross-selling and personalized marketing.
""")

    st.info("""
### Executive Monitoring

Review KPIs monthly and monitor revenue,
customer growth and churn trends.
""")

st.divider()

# -----------------------------------------------------
# Application Information
# -----------------------------------------------------

st.subheader("ℹ️ About This Dashboard")

st.markdown("""
This report is automatically generated using:

- Google Gemini AI
- Customer Segmentation
- Revenue Analytics
- Churn Risk Analysis
- Executive KPI Summary

The objective is to provide management with actionable
business insights and strategic recommendations.
""")

st.success("AI Insights Dashboard Ready")