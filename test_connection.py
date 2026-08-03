from database.mysql_connection import get_connection, close_connection

print("Starting...")

conn = get_connection()

print("✅ Database Connected Successfully!")

close_connection(conn)