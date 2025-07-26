# gui/view_edit.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.project_logic import get_all_projects, update_project, delete_project
from gui.tag_selector import open_tag_selector

class EditProjectWindow:
    def __init__(self, root, project_data):
        self.root = root
        self.root.title("Edit Project")
        self.root.configure(bg="#1e1e1e")
        self.root.geometry("1000x750")
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
            has_showcase,
            notes
        ) = project_data

        category = category.split(", ") if category else []
        project_type = project_type.split(", ") if project_type else []
        creative_skills = creative_skills.split(", ") if creative_skills else []
        technical_skills = technical_skills.split(", ") if technical_skills else []
        tools = tools.split(", ") if tools else []
        status = status.split(", ") if status else []
        languages = languages.split(", ") if languages else []

        top_frame = tk.Frame(self.root, bg="#1e1e1e")
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Project Title:", fg="white", bg="#1e1e1e").grid(row=0, column=0, sticky='e', padx=5)
        self.title_entry = tk.Entry(top_frame, width=60)
        self.title_entry.grid(row=0, column=1, pady=5)
        self.title_entry.insert(0, title)

        tk.Label(top_frame, text="Collaborators:", fg="white", bg="#1e1e1e").grid(row=1, column=0, sticky='e', padx=5)
        self.collab_entry = tk.Entry(top_frame, width=60)
        self.collab_entry.grid(row=1, column=1, pady=5)
        self.collab_entry.insert(0, collaborators)

        tk.Label(top_frame, text="Duration (hrs/days):", fg="white", bg="#1e1e1e").grid(row=2, column=0, sticky='e', padx=5)
        self.duration_entry = tk.Entry(top_frame, width=60)
        self.duration_entry.grid(row=2, column=1, pady=5)
        self.duration_entry.insert(0, duration)

        tag_frame = tk.Frame(self.root, bg="#1e1e1e")
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

        for i, (tag_type, value_list) in enumerate(tag_data.items()):
            col = i % 2
            row = i // 2
            frame = tk.Frame(tag_frame, bg="#1e1e1e")
            frame.grid(row=row, column=col, padx=20, pady=10, sticky='w')

            tk.Label(frame, text=f"{tag_type.replace('_', ' ').title()}:", fg="white", bg="#1e1e1e").pack(anchor='w')
            entry = tk.Entry(frame, width=40)
            entry.pack(anchor='w')
            entry.insert(0, ", ".join(value_list))
            entry.bind("<Button-1>", lambda e, t=tag_type, ent=entry: open_tag_selector(self.root, t, ent))
            self.tag_inputs[tag_type] = entry

        boolean_frame = tk.Frame(self.root, bg="#1e1e1e")
        boolean_frame.pack(pady=10)

        self.report_var = tk.BooleanVar(value=(int(report_done) == 1))
        self.portfolio_var = tk.BooleanVar(value=(int(added_to_portfolio) == 1))
        self.showcase_var = tk.BooleanVar(value=(int(has_showcase) == 1))

        tk.Checkbutton(boolean_frame, text="Technical/Professional Report Done", variable=self.report_var, fg="white", bg="#1e1e1e", selectcolor="#3e3e3e").pack(anchor='w')
        tk.Checkbutton(boolean_frame, text="Added to Portfolio", variable=self.portfolio_var, fg="white", bg="#1e1e1e", selectcolor="#3e3e3e").pack(anchor='w')
        tk.Checkbutton(boolean_frame, text="Has Showcase Material", variable=self.showcase_var, fg="white", bg="#1e1e1e", selectcolor="#3e3e3e").pack(anchor='w')

        notes_frame = tk.Frame(self.root, bg="#1e1e1e")
        notes_frame.pack(pady=10)

        tk.Label(notes_frame, text="Notes:", fg="white", bg="#1e1e1e").pack(anchor='w')
        self.notes_text = tk.Text(notes_frame, width=80, height=4)
        self.notes_text.pack()
        self.notes_text.insert("1.0", notes)

        button_frame = tk.Frame(self.root, bg="#1e1e1e")
        button_frame.pack(pady=20)

        save_btn = tk.Button(button_frame, text="Save Changes", command=self.save_changes, bg="#3e3e3e", fg="white", width=20)
        save_btn.grid(row=0, column=0, padx=10)

        cancel_btn = tk.Button(button_frame, text="Cancel", command=self.cancel_edit, bg="#3e3e3e", fg="white", width=20)
        cancel_btn.grid(row=0, column=1, padx=10)

        delete_btn = tk.Button(button_frame, text="Delete Project", command=self.delete_project, bg="#882222", fg="white", width=20)
        delete_btn.grid(row=0, column=2, padx=10)

    def save_changes(self):
        from gui.menu import main
        selected_tags = {}
        for tag_type, entry in self.tag_inputs.items():
            tags = entry.get()
            selected_tags[tag_type] = ', '.join([t.strip() for t in tags.split(',') if t.strip()])

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
            report_done=self.report_var.get(),
            added_to_portfolio=self.portfolio_var.get(),
            has_showcase=self.showcase_var.get(),
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
        confirm = messagebox.askyesno("Delete Project", "Are you sure you want to delete this project?")
        if confirm:
            delete_project(self.project_id)
            messagebox.showinfo("Deleted", "Project deleted successfully.")
            self.root.destroy()
            main()

def launch_edit_project(root, project_data):
    root.destroy()
    new_root = tk.Tk()
    EditProjectWindow(new_root, project_data)
    new_root.mainloop()
