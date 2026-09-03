def test_explore_dataset():
    from src.explore_data import explore_dataset

    df = explore_dataset()

    assert df is not None
    assert not df.empty
    assert len(df.columns) == 8
    assert "Invoice" in df.columns
    assert "Customer ID" in df.columns
    assert "Quantity" in df.columns
    assert "Price" in df.columns