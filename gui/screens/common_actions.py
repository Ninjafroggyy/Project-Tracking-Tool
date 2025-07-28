# gui/screens/common_actions.py
import customtkinter as ctk
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR

class CommonActionsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        title = ctk.CTkLabel(
            self, text="Common Actions", font=(FONT_FAMILY, 20), text_color=TEXT_COLOR
        )
        title.pack(pady=(20,10))

        # Placeholder for any shared utilities
        info = ctk.CTkLabel(
            self, text="No additional actions configured.",
            font=(FONT_FAMILY, 14), text_color=TEXT_COLOR
        )
        info.pack(pady=10)