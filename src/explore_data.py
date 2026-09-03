import pandas as pd


# Path to the dataset
file_path = "data/raw/online_retail_II.csv"


def explore_dataset(file_path=file_path):
    """
    Load the dataset and display basic exploratory information.
    """

    df = pd.read_csv(file_path)

    print("=" * 60)
    print("DATASET SHAPE")
    print("=" * 60)
    print(df.shape)

    print("\n" + "=" * 60)
    print("COLUMN NAMES")
    print("=" * 60)
    print(df.columns.tolist())

    print("\n" + "=" * 60)
    print("DATA TYPES")
    print("=" * 60)
    print(df.dtypes)

    print("\n" + "=" * 60)
    print("MISSING VALUES")
    print("=" * 60)
    print(df.isnull().sum())

    print("\n" + "=" * 60)
    print("FIRST 5 ROWS")
    print("=" * 60)
    print(df.head())

    return df


if __name__ == "__main__":
    explore_dataset()