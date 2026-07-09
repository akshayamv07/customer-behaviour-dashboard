import duckdb
import pandas as pd

from config import (
    DATABASE_PATH,
    CUSTOMER_SEGMENTS_TABLE
)

OUTPUT_PATH = "data/processed/purchase_funnel.csv"


def load_segments():
    print("Loading segmented customer data...")

    conn = duckdb.connect(DATABASE_PATH)

    df = conn.execute(f"""
        SELECT *
        FROM {CUSTOMER_SEGMENTS_TABLE}
    """).fetchdf()

    conn.close()

    print(f"Rows Loaded : {len(df)}")

    return df


def generate_purchase_funnel(df):

    print("\nGenerating Purchase Funnel...")

    acquired = len(df)

    repeat = (df["TotalOrders"] > 1).sum()

    loyal = (df["TotalOrders"] > 5).sum()

    champion = (df["Segment"] == "Champion").sum()

    funnel = pd.DataFrame({
        "Stage": [
            "Customers Acquired",
            "Repeat Customers",
            "Loyal Customers",
            "Champion Customers"
        ],
        "Customers": [
            acquired,
            repeat,
            loyal,
            champion
        ]
    })

    funnel.to_csv(
        OUTPUT_PATH,
        index=False
    )

    print(f"Saved : {OUTPUT_PATH}")

    print("\nPurchase Funnel\n")

    print(funnel)


if __name__ == "__main__":

    df = load_segments()

    generate_purchase_funnel(df)