# gui/screens/view_edit.py
import customtkinter as ctk
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR, GREY_COLOR
from backend.project_logic import get_all_projects, delete_project

class ViewEditScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="Projects Overview", font=(FONT_FAMILY,20), text_color=TEXT_COLOR).grid(row=0, column=0, columnspan=3, pady=(20,10))
        self.table = ctk.CTkTextbox(self, font=(FONT_FAMILY,12))
        self.table.grid(row=1, column=0, columnspan=3, sticky="nsew", padx=10, pady=5)
        self.grid_rowconfigure(1, weight=1)

        ctk.CTkButton(self, text="Refresh", fg_color=HIGHLIGHT_COLOR, hover_color=GREY_COLOR,
                      command=self._load_projects).grid(row=2, column=0, pady=10)
        ctk.CTkButton(self, text="Edit Selected", fg_color=HIGHLIGHT_COLOR, hover_color=GREY_COLOR,
                      command=self._edit_selected).grid(row=2, column=1, pady=10)
        ctk.CTkButton(self, text="Delete Selected", fg_color=HIGHLIGHT_COLOR, hover_color=GREY_COLOR,
                      command=self._delete_selected).grid(row=2, column=2, pady=10)

        self._load_projects()

    def _load_projects(self):
        projects = get_all_projects()
        self.table.delete("1.0", "end")
        for p in projects:
            # Use mapping access for sqlite3.Row
            self.table.insert("end", f"{p['id']}: {p['title']}\n")

    def _edit_selected(self):
        try:
            sel = self.table.get("sel.first", "sel.last").strip()
            proj_id = int(sel.split(":")[0])
        except Exception:
            ctk.CTkMessagebox(title="Error", message="Select a project to edit.")
            return
        setattr(self.controller, 'selected_project_id', proj_id)
        self.controller.show_frame("EditProjectScreen")

    def _delete_selected(self):
        try:
            sel = self.table.get("sel.first", "sel.last").strip()
            proj_id = int(sel.split(":")[0])
        except Exception:
            ctk.CTkMessagebox(title="Error", message="Select a project to delete.")
            return
        if ctk.CTkMessagebox(title="Confirm", message="Delete this project?"):
            try:
                delete_project(proj_id)
                self._load_projects()
                ctk.CTkMessagebox(title="Success", message="Project deleted.")
            except Exception as e:
                ctk.CTkMessagebox(title="Error", message=f"Deletion failed: {e}")