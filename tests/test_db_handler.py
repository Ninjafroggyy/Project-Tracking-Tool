# tests/test_db_handler.py
import sqlite3
import pytest
import datalayer.db_handler as dbh
from datalayer.db_handler import (
    execute,
    execute_returning_lastrowid,
    executemany,
    fetch_all,
    fetch_one,
    fetch_val,
    to_dicts,
    transaction,
)

# Dummy cursor/connection to simulate sqlite3
class DummyCursor:
    def __init__(self):
        self.rowcount = 42
        self.lastrowid = 99
        self._data = [(1, 'a'), (2, 'b')]
    def execute(self, sql, params=()):
        DummyCursor.last_sql = sql
        DummyCursor.last_params = params
        return self
    def executemany(self, sql, seq_of_params):
        DummyCursor.many_sql = sql
        DummyCursor.many_params = seq_of_params
        return self
    def fetchall(self):
        return self._data
    def fetchone(self):
        return ('only',)

class DummyConn:
    def __init__(self, cursor):
        self._cursor = cursor
        self.committed = False
        self.rolled_back = False
    def execute(self, sql, params=()):
        return self._cursor.execute(sql, params)
    def executemany(self, sql, seq_of_params):
        return self._cursor.executemany(sql, seq_of_params)
    def commit(self):
        self.committed = True
    def rollback(self):
        self.rolled_back = True
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc, tb):
        if exc_type:
            self.rollback()
        else:
            self.commit()
    def close(self):
        pass  # Added to avoid attribute errors

@pytest.fixture(autouse=True)
def patch_connect(monkeypatch):
    # Monkeypatch _connect to return DummyConn
    cursor = DummyCursor()
    conn = DummyConn(cursor)
    monkeypatch.setattr(dbh, '_connect', lambda: conn)
    return cursor, conn


def test_execute_returns_rowcount(patch_connect):
    cursor, conn = patch_connect
    rc = execute("SQL STATEMENT", (1, 2))
    assert rc == cursor.rowcount
    assert DummyCursor.last_sql == "SQL STATEMENT"
    assert DummyCursor.last_params == (1, 2)
    assert conn.committed is True


def test_execute_returning_lastrowid(patch_connect):
    cursor, conn = patch_connect
    lid = execute_returning_lastrowid("INSERT SQL", ())
    assert lid == cursor.lastrowid
    assert conn.committed is True


def test_executemany_returns_rowcount(patch_connect):
    cursor, conn = patch_connect
    seq = [(1,), (2,)]
    rc = executemany("SQL MANY", seq)
    assert rc == cursor.rowcount
    assert DummyCursor.many_sql == "SQL MANY"
    assert DummyCursor.many_params == seq
    assert conn.committed is True


def test_fetch_all_fetches_all(patch_connect):
    cursor, conn = patch_connect
    rows = fetch_all("SELECT *", ())
    assert rows == cursor._data
    # fetch_all context manager commits on exit
    assert conn.committed is True


def test_fetch_one_fetches_one(patch_connect):
    cursor, conn = patch_connect
    row = fetch_one("SELECT ONE", ())
    assert row == ('only',)
    # fetch_one context manager commits on exit
    assert conn.committed is True


def test_fetch_val_returns_value_and_none(patch_connect, monkeypatch):
    # Case where fetch_one returns a row-like
    monkeypatch.setattr(dbh, 'fetch_one', lambda sql, params=(): (['val'],))
    val = fetch_val("SQL", ())
    assert val == ['val']
    # Case where fetch_one returns None
    monkeypatch.setattr(dbh, 'fetch_one', lambda sql, params=(): None)
    val2 = fetch_val("SQL2", ())
    assert val2 is None


def test_to_dicts_converts_rows():
    # create dummy sqlite3.Row analog
    class FakeRow(dict):
        pass
    rows = [FakeRow(a=1), FakeRow(b=2)]
    dicts = to_dicts(rows)
    assert isinstance(dicts, list)
    assert dicts[0]['a'] == 1


def test_transaction_commits_on_success(monkeypatch):
    # Patch _connect to return our DummyConn
    cursor = DummyCursor()
    conn = DummyConn(cursor)
    monkeypatch.setattr(dbh, '_connect', lambda: conn)
    with transaction() as tconn:
        assert tconn is conn
    assert conn.committed is True


def test_transaction_rolls_back_on_exception(monkeypatch):
    cursor = DummyCursor()
    conn = DummyConn(cursor)
    monkeypatch.setattr(dbh, '_connect', lambda: conn)
    with pytest.raises(RuntimeError):
        with transaction() as tconn:
            raise RuntimeError("fail")
    assert conn.rolled_back is True

