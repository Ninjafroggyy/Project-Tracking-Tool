# backend/export_logic.py
import pandas as pd
from backend.project_logic import get_all_projects
from backend.mini_logic import get_all_mini_projects
from backend.tag_logic import get_all_tags

def export_to_excel(filepath):
    projects_df = pd.DataFrame(get_all_projects())
    mini_df = pd.DataFrame(get_all_mini_projects())
    tags_df = pd.DataFrame(get_all_tags())

    with pd.ExcelWriter(filepath) as writer:
        projects_df.to_excel(writer, sheet_name="Projects", index=False)
        mini_df.to_excel(writer, sheet_name="Mini Projects", index=False)
        tags_df.to_excel(writer, sheet_name="Tags", index=False)
