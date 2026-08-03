import csv

from database.mysql_connection import get_connection


OUTPUT_FILE = "data/processed/merged_dataset.csv"


def main():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM merged_dataset
        ORDER BY timestamp, node, socket, core
    """)

    rows = cursor.fetchall()

    if not rows:
        print("No data found.")
        return

    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8"
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=rows[0].keys()
        )

        writer.writeheader()
        writer.writerows(rows)

    cursor.close()
    conn.close()

    print(f"\n✅ Export completed")

    print(f"Rows exported : {len(rows)}")

    print(f"Saved to : {OUTPUT_FILE}")


if __name__ == "__main__":
    main()