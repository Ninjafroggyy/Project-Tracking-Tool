# backend/project_logic.py
from datalayer.db_handler import run_query, fetch_all
from config import SELECT_PROJECTS_SQL, INSERT_PROJECTS_SQL, UPDATE_PROJECTS_SQL, DELETE_PROJECTS_SQL


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
        has_showcase=False,
        notes=""
):

    # Convert all tag lists to comma-separated strings
    category = ", ".join(category) if isinstance(category, list) else category
    project_type = ", ".join(project_type) if isinstance(project_type, list) else project_type
    creative_skills = ", ".join(creative_skills) if isinstance(creative_skills, list) else creative_skills
    technical_skills = ", ".join(technical_skills) if isinstance(technical_skills, list) else technical_skills
    tools = ", ".join(tools) if isinstance(tools, list) else tools
    status = ", ".join(status) if isinstance(status, list) else status
    languages = ", ".join(languages) if isinstance(languages, list) else languages

    params = (
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
        int(report_done),
        int(added_to_portfolio),
        int(has_showcase),
        notes
    )
    run_query(INSERT_PROJECTS_SQL, params)

def get_all_projects():
    return fetch_all(SELECT_PROJECTS_SQL)

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
        has_showcase,
        notes=""
):
    # Convert all tag lists to comma-separated strings
    category = ", ".join(category) if isinstance(category, list) else category
    project_type = ", ".join(project_type) if isinstance(project_type, list) else project_type
    creative_skills = ", ".join(creative_skills) if isinstance(creative_skills, list) else creative_skills
    technical_skills = ", ".join(technical_skills) if isinstance(technical_skills, list) else technical_skills
    tools = ", ".join(tools) if isinstance(tools, list) else tools
    status = ", ".join(status) if isinstance(status, list) else status
    languages = ", ".join(languages) if isinstance(languages, list) else languages

    params = (
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
        int(report_done),
        int(added_to_portfolio),
        int(has_showcase),
        notes,
        project_id
    )
    run_query(UPDATE_PROJECTS_SQL, params)

def delete_project(project_id):
    run_query(DELETE_PROJECTS_SQL, (project_id,))
