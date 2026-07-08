import duckdb
import pandas as pd

from config import (
    DATABASE_PATH,
    CUSTOMER_EVENTS_TABLE,
    CUSTOMER_FEATURES_TABLE
)


def load_customer_events():
    """
    Load cleaned customer events from DuckDB.
    """

    print("Connecting to DuckDB...")

    conn = duckdb.connect(DATABASE_PATH)

    query = f"""
        SELECT *
        FROM {CUSTOMER_EVENTS_TABLE}
    """

    df = conn.execute(query).fetchdf()

    conn.close()

    print("Data loaded successfully!")
    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    return df


def create_customer_features():
    """
    Create customer-level features from transaction data.
    """

    print("\nCreating customer features...")

    conn = duckdb.connect(DATABASE_PATH)

    query = f"""
    CREATE OR REPLACE TABLE {CUSTOMER_FEATURES_TABLE} AS

    SELECT

        "Customer ID"                       AS CustomerID,

        COUNT(DISTINCT Invoice)             AS TotalOrders,

        SUM(Quantity)                       AS TotalQuantity,

        ROUND(SUM(TotalAmount), 2)          AS TotalRevenue,

        ROUND(AVG(TotalAmount), 2)          AS AverageOrderValue,

        MIN(InvoiceDate)                    AS FirstPurchaseDate,

        MAX(InvoiceDate)                    AS LastPurchaseDate,

        MIN(Country)                        AS Country

    FROM {CUSTOMER_EVENTS_TABLE}

    GROUP BY "Customer ID"

    ORDER BY TotalRevenue DESC
    """

    conn.execute(query)

    total_customers = conn.execute(
        f"SELECT COUNT(*) FROM {CUSTOMER_FEATURES_TABLE}"
    ).fetchone()[0]

    conn.close()

    print("Customer features created successfully!")
    print(f"Total Customers : {total_customers}")

def preview_customer_features():
    """
    Display the first 10 customer feature records.
    """

    print("\nPreviewing customer features...\n")

    conn = duckdb.connect(DATABASE_PATH)

    df = conn.execute(f"""
        SELECT *
        FROM {CUSTOMER_FEATURES_TABLE}
        LIMIT 10
    """).fetchdf()

    conn.close()

    print(df)

if __name__ == "__main__":
    load_customer_events()
    create_customer_features()
    preview_customer_features()