# Customer Behaviour Analytics Dashboard

A complete end-to-end Customer Behaviour Analytics solution built using Python, DuckDB, Power BI, and Machine Learning. The project analyzes customer purchasing behavior, segments customers using RFM analysis and K-Means clustering, generates KPIs, and provides interactive business dashboards for decision making.

---

## Project Overview

This project demonstrates a complete analytics pipeline from raw retail transaction data to interactive Power BI dashboards.

The project includes:

- Data Cleaning & ETL Pipeline
- DuckDB Data Warehouse
- Feature Engineering
- RFM Analysis
- K-Means Customer Segmentation
- Purchase Funnel Analysis
- KPI Generation
- Power BI Dashboards
- AI Business Insights

---

## Tech Stack

- Python 3.12
- Pandas
- NumPy
- Scikit-Learn
- DuckDB
- Power BI Desktop
- Git
- GitHub

---

## Project Structure

```
CustomerBehaviourAnalytics
│
├── app/
├── data/
│   ├── raw/
│   ├── processed/
│   └── customer_analytics.duckdb
│
├── docs/
├── notebooks/
│
├── src/
│   ├── pipeline.py
│   ├── feature_engineering.py
│   ├── segmentation.py
│   ├── purchase_funnel.py
│   ├── kpis.py
│   ├── ai_insights.py
│   └── config.py
│
├── requirements.txt
├── README.md
└── CustomerBehaviourAnalytics.pbix
```

---

## Project Workflow

```
Raw Dataset
      │
      ▼
Data Cleaning
      │
      ▼
DuckDB Storage
      │
      ▼
Feature Engineering
      │
      ▼
RFM Analysis
      │
      ▼
K-Means Segmentation
      │
      ▼
Purchase Funnel
      │
      ▼
KPI Generation
      │
      ▼
Power BI Dashboards
```

---

## Dashboards

### Executive Dashboard

Displays:

- Total Revenue
- Total Customers
- Total Orders
- Average Order Value
- Revenue by Segment
- Revenue Trend
- Revenue by Country
- Purchase Funnel

---

### Customer Segmentation Dashboard

Displays:

- Customer Count
- Average Customer Lifetime Value
- Average Spend
- Average Purchase Frequency
- Customer Segments
- Churn Risk Distribution
- Cluster Distribution
- Customer Value Distribution

---

### Customer Retention Dashboard

Displays:

- Customer Count
- Average Recency
- Average Purchase Frequency
- Churn Risk Analysis
- Customer Retention Distribution
- Customer Value Analysis
- Segment Analysis

---

## Machine Learning

Implemented:

- RFM Analysis
- K-Means Clustering
- Customer Segmentation
- Churn Risk Categorization

---

## Key Features

- ETL Pipeline
- Automated KPI Generation
- Customer Segmentation
- Purchase Funnel Analysis
- Revenue Analysis
- Customer Lifetime Value
- Interactive Power BI Dashboards
- AI Generated Business Insights

---

## Installation

Clone the repository

```bash
git clone https://github.com/akshayamv07/customer-behaviour-dashboard.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run ETL

```bash
python src/pipeline.py
```

Generate Features

```bash
python src/feature_engineering.py
```

Run Segmentation

```bash
python src/segmentation.py
```

Generate KPIs

```bash
python src/kpis.py
```

Generate AI Insights

```bash
python src/ai_insights.py
```

---

## Future Enhancements

- Azure SQL Integration
- Azure Data Factory Pipeline
- Power BI Service Deployment
- Automated Dashboard Refresh
- Real-time Streaming Data
- Customer Recommendation Engine
- Predictive Churn Model

---

## Author

**Akshaya Velumani**

Full Stack Developer (.NET | React | Python | Power BI)

GitHub:
https://github.com/akshayamv07

## AI Prompt Engineering

The project uses Google Gemini 2.5 Flash to generate executive-level customer behaviour insights from the calculated analytics summary.

The prompt follows a structured approach:

- **Role definition:** The model is assigned the role of a Senior Business Analyst.
- **Structured output:** The response is requested in five sections:
  1. Executive Summary
  2. Customer Insights
  3. Business Risks
  4. Marketing Recommendations
  5. Executive Action Plan
- **Data grounding:** The model receives the calculated Customer Analytics Summary as its input.
- **Accuracy constraint:** The prompt explicitly instructs the model not to invent numbers.
- **Presentation constraint:** The response is requested in professional language using bullet points.

This approach is intended to keep the generated narrative focused on the calculated customer analytics while producing actionable business insights.
