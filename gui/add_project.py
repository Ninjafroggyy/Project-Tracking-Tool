# gui/add_project.py
import tkinter as tk
from tkinter import messagebox
from backend.project_logic import add_project
from backend.tag_logic import get_tags_by_type
from gui.tag_selector import open_tag_selector
from gui.tag_manager import launch_tag_manager

class AddProjectWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Add New Project")
        self.root.configure(bg="#1e1e1e")
        self.root.geometry("1000x750")

        # --- Top Info Section ---
        top_frame = tk.Frame(self.root, bg="#1e1e1e")
        top_frame.pack(pady=10)

        tk.Label(top_frame, text="Project Title:", fg="white", bg="#1e1e1e").grid(row=0, column=0, sticky='e', padx=5)
        self.title_entry = tk.Entry(top_frame, width=60)
        self.title_entry.grid(row=0, column=1, pady=5)

        tk.Label(top_frame, text="Collaborators:", fg="white", bg="#1e1e1e").grid(row=1, column=0, sticky='e', padx=5)
        self.collab_entry = tk.Entry(top_frame, width=60)
        self.collab_entry.grid(row=1, column=1, pady=5)

        tk.Label(top_frame, text="Duration (hrs/days):", fg="white", bg="#1e1e1e").grid(row=2, column=0, sticky='e', padx=5)
        self.duration_entry = tk.Entry(top_frame, width=60)
        self.duration_entry.grid(row=2, column=1, pady=5)

        tk.Label(top_frame, text="Notes:", fg="white", bg="#1e1e1e").grid(row=3, column=0, sticky='ne', padx=5)
        self.notes_text = tk.Text(top_frame, width=60, height=4)
        self.notes_text.grid(row=3, column=1, pady=5)

        # --- Tag Selector Fields ---
        tag_frame = tk.Frame(self.root, bg="#1e1e1e")
        tag_frame.pack(pady=10)

        self.tag_inputs = {}
        tag_types = ["language", "creative_skill", "technical_skill", "tool", "type", "category", "status"]

        for i, tag_type in enumerate(tag_types):
            col = i % 2
            row = i // 2

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

        # --- Boolean Options ---
        boolean_frame = tk.Frame(self.root, bg="#1e1e1e")
        boolean_frame.pack(pady=10)

        self.report_var = tk.BooleanVar()
        self.portfolio_var = tk.BooleanVar()
        self.showcase_var = tk.BooleanVar()

        tk.Checkbutton(boolean_frame, text="Technical/Professional Report Done", variable=self.report_var, fg="white", bg="#1e1e1e", selectcolor="#3e3e3e").pack(anchor='w')
        tk.Checkbutton(boolean_frame, text="Added to Portfolio", variable=self.portfolio_var, fg="white", bg="#1e1e1e", selectcolor="#3e3e3e").pack(anchor='w')
        tk.Checkbutton(boolean_frame, text="Has Showcase Material", variable=self.showcase_var, fg="white", bg="#1e1e1e", selectcolor="#3e3e3e").pack(anchor='w')

        # --- Submit Button ---
        submit_btn = tk.Button(self.root, text="Submit Project", command=self.submit, bg="#3e3e3e", fg="white", width=30)
        submit_btn.pack(pady=10)

        # --- Cancel Button ---
        cancel_btn = tk.Button(self.root, text="Back to Menu", command=self.go_back, bg="#3e3e3e", fg="white", width=30)
        cancel_btn.pack()

    def go_back(self):
        from gui.menu import main
        self.root.destroy()
        main()

    def submit(self):
        title = self.title_entry.get()
        collab = self.collab_entry.get()
        notes = self.notes_text.get("1.0", tk.END).strip()
        duration = self.duration_entry.get()

        if not title:
            messagebox.showerror("Input Error", "Project Title is required.")
            return

        selected_tags = {}
        for tag_type, entry in self.tag_inputs.items():
            tags = entry.get()
            selected_tags[tag_type] = ', '.join([t.strip() for t in tags.split(',') if t.strip()])

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
            has_showcase=self.showcase_var.get(),
            notes=notes
        )

        messagebox.showinfo("Success", "Project added successfully!")
        self.root.destroy()
        from gui.menu import main
        main()

def launch_add_project(root):
    root.destroy()
    new_root = tk.Tk()
    app = AddProjectWindow(new_root)
    new_root.mainloop()