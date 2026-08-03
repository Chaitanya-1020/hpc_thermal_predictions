"""
Dataset Validation before Model Training
"""

from pathlib import Path
import numpy as np
import pandas as pd

DATASET = Path("data/processed/training_dataset.csv")


def main():

    print("=" * 70)
    print("DATASET VALIDATION")
    print("=" * 70)

    df = pd.read_csv(DATASET)

    print(f"\nShape : {df.shape}")

    print("\nData Types")
    print(df.dtypes)

    print("\nMissing Values")
    print(df.isnull().sum())

    print("\nInfinite Values")

    numeric = df.select_dtypes(include=[np.number])

    print(np.isinf(numeric).sum())

    print("\nDuplicate Rows")

    print(df.duplicated().sum())

    print("\nObject Columns")

    print(df.select_dtypes(include="object").columns.tolist())

    print("\nNumeric Summary")

    print(numeric.describe())

    print("\nValidation Completed")


if __name__ == "__main__":
    main()