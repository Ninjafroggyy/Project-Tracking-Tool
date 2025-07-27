# gui/screens/tag_manager.py
import customtkinter as ctk
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR, GREY_COLOR
from backend.tag_logic import get_all_tags, add_tag, delete_tag

class TagManagerScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Manage Tags", font=(FONT_FAMILY, 20), text_color=TEXT_COLOR
        )
        title.grid(row=0, column=0, columnspan=2, pady=(20,10))

        # Existing Tags List
        self.tag_list = ctk.CTkTextbox(self, font=(FONT_FAMILY, 12))
        self.tag_list.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=10)
        self.grid_rowconfigure(1, weight=1)

        # New Tag Entry
        new_label = ctk.CTkLabel(
            self, text="New Tag:", font=(FONT_FAMILY, 14), text_color=TEXT_COLOR
        )
        new_label.grid(row=2, column=0, sticky="e", padx=10, pady=5)
        self.new_entry = ctk.CTkEntry(self, placeholder_text="Enter tag...", font=(FONT_FAMILY,14))
        self.new_entry.grid(row=2, column=1, sticky="w", padx=10, pady=5)

        # Buttons
        add_btn = ctk.CTkButton(
            self, text="Add", fg_color=HIGHLIGHT_COLOR,
            hover_color=GREY_COLOR, command=self._add_tag
        )
        del_btn = ctk.CTkButton(
            self, text="Delete Selected", fg_color=HIGHLIGHT_COLOR,
            hover_color=GREY_COLOR, command=self._delete_tag
        )
        add_btn.grid(row=3, column=0, pady=10)
        del_btn.grid(row=3, column=1, pady=10)

        self._load_tags()

    def _load_tags(self):
        tags = get_all_tags()
        self.tag_list.delete("1.0", "end")
        for t in tags:
            # sqlite3.Row maps columns by string keys
            self.tag_list.insert("end", f"{t['id']}: {t['name']}\n")

    def _add_tag(self):
        name = self.new_entry.get().strip()
        if name:
            try:
                add_tag(name)
                self.new_entry.delete(0, "end")
                self._load_tags()
            except Exception as e:
                ctk.CTkMessagebox(title="Error", message=f"Add tag failed: {e}")

    def _delete_tag(self):
        try:
            sel_text = self.tag_list.get("sel.first", "sel.last").strip()
            if not sel_text:
                raise ValueError
            tag_id = int(sel_text.split(":")[0])
        except Exception:
            ctk.CTkMessagebox(
                title="Error", message="Please select a tag line to delete."
            )
            return
        confirm = ctk.CTkMessagebox(
            title="Confirm", message="Delete this tag?"
        )
        if confirm:
            try:
                delete_tag(tag_id)
                self._load_tags()
                ctk.CTkMessagebox(
                    title="Success", message="Tag deleted."
                )
            except Exception as e:
                ctk.CTkMessagebox(
                    title="Error", message=f"Deletion failed: {e}"
                )