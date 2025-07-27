# gui/edit_project.py — Refactored Edit Project Window
import tkinter as tk
from tkinter import messagebox
from backend.project_logic import update_project, delete_project
from gui.tag_selector import open_tag_selector
from gui.common import create_themed_window, style_button

def launch_edit_project(prev_window, project_data):
    prev_window.destroy()
    root = create_themed_window("Edit Project")
    EditProjectWindow(root, project_data)
    root.mainloop()

class EditProjectWindow:
    def __init__(self, root, project_data):
        self.root = root
        (
            self.project_id,
            title,
            category,
            project_type,
            creative_skills,
            technical_skills,
            tools,
            status,
            duration,
            collaborators,
            languages,
            report_done,
            added_to_portfolio,
            has_showcase_material,
            notes
        ) = project_data

        category = category.split(", ") if category else []
        project_type = project_type.split(", ") if project_type else []
        creative_skills = creative_skills.split(", ") if creative_skills else []
        technical_skills = technical_skills.split(", ") if technical_skills else []
        tools = tools.split(", ") if tools else []
        status = status.split(", ") if status else []
        languages = languages.split(", ") if languages else []

        top = tk.Frame(root, bg="#1e1e1e")
        top.pack(pady=10)

        self.title_entry = self._labeled_entry(top, "Project Title:", 0, title)
        self.collab_entry = self._labeled_entry(top, "Collaborators:", 1, collaborators)
        self.duration_entry = self._labeled_entry(top, "Duration (hrs/days):", 2, duration)

        tag_frame = tk.Frame(root, bg="#1e1e1e")
        tag_frame.pack(pady=10)

        self.tag_inputs = {}
        tag_data = {
            "language": languages,
            "creative_skill": creative_skills,
            "technical_skill": technical_skills,
            "tool": tools,
            "type": project_type,
            "category": category,
            "status": status
        }

        for i, (tag_type, values) in enumerate(tag_data.items()):
            col, row = i % 2, i // 2
            frame = tk.Frame(tag_frame, bg="#1e1e1e")
            frame.grid(row=row, column=col, padx=20, pady=10, sticky='w')

            tk.Label(frame, text=f"{tag_type.replace('_', ' ').title()}:", fg="white", bg="#1e1e1e").pack(anchor='w')
            entry = tk.Entry(frame, width=40)
            entry.insert(0, ", ".join(values))
            entry.pack(anchor='w')
            entry.bind("<Button-1>", lambda e, t=tag_type, ent=entry: open_tag_selector(self.root, t, ent))
            entry.config(state='readonly')
            self.tag_inputs[tag_type] = entry

        self.report_var = tk.IntVar(value=int(report_done or 0))
        self.portfolio_var = tk.IntVar(value=int(added_to_portfolio or 0))
        self.showcase_var = tk.IntVar(value=int(has_showcase_material or 0))

        bools = tk.Frame(root, bg="#1e1e1e")
        bools.pack(pady=10)
        for label, var in [
            ("Technical/Professional Report Done", self.report_var),
            ("Added to Portfolio", self.portfolio_var),
            ("Has Showcase Material", self.showcase_var)
        ]:
            # Create checkbox with explicit toggle command to ensure var updates
            cb = tk.Checkbutton(
                bools,
                text=label,
                variable=var,
                command=lambda v=var: v.set(1 - v.get()),
                fg="white",
                bg="#1e1e1e",
                selectcolor="#3e3e3e"
            )
            # Pre-select if the flag is true
            if var.get():
                cb.select()
            cb.pack(anchor='w')

        self.notes_text = self._labeled_text(root, "Notes:", notes)

        buttons = tk.Frame(root, bg="#1e1e1e")
        buttons.pack(pady=20)

        self._action_button(buttons, "Save Changes", self.save_changes, 0)
        self._action_button(buttons, "Cancel", self.cancel_edit, 1)
        self._action_button(buttons, "Delete Project", self.delete_project, 2, bg="#882222")

    def _labeled_entry(self, parent, label, row, default=""):
        tk.Label(parent, text=label, fg="white", bg="#1e1e1e").grid(row=row, column=0, sticky='e', padx=5)
        entry = tk.Entry(parent, width=60)
        entry.grid(row=row, column=1, pady=5)
        entry.insert(0, default)
        return entry

    def _labeled_text(self, parent, label, content=""):
        frame = tk.Frame(parent, bg="#1e1e1e")
        frame.pack(pady=10)
        tk.Label(frame, text=label, fg="white", bg="#1e1e1e").pack(anchor='w')
        text = tk.Text(frame, width=80, height=4)
        text.insert("1.0", content)
        text.pack()
        return text

    def _action_button(self, parent, label, command, col, bg="#3e3e3e"):
        btn = tk.Button(parent, text=label, command=command, bg=bg, fg="white", width=20)
        btn.grid(row=0, column=col, padx=10)

    def save_changes(self):
        from gui.menu import main
        selected_tags = {
            tag: ', '.join([t.strip() for t in entry.get().split(',') if t.strip()])
            for tag, entry in self.tag_inputs.items()
        }

        update_project(
            project_id=self.project_id,
            title=self.title_entry.get(),
            category=selected_tags["category"],
            project_type=selected_tags["type"],
            creative_skills=selected_tags["creative_skill"],
            technical_skills=selected_tags["technical_skill"],
            tools=selected_tags["tool"],
            status=selected_tags["status"],
            duration=self.duration_entry.get(),
            collaborators=self.collab_entry.get(),
            languages=selected_tags["language"],
            report_done=int(self.report_var.get()),
            added_to_portfolio=int(self.portfolio_var.get()),
            has_showcase_material=int(self.showcase_var.get()),
            notes=self.notes_text.get("1.0", tk.END).strip()
        )

        messagebox.showinfo("Success", "Project updated successfully!")
        self.root.destroy()
        main()

    def cancel_edit(self):
        from gui.menu import main
        self.root.destroy()
        main()

    def delete_project(self):
        from gui.menu import main
        if messagebox.askyesno("Delete Project", "Are you sure you want to delete this project?"):
            delete_project(self.project_id)
            messagebox.showinfo("Deleted", "Project deleted successfully.")
            self.root.destroy()
            main()