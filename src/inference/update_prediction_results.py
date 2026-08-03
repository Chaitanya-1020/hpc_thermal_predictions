"""
Update actual temperatures and prediction errors
after new telemetry arrives.
"""

from database.mysql_connection import (
    get_connection,
    close_connection,
)


SELECT_QUERY = """
SELECT
    id,
    prediction_for,
    node,
    socket,
    core,
    predicted_temperature
FROM temperature_predictions
WHERE actual_temperature IS NULL
"""


UPDATE_QUERY = """
UPDATE temperature_predictions tp
JOIN temperature t
ON tp.prediction_for = t.timestamp
AND tp.node = t.node
AND tp.socket = t.socket
AND tp.core = t.core

SET

tp.actual_temperature = t.temperature,

tp.prediction_error =
ROUND(
    t.temperature - tp.predicted_temperature,
    4
)

WHERE tp.actual_temperature IS NULL
"""


def main():

    print("=" * 70)
    print("UPDATING PREDICTION RESULTS")
    print("=" * 70)

    conn = get_connection()

    cursor = conn.cursor()

    # Pending predictions
    cursor.execute(SELECT_QUERY)

    pending = cursor.fetchall()

    print(f"\nPending Predictions : {len(pending)}")

    if len(pending) == 0:

        print("\nNothing to update.")

        close_connection(conn)

        return

    # Update actual values
    cursor.execute(UPDATE_QUERY)

    conn.commit()

    print(f"\nUpdated Rows : {cursor.rowcount}")

    close_connection(conn)

    print("\nPrediction results updated successfully.")


if __name__ == "__main__":
    main()