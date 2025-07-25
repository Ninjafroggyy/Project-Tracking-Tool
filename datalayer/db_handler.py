# datalayer/db_handler.py
import sqlite3
from pathlib import Path

DB_PATH = Path("data/project_tracker.db")
SCHEMA_PATH = Path("create_schema.sql")


def init_db():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        with open(SCHEMA_PATH, "r") as schema_file:
            conn.executescript(schema_file.read())
        conn.commit()


def run_query(query_path, params):
    with sqlite3.connect(DB_PATH) as conn:
        with open(query_path, "r") as f:
            sql = f.read()
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()


def fetch_all(query_path):
    with sqlite3.connect(DB_PATH) as conn:
        with open(query_path, "r") as f:
            sql = f.read()
        cur = conn.cursor()
        cur.execute(sql)
        return cur.fetchall()

if __name__ == "__main__":
    init_db()
    print("Database created successfully.")