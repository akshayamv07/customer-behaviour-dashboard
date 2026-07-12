from pathlib import Path
import pandas as pd


def test_customer_segments_exists():
    assert Path("data/processed/customer_segments.csv").exists()


def test_segment_column_exists():
    df = pd.read_csv("data/processed/customer_segments.csv")
    assert "Segment" in df.columns


def test_customerid_exists():
    df = pd.read_csv("data/processed/customer_segments.csv")
    assert "CustomerID" in df.columns


def test_segmentation_not_empty():
    df = pd.read_csv("data/processed/customer_segments.csv")
    assert len(df) > 0


def test_segment_values():
    df = pd.read_csv("data/processed/customer_segments.csv")
    assert df["Segment"].nunique() > 0