import pandas as pd


def test_load_segments():
    from src.ai_insights import load_segments

    df = load_segments()

    assert df is not None
    assert not df.empty
    assert "Monetary" in df.columns
    assert "Frequency" in df.columns
    assert "Recency" in df.columns
    assert "Segment" in df.columns
    assert "ChurnRisk" in df.columns


def test_create_business_summary():
    from src.ai_insights import create_business_summary

    df = pd.DataFrame({
        "Monetary": [100.0, 200.0, 300.0],
        "Frequency": [2, 4, 6],
        "Recency": [10, 20, 30],
        "Segment": ["Champion", "Loyal", "Champion"],
        "ChurnRisk": ["Low", "Medium", "Low"]
    })

    summary = create_business_summary(df)

    assert summary["Total Customers"] == 3
    assert summary["Total Revenue"] == 600.0
    assert summary["Average Revenue"] == 200.0
    assert summary["Average Frequency"] == 4.0
    assert summary["Average Recency"] == 20.0
    assert summary["Segment Distribution"]["Champion"] == 2
    assert summary["Churn Distribution"]["Low"] == 2


def test_generate_ai_insights(monkeypatch):
    from src import ai_insights

    class MockResponse:
        text = "Executive Summary\n- Customer performance is strong."

    class MockModels:
        def generate_content(self, model, contents):
            assert model == "gemini-2.5-flash"
            assert "Customer Analytics Summary" in contents
            return MockResponse()

    class MockClient:
        models = MockModels()

    monkeypatch.setattr(ai_insights, "client", MockClient())

    summary = {"Total Customers": 3}

    result = ai_insights.generate_ai_insights(summary)

    assert result == "Executive Summary\n- Customer performance is strong."


def test_save_ai_report(tmp_path, monkeypatch):
    from src import ai_insights

    monkeypatch.chdir(tmp_path)

    output_dir = tmp_path / "data" / "processed"
    output_dir.mkdir(parents=True)

    output_file = output_dir / "ai_executive_report.md"

    ai_insights.save_ai_report("# Executive Report\n\nTest report.")

    assert output_file.exists()
    assert output_file.read_text(encoding="utf-8") == "# Executive Report\n\nTest report."