import os
import pandas as pd
import streamlit as st

# ---------------------------------------------------
# Data Folder
# ---------------------------------------------------

DATA_PATH = "data/processed"

# ---------------------------------------------------
# Generic CSV Loader
# ---------------------------------------------------

@st.cache_data(show_spinner=False)
def load_csv(file_name):
    """
    Load a CSV file from the processed data folder.
    """

    file_path = os.path.join(DATA_PATH, file_name)

    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        return pd.DataFrame()

    return pd.read_csv(file_path)

# ---------------------------------------------------
# Dashboard Files
# ---------------------------------------------------

@st.cache_data(show_spinner=False)
def load_dashboard_summary():
    return load_csv("dashboard_summary.csv")


@st.cache_data(show_spinner=False)
def load_monthly_revenue():
    return load_csv("monthly_revenue.csv")


@st.cache_data(show_spinner=False)
def load_revenue_by_country():
    return load_csv("revenue_by_country.csv")


@st.cache_data(show_spinner=False)
def load_revenue_by_segment():
    return load_csv("revenue_by_segment.csv")


@st.cache_data(show_spinner=False)
def load_segment_overview():
    return load_csv("segment_overview.csv")


@st.cache_data(show_spinner=False)
def load_customer_segments():
    return load_csv("customer_segments.csv")


@st.cache_data(show_spinner=False)
def load_purchase_funnel():
    return load_csv("purchase_funnel.csv")


@st.cache_data(show_spinner=False)
def load_top_customers():
    return load_csv("top_customers.csv")


@st.cache_data(show_spinner=False)
def load_cohort_retention():
    return load_csv("cohort_retention.csv")

# ---------------------------------------------------
# AI Report
# ---------------------------------------------------

@st.cache_data(show_spinner=False)
def load_ai_report():

    report_path = os.path.join(DATA_PATH, "ai_executive_report.md")

    if not os.path.exists(report_path):
        return None

    with open(report_path, "r", encoding="utf-8") as file:
        return file.read()

# ---------------------------------------------------
# Utility Functions
# ---------------------------------------------------

def currency(value):
    """
    Format numbers as currency.
    """

    try:
        return f"${value:,.2f}"
    except:
        return "$0.00"


def percentage(value):
    """
    Format percentage values.
    """

    try:
        return f"{value:.2f}%"
    except:
        return "0.00%"


def integer(value):
    """
    Format integer values.
    """

    try:
        return f"{int(value):,}"
    except:
        return "0"