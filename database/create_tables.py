from pathlib import Path
from database.mysql_connection import get_connection, close_connection


def execute_schema():
    conn = get_connection()
    cursor = conn.cursor()

    schema_path = Path(__file__).parent / "schema.sql"

    with open(schema_path, "r", encoding="utf-8") as f:
        sql = f.read()

    # Execute each SQL statement separately
    for statement in sql.split(";"):
        statement = statement.strip()
        if statement:
            print("\nExecuting:")
            print(statement[:100] + "..." if len(statement) > 100 else statement)
            cursor.execute(statement)

    conn.commit()

    print("✅ All tables created successfully.")

    cursor.close()
    close_connection(conn)


if __name__ == "__main__":
    execute_schema()