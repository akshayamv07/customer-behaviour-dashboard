from pathlib import Path


def test_ai_report_exists():
    assert Path("data/processed/ai_executive_report.md").exists()