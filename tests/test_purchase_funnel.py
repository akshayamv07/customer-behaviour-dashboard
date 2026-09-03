import pandas as pd


def test_load_segments():
    from src.purchase_funnel import load_segments

    df = load_segments()

    assert df is not None
    assert not df.empty
    assert "TotalOrders" in df.columns
    assert "Segment" in df.columns


def test_generate_purchase_funnel():
    from src.purchase_funnel import generate_purchase_funnel

    df = pd.DataFrame({
        "TotalOrders": [1, 2, 6, 10],
        "Segment": ["Lost", "Regular", "Loyal", "Champion"]
    })

    result = generate_purchase_funnel(df)

    assert result is None