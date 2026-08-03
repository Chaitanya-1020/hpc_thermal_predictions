"""
Insert Energy telemetry into MySQL.
"""

from src.ingestion.file_scanner import find_json_files
from src.ingestion.json_parser import iter_json_records
from src.ingestion.db_writer import batch_insert
from src.ingestion.config import RAW_DATA_DIR


INSERT_QUERY = """
INSERT IGNORE INTO energy
(
    timestamp,
    node,
    socket,
    cpu_energy,
    memory_energy
)
VALUES (%s,%s,%s,%s,%s)
"""
import json
from json import JSONDecodeError


def read_energy_objects(file_path):
    """
    Reads concatenated JSON objects from energy.json.

    If a JSON object is malformed (as in the first few records of the
    mentor dataset), it is skipped and ingestion continues.

    The original dataset is NEVER modified.
    """

    with open(file_path, "r", encoding="utf-8") as file:

        buffer = ""
        braces = 0
        skipped = 0

        for line in file:

            buffer += line

            braces += line.count("{")
            braces -= line.count("}")

            # wait until one complete object is collected
            if braces != 0:
                continue

            if not buffer.strip():
                buffer = ""
                continue

            try:

                obj = json.loads(buffer)

                # Skip records whose data field is missing/empty
                if (
                    "data" not in obj
                    or obj["data"] is None
                    or obj["data"] == {}
                ):
                    print(
                        f"⚠ Skipping empty record at {obj.get('timestamp')}"
                    )

                else:
                    yield obj

            except JSONDecodeError:

                # Expected for the first few malformed records
                preview = buffer.replace("\n", " ")[:80]

                print(
                    f"⚠ Skipping malformed record: {preview}..."
                )

                skipped += 1

            finally:

                buffer = ""

        if skipped:
            print(f"\nSkipped {skipped} malformed records.\n")
def extract_energy_records(record):

    rows = []

    timestamp = record["timestamp"]

    node = next(iter(record["data"]))

    node_data = record["data"][node]

    for socket_name, socket_data in node_data.items():

        if not socket_name.startswith("socket_"):
            continue

        socket = int(socket_name.replace("socket_", ""))

        cpu_energy = float(
            socket_data.get("energy_cpu_joules", 0)
        )

        memory_energy = float(
            socket_data.get("energy_mem_joules", 0)
        )

        rows.append(
            (
                timestamp,
                node,
                socket,
                cpu_energy,
                memory_energy,
            )
        )

    return rows


def main():

    all_rows = []

    json_files = find_json_files(
        RAW_DATA_DIR,
        "energy.json"
    )

    print(f"\nFound {len(json_files)} energy files.\n")

    for file in json_files:

        print(f"Reading: {file}")

        for record in read_energy_objects(file):

            all_rows.extend(
                extract_energy_records(record)
            )

    print(f"\nTotal rows extracted: {len(all_rows)}")

    batch_insert(
        INSERT_QUERY,
        all_rows
    )


if __name__ == "__main__":
    main()