# gui/screens/edit_project.py
import customtkinter as ctk
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR, GREY_COLOR
from backend.project_logic import get_project_by_id, update_project

class EditProjectScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        self.project_id = None
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Edit Project", font=(FONT_FAMILY, 20), text_color=TEXT_COLOR
        )
        title.grid(row=0, column=0, columnspan=2, pady=(20,10))

        # Project Name
        name_label = ctk.CTkLabel(
            self, text="Project Name:", font=(FONT_FAMILY, 14), text_color=TEXT_COLOR
        )
        name_label.grid(row=1, column=0, sticky="e", padx=10, pady=5)
        self.name_entry = ctk.CTkEntry(self, font=(FONT_FAMILY,14))
        self.name_entry.grid(row=1, column=1, sticky="ew", padx=10, pady=5)

        # Save Button
        save_btn = ctk.CTkButton(
            self, text="Update", fg_color=HIGHLIGHT_COLOR,
            hover_color=GREY_COLOR, command=self._update_project
        )
        save_btn.grid(row=2, column=0, columnspan=2, pady=20)

        self.grid_columnconfigure(1, weight=1)

    def load_project(self, project_id):
        """Called by controller when navigating to this screen."""
        self.project_id = project_id
        proj = get_project_by_id(project_id)
        self.name_entry.delete(0, "end")
        self.name_entry.insert(0, proj.name)

    def _update_project(self):
        name = self.name_entry.get().strip()
        if not name:
            ctk.CTkMessagebox(title="Error", message="Project name cannot be empty.")
            return
        try:
            update_project(self.project_id, name=name)
            ctk.CTkMessagebox(title="Success", message="Project updated.")
            self.controller.show_frame("ViewEditScreen")
        except Exception as e:
            ctk.CTkMessagebox(title="Error", message=f"Update failed: {e}")