# gui/view_edit.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.project_logic import get_all_projects, update_project
from gui.tag_selector import open_tag_selector
from gui.edit_project import launch_edit_project

def launch_view_edit(root):
    root.withdraw()
    new_window = tk.Toplevel()
    new_window.title("View/Edit Projects")
    new_window.configure(bg="#1e1e1e")
    new_window.geometry("1200x700")

    frame = tk.Frame(new_window, bg="#1e1e1e")
    frame.pack(fill='both', expand=True, padx=10, pady=10)

    tree = ttk.Treeview(frame, columns=(
        "ID", "Title", "Category", "Type", "Creative Skills", "Technical Skills", "Tools",
        "Status", "Duration", "Collaborators", "Languages",
        "Report", "Portfolio", "Showcase", "Notes",
    ), show='headings')

    # Set up column headings and widths
    headings = [
        ("ID", 30), ("Title", 150), ("Category", 100), ("Type", 100),
        ("Creative Skills", 150), ("Technical Skills", 150), ("Tools", 120),
        ("Status", 80), ("Duration", 80), ("Collaborators", 120), ("Notes", 150),
        ("Languages", 120), ("Report", 80), ("Portfolio", 80), ("Showcase", 80)
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
    for proj in projects:
        tree.insert("", "end", values=proj)

    # Double-click binding
    def on_double_click(event):
        item = tree.focus()
        if not item:
            return
        values = tree.item(item, "values")
        if len(values) >= 15:
            launch_edit_project(new_window, values)
        else:
            messagebox.showerror("Error", "Incomplete project data")

    tree.bind("<Double-1>", on_double_click)

    # Back button
    tk.Button(new_window, text="Back to Menu", command=lambda: go_back_to_menu(new_window),
              bg="#3e3e3e", fg="white", width=30).pack(pady=10)

def go_back_to_menu(window):
    from gui.menu import main

    window.destroy()
    main()
