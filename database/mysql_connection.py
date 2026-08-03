import pymysql

def get_connection():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="#Chaitanya102005#",   # <-- Your MySQL password
            database="hpc_thermal_prediction",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=False
        )

        print("✅ Connected to MySQL")
        return conn

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        raise


def close_connection(conn):
    if conn:
        conn.close()
        print("🔒 Connection Closed")