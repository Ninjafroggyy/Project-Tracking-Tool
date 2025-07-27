# datalayer/db_handler.py — Refined DB Layer
from __future__ import annotations

import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Iterable, Optional, Sequence

from config import DB_PATH as CONFIG_DB_PATH, SCHEMA_PATH

DB_PATH = Path(CONFIG_DB_PATH)

def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def create_database() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    with _connect() as conn:
        conn.executescript(schema_sql)
        conn.commit()

def get_connection() -> sqlite3.Connection:
    return _connect()

@contextmanager
def transaction() -> Iterable[sqlite3.Connection]:
    conn = _connect()
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

def execute(sql: str, params: Sequence[Any] = ()) -> int:
    with _connect() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.rowcount

def execute_returning_lastrowid(sql: str, params: Sequence[Any] = ()) -> int:
    with _connect() as conn:
        cur = conn.execute(sql, params)
        conn.commit()
        return cur.lastrowid

def executemany(sql: str, seq_of_params: Iterable[Sequence[Any]]) -> int:
    with _connect() as conn:
        cur = conn.executemany(sql, seq_of_params)
        conn.commit()
        return cur.rowcount

def fetch_all(sql: str, params: Sequence[Any] = ()) -> list[sqlite3.Row]:
    with _connect() as conn:
        return conn.execute(sql, params).fetchall()

def fetch_one(sql: str, params: Sequence[Any] = ()) -> Optional[sqlite3.Row]:
    with _connect() as conn:
        return conn.execute(sql, params).fetchone()

def fetch_val(sql: str, params: Sequence[Any] = ()) -> Any:
    row = fetch_one(sql, params)
    return row[0] if row else None

def to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    return [dict(r) for r in rows]

if __name__ == "__main__":
    create_database()
    print("Database created successfully.")
