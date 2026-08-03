"""
Insert temperature telemetry into MySQL.

This script:

1. Scans all temperature.json files
2. Reads JSON records
3. Extracts every socket and every core
4. Inserts data into MySQL
"""

from pathlib import Path

from src.ingestion.file_scanner import find_json_files
from src.ingestion.json_parser import iter_json_records
from src.ingestion.db_writer import batch_insert
from src.ingestion.config import RAW_DATA_DIR


INSERT_QUERY = """
INSERT IGNORE INTO temperature
(
    timestamp,
    node,
    socket,
    core,
    temperature
)
VALUES (%s,%s,%s,%s,%s)
"""


def extract_temperature_records(record):
    rows = []

    timestamp = record["timestamp"]

    node = next(iter(record["data"]))

    node_data = record["data"][node]

    for socket_name, socket_data in node_data.items():

        # Skip metadata keys like "timestamp"
        if not socket_name.startswith("socket_"):
            continue

        socket_id = int(socket_name.replace("socket_", ""))

        cpu = socket_data.get("CPU", {})

        core_data = cpu.get("Core", {})

        for key, value in core_data.items():

            if not key.startswith("temp_celsius_core_"):
                continue

            core_id = int(key.replace("temp_celsius_core_", ""))

            rows.append(
                (
                    timestamp,
                    node,
                    socket_id,
                    core_id,
                    float(value),
                )
            )

    return rows


def main():

    all_rows = []

    json_files = find_json_files(
        RAW_DATA_DIR,
        "temp.json"
    )

    print(f"\nFound {len(json_files)} temperature files.\n")

    for file in json_files:

        print(f"Reading: {file}")

        for record in iter_json_records(file):

            all_rows.extend(
                extract_temperature_records(record)
            )

    print(f"\nTotal rows extracted: {len(all_rows)}")

    batch_insert(
        INSERT_QUERY,
        all_rows
    )


if __name__ == "__main__":
    main()