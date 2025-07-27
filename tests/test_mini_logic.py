# tests/test_mini_logic.py
import pytest
import backend.mini_logic as mini_logic
import datalayer.db_handler as db_handler
import datalayer.sql_queries as queries

class DummyCursor:
    def __init__(self):
        self.rowcount = None
        self._data = []
    def fetchall(self):
        return self._data

class DummyConn:
    def __init__(self, cursor):
        self._cursor = cursor
    def execute(self, sql, params=()):
        # simulate execution by storing params and sql
        self._cursor.rowcount = 1
        DummyConn.last_sql = sql
        DummyConn.last_params = params
        return self._cursor
    def commit(self):
        pass
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): pass

@pytest.fixture(autouse=True)
def fake_connect(monkeypatch):
    # Patch _connect in db_handler to return DummyConn for INSERT
    cursor = DummyCursor()
    cursor._data = [('m1', 'tag1', 'sum1')]
    def fake_connect_func():
        return DummyConn(cursor)
    monkeypatch.setattr(db_handler, '_connect', fake_connect_func)
    return cursor


def test_add_mini_project_executes_insert(monkeypatch):
    captured = {}
    def fake_execute(sql, params=()):
        captured['sql'] = sql
        captured['params'] = params
        return 1
    monkeypatch.setattr(mini_logic, 'execute', fake_execute)

    # Call add_mini_project
    mini_logic.add_mini_project('TestMini', 'tagA, tagB', 'Summary text')

    # Verify correct SQL and parameters
    assert captured['sql'].strip().upper().startswith('INSERT INTO')
    assert captured['params'] == ('TestMini', 'tagA, tagB', 'Summary text')


def test_get_all_mini_projects_returns_rows():
    # Patch fetch_all to return sentinel data
    sentinel = [('m1', 'tag1', 'sum1')]
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(mini_logic, 'fetch_all', lambda q: sentinel)
    result = mini_logic.get_all_mini_projects()
    monkeypatch.undo()
    assert result is sentinel
    # Ensure SQL constant is correct
    assert 'SELECT' in queries.SELECT_MINI.upper()
