UPDATE projects
SET
    title = ?,
    category = ?,
    type = ?,
    creative_skills = ?,
    technical_skills = ?,
    tools = ?,
    status = ?,
    duration = ?,
    collaborators = ?,
    languages = ?,
    report_done = ?,
    added_to_portfolio = ?,
    has_showcase_material = ?,
    notes = ?
WHERE id = ?;
