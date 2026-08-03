"""
Build inference features from latest telemetry history.

This module recreates the SAME feature engineering
used during training.
"""

import pandas as pd


def build_features(rows, feature_columns):
    """
    Parameters
    ----------
    rows : list[dict]
        Output of mysql_reader.get_latest_history()

    feature_columns : list
        Loaded from models/feature_columns.pkl

    Returns
    -------
    pd.DataFrame
        Ready for model.predict()
    """

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("No telemetry data received.")

    # -------------------------------------------------------
    # Timestamp
    # -------------------------------------------------------

    df["timestamp"] = pd.to_datetime(df["timestamp"])

    df = (
        df.sort_values(
            ["node", "socket", "core", "timestamp"]
        )
        .reset_index(drop=True)
    )

    group_cols = ["node", "socket", "core"]

    # -------------------------------------------------------
    # Time Features
    # -------------------------------------------------------

    df["hour"] = df["timestamp"].dt.hour
    df["day"] = df["timestamp"].dt.day
    df["month"] = df["timestamp"].dt.month

    # -------------------------------------------------------
    # Lag Features
    # -------------------------------------------------------

    df["temperature_lag_1"] = (
        df.groupby(group_cols)["temperature"].shift(1)
    )

    df["temperature_lag_2"] = (
        df.groupby(group_cols)["temperature"].shift(2)
    )

    df["temperature_lag_3"] = (
        df.groupby(group_cols)["temperature"].shift(3)
    )

    df["frequency_lag_1"] = (
        df.groupby(group_cols)["frequency"].shift(1)
    )

    df["cpu_usage_lag_1"] = (
        df.groupby(group_cols)["cpu_usage"].shift(1)
    )

    df["power_lag_1"] = (
        df.groupby(group_cols)["cpu_power"].shift(1)
    )

    df["energy_lag_1"] = (
        df.groupby(group_cols)["cpu_energy"].shift(1)
    )

    # -------------------------------------------------------
    # Rolling Mean
    # -------------------------------------------------------

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

    # -------------------------------------------------------
    # Difference Features
    # -------------------------------------------------------

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

    # -------------------------------------------------------
    # Keep latest row for each stream
    # -------------------------------------------------------

    latest = (
        df.groupby(group_cols)
        .tail(1)
        .reset_index(drop=True)
    )

    # -------------------------------------------------------
    # Remove timestamp
    # -------------------------------------------------------

    latest = latest.drop(columns=["timestamp"])

    # -------------------------------------------------------
    # Encode node exactly like training
    # -------------------------------------------------------

    latest = pd.get_dummies(
        latest,
        columns=["node"],
        drop_first=True,
    )

    # -------------------------------------------------------
    # Add missing columns
    # -------------------------------------------------------

    for col in feature_columns:

        if col not in latest.columns:
            latest[col] = 0

    # -------------------------------------------------------
    # Remove unexpected columns
    # -------------------------------------------------------

    latest = latest[feature_columns]

    # -------------------------------------------------------
    # Numeric conversion
    # -------------------------------------------------------

    latest = latest.apply(
        pd.to_numeric,
        errors="coerce"
    )

    latest = latest.fillna(0)

    latest = latest.astype("float32")

    return latest


if __name__ == "__main__":

    from src.inference.mysql_reader import get_latest_history
    from src.inference.load_model import load

    model, feature_columns, metadata = load()

    rows = get_latest_history()

    features = build_features(
        rows,
        feature_columns
    )

    print("=" * 70)
    print("FEATURE BUILDER")
    print("=" * 70)

    print()

    print(features.head())

    print()

    print("Shape :", features.shape)

    print()

    print("Columns :", len(features.columns))