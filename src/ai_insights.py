import os
import duckdb
import pandas as pd

from dotenv import load_dotenv
from google import genai

from config import (
    DATABASE_PATH,
    CUSTOMER_SEGMENTS_TABLE
)

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)
def load_segments():
    """
    Load customer segmentation results.
    """

    print("Loading customer segments...")

    conn = duckdb.connect(DATABASE_PATH)

    df = conn.execute(f"""
        SELECT *
        FROM {CUSTOMER_SEGMENTS_TABLE}
    """).fetchdf()

    conn.close()

    print(f"Rows Loaded : {len(df)}")

    return df

def create_business_summary(df):
    """
    Create business summary for Gemini.
    """

    summary = {}

    summary["Total Customers"] = len(df)

    summary["Total Revenue"] = round(df["Monetary"].sum(), 2)

    summary["Average Revenue"] = round(df["Monetary"].mean(), 2)

    summary["Average Frequency"] = round(df["Frequency"].mean(), 2)

    summary["Average Recency"] = round(df["Recency"].mean(), 2)

    summary["Segment Distribution"] = (
        df["Segment"]
        .value_counts()
        .to_dict()
    )

    summary["Churn Distribution"] = (
        df["ChurnRisk"]
        .value_counts()
        .to_dict()
    )

    return summary

def generate_ai_insights(summary):
    """
    Generate executive insights using Gemini.
    """

    print("\nGenerating AI Insights...")

    prompt = f"""
You are a Senior Business Analyst.

Based on the following customer analytics summary, provide:

1. Executive Summary
2. Customer Insights
3. Business Risks
4. Marketing Recommendations
5. Executive Action Plan

Customer Analytics Summary

{summary}

Keep the response professional.
Use bullet points.
Do not invent numbers.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text

def save_ai_report(report):
    """
    Save AI-generated business insights to a Markdown file.
    """

    output_path = "data/processed/ai_executive_report.md"

    with open(output_path, "w", encoding="utf-8") as file:
        file.write(report)

    print(f"\nAI report saved: {output_path}")

if __name__ == "__main__":

    df = load_segments()

    summary = create_business_summary(df)

    insights = generate_ai_insights(summary)

    print("\n")
    print("=" * 80)
    print("AI EXECUTIVE REPORT")
    print("=" * 80)
    print(insights)

    save_ai_report(insights)