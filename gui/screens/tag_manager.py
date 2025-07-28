import customtkinter as ctk
from tkinter import messagebox
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR, GREY_COLOR
from backend.tag_logic import get_tags_by_type, add_tag, update_tag_name, delete_tag

class TagManagerScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        self.current_cat = None
        self.selected_btn = None
        self.selected_tag = None
        self.tag_buttons = {}
        self.tag_widgets = []
        self._build_ui()

    def _build_ui(self):
        # Middle pane: category buttons
        self.cat_frame = ctk.CTkFrame(self, fg_color=CONTENT_BG)
        self.cat_frame.grid(row=0, column=0, sticky="nsw", padx=10, pady=10)
        cats = ['language','creative_skill','technical_skill','tool','type','category','status']
        for idx, cat in enumerate(cats):
            btn = ctk.CTkButton(
                self.cat_frame,
                text=cat.replace('_',' ').title(),
                fg_color=GREY_COLOR,
                hover_color=HIGHLIGHT_COLOR,
                command=lambda c=cat: self._select_category(c)
            )
            btn.grid(row=idx, column=0, sticky="ew", pady=5)
            self.tag_buttons[cat] = btn

        # Right pane: tags grid (empty initially)
        self.grid_columnconfigure(1, weight=1)
        self.tags_frame = ctk.CTkFrame(self, fg_color=CONTENT_BG)
        self.tags_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        # Control frame (hidden until category selected)
        self.control_frame = ctk.CTkFrame(self, fg_color=CONTENT_BG)
        self.control_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=(0,10))
        self.control_frame.grid_columnconfigure(1, weight=1)

        # Controls: entry + buttons
        self.new_tag_entry = ctk.CTkEntry(self.control_frame, placeholder_text="Tag name", font=(FONT_FAMILY,14))
        self.new_tag_entry.grid(row=0, column=0, padx=5)
        self.add_btn = ctk.CTkButton(self.control_frame, text="Add Tag", command=self._add_tag)
        self.add_btn.grid(row=0, column=1, padx=5)
        self.update_btn = ctk.CTkButton(self.control_frame, text="Update Tag", command=self._update_tag)
        self.update_btn.grid(row=0, column=2, padx=5)
        self.del_btn = ctk.CTkButton(self.control_frame, text="Delete Tag", command=self._delete_tag)
        self.del_btn.grid(row=0, column=3, padx=5)
        self.control_frame.grid_remove()

    def _select_category(self, category):
        self.current_cat = category
        # Highlight selected category
        for cat, btn in self.tag_buttons.items():
            btn.configure(fg_color=HIGHLIGHT_COLOR if cat==category else GREY_COLOR)
        self.selected_tag = None
        if self.selected_btn:
            self.selected_btn.configure(fg_color=GREY_COLOR)
            self.selected_btn = None
        self.control_frame.grid()
        self.new_tag_entry.delete(0,'end')
        self._render_tags_grid()
        self._show_add_only()

    def _render_tags_grid(self):
        # Clear existing tag buttons
        for w in self.tag_widgets:
            w.destroy()
        self.tag_widgets.clear()

        tags = get_tags_by_type(self.current_cat)
        cols = 4
        for idx, tag in enumerate(tags):
            r, c = divmod(idx, cols)
            btn = ctk.CTkButton(
                self.tags_frame,
                text=tag['name'],
                fg_color=GREY_COLOR,
                hover_color=HIGHLIGHT_COLOR,
                command=lambda t=tag, b=None: self._select_tag(t, b)
            )
            btn.grid(row=r, column=c, sticky="ew", padx=5, pady=5)
            self.tag_widgets.append(btn)
            # bind with closure
            btn.configure(command=lambda t=tag, b=btn: self._select_tag(t, b))

    def _show_add_only(self):
        self.add_btn.grid()
        self.update_btn.grid_remove()
        self.del_btn.grid_remove()

    def _show_update_delete(self):
        self.add_btn.grid_remove()
        self.update_btn.grid()
        self.del_btn.grid()

    def _select_tag(self, tag, btn):
        # Highlight selected tag
        if self.selected_btn:
            self.selected_btn.configure(fg_color=GREY_COLOR)
        self.selected_tag = tag
        self.selected_btn = btn
        btn.configure(fg_color=HIGHLIGHT_COLOR)
        # Prefill entry and show update/delete
        self.new_tag_entry.delete(0,'end')
        self.new_tag_entry.insert(0, tag['name'])
        self._show_update_delete()

    def _add_tag(self):
        name = self.new_tag_entry.get().strip()
        if not name:
            messagebox.showerror("Error","Enter a tag name.")
            return
        add_tag(name, self.current_cat)
        self.new_tag_entry.delete(0,'end')
        self._render_tags_grid()
        self._show_add_only()

    def _update_tag(self):
        if not self.selected_tag:
            messagebox.showerror("Error","Select a tag first.")
            return
        new_name = self.new_tag_entry.get().strip()
        if not new_name:
            messagebox.showerror("Error","Enter a new name.")
            return
        # Update in database
        update_tag_name(self.selected_tag['name'], new_name, self.current_cat)
        # Reset selection and refresh grid
        self.selected_tag = None
        self.selected_btn = None
        self.new_tag_entry.delete(0,'end')
        self._render_tags_grid()
        self._show_add_only()

    def _delete_tag(self):
        if not self.selected_tag:
            messagebox.showerror("Error","Select a tag first.")
            return
        delete_tag(self.selected_tag['name'], self.current_cat)
        self.selected_tag = None
        self.new_tag_entry.delete(0,'end')
        self._render_tags_grid()
        self._show_add_only()