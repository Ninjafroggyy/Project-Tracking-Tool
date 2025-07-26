# gui/menu.py
import tkinter as tk
import os
from gui.add_project import launch_add_project
from gui.view_edit import launch_view_edit
from datalayer.db_handler import create_database
from gui.tag_manager import launch_tag_manager
from config import DB_PATH

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Tracker Main Menu")
        self.root.configure(bg="#1e1e1e")
        self.root.geometry("500x400")

        tk.Label(root, text="Project Tracker", fg="white", bg="#1e1e1e", font=("Arial", 18, "bold")).pack(pady=30)

        tk.Button(root, text="Add New Project", command=lambda: launch_add_project(root), width=30, bg="#3e3e3e", fg="white").pack(pady=10)
        tk.Button(root, text="View/Edit Projects", command=self.go_to_view_edit, width=30, bg="#3e3e3e", fg="white").pack(pady=10)
        tk.Button(root, text="Tag Manager", command=lambda: launch_tag_manager(root), width=30, bg="#3e3e3e", fg="white").pack(pady=10)

        tk.Button(root, text="Exit", command=root.quit, width=30, bg="#3e3e3e", fg="white").pack(pady=10)

    def go_to_add_project(self):
        self.root.withdraw()
        launch_add_project(self.root)

    def go_to_view_edit(self):
        self.root.withdraw()
        launch_view_edit(self.root)

def main():
    if not os.path.exists(DB_PATH):
        create_database()

    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()