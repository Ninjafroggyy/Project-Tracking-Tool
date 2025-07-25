# gui/view_edit.py
import tkinter as tk
from tkinter import ttk, messagebox
from backend.project_logic import get_all_projects, update_project, delete_project

def launch_view_edit():
    window = tk.Toplevel()
    window.title("View/Edit Projects")
    window.configure(bg="#1e1e1e")
    window.geometry("1000x600")

    tk.Label(window, text="Select a Project to Edit", fg="white", bg="#1e1e1e", font=("Arial", 14)).pack(pady=10)

    tree = ttk.Treeview(window, columns=("Title", "Category", "Status"), show="headings")
    tree.heading("Title", text="Title")
    tree.heading("Category", text="Category")
    tree.heading("Status", text="Status")
    tree.pack(expand=True, fill=tk.BOTH)

    scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_projects():
        for row in get_all_projects():
            tree.insert("", tk.END, values=(row[1], row[2], row[6]))

    def on_double_click(event):
        item = tree.selection()
        if not item:
            return
        values = tree.item(item, "values")
        edit_window = tk.Toplevel(window)
        edit_window.title(f"Edit Project: {values[0]}")
        edit_window.geometry("800x600")
        edit_window.configure(bg="#1e1e1e")

        labels = ["Title", "Category", "Type", "Creative Skills", "Technical Skills", "Tools", "Status", "Duration", "Collaborators", "Notes"]
        entries = {}
        for i, label in enumerate(labels):
            frame = tk.Frame(edit_window, bg="#1e1e1e")
            frame.pack(pady=2)
            tk.Label(frame, text=label + ":", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
            entry = tk.Entry(frame, width=50)
            entry.insert(0, values[i])
            entry.pack(side=tk.RIGHT)
            entries[label] = entry

        def save_changes():
            if not entries["Title"].get().strip():
                messagebox.showerror("Error", "Title cannot be empty!")
                return
            try:
                update_project(
                    entries["Title"].get(),
                    entries["Category"].get(),
                    entries["Type"].get(),
                    entries["Creative Skills"].get(),
                    entries["Technical Skills"].get(),
                    entries["Tools"].get(),
                    entries["Status"].get(),
                    entries["Duration"].get(),
                    entries["Collaborators"].get(),
                    entries["Notes"].get()
                )
                messagebox.showinfo("Updated", "Project updated successfully")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        def confirm_delete():
            if messagebox.askyesno("Delete", f"Are you sure you want to delete '{values[0]}'?"):
                delete_project(values[0])
                messagebox.showinfo("Deleted", "Project deleted.")
                edit_window.destroy()
                window.destroy()
                launch_view_edit()

        tk.Button(edit_window, text="Save Changes", command=save_changes, bg="#3e3e3e", fg="white").pack(pady=10)
        tk.Button(edit_window, text="Delete Project", command=confirm_delete, bg="#6e3e3e", fg="white").pack(pady=5)

    tree.bind("<Double-1>", on_double_click)
    load_projects()