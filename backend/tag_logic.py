# backend/tag_logic.py
from datalayer.db_handler import run_query, fetch_all, fetch_one
from config import INSERT_TAG_SQL, SELECT_TAGS_SQL, SELECT_TAGS_BY_TYPE_SQL, CHECK_TAG_EXISTS_SQL, UPDATE_TAG_SQL, DELETE_TAG_SQL

# Add a new tag to the database
def add_tag(tag_name, tag_type):
    params = (tag_name, tag_type)
    run_query(INSERT_TAG_SQL, params)

# Retrieve all tags
def get_all_tags():
    return fetch_all(SELECT_TAGS_SQL)

# Retrieve tags by specific category
def get_tags_by_type(tag_type):
    return fetch_all(SELECT_TAGS_BY_TYPE_SQL, (tag_type,))

# Check if tag name already exists
def tag_exists(tag_name):
    result = fetch_one(CHECK_TAG_EXISTS_SQL, (tag_name,))
    return result is not None

def update_tag_name(old_name, new_name, category):
    if tag_exists(new_name):
        raise ValueError("Tag with new name already exists.")
    params = (new_name, old_name, category)
    run_query(UPDATE_TAG_SQL, params)

def delete_tag(tag_name, category):
    params = (tag_name, category)
    run_query(DELETE_TAG_SQL, params)