"""
End-to-end temperature prediction pipeline.
"""

from datetime import timedelta

import numpy as np

from src.inference.load_model import load
from src.inference.mysql_reader import get_latest_history
from src.inference.feature_builder import build_features
from src.inference.mysql_writer import insert_predictions


def main():

    print("=" * 70)
    print("TEMPERATURE PREDICTION PIPELINE")
    print("=" * 70)

    # -----------------------------------------------------
    # Load model
    # -----------------------------------------------------

    model, feature_columns, metadata = load()

    print(f"\nLoaded Model : {metadata['best_model']}")

    # -----------------------------------------------------
    # Read telemetry
    # -----------------------------------------------------

    rows = get_latest_history()

    print(f"Telemetry Rows : {len(rows)}")

    # -----------------------------------------------------
    # Build Features
    # -----------------------------------------------------

    X = build_features(
        rows,
        feature_columns
    )

    print(f"Prediction Samples : {len(X)}")

    # -----------------------------------------------------
    # Predict
    # -----------------------------------------------------

    predictions = model.predict(X)

    # -----------------------------------------------------
    # Latest row of each stream
    # -----------------------------------------------------

    latest_rows = {}

    for row in rows:

        key = (
            row["node"],
            row["socket"],
            row["core"]
        )

        latest_rows[key] = row

    # -----------------------------------------------------
    # Build insert records
    # -----------------------------------------------------

    insert_rows = []

    keys = list(latest_rows.keys())

    for idx, key in enumerate(keys):

        row = latest_rows[key]

        timestamp = row["timestamp"]

        prediction_for = timestamp + timedelta(minutes=5)

        insert_rows.append(

            (
                timestamp,
                prediction_for,
                row["node"],
                row["socket"],
                row["core"],
                float(predictions[idx]),
                None,
                None,
                metadata["best_model"]
            )

        )

    # -----------------------------------------------------
    # Save
    # -----------------------------------------------------

    insert_predictions(insert_rows)

    print("\nPrediction Pipeline Completed.")

    print(f"\nPredictions Saved : {len(insert_rows)}")


if __name__ == "__main__":
    main()