import pandas as pd
import duckdb

from .config import (
    RAW_DATA_PATH,
    CRM_DATA_PATH,
    DATABASE_PATH,
    CUSTOMER_EVENTS_TABLE
)

def load_data():
    """
    Load the Online Retail dataset and CRM dataset.
    """

    retail_df = pd.read_csv(RAW_DATA_PATH)
    crm_df = pd.read_csv(CRM_DATA_PATH)

    print("\nRetail Dataset Loaded Successfully!")
    print(f"Rows    : {retail_df.shape[0]}")
    print(f"Columns : {retail_df.shape[1]}")

    print("\nCRM Dataset Loaded Successfully!")
    print(f"Rows    : {crm_df.shape[0]}")
    print(f"Columns : {crm_df.shape[1]}")

    return retail_df, crm_df


def clean_data(df):
    """
    Clean the dataset.
    """

    print("\nCleaning Dataset...")

    # Remove rows with missing Customer ID
    df = df.dropna(subset=["Customer ID"])

    # Remove rows with missing Description
    df = df.dropna(subset=["Description"])

    # Remove duplicate rows
    df = df.drop_duplicates()

    # Keep only positive quantities
    df = df[df["Quantity"] > 0]

    # Keep only positive prices
    df = df[df["Price"] > 0]

    # Convert InvoiceDate to datetime
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # Create TotalAmount column
    df["TotalAmount"] = df["Quantity"] * df["Price"]

    print("Cleaning Completed!")

    print(f"Rows after cleaning : {len(df)}")
    print(f"Columns             : {len(df.columns)}")

    return df

def merge_data(retail_df, crm_df):
    """
    Merge Retail and CRM datasets.
    """

    print("\nMerging Retail and CRM datasets...")

    merged_df = retail_df.merge(
        crm_df,
        on="Customer ID",
        how="left"
    )

    print("Merge Completed!")
    print(f"Rows after merge : {len(merged_df)}")
    print(f"Columns          : {len(merged_df.columns)}")

    return merged_df

def save_to_duckdb(df):
    """
    Save cleaned data into DuckDB.
    """

    print("\nSaving data to DuckDB...")

    conn = duckdb.connect(DATABASE_PATH)

    conn.execute(f"DROP TABLE IF EXISTS {CUSTOMER_EVENTS_TABLE}")

    conn.register("customer_df", df)

    conn.execute(f"""
        CREATE TABLE {CUSTOMER_EVENTS_TABLE} AS
        SELECT *
        FROM customer_df
    """)

    conn.close()

    print("DuckDB database created successfully!")

if __name__ == "__main__":

    retail_df, crm_df = load_data()

    retail_df = clean_data(retail_df)

    merged_df = merge_data(retail_df, crm_df)

    save_to_duckdb(merged_df)

