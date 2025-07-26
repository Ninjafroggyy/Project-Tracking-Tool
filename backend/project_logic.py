# backend/project_logic.py — Refactored Project Logic
from datalayer.db_handler import execute, fetch_all, fetch_one
from datalayer.sql_queries import DELETE_PRO, UPDATE_PRO, INSERT_PRO, SELECT_PRO, SELECT_PROJECT_BY_ID

def add_project(
    title,
    category,
    project_type,
    creative_skills,
    technical_skills,
    tools,
    status,
    duration,
    collaborators,
    languages,
    report_done=False,
    added_to_portfolio=False,
    has_showcase_material=False,
    notes=""
):
    params = _format_project_params(
        title, category, project_type, creative_skills, technical_skills,
        tools, status, duration, collaborators, languages,
        report_done, added_to_portfolio, has_showcase_material, notes
    )
    execute(INSERT_PRO, params)

def get_all_projects():
    return fetch_all(SELECT_PRO)

def update_project(
    project_id,
    title,
    category,
    project_type,
    creative_skills,
    technical_skills,
    tools,
    status,
    duration,
    collaborators,
    languages,
    report_done,
    added_to_portfolio,
    has_showcase_material,
    notes=""
):
    params = _format_project_params(
        title, category, project_type, creative_skills, technical_skills,
        tools, status, duration, collaborators, languages,
        report_done, added_to_portfolio, has_showcase_material, notes
    ) + (project_id,)
    execute(UPDATE_PRO, params)

def delete_project(project_id):
    execute(DELETE_PRO, (project_id,))

def _format_project_params(
    title, category, project_type, creative_skills, technical_skills,
    tools, status, duration, collaborators, languages,
    report_done, added_to_portfolio, has_showcase_material, notes
):
    def normalize(val):
        return ", ".join(val) if isinstance(val, list) else val

    return (
        title,
        normalize(category),
        normalize(project_type),
        normalize(creative_skills),
        normalize(technical_skills),
        normalize(tools),
        normalize(status),
        duration,
        collaborators,
        normalize(languages),
        int(report_done),
        int(added_to_portfolio),
        int(has_showcase_material),
        notes
    )


def get_project_by_id(project_id):
    """Fetch a single project record by its ID."""
    return fetch_one(SELECT_PROJECT_BY_ID, (project_id,))