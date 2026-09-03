from pathlib import Path


def test_processed_folder_exists():
    assert Path("data/processed").exists()


def test_dashboard_summary_exists():
    assert Path("data/processed/dashboard_summary.csv").exists()


def test_customer_segments_exists():
    assert Path("data/processed/customer_segments.csv").exists()


def test_monthly_revenue_exists():
    assert Path("data/processed/monthly_revenue.csv").exists()


def test_database_load_functions():
    from src.database import load_customer_events, load_customer_segments

    events = load_customer_events()
    segments = load_customer_segments()

    assert events is not None
    assert segments is not None
    assert not events.empty
    assert not segments.empty


def test_pipeline_load_data():
    from src.pipeline import load_data

    retail_df, crm_df = load_data()

    assert not retail_df.empty
    assert not crm_df.empty


def test_pipeline_clean_data():
    from src.pipeline import clean_data
    import pandas as pd

    df = pd.DataFrame({
        "Invoice": ["10001", "10002", "10003"],
        "Description": ["Product A", "Product B", "Product C"],
        "InvoiceDate": ["2025-01-01", "2025-01-02", "2025-01-03"],
        "Quantity": [2, -1, 3],
        "Price": [10.0, 20.0, 5.0],
        "Customer ID": [123, 456, 789]
    })

    result = clean_data(df)

    assert not result.empty
    assert (result["Quantity"] > 0).all()


def test_pipeline_merge_data():
    from src.pipeline import merge_data
    import pandas as pd

    retail_df = pd.DataFrame({
        "Customer ID": [123, 456],
        "Invoice": ["10001", "10002"],
        "TotalAmount": [20.0, 40.0]
    })

    crm_df = pd.DataFrame({
        "Customer ID": [123, 456],
        "Country": ["United Kingdom", "France"]
    })

    result = merge_data(retail_df, crm_df)

    assert not result.empty
    assert "Country" in result.columns


def test_pipeline_save_to_duckdb():
    from src.pipeline import save_to_duckdb
    import duckdb
    import pandas as pd
    import shutil
    from pathlib import Path

    db_path = Path("data/customer_analytics.duckdb")
    backup_path = Path("data/customer_analytics_test_backup.duckdb")

    shutil.copy2(db_path, backup_path)

    try:
        df = pd.DataFrame({
            "Customer ID": [123],
            "Invoice": ["10001"],
            "Description": ["Product A"],
            "Quantity": [2],
            "Price": [10.0],
            "InvoiceDate": ["2025-01-01"],
            "Country": ["United Kingdom"],
            "TotalAmount": [20.0]
        })

        save_to_duckdb(df)

        conn = duckdb.connect(str(db_path))
        result = conn.execute("SELECT * FROM customer_events").fetchdf()
        conn.close()

        assert not result.empty

    finally:
        shutil.copy2(backup_path, db_path)
        backup_path.unlink()

def test_database_load_customer_features_and_segments():
    from src.database import load_customer_features, load_customer_segments

    features = load_customer_features()
    segments = load_customer_segments()

    assert features is not None
    assert not features.empty

    assert segments is not None
    assert not segments.empty