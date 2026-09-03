import os
import pandas as pd

from .config import PROCESSED_DATA_PATH

from .database import (
    load_customer_segments,
    load_customer_events
)

def generate_segment_overview(df):
    """
    Generate segment overview KPI and export to CSV.
    """

    print("\nGenerating Segment Overview...")

    segment_overview = (
        df.groupby("Segment")
        .agg(
            Customers=("CustomerID", "count"),
            AverageRevenue=("Monetary", "mean"),
            AverageFrequency=("Frequency", "mean"),
            AverageRecency=("Recency", "mean"),
            AverageOrderValue=("AverageOrderValue", "mean")
        )
        .round(2)
        .reset_index()
    )

    output_path = os.path.join(
        PROCESSED_DATA_PATH,
        "segment_overview.csv"
    )

    segment_overview.to_csv(output_path, index=False)

    print(f"Saved : {output_path}")

    return segment_overview

def generate_revenue_by_segment(df):
    """
    Generate revenue by segment and export to CSV.
    """

    print("\nGenerating Revenue by Segment...")

    revenue = (
        df.groupby("Segment")
        .agg(
            TotalRevenue=("Monetary", "sum")
        )
        .round(2)
        .reset_index()
        .sort_values("TotalRevenue", ascending=False)
    )

    output_path = os.path.join(
        PROCESSED_DATA_PATH,
        "revenue_by_segment.csv"
    )

    revenue.to_csv(output_path, index=False)

    print(f"Saved : {output_path}")

    return revenue

def generate_monthly_revenue(df):
    """
    Generate monthly revenue from transaction-level data.
    """

    print("\nGenerating Monthly Revenue Trend...")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    df["YearMonth"] = df["InvoiceDate"].dt.to_period("M").astype(str)

    monthly = (
        df.groupby("YearMonth")
        .agg(
            TotalRevenue=("TotalAmount", "sum"),
            Orders=("Invoice", "nunique"),
            Customers=("Customer ID", "nunique")
        )
        .round(2)
        .reset_index()
    )

    output_path = os.path.join(
        PROCESSED_DATA_PATH,
        "monthly_revenue.csv"
    )

    monthly.to_csv(output_path, index=False)

    print(f"Saved : {output_path}")

    return monthly

def generate_revenue_by_country(df):
    """
    Generate revenue by country and export to CSV.
    """

    print("\nGenerating Revenue by Country...")

    revenue_country = (
        df.groupby("Country")
        .agg(
            TotalRevenue=("TotalAmount", "sum"),
            Orders=("Invoice", "nunique"),
            Customers=("Customer ID", "nunique")
        )
        .round(2)
        .reset_index()
        .sort_values("TotalRevenue", ascending=False)
    )

    output_path = os.path.join(
        PROCESSED_DATA_PATH,
        "revenue_by_country.csv"
    )

    revenue_country.to_csv(output_path, index=False)

    print(f"Saved : {output_path}")

    return revenue_country

def generate_top_customers(df):
    """
    Generate Top 10 customers by revenue.
    """

    print("\nGenerating Top Customers...")

    top_customers = (
        df.groupby("Customer ID")
        .agg(
            TotalRevenue=("TotalAmount", "sum"),
            Orders=("Invoice", "nunique"),
            TotalQuantity=("Quantity", "sum"),
            Country=("Country", "first")
        )
        .round(2)
        .reset_index()
        .sort_values("TotalRevenue", ascending=False)
        .head(10)
    )

    output_path = os.path.join(
        PROCESSED_DATA_PATH,
        "top_customers.csv"
    )

    top_customers.to_csv(output_path, index=False)

    print(f"Saved : {output_path}")

    return top_customers

def generate_cohort_retention(df):
    """
    Generate monthly cohort retention table and export to CSV.
    """

    print("\nGenerating Cohort Retention...")

    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

    # First purchase date per customer
    df["CohortMonth"] = (
        df.groupby("Customer ID")["InvoiceDate"]
        .transform("min")
        .dt.to_period("M")
    )

    # Purchase month
    df["PurchaseMonth"] = df["InvoiceDate"].dt.to_period("M")

    # Month index
    df["MonthIndex"] = (
        (df["PurchaseMonth"] - df["CohortMonth"])
        .apply(lambda x: x.n)
    )

    cohort = (
        df.groupby(["CohortMonth", "MonthIndex"])
        ["Customer ID"]
        .nunique()
        .reset_index()
    )

    cohort = cohort.pivot(
        index="CohortMonth",
        columns="MonthIndex",
        values="Customer ID"
    )

    cohort = cohort.fillna(0).astype(int)

    cohort_size = cohort.iloc[:, 0]

    retention = cohort.divide(cohort_size, axis=0)

    retention = (retention * 100).round(1)

    output_path = os.path.join(
        PROCESSED_DATA_PATH,
        "cohort_retention.csv"
    )

    retention.to_csv(output_path)

    print(f"Saved : {output_path}")

    return retention

def generate_dashboard_summary(events_df):
    """
    Generate executive dashboard summary.
    """

    print("\nGenerating Dashboard Summary...")

    summary = pd.DataFrame([{
        "TotalRevenue": round(events_df["TotalAmount"].sum(), 2),
        "TotalCustomers": events_df["Customer ID"].nunique(),
        "TotalOrders": events_df["Invoice"].nunique(),
        "AverageOrderValue": round(events_df["TotalAmount"].sum()/ events_df["Invoice"].nunique(),2)
    }])

    output_path = os.path.join(
        PROCESSED_DATA_PATH,
        "dashboard_summary.csv"
    )

    summary.to_csv(output_path, index=False)

    print(f"Saved : {output_path}")

    return summary

if __name__ == "__main__":

    os.makedirs(PROCESSED_DATA_PATH, exist_ok=True)

    segments_df = load_customer_segments()

    events_df = load_customer_events()

    segment_overview = generate_segment_overview(segments_df)

    revenue = generate_revenue_by_segment(segments_df)

    monthly = generate_monthly_revenue(events_df)

    country = generate_revenue_by_country(events_df)

    top_customers = generate_top_customers(events_df)

    retention = generate_cohort_retention(events_df)

    dashboard_summary = generate_dashboard_summary(events_df)

    print("\nSegment Overview\n")
    print(segment_overview)

    print("\nRevenue By Segment\n")
    print(revenue)

    print("\nMonthly Revenue\n")
    print(monthly)

    print("\nRevenue By Country\n")
    print(country.head(10))

    print("\nTop Customers\n")
    print(top_customers)

    print("\nCohort Retention\n")
    print(retention.head())

    segments_df.to_csv(
        os.path.join(
            PROCESSED_DATA_PATH,
            "customer_segments.csv"
        ),
        index=False
    )

    print("Saved : customer_segments.csv")