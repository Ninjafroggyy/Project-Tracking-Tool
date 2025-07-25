# backend/mini_logic.py
from datalayer.db_handler import run_query, fetch_all
from pathlib import Path

INSERT_MINI = Path("../datalayer/insert_mini.sql")
SELECT_MINI = Path("../datalayer/select_mini.sql")

def add_mini_project(title, tags, summary):
    run_query(INSERT_MINI, (title, tags, summary))

def get_all_mini_projects():
    return fetch_all(SELECT_MINI)
