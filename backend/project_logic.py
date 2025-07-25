# backend/project_logic.py
from datalayer.db_handler import run_query, fetch_all
from pathlib import Path

INSERT_PATH = Path("../datalayer/insert_project.sql")
SELECT_PATH = Path("../datalayer/select_projects.sql")
UPDATE_PATH = Path("../datalayer/update_project.sql")
DELETE_PATH = Path("../datalayer/delete_project.sql")

def add_project(
    title,
    category,
    type_,
    creative_skills,
    technical_skills,
    tools,
    status,
    duration,
    collaborators,
    notes,
    report_done=False,
    added_to_portfolio=False,
    has_showcase_material=False
):
    params = (
        title,
        category,
        type_,
        creative_skills,
        technical_skills,
        tools,
        status,
        duration,
        collaborators,
        notes,
        int(report_done),
        int(added_to_portfolio),
        int(has_showcase_material)
    )
    run_query(INSERT_PATH, params)

def get_all_projects():
    return fetch_all(SELECT_PATH)

def update_project(
    project_id,
    title,
    category,
    type_,
    creative_skills,
    technical_skills,
    tools,
    status,
    duration,
    collaborators,
    notes,
    report_done,
    added_to_portfolio,
    has_showcase_material
):
    params = (
        title,
        category,
        type_,
        creative_skills,
        technical_skills,
        tools,
        status,
        duration,
        collaborators,
        notes,
        int(report_done),
        int(added_to_portfolio),
        int(has_showcase_material),
        project_id
    )
    run_query(UPDATE_PATH, params)

def delete_project(project_id):
    run_query(DELETE_PATH, (project_id,))
