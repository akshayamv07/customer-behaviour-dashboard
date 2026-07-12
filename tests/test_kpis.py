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