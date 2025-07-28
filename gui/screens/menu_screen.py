# gui/screens/menu_screen.py
import customtkinter as ctk
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR, GREY_COLOR

class MenuScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        # Welcome Title
        title = ctk.CTkLabel(
            self, text="Project Tracker Dashboard", font=(FONT_FAMILY, 24), text_color=TEXT_COLOR
        )
        title.pack(pady=(40, 20))

        # Description
        desc = ctk.CTkLabel(
            self, text="Use the navigation pane to access different tools.",
            font=(FONT_FAMILY, 14), text_color=GREY_COLOR
        )
        desc.pack(pady=(0, 30))

        # Quick Access Buttons
        btn_frame = ctk.CTkFrame(self, fg_color=CONTENT_BG)
        btn_frame.pack(pady=10)
        buttons = [
            ("Add Project", lambda: self.controller.show_frame("AddProjectScreen")),
            ("View/Edit Projects", lambda: self.controller.show_frame("ViewEditScreen")),
        ]
        for text, cmd in buttons:
            btn = ctk.CTkButton(
                btn_frame, text=text, font=(FONT_FAMILY, 16),
                fg_color=HIGHLIGHT_COLOR, hover_color=GREY_COLOR,
                command=cmd, corner_radius=8
            )
            btn.pack(padx=10, pady=5, fill="x")