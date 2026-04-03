import psycopg2
import csv
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
def connect_db():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )

# Создание таблицы contacts
def create_table():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        first_name VARCHAR(50),
        phone VARCHAR(20) UNIQUE
    )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("Table created successfully!")


def insert_from_csv(file_path="contacts.csv"):
    conn = connect_db()
    cur = conn.cursor()
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            first_name, phone = row
            try:
                cur.execute(
                    "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
                    (first_name, phone)
                )
            except psycopg2.errors.UniqueViolation:
                conn.rollback()  
            else:
                conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted!")


def view_contacts():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contacts")
    rows = cur.fetchall()
    for row in rows:
        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    cur.close()
    conn.close()