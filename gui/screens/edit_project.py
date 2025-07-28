# gui/screens/edit_project.py
import customtkinter as ctk
from tkinter import messagebox
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR, GREY_COLOR
from backend.project_logic import get_project_by_id, update_project, delete_project
from gui.utils.tag_selector import TagSelectorPanel

class EditProjectScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        self.selected_tags = {cat: [] for cat in [
            'category','type','status',
            'creative_skill','technical_skill','tool','language'
        ]}
        self._build_ui()

    def _build_ui(self):
        # — Title —
        ctk.CTkLabel(self, text="Edit Project", font=(FONT_FAMILY,24), text_color=TEXT_COLOR)\
           .grid(row=0, column=0, columnspan=3, pady=20)

        # — Title Entry —
        ctk.CTkLabel(self, text="Title:", font=(FONT_FAMILY,14), text_color=TEXT_COLOR)\
           .grid(row=1,column=0,sticky="e")
        self.title_entry = ctk.CTkEntry(self, font=(FONT_FAMILY,14))
        self.title_entry.grid(row=1,column=1,columnspan=2,sticky="ew",padx=5,pady=5)

        # — Tag selector buttons (category, type, status, etc.) —
        tag_cats = ['category','type','status','creative_skill','technical_skill','tool','language']
        for i,cat in enumerate(tag_cats, start=2):
            ctk.CTkButton(self,
                text=f"Select {cat.replace('_',' ').title()}",
                fg_color=HIGHLIGHT_COLOR,
                text_color="#000000",
                hover_color=GREY_COLOR,
                command=lambda c=cat: self._open_tag_selector(c)
            ).grid(row=i,column=0,columnspan=3,sticky="ew",padx=5,pady=3)

        # — Boolean checkboxes —
        self.report_var = ctk.BooleanVar()
        self.portfolio_var = ctk.BooleanVar()
        self.showcase_var = ctk.BooleanVar()
        ctk.CTkCheckBox(self, text="Report Done",       variable=self.report_var).grid(row=9,column=0)
        ctk.CTkCheckBox(self, text="Added to Portfolio",variable=self.portfolio_var).grid(row=9,column=1)
        ctk.CTkCheckBox(self, text="Has Showcase Material",variable=self.showcase_var).grid(row=9,column=2)

        # — Duration & Collaborators —
        ctk.CTkLabel(self, text="Duration:",      font=(FONT_FAMILY,14), text_color=TEXT_COLOR)\
           .grid(row=10,column=0,sticky="e")
        self.duration_entry = ctk.CTkEntry(self, font=(FONT_FAMILY,14))
        self.duration_entry.grid(row=10,column=1,sticky="ew",padx=5,pady=5)
        ctk.CTkLabel(self, text="Collaborators:", font=(FONT_FAMILY,14), text_color=TEXT_COLOR)\
           .grid(row=11,column=0,sticky="e")
        self.collab_entry = ctk.CTkEntry(self, font=(FONT_FAMILY,14))
        self.collab_entry.grid(row=11,column=1,sticky="ew",padx=5,pady=5)

        # — Notes —
        ctk.CTkLabel(self, text="Notes:", font=(FONT_FAMILY,14), text_color=TEXT_COLOR)\
           .grid(row=12,column=0,sticky="ne")
        self.notes_box = ctk.CTkTextbox(self, width=400, height=100)
        self.notes_box.grid(row=12,column=1,columnspan=2,sticky="ew",padx=5,pady=5)

        # — Action Buttons —
        btn_frame = ctk.CTkFrame(self, fg_color=CONTENT_BG)
        btn_frame.grid(row=13,column=0,columnspan=3,pady=20)
        ctk.CTkButton(btn_frame, text="Update", fg_color=HIGHLIGHT_COLOR,
            command=self._update_project).pack(side="left",padx=5)
        ctk.CTkButton(btn_frame, text="Cancel", fg_color=GREY_COLOR,
            command=lambda: self.controller.show_frame("ViewEditScreen")).pack(side="left",padx=5)
        ctk.CTkButton(btn_frame, text="Delete", fg_color="#ff5555",
            command=self._delete_current).pack(side="left",padx=5)

        self.grid_columnconfigure(1, weight=1)

    def _open_tag_selector(self, tag_type):
        initial = self.selected_tags.get(tag_type, [])
        panel = TagSelectorPanel(self, tag_type,
            on_submit=lambda tags: self.selected_tags.__setitem__(tag_type, tags),
            initial=initial)
        panel.grid(row=0,column=3,rowspan=14,sticky="nsew")
        self.grid_columnconfigure(3, weight=0)

    def load_project(self, project_id):
        self.project_id = project_id
        p = get_project_by_id(project_id)
        # populate each field:
        self.title_entry.delete(0,"end")
        self.title_entry.insert(0, p['title'])
        self.selected_tags = {
            'category':p['category'].split(',') if p['category'] else [],
            'type':    p['type'].split(',')     if p['type']     else [],
            'status':  p['status'].split(',')   if p['status']   else [],
            'creative_skill':p['creative_skills'].split(',') if p['creative_skills'] else [],
            'technical_skill':p['technical_skills'].split(',') if p['technical_skills'] else [],
            'tool':     p['tools'].split(',')   if p['tools']   else [],
            'language': p['languages'].split(',') if p['languages'] else []
        }
        self.report_var.set(bool(p['report_done']))
        self.portfolio_var.set(bool(p['added_to_portfolio']))
        self.showcase_var.set(bool(p['has_showcase_material']))
        self.duration_entry.delete(0,"end")
        self.duration_entry.insert(0, p['duration'] or "")
        self.collab_entry.delete(0,"end")
        self.collab_entry.insert(0, p['collaborators'] or "")
        self.notes_box.delete("1.0","end")
        self.notes_box.insert("1.0", p['notes'] or "")

    def _update_project(self):
        from tkinter import messagebox

        # Validate title (column is 'title')
        title = self.title_entry.get().strip()
        if not title:
            messagebox.showerror("Error", "Project title cannot be empty.")
            return

        # Build kwargs matching your database columns
        kwargs = {
            'title': title,
            'category': ','.join(self.selected_tags['category']),
            'project_type': ','.join(self.selected_tags['type']),
            'status': ','.join(self.selected_tags['status']),
            'creative_skills': ','.join(self.selected_tags['creative_skill']),
            'technical_skills': ','.join(self.selected_tags['technical_skill']),
            'tools': ','.join(self.selected_tags['tool']),
            'languages': ','.join(self.selected_tags['language']),
            'report_done': int(self.report_var.get()),
            'added_to_portfolio': int(self.portfolio_var.get()),
            'has_showcase_material': int(self.showcase_var.get()),
            'duration': self.duration_entry.get().strip(),
            'collaborators': self.collab_entry.get().strip(),
            'notes': self.notes_box.get("1.0", "end").strip()
        }

        try:
            # Pass self.project_id as the first positional arg, then all other fields
            update_project(self.project_id, **kwargs)
            messagebox.showinfo("Success", "Project updated.")
            self.controller.show_frame("ViewEditScreen")
        except Exception as e:
            messagebox.showerror("Error", f"Update failed: {e}")

    def _delete_current(self):
        if messagebox.askyesno("Confirm","Delete this project?"):
            delete_project(self.project_id)
            self.controller.show_frame("ViewEditScreen")
