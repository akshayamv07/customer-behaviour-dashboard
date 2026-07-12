from pathlib import Path

def test_processed_folder_exists():
    assert Path("data/processed").exists()

def test_dashboard_summary_exists():
    assert Path("data/processed/dashboard_summary.csv").exists()

def test_customer_segments_exists():
    assert Path("data/processed/customer_segments.csv").exists()

def test_monthly_revenue_exists():
    assert Path("data/processed/monthly_revenue.csv").exists()