import sys
import sqlite3

def run_query(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Exception as e:
        print(e)

create_table = """
CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    name text NOT NULL
);"""

insert_records = """
INSERT INTO users (name) VALUES ('Alice');
INSERT INTO users (name) VALUES ('Bob');
INSERT INTO users (name) VALUES ('Charlie');
"""

conn = sqlite3.connect("database.db")
run_query(conn, create_table)
conn.executescript(insert_records)
conn.commit()

def main():
    user_id = sys.argv[1]
    query = f"SELECT name FROM users WHERE id = {user_id}"

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    if result:
        print(f"User name: {result}")
    else:
        print("User not found")

if __name__ == "__main__":
    main()