"""
Read latest telemetry from merged_dataset for inference.
"""

from database.mysql_connection import get_connection, close_connection


def get_latest_history(history_size=10):
    """
    Returns the latest N telemetry records for every
    (node, socket, core).

    Parameters
    ----------
    history_size : int
        Number of historical records required
        for feature generation.

    Returns
    -------
    list[dict]
        Telemetry rows ordered by:
        node -> socket -> core -> timestamp
    """

    conn = get_connection()

    cursor = conn.cursor()

    query = f"""
    SELECT
        timestamp,
        node,
        socket,
        core,
        temperature,
        frequency,
        cpu_usage,
        cpu_power,
        memory_power,
        cpu_energy,
        memory_energy
    FROM
    (
        SELECT
            *,
            ROW_NUMBER() OVER (
                PARTITION BY node, socket, core
                ORDER BY timestamp DESC
            ) AS rn
        FROM merged_dataset
    ) t
    WHERE rn <= {history_size}
    ORDER BY
        node,
        socket,
        core,
        timestamp;
    """

    cursor.execute(query)

    rows = cursor.fetchall()

    close_connection(conn)

    return rows


def main():

    print("=" * 70)
    print("READING TELEMETRY FROM MYSQL")
    print("=" * 70)

    rows = get_latest_history()

    print(f"\nRows fetched : {len(rows)}")

    print("\nFirst five rows:\n")

    for row in rows[:5]:
        print(row)


if __name__ == "__main__":
    main()