CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    category TEXT,
    type TEXT,
    creative_skills TEXT,
    technical_skills TEXT,
    tools TEXT,
    status TEXT,
    duration TEXT,
    collaborators TEXT,
    languages TEXT,
    report_done INTEGER DEFAULT 0,
    added_to_portfolio INTEGER DEFAULT 0,
    has_showcase_material INTEGER DEFAULT 0,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS mini_projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    tags TEXT,
    summary TEXT
);

CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    category TEXT CHECK(category IN (
        'language', 'creative_skill', 'technical_skill', 'tool', 'type', 'category', 'status'
    ))
);
