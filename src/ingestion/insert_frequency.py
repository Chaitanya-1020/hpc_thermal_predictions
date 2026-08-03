"""
Insert frequency telemetry into MySQL.
"""

from src.ingestion.file_scanner import find_json_files
from src.ingestion.json_parser import iter_json_records
from src.ingestion.db_writer import batch_insert
from src.ingestion.config import RAW_DATA_DIR


INSERT_QUERY = """
INSERT IGNORE INTO frequency
(
    timestamp,
    node,
    socket,
    core,
    frequency
)
VALUES (%s,%s,%s,%s,%s)
"""


def extract_frequency_records(record):
    rows = []

    timestamp = record["timestamp"]

    node = next(iter(record["data"]))

    node_data = record["data"][node]

    for socket_name, socket_data in node_data.items():

        # Skip metadata (timestamp etc.)
        if not socket_name.startswith("socket_"):
            continue

        socket_id = int(socket_name.replace("socket_", ""))

        cpu = socket_data.get("CPU", {})

        # frequency.json uses "core" (lowercase)
        core_data = cpu.get("core", {})

        for key, value in core_data.items():

            if not key.startswith("core_"):
                continue

            if not key.endswith("_avg_freq_mhz"):
                continue

            core_id = int(
                key.replace("core_", "").replace("_avg_freq_mhz", "")
            )

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
        "frequency.json"
    )

    print(f"\nFound {len(json_files)} frequency files.\n")

    for file in json_files:

        print(f"Reading: {file}")

        for record in iter_json_records(file):

            all_rows.extend(
                extract_frequency_records(record)
            )

    print(f"\nTotal rows extracted: {len(all_rows)}")

    batch_insert(
        INSERT_QUERY,
        all_rows
    )


if __name__ == "__main__":
    main()