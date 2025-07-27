import customtkinter as ctk
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR, GREY_COLOR
from backend.project_logic import add_project
from gui.utils.tag_selector import TagSelectorPanel

class AddProjectScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        self.selected_tags = {cat: [] for cat in [
            'category','type','status','creative_skill',
            'technical_skill','tool','language'
        ]}
        self._build_ui()

    def _build_ui(self):
        # Title Label and Entry
        ctk.CTkLabel(self, text="Add New Project", font=(FONT_FAMILY,24), text_color=TEXT_COLOR)
        ctk.CTkLabel(self, text="Title:", font=(FONT_FAMILY,14), text_color=TEXT_COLOR).grid(row=1, column=0, sticky="e")
        self.title_entry = ctk.CTkEntry(self, font=(FONT_FAMILY,14))
        self.title_entry.grid(row=1, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # Tag selectors
        tag_cats = [
            'category','type','status','creative_skill',
            'technical_skill','tool','language'
        ]
        for i, cat in enumerate(tag_cats, start=2):
            btn = ctk.CTkButton(
                self,
                text=f"Select {cat.replace('_',' ').title()}",
                fg_color=HIGHLIGHT_COLOR,
                text_color="#000000",
                hover_color=GREY_COLOR,
                command=lambda tag_type=cat: self._open_tag_selector(tag_type)
            )
            btn.grid(row=i, column=0, columnspan=3, sticky="ew", padx=5, pady=3)

        # Boolean options
        self.report_var = ctk.BooleanVar()
        self.portfolio_var = ctk.BooleanVar()
        self.showcase_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self, text="Report Done", variable=self.report_var).grid(row=9, column=0)
        ctk.CTkCheckBox(self, text="Added to Portfolio", variable=self.portfolio_var).grid(row=9, column=1)
        ctk.CTkCheckBox(self, text="Has Showcase Material", variable=self.showcase_var).grid(row=9, column=2)

        # Duration and Collaborators
        ctk.CTkLabel(self, text="Duration:", font=(FONT_FAMILY,14), text_color=TEXT_COLOR).grid(row=10, column=0, sticky="e")
        self.duration_entry = ctk.CTkEntry(self, font=(FONT_FAMILY,14))
        self.duration_entry.grid(row=10, column=1, sticky="ew", padx=5, pady=5)
        ctk.CTkLabel(self, text="Collaborators:", font=(FONT_FAMILY,14), text_color=TEXT_COLOR).grid(row=11, column=0, sticky="e")
        self.collab_entry = ctk.CTkEntry(self, font=(FONT_FAMILY,14))
        self.collab_entry.grid(row=11, column=1, sticky="ew", padx=5, pady=5)

        # Notes
        ctk.CTkLabel(self, text="Notes:", font=(FONT_FAMILY,14), text_color=TEXT_COLOR).grid(row=12, column=0, sticky="ne")
        self.notes_box = ctk.CTkTextbox(self, width=400, height=100)
        self.notes_box.grid(row=12, column=1, columnspan=2, sticky="ew", padx=5, pady=5)

        # Save Button
        ctk.CTkButton(
            self,
            text="Save Project",
            fg_color=HIGHLIGHT_COLOR,
            text_color="#000000",
            hover_color=GREY_COLOR,
            command=self._save_project
        ).grid(row=13, column=0, columnspan=3, pady=15)

        self.grid_columnconfigure(1, weight=1)

    def _open_tag_selector(self, tag_type):
        # Remove existing panel if present
        if hasattr(self, 'tag_panel') and self.tag_panel is not None:
            self.tag_panel.hide()

        # Create or re-show panel with initial selections
        initial = self.selected_tags.get(tag_type, [])
        self.tag_panel = TagSelectorPanel(
            parent=self,
            tag_type=tag_type,
            on_submit=lambda tags: self._set_tags(tag_type, tags),
            initial=initial
        )
        # Place panel in right-hand column
        self.tag_panel.grid(row=0, column=3, rowspan=99, sticky="nsew")
        self.grid_columnconfigure(3, weight=0)

    def _set_tags(self, tag_type, tags):
        self.selected_tags[tag_type] = tags

    def _save_project(self):
        title = self.title_entry.get().strip()
        if not title:
            ctk.CTkMessagebox(title="Error", message="Title is required.")
            return
        data = {
            'title': title,
            'category': None, 'type': None, 'status': None,
            'creative_skills': ','.join(self.selected_tags['creative_skill']),
            'technical_skills': ','.join(self.selected_tags['technical_skill']),
            'tools': ','.join(self.selected_tags['tool']),
            'languages': ','.join(self.selected_tags['language']),
            'report_done': int(self.report_var.get()),
            'added_to_portfolio': int(self.portfolio_var.get()),
            'has_showcase_material': int(self.showcase_var.get()),
            'duration': self.duration_entry.get().strip(),
            'collaborators': self.collab_entry.get().strip(),
            'notes': self.notes_box.get("1.0","end").strip()
        }
        try:
            add_project(**data)
            ctk.CTkMessagebox(title="Success", message="Project saved.")
            self.controller.show_frame("ViewEditScreen")
        except Exception as e:
            ctk.CTkMessagebox(title="Error", message=f"Save failed: {e}")