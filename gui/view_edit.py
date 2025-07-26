# gui/view_edit.py — Refactored View/Edit Project Table
import tkinter as tk
from tkinter import ttk, messagebox
from backend.project_logic import get_all_projects
from gui.edit_project import launch_edit_project
from gui.common import create_themed_window, style_button

def launch_view_edit(previous_root):
    previous_root.withdraw()
    root = create_themed_window("View/Edit Projects")

    frame = tk.Frame(root, bg="#1e1e1e")
    frame.pack(fill='both', expand=True, padx=10, pady=10)

    columns = (
        "ID", "Title", "Category", "Type", "Creative Skills", "Technical Skills", "Tools",
        "Status", "Duration", "Collaborators", "Languages",
        "Report", "Portfolio", "Showcase", "Notes"
    )

    tree = ttk.Treeview(frame, columns=columns, show='headings')

    # Set up column headings and widths
    headings = [
        ("ID", 30), ("Title", 150), ("Category", 100), ("Type", 100),
        ("Creative Skills", 150), ("Technical Skills", 150), ("Tools", 120),
        ("Status", 80), ("Duration", 80), ("Collaborators", 120),
        ("Languages", 120), ("Report", 80), ("Portfolio", 80), ("Showcase", 80),
        ("Notes", 200)
    ]
    for col, width in headings:
        tree.heading(col, text=col)
        tree.column(col, width=width, anchor='w')

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    hsb = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
    tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

    tree.grid(row=0, column=0, sticky='nsew')
    vsb.grid(row=0, column=1, sticky='ns')
    hsb.grid(row=1, column=0, sticky='ew')

    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Load project data
    projects = get_all_projects()
    # Convert boolean flags to human-readable
    for proj in projects:
        proj_list = list(proj)
        # Indices 11,12,13 correspond to Report, Portfolio, Showcase
        for idx in (11, 12, 13):
            try:
                proj_list[idx] = "Completed" if int(proj_list[idx]) == 1 else "Incomplete"
            except (ValueError, TypeError):
                proj_list[idx] = "Incomplete"
        tree.insert("", "end", values=tuple(proj_list))

    from backend.project_logic import get_project_by_id

    def on_double_click(event):
            item = tree.focus()
            if not item:
                return
            vals = tree.item(item, "values")
            if not vals:
                messagebox.showerror("Error", "No project selected")
                return
            proj_id = vals[0]
            try:
                project_data = get_project_by_id(proj_id)
            except Exception as e:
                messagebox.showerror("Error", f"Could not load project data: {e}")
                return
            if project_data and len(project_data) >= 15:
                launch_edit_project(root, project_data)
            else:
                messagebox.showerror("Error", "Incomplete project data")

    tree.bind("<Double-1>", on_double_click)

    back_btn = tk.Button(root, text="Back to Menu", command=lambda: go_back_to_menu(root))
    style_button(back_btn)
    back_btn.pack(pady=10)

def go_back_to_menu(window):
    from gui.menu import main
    window.destroy()
    main()