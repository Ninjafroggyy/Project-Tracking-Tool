# gui/add_project.py
import tkinter as tk
from tkinter import messagebox
from backend.project_logic import add_project

def launch_add_project(parent):
    window = tk.Toplevel()
    window.title("Add New Project")
    window.configure(bg="#1e1e1e")
    window.geometry("700x700")

    def go_back():
        window.destroy()
        parent.deiconify()

    tk.Label(window, text="Add New Project", fg="white", bg="#1e1e1e", font=("Arial", 16)).pack(pady=10)

    entries = {}
    fields = ["Title", "Category", "Type", "Creative Skills", "Technical Skills", "Tools", "Status", "Duration", "Collaborators", "Notes"]
    for field in fields:
        frame = tk.Frame(window, bg="#1e1e1e")
        frame.pack(pady=2)
        tk.Label(frame, text=field + ":", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=50)
        entry.pack(side=tk.RIGHT)
        entries[field] = entry

    report_done = tk.IntVar()
    added_to_portfolio = tk.IntVar()
    has_showcase_material = tk.IntVar()

    tk.Checkbutton(window, text="Report Done", variable=report_done, fg="white", bg="#1e1e1e", selectcolor="#1e1e1e").pack()
    tk.Checkbutton(window, text="Added to Portfolio", variable=added_to_portfolio, fg="white", bg="#1e1e1e", selectcolor="#1e1e1e").pack()
    tk.Checkbutton(window, text="Has Showcase Material", variable=has_showcase_material, fg="white", bg="#1e1e1e", selectcolor="#1e1e1e").pack()

    def save():
        if not entries["Title"].get().strip():
            messagebox.showerror("Error", "Title cannot be empty!")
            return
        try:
            add_project(
                entries["Title"].get(),
                entries["Category"].get(),
                entries["Type"].get(),
                entries["Creative Skills"].get(),
                entries["Technical Skills"].get(),
                entries["Tools"].get(),
                entries["Status"].get(),
                entries["Duration"].get(),
                entries["Collaborators"].get(),
                entries["Notes"].get(),
                report_done.get(),
                added_to_portfolio.get(),
                has_showcase_material.get()
            )
            messagebox.showinfo("Success", "Project saved!")
            window.destroy()
            parent.deiconify()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(window, text="Save Project", command=save, bg="#3e3e3e", fg="white").pack(pady=10)
    tk.Button(window, text="Back", command=go_back, bg="#2e2e2e", fg="white").pack(pady=5)
