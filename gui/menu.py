# gui/menu.py — Refactored Main Menu
import tkinter as tk
import os
from gui.add_project import launch_add_project
from gui.view_edit import launch_view_edit
from gui.tag_manager import launch_tag_manager
from datalayer.db_handler import create_database
from config import DB_PATH
from gui.common import create_themed_window, style_button

def main():
    if not os.path.exists(DB_PATH):
        create_database()

    root = create_themed_window("Project Tracker Main Menu", size="500x400")
    MainMenu(root)
    root.mainloop()

class MainMenu:
    def __init__(self, root):
        self.root = root

        tk.Label(root, text="Project Tracker", fg="white", bg="#1e1e1e", font=("Arial", 18, "bold")).pack(pady=30)

        btn_add = tk.Button(root, text="Add New Project", command=lambda: launch_add_project(root))
        style_button(btn_add)
        btn_add.pack(pady=10)

        btn_view = tk.Button(root, text="View/Edit Projects", command=self.go_to_view_edit)
        style_button(btn_view)
        btn_view.pack(pady=10)

        btn_tags = tk.Button(root, text="Tag Manager", command=lambda: launch_tag_manager(root))
        style_button(btn_tags)
        btn_tags.pack(pady=10)

        btn_exit = tk.Button(root, text="Exit", command=root.quit)
        style_button(btn_exit)
        btn_exit.pack(pady=10)

    def go_to_view_edit(self):
        self.root.withdraw()
        launch_view_edit(self.root)
