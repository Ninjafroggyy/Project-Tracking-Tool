# gui/tag_selector.py — Refactored tag popup window
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
        entry_widget.config(state='normal')
        entry_widget.delete(0, tk.END)
        entry_widget.insert(0, ", ".join(selected_tags))
        entry_widget.config(state='readonly')
        popup.destroy()

    tags = get_tags_by_type(tag_type)
    current = entry_widget.get().split(",")
    current_tags = set(t.strip() for t in current if t.strip())

    for tag in tags:
        tag_name = tag[1]  # assuming tag = (id, name)
        is_checked = tag_name in current_tags
        var = tk.BooleanVar(value=is_checked)
        cb = tk.Checkbutton(
            popup, text=tag_name, variable=var,
            command=lambda t=tag_name: toggle_tag(t),
            fg="white", bg="#1e1e1e", selectcolor="#3e3e3e"
        )
        cb.pack(anchor="w", padx=20)
        if is_checked:
            cb.select()
            selected_tags.append(tag_name)

    tk.Button(popup, text="Apply", command=apply_selection, bg="#3e3e3e", fg="white").pack(pady=10)
