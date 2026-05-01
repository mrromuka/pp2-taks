import psycopg2
from config import DB_CONFIG

def get_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("✅ Connected to DB")
        return conn
    except Exception as e:
        print("❌ Connection error:", e)
        raise