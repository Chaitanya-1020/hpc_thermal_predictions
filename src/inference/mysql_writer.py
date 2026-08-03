"""
Write predictions into MySQL.
"""

from database.mysql_connection import (
    get_connection,
    close_connection,
)


INSERT_QUERY = """
INSERT INTO temperature_predictions
(
    timestamp,
    prediction_for,
    node,
    socket,
    core,
    predicted_temperature,
    actual_temperature,
    prediction_error,
    model_version
)
VALUES
(
    %s,%s,%s,%s,%s,%s,%s,%s,%s
)
"""


def insert_predictions(records):

    if not records:

        print("No predictions to insert.")

        return

    conn = get_connection()

    cursor = conn.cursor()

    cursor.executemany(
        INSERT_QUERY,
        records
    )

    conn.commit()

    print(
        f"\nInserted {cursor.rowcount} predictions."
    )

    close_connection(conn)


if __name__ == "__main__":

    from datetime import datetime, timedelta

    now = datetime.now()

    rows = [

        (
            now,
            now + timedelta(minutes=5),
            "cn21",
            0,
            0,
            27.15,
            None,
            None,
            "XGBoost"
        )

    ]

    insert_predictions(rows)