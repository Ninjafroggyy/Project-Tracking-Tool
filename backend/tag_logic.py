# backend/tag_logic.py — Refactored Tag Logic
from datalayer.db_handler import execute, fetch_all, fetch_one
from datalayer.sql_queries import (
    TAG_EXISTS, TAGS_BY_TYPE, DELETE_TAG, INSERT_TAG,
    UPDATE_TAG, SELECT_TAGS
)

def add_tag(tag_name, tag_type):
    if tag_exists(tag_name):
        raise ValueError("Tag with new name already exists.")
    execute(INSERT_TAG, (tag_name, tag_type))

def get_all_tags():
    return fetch_all(SELECT_TAGS)

def get_tags_by_type(tag_type):
    return fetch_all(TAGS_BY_TYPE, (tag_type,))

def tag_exists(tag_name):
    return fetch_one(TAG_EXISTS, (tag_name,)) is not None

def update_tag_name(old_name, new_name, tag_type):
    if tag_exists(new_name):
        raise ValueError("Tag with new name already exists.")
    execute(UPDATE_TAG, (new_name, old_name, tag_type))

def delete_tag(tag_name, tag_type):
    execute(DELETE_TAG, (tag_name, tag_type))
