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

def test_calculate_recency():
    from src.segmentation import calculate_recency

    df = pd.DataFrame({
        "LastPurchaseDate": ["2025-01-01", "2025-01-10"]
    })

    result = calculate_recency(df)

    assert "Recency" in result.columns
    assert result["Recency"].tolist() == [10, 1]


def test_prepare_rfm():
    from src.segmentation import prepare_rfm

    df = pd.DataFrame({
        "TotalOrders": [5, 10],
        "TotalRevenue": [100.0, 250.0]
    })

    result = prepare_rfm(df)

    assert result["Frequency"].tolist() == [5, 10]
    assert result["Monetary"].tolist() == [100.0, 250.0]


def test_rfm_scores():
    from src.segmentation import (
        calculate_r_score,
        calculate_f_score,
        calculate_m_score,
        create_rfm_score
    )

    df = pd.DataFrame({
        "Recency": [5, 10, 20, 30, 40],
        "Frequency": [50, 40, 30, 20, 10],
        "Monetary": [500, 400, 300, 200, 100]
    })

    df = calculate_r_score(df)
    df = calculate_f_score(df)
    df = calculate_m_score(df)
    df = create_rfm_score(df)

    assert df["R_Score"].between(1, 5).all()
    assert df["F_Score"].between(1, 5).all()
    assert df["M_Score"].between(1, 5).all()
    assert df["RFM_Score"].notna().all()


def test_assign_segment_labels():
    from src.segmentation import assign_segment_labels

    df = pd.DataFrame({
        "Cluster": [0, 1, 2, 3, 4]
    })

    result = assign_segment_labels(df)

    assert result["Segment"].tolist() == [
        "Lost",
        "Regular",
        "Champion",
        "VIP Wholesale",
        "Loyal"
    ]


def test_calculate_churn_risk():
    from src.segmentation import calculate_churn_risk

    df = pd.DataFrame({
        "Recency": [10, 60, 120, 200]
    })

    result = calculate_churn_risk(df)

    assert result["ChurnRisk"].tolist() == [
        "Low",
        "Medium",
        "High",
        "Very High"
    ]

def test_prepare_ml_features():
    from src.segmentation import prepare_ml_features

    df = pd.DataFrame({
        "Recency": [10, 20, 30, 40, 50],
        "Frequency": [5, 10, 15, 20, 25],
        "Monetary": [100, 200, 300, 400, 500],
        "AverageOrderValue": [20, 20, 20, 20, 20],
        "TotalQuantity": [10, 20, 30, 40, 50]
    })

    result = prepare_ml_features(df)

    assert result.shape == (5, 5)
    assert result.shape[1] == 5

def test_run_kmeans():
    from src.segmentation import run_kmeans, prepare_ml_features

    df = pd.DataFrame({
        "Recency": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        "Frequency": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50],
        "Monetary": [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000],
        "AverageOrderValue": [20, 20, 20, 20, 20, 20, 20, 20, 20, 20],
        "TotalQuantity": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
    })

    scaled_features = prepare_ml_features(df)

    result, score = run_kmeans(df, scaled_features)

    assert "Cluster" in result.columns
    assert len(result) == 10
    assert result["Cluster"].nunique() == 5
    assert -1 <= score <= 1

def test_analyze_clusters():
    from src.segmentation import analyze_clusters

    df = pd.DataFrame({
        "Cluster": [0, 0, 1, 1],
        "Recency": [10, 20, 30, 40],
        "Frequency": [5, 10, 15, 20],
        "Monetary": [100, 200, 300, 400],
        "AverageOrderValue": [20, 20, 20, 20],
        "TotalQuantity": [10, 20, 30, 40]
    })

    result = analyze_clusters(df)

    assert len(result) == 2
    assert list(result.index) == [0, 1]
    assert "Recency" in result.columns
    assert "Frequency" in result.columns
    assert "Monetary" in result.columns

def test_calculate_churn_risk_boundaries():
    from src.segmentation import calculate_churn_risk

    df = pd.DataFrame({
        "Recency": [0, 30, 31, 90, 91, 180, 181]
    })

    result = calculate_churn_risk(df)

    assert result["ChurnRisk"].tolist() == [
        "Low",
        "Low",
        "Medium",
        "Medium",
        "High",
        "High",
        "Very High"
    ]