from pathlib import Path
import pandas as pd


def test_customer_segments_file_exists():
    assert Path("data/processed/customer_segments.csv").exists()


def test_customer_segments_not_empty():
    df = pd.read_csv("data/processed/customer_segments.csv")
    assert len(df) > 0


def test_required_columns_exist():
    df = pd.read_csv("data/processed/customer_segments.csv")

    required_columns = [
        "CustomerID",
        "Recency",
        "Frequency",
        "Monetary",
        "Segment"
    ]

    for column in required_columns:
        assert column in df.columns


def test_no_missing_customer_ids():
    df = pd.read_csv("data/processed/customer_segments.csv")
    assert df["CustomerID"].notna().all()


def test_recency_is_non_negative():
    df = pd.read_csv("data/processed/customer_segments.csv")
    assert (df["Recency"] >= 0).all()


def test_frequency_is_positive():
    df = pd.read_csv("data/processed/customer_segments.csv")
    assert (df["Frequency"] > 0).all()


def test_monetary_is_positive():
    df = pd.read_csv("data/processed/customer_segments.csv")
    assert (df["Monetary"] > 0).all()

def test_load_customer_events():
    from src.feature_engineering import load_customer_events

    df = load_customer_events()

    assert df is not None
    assert not df.empty
    assert "Customer ID" in df.columns
    assert "TotalAmount" in df.columns


def test_create_customer_features():
    from src.feature_engineering import create_customer_features
    from src.database import load_customer_events
    import duckdb

    # Ensure the real customer_events table is available
    events = load_customer_events()

    assert events is not None
    assert not events.empty

    result = create_customer_features()

    assert result is None

    conn = duckdb.connect("data/customer_analytics.duckdb")
    features = conn.execute("SELECT * FROM customer_features").fetchdf()
    conn.close()

    assert not features.empty


def test_preview_customer_features():
    from src.feature_engineering import preview_customer_features

    result = preview_customer_features()

    assert result is None