# gui/tag_manager.py
import tkinter as tk
from tkinter import messagebox, simpledialog
from functools import partial
from backend.tag_logic import get_tags_by_type, add_tag, update_tag_name, delete_tag

def launch_tag_manager(root):
    from gui.menu import main  # put at the top if not already imported

    root.title("Tag Manager")
    for widget in root.winfo_children():
        widget.destroy()

    label = tk.Label(root, text="Select a Tag Category", font=("Helvetica", 16))
    label.pack(pady=10)

    categories = ["language", "creative", "tool", "type", "system"]

    for category in categories:
        btn = tk.Button(
            root, text=category.capitalize(), width=30,
            bg="#3e3e3e", fg="white",
            command=partial(open_category_view, root, category)
        )
        btn.pack(pady=5)

    back_btn = tk.Button(root, text="Back to Menu", command=lambda: (root.destroy(), main()))
    back_btn.pack(pady=20)

def open_category_view(root, category):
    for widget in root.winfo_children():
        widget.destroy()

    root.title(f"{category.capitalize()} Tags")

    header = tk.Label(root, text=f"Tags in {category.capitalize()} Category", font=("Helvetica", 14))
    header.pack(pady=10)

    tags = get_tags_by_type(category)

    listbox = tk.Listbox(root, width=40, height=10)
    for tag in tags:
        listbox.insert(tk.END, tag[1])  # tag[1] is the tag name
    listbox.pack(pady=5)

    def create_tag():
        tag_name = simpledialog.askstring("Create Tag", f"Enter new {category} tag name:")
        if tag_name:
            try:
                add_tag(tag_name, category)
                listbox.insert(tk.END, tag_name)
            except ValueError:
                messagebox.showerror("Error", "Tag already exists.")

    def delete_selected_tag():
        selection = listbox.curselection()
        if selection:
            tag_to_delete = listbox.get(selection[0])
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{tag_to_delete}'?")
            if confirm:
                try:
                    delete_tag(tag_to_delete, category)
                    listbox.delete(selection[0])
                except Exception as e:
                    messagebox.showerror("Error", str(e))

    def edit_selected_tag():
        selection = listbox.curselection()
        if selection:
            old_tag = listbox.get(selection[0])
            new_tag = simpledialog.askstring("Edit Tag", f"Rename tag '{old_tag}' to:")
            if new_tag:
                try:
                    update_tag_name(old_tag, new_tag, category)
                    listbox.delete(selection[0])
                    listbox.insert(tk.END, new_tag)
                except ValueError as ve:
                    messagebox.showerror("Error", str(ve))

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Create Tag", command=create_tag).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Edit Selected", command=edit_selected_tag).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected_tag).grid(row=0, column=2, padx=5)
    tk.Button(btn_frame, text="Back", command=lambda: launch_tag_manager(root)).grid(row=0, column=3, padx=5)
