"""
Feature Engineering Pipeline

Creates the final training dataset for temperature prediction.
"""

from pathlib import Path
import pandas as pd

INPUT_FILE = Path("data/processed/merged_dataset.csv")
OUTPUT_FILE = Path("data/processed/training_dataset.csv")


def main():

    print("=" * 70)
    print("FEATURE ENGINEERING")
    print("=" * 70)

    df = pd.read_csv(INPUT_FILE)

    print(f"\nLoaded {len(df)} rows")

    # -----------------------------------------------------
    # Timestamp
    # -----------------------------------------------------

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = (
        df.sort_values(
            ["node", "socket", "core", "timestamp"]
        )
        .reset_index(drop=True)
    )

    group_cols = ["node", "socket", "core"]

    # -----------------------------------------------------
    # Time Features
    # -----------------------------------------------------

    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month

    # -----------------------------------------------------
    # Historical Features
    # -----------------------------------------------------

    # Temperature
    df["temperature_lag_1"] = (
        df.groupby(group_cols)["temperature"].shift(1)
    )

    df["temperature_lag_2"] = (
        df.groupby(group_cols)["temperature"].shift(2)
    )

    df["temperature_lag_3"] = (
        df.groupby(group_cols)["temperature"].shift(3)
    )

    # Frequency
    df["frequency_lag_1"] = (
        df.groupby(group_cols)["frequency"].shift(1)
    )

    # CPU Usage
    df["cpu_usage_lag_1"] = (
        df.groupby(group_cols)["cpu_usage"].shift(1)
    )

    # Socket Power
    df["power_lag_1"] = (
        df.groupby(group_cols)["cpu_power"].shift(1)
    )

    # Socket Energy
    df["energy_lag_1"] = (
        df.groupby(group_cols)["cpu_energy"].shift(1)
    )

    # -----------------------------------------------------
    # Rolling Mean Features
    # -----------------------------------------------------

    df["temperature_roll3"] = (
        df.groupby(group_cols)["temperature"]
        .transform(lambda x: x.rolling(3, min_periods=1).mean())
    )

    df["frequency_roll3"] = (
        df.groupby(group_cols)["frequency"]
        .transform(lambda x: x.rolling(3, min_periods=1).mean())
    )

    df["cpu_usage_roll3"] = (
        df.groupby(group_cols)["cpu_usage"]
        .transform(lambda x: x.rolling(3, min_periods=1).mean())
    )

    df["power_roll3"] = (
        df.groupby(group_cols)["cpu_power"]
        .transform(lambda x: x.rolling(3, min_periods=1).mean())
    )

    df["energy_roll3"] = (
        df.groupby(group_cols)["cpu_energy"]
        .transform(lambda x: x.rolling(3, min_periods=1).mean())
    )

    # -----------------------------------------------------
    # Rate of Change
    # -----------------------------------------------------

    df["temperature_diff"] = (
        df.groupby(group_cols)["temperature"].diff()
    )

    df["frequency_diff"] = (
        df.groupby(group_cols)["frequency"].diff()
    )

    df["cpu_usage_diff"] = (
        df.groupby(group_cols)["cpu_usage"].diff()
    )

    df["power_diff"] = (
        df.groupby(group_cols)["cpu_power"].diff()
    )

    df["energy_diff"] = (
        df.groupby(group_cols)["cpu_energy"].diff()
    )

    # -----------------------------------------------------
    # Target Variable
    # -----------------------------------------------------

    df["target_temperature"] = (
        df.groupby(group_cols)["temperature"].shift(-1)
    )

    # -----------------------------------------------------
    # Remove rows with missing values
    # -----------------------------------------------------

    before = len(df)

    df = df.dropna().reset_index(drop=True)

    after = len(df)

    print(f"\nRemoved {before - after} rows")

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(f"\nTraining rows : {len(df)}")
    print(f"Saved to:\n{OUTPUT_FILE}")

    print("\nFeature Engineering Completed.")


if __name__ == "__main__":
    main()