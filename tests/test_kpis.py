from pathlib import Path
import pandas as pd


def test_dashboard_summary_exists():
    assert Path("data/processed/dashboard_summary.csv").exists()


def test_monthly_revenue_exists():
    assert Path("data/processed/monthly_revenue.csv").exists()


def test_revenue_by_country_exists():
    assert Path("data/processed/revenue_by_country.csv").exists()


def test_segment_overview_exists():
    assert Path("data/processed/segment_overview.csv").exists()


def test_dashboard_summary_not_empty():
    df = pd.read_csv("data/processed/dashboard_summary.csv")
    assert len(df) > 0


def test_monthly_revenue_not_empty():
    df = pd.read_csv("data/processed/monthly_revenue.csv")
    assert len(df) > 0

def test_generate_dashboard_summary():
    from src.kpis import generate_dashboard_summary

    df = pd.DataFrame({
        "Customer ID": [1, 1, 2],
        "Invoice": ["A", "B", "C"],
        "TotalAmount": [100.0, 50.0, 200.0]
    })

    result = generate_dashboard_summary(df)

    assert result["TotalRevenue"].iloc[0] == 350.0
    assert result["TotalCustomers"].iloc[0] == 2
    assert result["TotalOrders"].iloc[0] == 3
    assert result["AverageOrderValue"].iloc[0] == round(350.0 / 3, 2)

def test_generate_segment_overview():
    from src.kpis import generate_segment_overview

    df = pd.DataFrame({
        "CustomerID": [1, 2, 3],
        "Segment": ["Champions", "At Risk", "Champions"],
        "Monetary": [100.0, 50.0, 200.0],
        "Frequency": [5, 2, 8],
        "Recency": [10, 30, 5],
        "AverageOrderValue": [20.0, 25.0, 25.0]
    })

    result = generate_segment_overview(df)

    assert len(result) == 2
    assert set(result["Segment"]) == {"Champions", "At Risk"}
    assert "Customers" in result.columns
    assert "AverageRevenue" in result.columns


def test_generate_revenue_by_segment():
    from src.kpis import generate_revenue_by_segment

    df = pd.DataFrame({
        "Segment": ["Champions", "At Risk", "Champions"],
        "Monetary": [100.0, 50.0, 200.0]
    })

    result = generate_revenue_by_segment(df)

    assert len(result) == 2
    assert result.iloc[0]["Segment"] == "Champions"
    assert result.iloc[0]["TotalRevenue"] == 300.0

def test_generate_revenue_by_country():
    from src.kpis import generate_revenue_by_country

    df = pd.DataFrame({
        "Country": ["UK", "UK", "France"],
        "TotalAmount": [100.0, 200.0, 50.0],
        "Invoice": ["A", "B", "C"],
        "Customer ID": [1, 2, 3]
    })

    result = generate_revenue_by_country(df)

    assert len(result) == 2
    assert result.iloc[0]["Country"] == "UK"
    assert result.iloc[0]["TotalRevenue"] == 300.0
    assert result.iloc[0]["Orders"] == 2
    assert result.iloc[0]["Customers"] == 2


def test_generate_top_customers():
    from src.kpis import generate_top_customers

    df = pd.DataFrame({
        "Customer ID": [1, 1, 2, 3],
        "TotalAmount": [100.0, 50.0, 200.0, 25.0],
        "Invoice": ["A", "B", "C", "D"],
        "Quantity": [2, 3, 4, 1],
        "Country": ["UK", "UK", "France", "Germany"]
    })

    result = generate_top_customers(df)

    assert len(result) == 3
    assert result.iloc[0]["Customer ID"] == 2
    assert result.iloc[0]["TotalRevenue"] == 200.0
    assert result.iloc[0]["TotalQuantity"] == 4

def test_generate_monthly_revenue():
    from src.kpis import generate_monthly_revenue

    df = pd.DataFrame({
        "InvoiceDate": [
            "2025-01-10",
            "2025-01-15",
            "2025-02-05"
        ],
        "TotalAmount": [100.0, 50.0, 200.0],
        "Invoice": ["A", "B", "C"],
        "Customer ID": [1, 2, 1]
    })

    result = generate_monthly_revenue(df)

    assert len(result) == 2
    assert result.iloc[0]["YearMonth"] == "2025-01"
    assert result.iloc[0]["TotalRevenue"] == 150.0
    assert result.iloc[0]["Orders"] == 2
    assert result.iloc[0]["Customers"] == 2


def test_generate_cohort_retention():
    from src.kpis import generate_cohort_retention

    df = pd.DataFrame({
        "Customer ID": [1, 1, 2, 2, 3],
        "InvoiceDate": [
            "2025-01-10",
            "2025-02-10",
            "2025-01-15",
            "2025-03-15",
            "2025-02-20"
        ]
    })

    result = generate_cohort_retention(df)

    assert not result.empty
    assert result.iloc[0, 0] == 100.0
    assert (result.values >= 0).all()
    assert (result.values <= 100).all()