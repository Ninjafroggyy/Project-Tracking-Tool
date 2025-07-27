import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from backend.project_logic import get_all_projects
from backend.mini_logic import get_all_mini_projects
from backend.tag_logic import get_all_tags

def export_to_excel(filepath: str) -> None:
    """Write Projects, Mini Projects, and Tags to an Excel file."""
    projects_df = pd.DataFrame(map(dict, get_all_projects()))
    mini_df     = pd.DataFrame(map(dict, get_all_mini_projects()))
    tags_df     = pd.DataFrame(map(dict, get_all_tags()))

    with pd.ExcelWriter(filepath) as writer:
        projects_df.to_excel(writer, sheet_name="Projects", index=False)
        mini_df.to_excel(writer,     sheet_name="Mini Projects", index=False)
        tags_df.to_excel(writer,     sheet_name="Tags",           index=False)

def export_to_excel_dialog(parent: tk.Widget) -> None:
    """
    Prompt the user for a path, run the export, and display success/error.
    """
    path = filedialog.asksaveasfilename(
        parent=parent,
        defaultextension=".xlsx",
        filetypes=[("Excel files","*.xlsx")],
        title="Export to Excel"
    )
    if not path:
        return  # user cancelled
    try:
        export_to_excel(path)
        messagebox.showinfo("Export", f"Exported data to:\n{path}", parent=parent)
    except Exception as e:
        messagebox.showerror("Export Error", str(e), parent=parent)
