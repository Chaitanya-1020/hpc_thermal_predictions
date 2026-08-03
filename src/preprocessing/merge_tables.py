"""
Merge all telemetry tables into one merged_dataset table.
"""

from database.mysql_connection import get_connection


DROP_TABLE = """
DROP TABLE IF EXISTS merged_dataset;
"""


CREATE_TABLE = """
CREATE TABLE merged_dataset AS

SELECT

    t.timestamp,
    t.node,
    t.socket,
    t.core,

    t.temperature,
    f.frequency,
    c.cpu_usage,

    p.cpu_power,
    p.memory_power,

    e.cpu_energy,
    e.memory_energy

FROM temperature t

INNER JOIN frequency f
ON  t.timestamp = f.timestamp
AND t.node      = f.node
AND t.socket    = f.socket
AND t.core      = f.core

INNER JOIN cpu_usage c
ON  t.timestamp = c.timestamp
AND t.node      = c.node
AND t.socket    = c.socket
AND t.core      = c.core

INNER JOIN power p
ON  t.timestamp = p.timestamp
AND t.node      = p.node
AND t.socket    = p.socket

INNER JOIN energy e
ON  t.timestamp = e.timestamp
AND t.node      = e.node
AND t.socket    = e.socket

ORDER BY
    t.timestamp,
    t.node,
    t.socket,
    t.core;
"""


COUNT_QUERY = """
SELECT COUNT(*) FROM merged_dataset;
"""


def main():

    conn = get_connection()
    cursor = conn.cursor()

    print("=" * 70)
    print("MERGING DATASETS")
    print("=" * 70)

    cursor.execute(DROP_TABLE)

    cursor.execute(CREATE_TABLE)

    conn.commit()

    cursor.execute(COUNT_QUERY)

    result = cursor.fetchone()

# Works for both tuple and DictCursor
    if isinstance(result, dict):
        rows = result["COUNT(*)"]
    else:
        rows = result[0]

    print(f"\nMerged rows : {rows}")

    cursor.close()
    conn.close()

    print("\nMerged dataset created successfully.")


if __name__ == "__main__":
    main()