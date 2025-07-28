# gui/menu.py
import customtkinter as ctk
from gui.styles import BACKGROUND_COLOR, HIGHLIGHT_COLOR, GREY_COLOR, FONT_FAMILY, CONTENT_BG
from gui.screens.add_project import AddProjectScreen
from gui.screens.view_edit import ViewEditScreen
from gui.screens.edit_project import EditProjectScreen
from gui.screens.tag_manager import TagManagerScreen
from gui.screens.common_actions import CommonActionsScreen
from gui.screens.export_excel import ExportExcelScreen
from gui.screens.menu_screen import MenuScreen

class AppShell(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Project Tracker")
        self.geometry("1200x700")
        self.configure(bg=BACKGROUND_COLOR)
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self._screens = {}
        self._create_grid()
        self._create_navigation()
        self._load_screens()
        self.bind("<Configure>", self._on_resize)

    def _create_grid(self):
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _create_navigation(self):
        self.nav_frame = ctk.CTkFrame(self, width=200, fg_color=BACKGROUND_COLOR)
        self.nav_frame.grid(row=0, column=0, sticky="nsw")

        buttons = [
            ("Menu", lambda: self.show_frame("MenuScreen")),
            ("Add Project", lambda: self.show_frame("AddProjectScreen")),
            ("View/Edit", lambda: self.show_frame("ViewEditScreen")),
            ("Tag Manager", lambda: self.show_frame("TagManagerScreen")),
            ("Actions", lambda: self.show_frame("CommonActionsScreen")),
            ("Export", lambda: self.show_frame("ExportExcelScreen")),
            ("Exit", self._on_close),
        ]
        for idx, (text, cmd) in enumerate(buttons):
            btn = ctk.CTkButton(
                self.nav_frame,
                text=text,
                font=(FONT_FAMILY, 14),
                fg_color=BACKGROUND_COLOR,
                hover_color=HIGHLIGHT_COLOR,
                command=cmd,
                corner_radius=0
            )
            btn.grid(row=idx*2, column=0, sticky="ew", padx=10, pady=5)
            sep = ctk.CTkFrame(self.nav_frame, height=1, fg_color=GREY_COLOR)
            sep.grid(row=idx*2+1, column=0, sticky="ew", padx=10, pady=(0,5))

        # Hamburger button for mobile view
        self.hamburger = ctk.CTkButton(
            self,
            text="☰",
            font=(FONT_FAMILY, 20),
            fg_color=BACKGROUND_COLOR,
            hover_color=HIGHLIGHT_COLOR,
            command=self._toggle_nav,
            corner_radius=0
        )
        self.hamburger.place(x=10, y=10)
        self.hamburger.lower()

    def _on_close(self):
        """Cleanly exit the application when user clicks Exit or window close."""
        try:
            self.destroy()
        except:
            pass

    def _load_screens(self):
        content = ctk.CTkFrame(self, fg_color=CONTENT_BG)
        content.grid(row=0, column=1, sticky="nsew")
        content.grid_rowconfigure(0, weight=1)
        content.grid_columnconfigure(0, weight=1)

        # Wrap each screen in its own subframe to isolate their grids
        for ScreenClass in [MenuScreen, EditProjectScreen, AddProjectScreen, ViewEditScreen, TagManagerScreen, CommonActionsScreen,
                            ExportExcelScreen]:
            container = ctk.CTkFrame(content, fg_color=CONTENT_BG)
            container.grid(row=0, column=0, sticky="nsew")
            container.grid_rowconfigure(0, weight=1)
            container.grid_columnconfigure(0, weight=1)
            screen = ScreenClass(container, self)
            name = ScreenClass.__name__
            self._screens[name] = container
            screen.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MenuScreen")

    def show_frame(self, name: str):
        # Hide all screen containers
        for container in self._screens.values():
            container.grid_remove()

        # Show target container
        container = self._screens.get(name)
        if not container:
            return
        container.grid()

        # If it’s the EditProjectScreen, populate it from the stored ID
        if name == "EditProjectScreen" and hasattr(self, "selected_project_id"):
            # The first child of this container is the actual EditProjectScreen instance
            edit_frame = container.winfo_children()[0]
            if hasattr(edit_frame, "load_project"):
                edit_frame.load_project(self.selected_project_id)

    def _on_resize(self, event):
        # Make sure nav_frame is still valid
        if not getattr(self, 'nav_frame', None) or not self.nav_frame.winfo_exists():
            return

        # Responsive breakpoints (from gui/styles.py)
        from gui.styles import BREAKPOINTS
        width = self.winfo_width()

        if width < BREAKPOINTS['mobile']:
            # Mobile view: hide sidebar, show hamburger
            self.nav_frame.grid_remove()
            self.hamburger.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
        elif width < BREAKPOINTS['tablet']:
            # Tablet: collapse or narrow sidebar
            self.nav_frame.grid(row=0, column=0, sticky="nsw")
            # potentially adjust width or icons only
        else:
            # Desktop: full sidebar
            self.hamburger.grid_remove()
            self.nav_frame.grid(row=0, column=0, sticky="nsw")

    def _toggle_nav(self):
        if self.nav_frame.winfo_ismapped():
            self.nav_frame.grid_remove()
        else:
            self.nav_frame.grid()

def main():
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = AppShell()
    app.mainloop()


if __name__ == "__main__":
    main()