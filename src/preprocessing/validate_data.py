"""
Validate telemetry tables before merging.

Checks:
1. Missing timestamps
2. Missing nodes
3. Missing sockets
4. Missing cores
5. Duplicate rows
6. Invalid temperatures
7. Invalid frequencies
8. Invalid CPU usage
9. Null values
"""

from database.mysql_connection import get_connection


TABLES = [
    "temperature",
    "frequency",
    "cpu_usage",
    "power",
    "energy"
]


def print_header(title):
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)


def run_query(cursor, title, query):

    print(f"\n{title}")

    cursor.execute(query)

    rows = cursor.fetchall()

    if not rows:
        print("✓ No issues found")
        return

    for row in rows:
        print(row)


def validate_temperature(cursor):

    print_header("TEMPERATURE TABLE")

    run_query(
        cursor,
        "Null Values",
        """
        SELECT *
        FROM temperature
        WHERE timestamp IS NULL
           OR node IS NULL
           OR socket IS NULL
           OR core IS NULL
           OR temperature IS NULL;
        """
    )

    run_query(
        cursor,
        "Duplicate Rows",
        """
        SELECT timestamp,node,socket,core,COUNT(*)
        FROM temperature
        GROUP BY timestamp,node,socket,core
        HAVING COUNT(*)>1;
        """
    )

    run_query(
        cursor,
        "Invalid Temperatures",
        """
        SELECT *
        FROM temperature
        WHERE temperature < 0
           OR temperature > 120;
        """
    )


def validate_frequency(cursor):

    print_header("FREQUENCY TABLE")

    run_query(
        cursor,
        "Null Values",
        """
        SELECT *
        FROM frequency
        WHERE timestamp IS NULL
           OR node IS NULL
           OR socket IS NULL
           OR core IS NULL
           OR frequency IS NULL;
        """
    )

    run_query(
        cursor,
        "Duplicate Rows",
        """
        SELECT timestamp,node,socket,core,COUNT(*)
        FROM frequency
        GROUP BY timestamp,node,socket,core
        HAVING COUNT(*)>1;
        """
    )

    run_query(
        cursor,
        "Invalid Frequency",
        """
        SELECT *
        FROM frequency
        WHERE frequency < 0;
        """
    )


def validate_cpu_usage(cursor):

    print_header("CPU USAGE TABLE")

    run_query(
        cursor,
        "Null Values",
        """
        SELECT *
        FROM cpu_usage
        WHERE timestamp IS NULL
           OR node IS NULL
           OR socket IS NULL
           OR core IS NULL
           OR cpu_usage IS NULL;
        """
    )

    run_query(
        cursor,
        "Duplicate Rows",
        """
        SELECT timestamp,node,socket,core,COUNT(*)
        FROM cpu_usage
        GROUP BY timestamp,node,socket,core
        HAVING COUNT(*)>1;
        """
    )

    run_query(
        cursor,
        "Invalid CPU Usage",
        """
        SELECT *
        FROM cpu_usage
        WHERE cpu_usage < 0
           OR cpu_usage > 100;
        """
    )


def validate_power(cursor):

    print_header("POWER TABLE")

    run_query(
        cursor,
        "Null Values",
        """
        SELECT *
        FROM power
        WHERE timestamp IS NULL
           OR node IS NULL
           OR socket IS NULL
           OR cpu_power IS NULL
           OR memory_power IS NULL;
        """
    )

    run_query(
        cursor,
        "Duplicate Rows",
        """
        SELECT timestamp,node,socket,COUNT(*)
        FROM power
        GROUP BY timestamp,node,socket
        HAVING COUNT(*)>1;
        """
    )


def validate_energy(cursor):

    print_header("ENERGY TABLE")

    run_query(
        cursor,
        "Null Values",
        """
        SELECT *
        FROM energy
        WHERE timestamp IS NULL
           OR node IS NULL
           OR socket IS NULL
           OR cpu_energy IS NULL
           OR memory_energy IS NULL;
        """
    )

    run_query(
        cursor,
        "Duplicate Rows",
        """
        SELECT timestamp,node,socket,COUNT(*)
        FROM energy
        GROUP BY timestamp,node,socket
        HAVING COUNT(*)>1;
        """
    )


def main():

    connection = get_connection()

    cursor = connection.cursor()

    validate_temperature(cursor)
    validate_frequency(cursor)
    validate_cpu_usage(cursor)
    validate_power(cursor)
    validate_energy(cursor)

    cursor.close()
    connection.close()

    print("\n")
    print("=" * 70)
    print("VALIDATION COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()