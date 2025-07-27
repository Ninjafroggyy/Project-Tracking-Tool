# tests/test_project_logic.py
import pytest
from backend import project_logic
from backend.project_logic import _format_project_params, update_project, get_all_projects, get_project_by_id

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
    # Patch _connect() in db_handler to return DummyConn
    import datalayer.db_handler as db_handler
    cursor = DummyCursor()
    cursor._data = [('row',)]
    def fake_connect_func():
        return DummyConn(cursor)
    monkeypatch.setattr(db_handler, '_connect', fake_connect_func)
    return cursor


def test_format_params_with_list_and_str():
    params = _format_project_params(
        title='T',
        category=['A', 'B'],
        project_type='X',
        creative_skills=['S'],
        technical_skills=[],
        tools='Tool',
        status=['st'],
        duration='5',
        collaborators='Me',
        languages=['Py'],
        report_done=1,
        added_to_portfolio=0,
        has_showcase_material=1,
        notes='Note'
    )
    assert isinstance(params, tuple)
    assert params[1] == 'A, B'
    assert params[4] == ''
    assert params[10] == 1
    assert params[12] == 1


def test_update_project_calls_execute():
    # Spy on execute in project_logic to capture SQL and params
    import backend.project_logic as logic
    captured = {}
    def fake_execute(sql, params=()):
        captured['sql'] = sql
        captured['params'] = params
        return 1
    # Patch execute function
    import backend.project_logic
    import pytest
    from backend.project_logic import update_project
    import backend.project_logic as project_logic
    from datalayer.sql_queries import UPDATE_PRO
    # Replace execute in project_logic
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(project_logic, 'execute', fake_execute)

    # Call update_project
    update_project(
        project_id=5,
        title='T',
        category='C',
        project_type='PT',
        creative_skills='CS',
        technical_skills='TS',
        tools='Tool',
        status='st',
        duration='10',
        collaborators='Col',
        languages='Lang',
        report_done=0,
        added_to_portfolio=1,
        has_showcase_material=0,
        notes='N'
    )
    monkeypatch.undo()
    # verify SQL and params
    assert captured['sql'].strip().upper().startswith('UPDATE PROJECTS SET')
    # last parameter should be project_id
    assert captured['params'][-1] == 5

def test_get_all_projects(monkeypatch):
    # Patch fetch_all in project_logic
    sentinel = [('row',)]
    monkeypatch.setattr(project_logic, 'fetch_all', lambda q: sentinel)
    result = get_all_projects()
    assert result is sentinel


def test_get_project_by_id(monkeypatch):
    # Patch fetch_one in project_logic
    sentinel = ('row',)
    monkeypatch.setattr(project_logic, 'fetch_one', lambda q, p: sentinel)
    result = get_project_by_id(10)
    assert result == sentinel
    import datalayer.sql_queries as queries
    assert 'WHERE id = ?' in queries.SELECT_PROJECT_BY_ID
