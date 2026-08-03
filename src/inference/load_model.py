"""
Load trained model and metadata.
"""

import json
import joblib
from pathlib import Path

MODELS = Path("models")


def load():

    model = joblib.load(
        MODELS / "best_model.pkl"
    )

    features = joblib.load(
        MODELS / "feature_columns.pkl"
    )

    with open(
        MODELS / "metadata.json"
    ) as f:

        metadata = json.load(f)

    return model, features, metadata


if __name__ == "__main__":

    model, features, metadata = load()

    print(metadata)