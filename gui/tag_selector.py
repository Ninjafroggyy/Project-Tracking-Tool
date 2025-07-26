# gui/tag_selector.py

import tkinter as tk
from backend.tag_logic import get_tags_by_type

def open_tag_selector(parent, tag_type, entry_widget):
    popup = tk.Toplevel(parent)
    popup.title(f"Select {tag_type.replace('_', ' ').title()}")
    popup.configure(bg="#1e1e1e")
    popup.geometry("400x400")

    selected_tags = []

    def toggle_tag(tag):
        if tag in selected_tags:
            selected_tags.remove(tag)
        else:
            selected_tags.append(tag)

    def apply_selection():
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ", ".join(selected_tags))
        popup.destroy()

    tags = get_tags_by_type(tag_type)

    for tag in tags:
        tag_name = tag[1]  # assuming tag = (id, name)
        cb = tk.Checkbutton(popup, text=tag_name, command=lambda t=tag_name: toggle_tag(t),
                            fg="white", bg="#1e1e1e", selectcolor="#3e3e3e")
        cb.pack(anchor="w", padx=20)

    tk.Button(popup, text="Apply", command=apply_selection, bg="#3e3e3e", fg="white").pack(pady=10)
