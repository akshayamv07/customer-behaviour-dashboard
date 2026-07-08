"""
Project Configuration File
Stores all paths and constants used across the project.
"""

# ==============================
# DATA PATHS
# ==============================

RAW_DATA_PATH = "data/raw/online_retail_II.csv"

PROCESSED_DATA_PATH = "data/processed"

DATABASE_PATH = "data/customer_analytics.duckdb"


# ==============================
# DATABASE TABLES
# ==============================

CUSTOMER_EVENTS_TABLE = "customer_events"


# ==============================
# SEGMENTATION
# ==============================

N_CLUSTERS = 5
RANDOM_STATE = 42