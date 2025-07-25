# backend/tag_logic.py
from datalayer.db_handler import run_query, fetch_all
from pathlib import Path

INSERT_TAG = Path("../datalayer/insert_tag.sql")
SELECT_TAGS = Path("../datalayer/select_tags.sql")

def add_tag(name, category):
    run_query(INSERT_TAG, (name, category))

def get_all_tags():
    return fetch_all(SELECT_TAGS)