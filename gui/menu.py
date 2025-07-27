# gui/menu.py — Refactored Main Menu
import tkinter as tk
import os
from gui.add_project import launch_add_project
from gui.view_edit import launch_view_edit
from gui.tag_manager import launch_tag_manager
from datalayer.db_handler import create_database
from config import DB_PATH
from gui.common import create_themed_window, style_button
from backend.export_logic import export_to_excel_dialog


def main():
    if not os.path.exists(DB_PATH):
        create_database()

    root = create_themed_window("Project Tracker Main Menu", size="1200x700")

    # Launch main menu UI
    MainMenu(root)
    root.mainloop()


class MainMenu:
    def __init__(self, root):
        self.root = root
        # Define export action using backend logic
        from backend.export_logic import export_to_excel

        # Header label
        tk.Label(root, text="Project Tracker", fg="white", bg="#1e1e1e", font=("Arial", 18, "bold")).pack(pady=30)

        # Add Project button
        btn_add = tk.Button(root, text="Add New Project", command=lambda: launch_add_project(root))
        style_button(btn_add)
        btn_add.pack(pady=10)

        # View/Edit Projects button
        btn_view = tk.Button(root, text="View/Edit Projects", command=lambda: self.go_to_view_edit())
        style_button(btn_view)
        btn_view.pack(pady=10)

        # Tag Manager button
        btn_tags = tk.Button(root, text="Tag Manager", command=lambda: launch_tag_manager(root))
        style_button(btn_tags)
        btn_tags.pack(pady=10)

        # Export to Excel button
        btn_export = tk.Button(root, text="Export to Excel", command=lambda: export_to_excel_dialog(root))
        style_button(btn_export)
        btn_export.pack(pady=10)

        # Exit button
        btn_exit = tk.Button(root, text="Exit", command=root.quit)
        style_button(btn_exit)
        btn_exit.pack(pady=10)

    def go_to_view_edit(self):
        self.root.withdraw()
        launch_view_edit(self.root)
