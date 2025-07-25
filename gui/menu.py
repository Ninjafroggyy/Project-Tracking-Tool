# gui/menu.py
import tkinter as tk
from gui.add_project import launch_add_project
from gui.view_edit import launch_view_edit

class MainMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("Project Tracker Main Menu")
        self.root.configure(bg="#1e1e1e")
        self.root.geometry("500x400")

        tk.Label(root, text="Project Tracker", fg="white", bg="#1e1e1e", font=("Arial", 18, "bold")).pack(pady=30)

        tk.Button(root, text="Add New Project", command=launch_add_project, width=30, bg="#3e3e3e", fg="white").pack(pady=10)
        tk.Button(root, text="View/Edit Projects", command=launch_view_edit, width=30, bg="#3e3e3e", fg="white").pack(pady=10)
        tk.Button(root, text="Exit", command=root.quit, width=30, bg="#3e3e3e", fg="white").pack(pady=10)

def main():
    root = tk.Tk()
    app = MainMenu(root)
    root.mainloop()

if __name__ == "__main__":
    main()

