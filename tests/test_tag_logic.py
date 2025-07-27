# tests/test_tag_logic.py
import pytest
import backend.tag_logic as tag_logic
import datalayer.db_handler as db_handler
import datalayer.sql_queries as queries

# Helper to stub DB connection
class DummyCursor:
    def __init__(self, data=None, one=None):
        self.rowcount = None
        self._data = data or []
        self._one = one
    def fetchall(self):
        return self._data
    def fetchone(self):
        return self._one

class DummyConn:
    def __init__(self, cursor):
        self._cursor = cursor
    def execute(self, sql, params=()):
        self._cursor.rowcount = 1
        DummyConn.last_sql = sql
        DummyConn.last_params = params
        return self._cursor
    def commit(self): pass
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): pass

@pytest.fixture(autouse=True)
def patch_db(monkeypatch):
    # Patch db_handler._connect to use DummyConn
    import datalayer.db_handler as dbh
    cursor = DummyCursor(data=[('T1', 'Type1')], one=('exists',))
    monkeypatch.setattr(dbh, '_connect', lambda: DummyConn(cursor))
    return cursor


def test_add_tag_success(monkeypatch):
    monkeypatch.setattr(tag_logic, 'tag_exists', lambda name: False)
    captured = {}
    def fake_execute(sql, params=()):
        captured['sql'] = sql
        captured['params'] = params
    monkeypatch.setattr(tag_logic, 'execute', fake_execute)
    tag_logic.add_tag('NewTag', 'Cat')
    assert captured['sql'] == queries.INSERT_TAG
    assert captured['params'] == ('NewTag', 'Cat')


def test_add_tag_duplicate(monkeypatch):
    monkeypatch.setattr(tag_logic, 'tag_exists', lambda name: True)
    with pytest.raises(ValueError) as exc:
        tag_logic.add_tag('DupTag', 'Cat')
    assert 'already exists' in str(exc.value)


def test_get_all_tags(monkeypatch, patch_db):
    # Should call fetch_all and return list
    result = tag_logic.get_all_tags()
    assert result == patch_db._data
    # verify SQL constant used
    assert queries.SELECT_TAGS in DummyConn.last_sql


def test_get_tags_by_type(monkeypatch, patch_db):
    captured = {}
    def fake_fetch_all(sql, params=None):
        captured['sql'] = sql
        captured['params'] = params
        return patch_db._data
    monkeypatch.setattr(tag_logic, 'fetch_all', fake_fetch_all)
    result = tag_logic.get_tags_by_type('MyType')
    assert result == patch_db._data
    assert captured['sql'] == queries.TAGS_BY_TYPE
    assert captured['params'] == ('MyType',)


def test_tag_exists_true_false(patch_db):
    # since patch_db.one = ('exists',)
    assert tag_logic.tag_exists('Any') is True
    # patch to None
    patch_db._one = None
    assert tag_logic.tag_exists('Any') is False


def test_update_tag_name_success(monkeypatch):
    monkeypatch.setattr(tag_logic, 'tag_exists', lambda name: False)
    captured = {}
    def fake_execute(sql, params=()):
        captured['sql'] = sql
        captured['params'] = params
    monkeypatch.setattr(tag_logic, 'execute', fake_execute)
    tag_logic.update_tag_name('Old', 'New', 'Cat')
    assert captured['sql'] == queries.UPDATE_TAG
    assert captured['params'] == ('New', 'Old', 'Cat')


def test_update_tag_duplicate():
    monkeypatch = pytest.MonkeyPatch()
    monkeypatch.setattr(tag_logic, 'tag_exists', lambda name: True)
    with pytest.raises(ValueError):
        tag_logic.update_tag_name('Old', 'Existing', 'Cat')
    monkeypatch.undo()


def test_delete_tag(monkeypatch):
    captured = {}
    def fake_execute(sql, params=()):
        captured['sql'] = sql
        captured['params'] = params
    monkeypatch.setattr(tag_logic, 'execute', fake_execute)
    tag_logic.delete_tag('TagX', 'CatX')
    assert captured['sql'] == queries.DELETE_TAG
    assert captured['params'] == ('TagX', 'CatX')
