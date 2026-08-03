"""
Insert CPU usage telemetry into MySQL.
"""

from src.ingestion.file_scanner import find_json_files
from src.ingestion.json_parser import iter_cpu_usage_records
from src.ingestion.db_writer import batch_insert
from src.ingestion.config import RAW_DATA_DIR


INSERT_QUERY = """
INSERT IGNORE INTO cpu_usage
(
    timestamp,
    node,
    socket,
    core,
    cpu_usage
)
VALUES (%s,%s,%s,%s,%s)
"""


def extract_cpu_usage_records(record):

    rows = []

    timestamp = record["timestamp"]

    data = record["data"]

    node = data["node"]

    cores = data["cores"]

    # Skip overall CPU usage entry
    core_values = cores[1:49]

    if len(core_values) != 48:

        print(
            f"Warning: {timestamp} -> Expected 48 cores, got {len(core_values)}"
        )

        return rows

    for idx, core_data in enumerate(core_values):

        cpu_usage = float(core_data["cpu_usage"])

        if idx < 24:
            socket = 0
            core = idx
        else:
            socket = 1
            core = idx - 24

        rows.append(
            (
                timestamp,
                node,
                socket,
                core,
                cpu_usage,
            )
        )

    return rows


def main():

    all_rows = []

    json_files = find_json_files(
        RAW_DATA_DIR,
        "cpu_usage.json"
    )

    print(f"\nFound {len(json_files)} cpu_usage files.\n")

    for file in json_files:

        print(f"Reading: {file}")

        for record in iter_cpu_usage_records(file):

            all_rows.extend(
                extract_cpu_usage_records(record)
            )

    print(f"\nTotal rows extracted: {len(all_rows)}")

    batch_insert(
        INSERT_QUERY,
        all_rows
    )


if __name__ == "__main__":
    main()