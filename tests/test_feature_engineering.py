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