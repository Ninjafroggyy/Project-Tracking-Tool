import customtkinter as ctk
from tkinter import messagebox
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR, GREY_COLOR
from backend.project_logic import add_project
from gui.utils.tag_selector import TagSelectorPanel

class AddProjectScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        # initialize selected tags for all categories
        self.selected_tags = {cat: [] for cat in [
            'category', 'type', 'status',
            'creative_skill', 'technical_skill',
            'tool', 'language'
        ]}
        self._build_ui()

    def _build_ui(self):
        # Title
        ctk.CTkLabel(self, text="Add New Project", font=(FONT_FAMILY, 24), text_color=TEXT_COLOR).grid(row=0, column=0, columnspan=3, pady=20)
        ctk.CTkLabel(self, text="Title:", font=(FONT_FAMILY, 14), text_color=TEXT_COLOR).grid(row=1, column=0, sticky="e")
        self.title_entry = ctk.CTkEntry(self, font=(FONT_FAMILY, 14))
        self.title_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # Tag selector buttons
        tag_cats = ['category', 'type', 'status', 'creative_skill', 'technical_skill', 'tool', 'language']
        for idx, cat in enumerate(tag_cats, start=2):
            btn = ctk.CTkButton(
                self,
                text=f"Select {cat.replace('_', ' ').title()}",
                fg_color=HIGHLIGHT_COLOR,
                text_color="#000000",
                hover_color=GREY_COLOR,
                command=lambda c=cat: self._open_tag_selector(c)
            )
            btn.grid(row=idx, column=0, columnspan=3, sticky="ew", padx=5, pady=3)

        # Boolean checkboxes
        self.report_var = ctk.BooleanVar()
        self.portfolio_var = ctk.BooleanVar()
        self.showcase_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self, text="Report Done", variable=self.report_var).grid(row=9, column=0)
        ctk.CTkCheckBox(self, text="Added to Portfolio", variable=self.portfolio_var).grid(row=9, column=1)
        ctk.CTkCheckBox(self, text="Has Showcase Material", variable=self.showcase_var).grid(row=9, column=2)

        # Duration and Collaborators
        ctk.CTkLabel(self, text="Duration:", font=(FONT_FAMILY, 14), text_color=TEXT_COLOR).grid(row=10, column=0, sticky="e")
        self.duration_entry = ctk.CTkEntry(self, font=(FONT_FAMILY, 14))
        self.duration_entry.grid(row=10, column=1, sticky="ew", padx=5, pady=5)
        ctk.CTkLabel(self, text="Collaborators:", font=(FONT_FAMILY, 14), text_color=TEXT_COLOR).grid(row=11, column=0, sticky="e")
        self.collab_entry = ctk.CTkEntry(self, font=(FONT_FAMILY, 14))
        self.collab_entry.grid(row=11, column=1, sticky="ew", padx=5, pady=5)

        # Notes
        ctk.CTkLabel(self, text="Notes:", font=(FONT_FAMILY, 14), text_color=TEXT_COLOR).grid(row=12, column=0, sticky="ne")
        self.notes_box = ctk.CTkTextbox(self, width=400, height=100)
        self.notes_box.grid(row=12, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # Save button
        ctk.CTkButton(
            self,
            text="Save Project",
            fg_color=HIGHLIGHT_COLOR,
            text_color="#000000",
            hover_color=GREY_COLOR,
            command=self._save_project
        ).grid(row=13, column=0, columnspan=3, pady=20)

        self.grid_columnconfigure(1, weight=1)

    def _open_tag_selector(self, tag_type):
        # create an inline panel for selecting tags
        initial = self.selected_tags.get(tag_type, [])
        self.tag_panel = TagSelectorPanel(
            self, tag_type,
            on_submit=lambda tags: self._set_tags(tag_type, tags),
            initial=initial
        )
        self.tag_panel.grid(row=0, column=3, rowspan=99, sticky="nsew")
        self.grid_columnconfigure(3, weight=0)

    def _set_tags(self, tag_type, tags):
        self.selected_tags[tag_type] = tags

    def _save_project(self):
        from tkinter import messagebox
        # Gather inputs
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Title is required.")
            return
        data = {
            'title': title,
            'category': ','.join(self.selected_tags['category']),
            'project_type': ','.join(self.selected_tags['type']),
            'creative_skills': ','.join(self.selected_tags['creative_skill']),
            'technical_skills': ','.join(self.selected_tags['technical_skill']),
            'tools': ','.join(self.selected_tags['tool']),
            'status': ','.join(self.selected_tags['status']),
            'duration': self.duration_entry.get().strip(),
            'collaborators': self.collab_entry.get().strip(),
            'languages': ','.join(self.selected_tags['language']),
            'report_done': int(self.report_var.get()),
            'added_to_portfolio': int(self.portfolio_var.get()),
            'has_showcase_material': int(self.showcase_var.get()),
            'notes': self.notes_box.get("1.0", "end").strip()
        }
        try:
            add_project(**data)
            messagebox.showinfo("Success", "Project saved.")
            self.controller.show_frame("ViewEditScreen")
        except Exception as e:
            messagebox.showerror("Error", f"Save failed: {e}")