# datalayer/sql_queries.py — Centralized SQL Strings

# --- Tags ---
TAG_EXISTS = "SELECT id FROM tags WHERE name = ?;"
DELETE_TAG = "DELETE FROM tags WHERE name = ? AND category = ?;"
INSERT_TAG = "INSERT INTO tags (name, category) VALUES (?, ?);"
SELECT_TAGS = "SELECT id, name, category FROM tags ORDER BY category, name;"
UPDATE_TAG = "UPDATE tags SET name = ? WHERE name = ? AND category = ?;"
TAGS_BY_TYPE = "SELECT id, name FROM tags WHERE category = ? ORDER BY name;"

# --- Projects ---
SELECT_PRO = "SELECT * FROM projects ORDER BY id DESC;"
DELETE_PRO = "DELETE FROM projects WHERE id = ?;"
SELECT_PROJECT_BY_ID = "SELECT * FROM projects WHERE id = ?"
INSERT_PRO = (
    "INSERT INTO projects ("
    "title, category, type, creative_skills, technical_skills, tools, "
    "status, duration, collaborators, languages, report_done, "
    "added_to_portfolio, has_showcase_material, notes) "
    "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);"
)
UPDATE_PRO = (
    "UPDATE projects SET "
    "title = ?, category = ?, type = ?, creative_skills = ?, technical_skills = ?, "
    "tools = ?, status = ?, duration = ?, collaborators = ?, languages = ?, "
    "report_done = ?, added_to_portfolio = ?, has_showcase_material = ?, notes = ? "
    "WHERE id = ?;"
)

# --- Mini Projects ---
INSERT_MINI = "INSERT INTO mini_projects (title, tags, summary) VALUES (?, ?, ?);"
SELECT_MINI = "SELECT * FROM mini_projects ORDER BY id DESC;"
