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
CUSTOMER_FEATURES_TABLE = "customer_features"
CUSTOMER_SEGMENTS_TABLE = "customer_segments"

# ==============================
# Output Folder
# ==============================

PROCESSED_DATA_PATH = "data/processed"

# ==============================
# SEGMENTATION
# ==============================

N_CLUSTERS = 5
RANDOM_STATE = 42