# backend/mini_logic.py — Refactored Mini-Project Logic
from datalayer.db_handler import execute, fetch_all
from datalayer.sql_queries import INSERT_MINI, SELECT_MINI

def add_mini_project(title, tags, summary):
    execute(INSERT_MINI, (title, tags, summary))

def get_all_mini_projects():
    return fetch_all(SELECT_MINI)
