# datalayer/db_handler.py
import os
import sqlite3
from config import DB_PATH, SCHEMA_PATH

def create_database():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    with open(SCHEMA_PATH, 'r') as f:
        schema_sql = f.read()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()


def get_connection():
    return sqlite3.connect(DB_PATH)


def run_query(query_path, params):
    with sqlite3.connect(DB_PATH) as conn:
        with open(query_path, "r") as f:
            sql = f.read()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()


def fetch_all(query_path, params=()):
    with open(query_path, "r") as f:
        query = f.read()
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()
    return rows


def fetch_one(query_path, params=None):
    with open(query_path, "r") as f:
        query = f.read()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    if params:
        cursor.execute(query, params)
    else:
        cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    return result


if __name__ == "__main__":
    create_database()
    print("Database created successfully.")