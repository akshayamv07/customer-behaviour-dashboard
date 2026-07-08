import duckdb
import pandas as pd

from config import (
    DATABASE_PATH,
    CUSTOMER_EVENTS_TABLE,
    CUSTOMER_FEATURES_TABLE,
    CUSTOMER_SEGMENTS_TABLE
)


def load_customer_events():
    """
    Load customer_events table.
    """

    conn = duckdb.connect(DATABASE_PATH)

    df = conn.execute(f"""
        SELECT *
        FROM {CUSTOMER_EVENTS_TABLE}
    """).fetchdf()

    conn.close()

    return df


def load_customer_features():
    """
    Load customer_features table.
    """

    conn = duckdb.connect(DATABASE_PATH)

    df = conn.execute(f"""
        SELECT *
        FROM {CUSTOMER_FEATURES_TABLE}
    """).fetchdf()

    conn.close()

    return df


def load_customer_segments():
    """
    Load customer_segments table.
    """

    conn = duckdb.connect(DATABASE_PATH)

    df = conn.execute(f"""
        SELECT *
        FROM {CUSTOMER_SEGMENTS_TABLE}
    """).fetchdf()

    conn.close()

    return df