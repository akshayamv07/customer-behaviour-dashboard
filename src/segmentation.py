import duckdb
import pandas as pd

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

from config import (
    DATABASE_PATH,
    CUSTOMER_FEATURES_TABLE,
    CUSTOMER_SEGMENTS_TABLE
)


def load_customer_features():
    """
    Load customer features from DuckDB.
    """

    print("Connecting to DuckDB...")

    conn = duckdb.connect(DATABASE_PATH)

    query = f"""
        SELECT *
        FROM {CUSTOMER_FEATURES_TABLE}
    """

    df = conn.execute(query).fetchdf()

    conn.close()

    print("Customer features loaded successfully!")
    print(f"Rows    : {len(df)}")
    print(f"Columns : {len(df.columns)}")

    return df


def calculate_recency(df):
    """
    Calculate Recency (days since last purchase).
    """

    print("\nCalculating Recency...")

    # Ensure datetime format
    df["LastPurchaseDate"] = pd.to_datetime(df["LastPurchaseDate"])

    # Reference date = one day after the latest purchase
    reference_date = df["LastPurchaseDate"].max() + pd.Timedelta(days=1)

    # Calculate Recency
    df["Recency"] = (
        reference_date - df["LastPurchaseDate"]
    ).dt.days

    print("Recency calculated successfully!")

    return df

def prepare_rfm(df):
    """
    Prepare RFM features for segmentation.
    """

    print("\nPreparing RFM Features...")

    df["Frequency"] = df["TotalOrders"]

    df["Monetary"] = df["TotalRevenue"]

    print("RFM Features Prepared Successfully!")

    return df

def calculate_r_score(df):
    """
    Calculate R Score (1-5).
    Lower Recency = Higher Score.
    """

    print("\nCalculating R Score...")

    df["R_Score"] = pd.qcut(
        df["Recency"].rank(method="first"),
        q=5,
        labels=[5, 4, 3, 2, 1]
    ).astype(int)

    print("R Score calculated successfully!")

    return df

def calculate_f_score(df):
    """
    Calculate F Score (1-5).
    Higher Frequency = Higher Score.
    """

    print("\nCalculating F Score...")

    df["F_Score"] = pd.qcut(
        df["Frequency"].rank(method="first"),
        q=5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)

    print("F Score calculated successfully!")

    return df

def calculate_m_score(df):
    """
    Calculate M Score (1-5).
    Higher Monetary = Higher Score.
    """

    print("\nCalculating M Score...")

    df["M_Score"] = pd.qcut(
        df["Monetary"].rank(method="first"),
        q=5,
        labels=[1, 2, 3, 4, 5]
    ).astype(int)

    print("M Score calculated successfully!")

    return df

def create_rfm_score(df):
    """
    Combine R, F and M scores into a single RFM Score.
    """

    print("\nCreating RFM Score...")

    df["RFM_Score"] = (
        df["R_Score"].astype(str)
        + df["F_Score"].astype(str)
        + df["M_Score"].astype(str)
    )

    print("RFM Score created successfully!")

    return df

def prepare_ml_features(df):
    """
    Prepare features for K-Means clustering.
    """

    print("\nPreparing Machine Learning Features...")

    features = df[
        [
            "Recency",
            "Frequency",
            "Monetary",
            "AverageOrderValue",
            "TotalQuantity"
        ]
    ]

    scaler = StandardScaler()

    scaled_features = scaler.fit_transform(features)

    print("Machine Learning Features Ready!")

    return scaled_features

def run_kmeans(df, scaled_features):
    """
    Train K-Means clustering model.
    """

    print("\nTraining K-Means Model...")

    model = KMeans(
        n_clusters=5,
        random_state=42,
        n_init=10
    )

    df["Cluster"] = model.fit_predict(scaled_features)

    score = silhouette_score(
        scaled_features,
        df["Cluster"]
    )

    print("K-Means Model Trained Successfully!")

    print(f"Silhouette Score : {score:.4f}")

    return df, score

def analyze_clusters(df):
    """
    Display average values for each cluster.
    """

    print("\nCluster Summary\n")

    summary = (
        df.groupby("Cluster")[
            [
                "Recency",
                "Frequency",
                "Monetary",
                "AverageOrderValue",
                "TotalQuantity"
            ]
        ]
        .mean()
        .round(2)
    )

    print(summary)

    return summary

def assign_segment_labels(df):
    """
    Assign business-friendly labels to clusters.
    """

    print("\nAssigning Business Segment Labels...")

    segment_map = {
        0: "Lost",
        1: "Regular",
        2: "Champion",
        3: "VIP Wholesale",
        4: "Loyal"
    }

    df["Segment"] = df["Cluster"].map(segment_map)

    print("Segment labels assigned successfully!")

    return df

def save_segments(df):
    """
    Save customer segmentation results to DuckDB.
    """

    print("\nSaving customer segments...")

    conn = duckdb.connect(DATABASE_PATH)

    conn.execute(f"""
        CREATE OR REPLACE TABLE {CUSTOMER_SEGMENTS_TABLE} AS
        SELECT * FROM df
    """)

    conn.close()

    print("Customer segments saved successfully!")

if __name__ == "__main__":

    df = load_customer_features()

    df = calculate_recency(df)

    df = prepare_rfm(df)

    df = calculate_r_score(df)

    df = calculate_f_score(df)

    df = calculate_m_score(df)

    df = create_rfm_score(df)

    scaled_features = prepare_ml_features(df)

    print("\nScaled Feature Shape:")
    print(scaled_features.shape)

    df, score = run_kmeans(
        df,
        scaled_features
    )

    summary = analyze_clusters(df)

    df = assign_segment_labels(df)

    save_segments(df)

    print("\nSegment Preview\n")

    print(
        df[
            [
                "CustomerID",
                "Cluster",
                "Segment",
                "RFM_Score"
            ]
        ].head(20)
    
    )
    print("\nCluster Distribution\n")

    print(
        df["Cluster"]
        .value_counts()
        .sort_index()
    )