# config.py
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
SCHEMA_DIR = os.path.join(BASE_DIR, 'datalayer')

DB_PATH = os.path.join(DATA_DIR, 'project_tracker.db')
SCHEMA_PATH = os.path.join(SCHEMA_DIR, 'create_schema.sql')


