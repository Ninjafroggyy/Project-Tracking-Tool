# gui/screens/view_edit.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR
from backend.project_logic import get_all_projects, delete_project

class ViewEditScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        # Ensure this frame uses only its own grid
        self.grid_columnconfigure(0, weight=1)
        self._build_ui()

    def _build_ui(self):
        # Header
        header = ctk.CTkLabel(self, text="Projects Overview", font=(FONT_FAMILY, 20), text_color=TEXT_COLOR)
        header.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Table
        cols = [
            "id", "title", "category", "type", "creative_skills",
            "technical_skills", "tools", "status", "duration",
            "collaborators", "languages", "report_done",
            "added_to_portfolio", "has_showcase_material", "notes"
        ]
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for col in cols:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=100, anchor="w")
        self.tree.grid(row=1, column=0, columnspan=3, sticky="nsew")

        # Scrollbars
        vsb = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        vsb.grid(row=1, column=3, sticky="ns")
        hsb = ttk.Scrollbar(self, orient="horizontal", command=self.tree.xview)
        hsb.grid(row=2, column=0, columnspan=3, sticky="ew")
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        # Buttons
        btn_frame = ctk.CTkFrame(self, fg_color=CONTENT_BG)
        btn_frame.grid(row=3, column=0, columnspan=3, pady=10, sticky="w")
        ctk.CTkButton(btn_frame, text="Refresh", fg_color=HIGHLIGHT_COLOR, command=self._load_projects).pack(
            side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Edit Selected", fg_color=HIGHLIGHT_COLOR, command=self._edit_selected).pack(
            side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Delete Selected", fg_color=HIGHLIGHT_COLOR, command=self._delete_selected).pack(
            side="left", padx=5)

        # Bind double-click to edit
        self.tree.bind("<Double-1>", lambda e: self._edit_selected())

        # Configure expansion
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)

        # Load data
        self._load_projects()

    def _load_projects(self):
        # Clear table
        for row in self.tree.get_children():
            self.tree.delete(row)
        # Populate
        for p in get_all_projects():
            self.tree.insert("", "end", values=[
                p['id'], p['title'], p['category'] or '', p['type'] or '',
                                     p['creative_skills'] or '', p['technical_skills'] or '',
                                     p['tools'] or '', p['status'] or '', p['duration'] or '',
                                     p['collaborators'] or '', p['languages'] or '', p['report_done'],
                p['added_to_portfolio'], p['has_showcase_material'], p['notes'] or ''
            ])

    def _get_selected_id(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showerror("Error", "Please select a project first.")
            return None
        return self.tree.item(sel[0])['values'][0]

    def _edit_selected(self):
        proj_id = self._get_selected_id()
        if proj_id is None: return
        self.controller.selected_project_id = proj_id
        self.controller.show_frame("EditProjectScreen")

    def _delete_selected(self):
        proj_id = self._get_selected_id()
        if proj_id and messagebox.askyesno("Confirm", "Delete this project?"):
            delete_project(proj_id)
            self._load_projects()

    def _on_double_click(self, event):
        self.tree.bind("<Double-1>", lambda e: self._edit_selected())
