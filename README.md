# Project Tracking Tool

A desktop application built with Python and Tkinter for managing projects, mini-projects, and tags, backed by an SQLite database and featuring export-to-Excel functionality.

## Features

- **Project Management**: Create, edit, delete projects with metadata (skills, tools, status, dates, collaborators).
- **Mini-Project Tracking**: Manage smaller tasks or sub-projects.
- **Tag System**: Organize projects and mini-projects by custom tags.
- **Export**: Generate an Excel workbook with separate sheets for Projects, Mini Projects, and Tags.
- **Unit Testing**: Comprehensive pytest suites for backend logic, database layer, export logic, and tag selector helpers.

## Installation

```bash
# Clone the repository
git clone https://github.com/Ninjafroggyy/Project-Tracking-Tool.git
cd project-tracking-tool

# Create and activate a virtual environment
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

By default, the SQLite database will be created at the path specified in `config.py`. You can modify `DB_PATH` and `SCHEMA_PATH` there as needed.

## Usage

```bash
# Initialize the database (creates schema if missing)
python -m datalayer.db_handler

# Launch the application
python main.py
```

- **View Projects**: Double-click a project entry to open the edit dialog.
- **Add/Edit Projects**: Fill fields, toggle checkboxes, select tags via pop-up.
- **Manage Tags**: Create, rename, delete tags by category.
- **Export**: Use the "Export to Excel" option in the menu to generate reports.

## Project Structure

```
project_tracker/
├── main.py
├── config.py
├── gui/            # Tkinter GUI modules
├── backend/        # Business logic
├── datalayer/      # Database handlers and SQL definitions
├── data/           # SQLite database file
├── tests/          # pytest test suites
├── README.md       # Project overview
└── requirements.txt
```

## Running Tests

```bash
pytest --maxfail=1 --disable-warnings -q
```