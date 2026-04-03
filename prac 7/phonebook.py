import psycopg2
import csv

def connect_db():
    return psycopg2.connect(
        dbname="mydb",
        user="postgres",
        password="1234",
        host="localhost",
        port=5432
    )

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

def insert_from_csv(file_path):
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

def insert_from_console():
    first_name = input("Enter first name: ")
    phone = input("Enter phone: ")
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO contacts (first_name, phone) VALUES (%s, %s)",
            (first_name, phone)
        )
        conn.commit()
        print("Contact added!")
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        print("Phone already exists!")
    cur.close()
    conn.close()

def update_contact():
    phone = input("Enter phone number of contact to update: ")
    conn = connect_db()
    cur = conn.cursor()
    choice = input("Update (1) Name or (2) Phone? ")
    if choice == "1":
        new_name = input("Enter new first name: ")
        cur.execute(
            "UPDATE contacts SET first_name=%s WHERE phone=%s",
            (new_name, phone)
        )
    elif choice == "2":
        new_phone = input("Enter new phone number: ")
        cur.execute(
            "UPDATE contacts SET phone=%s WHERE phone=%s",
            (new_phone, phone)
        )
    conn.commit()
    print("Contact updated!")
    cur.close()
    conn.close()

def query_contacts():
    print("Search by: (1) Name (2) Phone prefix")
    choice = input("Choice: ")
    conn = connect_db()
    cur = conn.cursor()
    if choice == "1":
        name = input("Enter name to search: ")
        cur.execute(
            "SELECT * FROM contacts WHERE first_name ILIKE %s",
            (f"%{name}%",)
        )
    elif choice == "2":
        prefix = input("Enter phone prefix: ")
        cur.execute(
            "SELECT * FROM contacts WHERE phone LIKE %s",
            (f"{prefix}%",)
        )
    rows = cur.fetchall()
    if not rows:
        print("No contacts found.")
    for row in rows:
        print(row)
    cur.close()
    conn.close()

def delete_contact():
    print("Delete by: (1) Name (2) Phone")
    choice = input("Choice: ")
    conn = connect_db()
    cur = conn.cursor()
    if choice == "1":
        name = input("Enter name to delete: ")
        cur.execute("DELETE FROM contacts WHERE first_name=%s", (name,))
    elif choice == "2":
        phone = input("Enter phone to delete: ")
        cur.execute("DELETE FROM contacts WHERE phone=%s", (phone,))
    conn.commit()
    print("Contact deleted!")
    cur.close()
    conn.close()

def main():
    create_table()
    while True:
        print("\nPhoneBook Menu:")
        print("1. Insert from console")
        print("2. Insert from CSV")
        print("3. Update contact")
        print("4. Query contacts")
        print("5. Delete contact")
        print("6. Exit")
        choice = input("Choose option: ")
        if choice == "1":
            insert_from_console()
        elif choice == "2":
            path = input("Enter CSV file path: ")
            insert_from_csv(path)
        elif choice == "3":
            update_contact()
        elif choice == "4":
            query_contacts()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()