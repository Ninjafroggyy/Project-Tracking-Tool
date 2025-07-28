# gui/screens/export_excel.py
import customtkinter as ctk
from gui.styles import CONTENT_BG, TEXT_COLOR, FONT_FAMILY, HIGHLIGHT_COLOR, GREY_COLOR
from backend.export_logic import export_to_excel, export_to_excel_dialog

class ExportExcelScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=CONTENT_BG)
        self.controller = controller
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(
            self, text="Export to Excel", font=(FONT_FAMILY, 20), text_color=TEXT_COLOR
        ).grid(row=0, column=0, pady=(20,10))
        ctk.CTkButton(
            self, text="Export All Projects", fg_color=HIGHLIGHT_COLOR,
            hover_color=GREY_COLOR, command=self._export
        ).grid(row=1, column=0, pady=20)

    def _export(self):
        try:
            save_path = export_to_excel_dialog(self)
            if save_path:
                export_to_excel(path=save_path)
                ctk.CTkMessagebox(title="Success", message=f"Exported to {save_path}")
        except Exception as e:
            ctk.CTkMessagebox(title="Error", message=f"Export failed: {e}")