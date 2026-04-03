import psycopg2
from config import load_config

def create_table():
    commands = """
    CREATE TABLE IF NOT EXISTS phonebook (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        phone VARCHAR(20) NOT NULL
    );
    """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(commands)
        print("Table 'phonebook' is ready.")
    except Exception as error:
        print(error)

def ups():
    username = input("Enter username: ").strip()
    phone = input("Enter phone: ").strip()
    sql = "CALL upsert_u(%s, %s);"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (username, phone))
        print(f"User {username} upserted successfully.")
    except Exception as error:
        print(error)

def hz():
    print("Enter list of usernames (space-separated):")
    u = input().split()
    print("Enter list of phones (space-separated):")
    p = input().split()
    if len(u) != len(p):
        print("Error: number of usernames and phones must match.")
        return
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute("CALL loophz(%s, %s);", (u, p))
                for notice in conn.notices:
                    print(notice.strip())
        print("Lists inserted successfully.")
    except Exception as error:
        print(error)

def delete_contact():
    choice = input("Delete by (1) username or (2) phone? ").strip()
    if choice == "1":
        value = input("Enter username: ").strip()
        sql = "CALL del_user(%s, NULL);"
    elif choice == "2":
        value = input("Enter phone: ").strip()
        sql = "CALL del_user(NULL, %s);"
    else:
        print("Invalid choice.")
        return
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (value,))
        print("User deleted successfully.")
    except Exception as error:
        print(error)

def match_return():
    pattern = input("Write the username or phone part to match: ").strip()
    sql = "SELECT * FROM records(%s);"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (pattern,))
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
                else:
                    print("No matching contacts.")
    except Exception as error:
        print(error)

def pages():
    try:
        lim = int(input("Enter limit: "))
        offs = int(input("Enter offset: "))
    except ValueError:
        print("Invalid number.")
        return
    sql = "SELECT * FROM pagination(%s, %s);"
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (lim, offs))
                rows = cur.fetchall()
                if rows:
                    for row in rows:
                        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
                else:
                    print("No records in this range.")
    except Exception as error:
        print(error)

def main():
    while True:
        print("1. Create table\n2. Upsert user\n3. Insert list of users\n4. Delete contact\n5. Return matching records\n6. Paginated data\n7. Exit")
        try:
            choice = int(input())
        except ValueError:
            print("Please enter a number.")
            continue
        if choice == 1:
            create_table()
        elif choice == 2:
            ups()
        elif choice == 3:
            hz()
        elif choice == 4:
            delete_contact()
        elif choice == 5:
            match_return()
        elif choice == 6:
            pages()
        elif choice == 7:
            print("Bye!")
            break
        else:
            print("Try again!")
            continue
        cont = input("Would you like to continue? y/n ").strip().lower()
        if cont == "n":
            print("Bye!")
            break

main()