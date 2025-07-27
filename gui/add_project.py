# gui/add_project.py — Refactored Add Project Window
import tkinter as tk
from tkinter import messagebox
from backend.project_logic import add_project
from gui.tag_selector import open_tag_selector
from gui.tag_manager import launch_tag_manager
from gui.common import create_themed_window, style_button

def launch_add_project(prev_root):
    prev_root.destroy()
    root = create_themed_window("Add New Project")
    AddProjectWindow(root)
    root.mainloop()

class AddProjectWindow:
    def __init__(self, root):
        self.root = root

        top = tk.Frame(root, bg="#1e1e1e")
        top.pack(pady=10)

        self.title_entry = self._labeled_entry(top, "Project Title:", 0)
        self.collab_entry = self._labeled_entry(top, "Collaborators:", 1)
        self.duration_entry = self._labeled_entry(top, "Duration (hrs/days):", 2)

        tk.Label(top, text="Notes:", fg="white", bg="#1e1e1e").grid(row=3, column=0, sticky='ne', padx=5)
        self.notes_text = tk.Text(top, width=60, height=4)
        self.notes_text.grid(row=3, column=1, pady=5)

        self.tag_inputs = {}
        tag_frame = tk.Frame(root, bg="#1e1e1e")
        tag_frame.pack(pady=10)
        tag_types = ["language", "creative_skill", "technical_skill", "tool", "type", "category", "status"]

        for i, tag_type in enumerate(tag_types):
            col, row = i % 2, i // 2
            frame = tk.Frame(tag_frame, bg="#1e1e1e")
            frame.grid(row=row, column=col, padx=20, pady=10, sticky='w')

            tk.Label(frame, text=f"{tag_type.replace('_', ' ').title()}:", fg="white", bg="#1e1e1e").pack(anchor='w')
            entry = tk.Entry(frame, width=40)
            entry.pack(anchor='w')
            entry.bind("<Button-1>", lambda e, t=tag_type, ent=entry: open_tag_selector(self.root, t, ent))
            self.tag_inputs[tag_type] = entry

            link = tk.Button(frame, text="Create new tag", bg="#1e1e1e", fg="#00afff", relief="flat", cursor="hand2",
                             command=lambda: launch_tag_manager(self.root))
            link.pack(anchor='w')

        self.report_var = tk.BooleanVar()
        self.portfolio_var = tk.BooleanVar()
        self.showcase_var = tk.BooleanVar()

        bools = tk.Frame(root, bg="#1e1e1e")
        bools.pack(pady=10)
        for label, var in [
            ("Technical/Professional Report Done", self.report_var),
            ("Added to Portfolio", self.portfolio_var),
            ("Has Showcase Material", self.showcase_var)
        ]:
            tk.Checkbutton(bools, text=label, variable=var, fg="white", bg="#1e1e1e", selectcolor="#3e3e3e").pack(anchor='w')

        tk.Button(root, text="Submit Project", command=self.submit, bg="#3e3e3e", fg="white", width=30).pack(pady=10)
        tk.Button(root, text="Back to Menu", command=self.go_back, bg="#3e3e3e", fg="white", width=30).pack()

    def _labeled_entry(self, parent, label, row):
        tk.Label(parent, text=label, fg="white", bg="#1e1e1e").grid(row=row, column=0, sticky='e', padx=5)
        entry = tk.Entry(parent, width=60)
        entry.grid(row=row, column=1, pady=5)
        return entry

    def go_back(self):
        from gui.menu import main
        self.root.destroy()
        main()

    def submit(self):
        from gui.menu import main

        title = self.title_entry.get().strip()
        collab = self.collab_entry.get().strip()
        duration = self.duration_entry.get().strip()
        notes = self.notes_text.get("1.0", tk.END).strip()

        if not title:
            messagebox.showerror("Input Error", "Project Title is required.")
            return

        selected_tags = {
            tag: ', '.join([t.strip() for t in entry.get().split(',') if t.strip()])
            for tag, entry in self.tag_inputs.items()
        }

        add_project(
            title=title,
            category=selected_tags["category"],
            project_type=selected_tags["type"],
            creative_skills=selected_tags["creative_skill"],
            technical_skills=selected_tags["technical_skill"],
            tools=selected_tags["tool"],
            status=selected_tags["status"],
            duration=duration,
            collaborators=collab,
            languages=selected_tags["language"],
            report_done=self.report_var.get(),
            added_to_portfolio=self.portfolio_var.get(),
            has_showcase_material=self.showcase_var.get(),
            notes=notes
        )

        messagebox.showinfo("Success", "Project added successfully!")
        self.root.destroy()
        main()
