# tests/test_export_logic.py
import pytest
import pandas as pd
from backend.export_logic import export_to_excel

# Tracking writer to capture sheet writes
_writer_instances = []
class TrackingWriter:
    def __init__(self, filepath, **kwargs):
        self.filepath = filepath
        self.sheets = {}
        _writer_instances.append(self)
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    def to_excel(self, df, sheet_name=None, index=False, **kwargs):
        # Store DataFrame for assertion
        self.sheets[sheet_name] = df.copy()

@pytest.fixture(autouse=True)
def patch_export(monkeypatch):
    # Prepare dummy data
    projects = [dict(id=1, name='P1'), dict(id=2, name='P2')]
    minis = [dict(id=1, summary='M1')]
    tags = [dict(tag_name='T1', tag_type='Type1')]
    # Patch backend data getters
    monkeypatch.setattr('backend.export_logic.get_all_projects', lambda: projects)
    monkeypatch.setattr('backend.export_logic.get_all_mini_projects', lambda: minis)
    monkeypatch.setattr('backend.export_logic.get_all_tags', lambda: tags)
    # Patch pandas.ExcelWriter
    monkeypatch.setattr(pd, 'ExcelWriter', TrackingWriter)
    # Patch DataFrame.to_excel to use our writer
    original_to_excel = pd.DataFrame.to_excel
    def fake_to_excel(self, writer, sheet_name=None, index=False, **kwargs):
        writer.to_excel(self, sheet_name=sheet_name, index=index)
    monkeypatch.setattr(pd.DataFrame, 'to_excel', fake_to_excel)
    yield projects, minis, tags
    # Restore
    monkeypatch.setattr(pd.DataFrame, 'to_excel', original_to_excel)


def test_export_to_excel_creates_sheets(patch_export, tmp_path):
    projects, minis, tags = patch_export
    filepath = tmp_path / 'out.xlsx'
    export_to_excel(str(filepath))
    # Ensure a writer was instantiated
    assert len(_writer_instances) >= 1
    writer = _writer_instances[-1]
    # Check that sheets were written
    assert set(writer.sheets.keys()) == {'Projects', 'Mini Projects', 'Tags'}


def test_export_sheets_content(patch_export, tmp_path):
    projects, minis, tags = patch_export
    filepath = tmp_path / 'out2.xlsx'
    export_to_excel(str(filepath))
    writer = _writer_instances[-1]
    # Assert dataframe equality
    pd.testing.assert_frame_equal(writer.sheets['Projects'], pd.DataFrame(projects))
    pd.testing.assert_frame_equal(writer.sheets['Mini Projects'], pd.DataFrame(minis))
    pd.testing.assert_frame_equal(writer.sheets['Tags'], pd.DataFrame(tags))
