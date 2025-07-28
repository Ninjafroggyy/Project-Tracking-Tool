# gui/utils/tag_selector.py
import customtkinter as ctk
from gui.styles import CONTENT_BG, HIGHLIGHT_COLOR, GREY_COLOR
from backend.tag_logic import get_tags_by_type

class TagSelectorPanel(ctk.CTkFrame):
    """
    Inline tag selector panel shown on the right side of Add/Edit screens.
    Preserves previous selections.
    """
    def __init__(self, parent, tag_type, on_submit, initial=None):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.tag_type = tag_type
        self.on_submit = on_submit
        self.selected = set(initial or [])
        self.vars = {}
        self._build_ui()

    def _build_ui(self):
        # Close button hides the panel (state is preserved)
        close_btn = ctk.CTkButton(self, text="Close", command=self.hide)
        close_btn.pack(anchor="ne", padx=5, pady=5)

        # Dynamically create a checkbox for each tag in this category
        for tag in get_tags_by_type(self.tag_type):
            name = tag['name']
            var = ctk.BooleanVar(value=(name in self.selected))
            chk = ctk.CTkCheckBox(
                self,
                text=name,
                variable=var,
                command=lambda t=name, v=var: self._toggle(t, v)
            )
            chk.pack(anchor="w", padx=10, pady=2)
            self.vars[name] = var

        # Submit button applies selection and hides panel
        submit = ctk.CTkButton(
            self,
            text="OK",
            fg_color=HIGHLIGHT_COLOR,
            hover_color=GREY_COLOR,
            command=self._submit
        )
        submit.pack(pady=10)

    def hide(self):
        """Hide panel but preserve its state for next open."""
        self.grid_forget()

    def _toggle(self, tag, var):
        if var.get():
            self.selected.add(tag)
        else:
            self.selected.discard(tag)

    def _submit(self):
        """Invoke callback with the current selection, then hide."""
        self.on_submit(list(self.selected))
        self.hide()