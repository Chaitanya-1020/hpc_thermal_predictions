"""
Generic database writer for HPC telemetry ingestion.

This module provides reusable functions for inserting
records into MySQL using batch inserts.
"""

from database.mysql_connection import get_connection, close_connection


def batch_insert(query: str, records: list):
    """
    Execute a batch insert.

    Parameters
    ----------
    query : str
        INSERT SQL query.

    records : list
        List of tuples to insert.
    """

    if not records:
        print("⚠ No records to insert.")
        return

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.executemany(query, records)

        connection.commit()

        print(f"✅ Successfully inserted {cursor.rowcount} records.")

    except Exception as e:

        if connection:
            connection.rollback()

        print(f"❌ Database Insert Error: {e}")

        raise

    finally:

        if cursor:
            cursor.close()

        if connection:
            close_connection(connection)