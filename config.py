# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SCHEMA_DIR = os.path.join(BASE_DIR, 'datalayer')

DB_PATH = os.path.join(DATA_DIR, 'project_tracker.db')
SCHEMA_PATH = os.path.join(SCHEMA_DIR, 'create_schema.sql')

SELECT_PROJECTS_SQL = os.path.join(SCHEMA_DIR, 'select_projects.sql')
INSERT_PROJECTS_SQL = os.path.join(SCHEMA_DIR, 'insert_project.sql')
UPDATE_PROJECTS_SQL = os.path.join(SCHEMA_DIR, 'update_projects.sql')
DELETE_PROJECTS_SQL = os.path.join(SCHEMA_DIR, 'delete_project.sql')

# Tag SQL
INSERT_TAG_SQL = "datalayer/insert_tag.sql"
SELECT_TAGS_SQL = "datalayer/select_tags.sql"
SELECT_TAGS_BY_TYPE_SQL = "datalayer/select_tags_by_type.sql"
CHECK_TAG_EXISTS_SQL = "datalayer/check_tag_exists.sql"

UPDATE_TAG_SQL = "datalayer/update_tag.sql"
DELETE_TAG_SQL = "datalayer/delete_tag.sql"

