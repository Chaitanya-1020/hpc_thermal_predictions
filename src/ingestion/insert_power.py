"""
Insert Power telemetry into MySQL.
"""

from src.ingestion.file_scanner import find_json_files
from src.ingestion.json_parser import iter_json_records
from src.ingestion.db_writer import batch_insert
from src.ingestion.config import RAW_DATA_DIR


INSERT_QUERY = """
INSERT IGNORE INTO power
(
    timestamp,
    node,
    socket,
    cpu_power,
    memory_power
)
VALUES (%s,%s,%s,%s,%s)
"""


def extract_power_records(record):

    rows = []

    timestamp = record["timestamp"]

    node = next(iter(record["data"]))

    node_data = record["data"][node]

    for socket_name, socket_data in node_data.items():

        if not socket_name.startswith("socket_"):
            continue

        socket = int(socket_name.replace("socket_", ""))

        cpu_power = float(
            socket_data.get("power_cpu_watts", 0)
        )

        memory_power = float(
            socket_data.get("power_mem_watts", 0)
        )

        rows.append(
            (
                timestamp,
                node,
                socket,
                cpu_power,
                memory_power,
            )
        )

    return rows

def main():

    all_rows = []

    json_files = find_json_files(
        RAW_DATA_DIR,
        "power.json"
    )

    print(f"\nFound {len(json_files)} power files.\n")

    for file in json_files:

        print(f"Reading: {file}")

        for record in iter_json_records(file):

            all_rows.extend(
                extract_power_records(record)
            )

    print(f"\nTotal rows extracted: {len(all_rows)}")

    batch_insert(
        INSERT_QUERY,
        all_rows
    )


if __name__ == "__main__":
    main()