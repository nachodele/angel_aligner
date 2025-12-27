# gui/navbar.py
import customtkinter as ctk
from core.config import Config
from core.theme import MEDICAL_COLORS, BUTTON_SIZES

class Navbar(ctk.CTkFrame):
    def __init__(self, parent, app):
        super().__init__(parent, corner_radius=0, width=220, fg_color=MEDICAL_COLORS["dark_navy"])
        self.app = app
        self.grid_propagate(False)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.create_medical_navbar()

    def create_medical_navbar(self):
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="transparent", height=70)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(15,15))
        header_frame.grid_propagate(False)

        ctk.CTkLabel(
            header_frame,
            text="🦷 Angel Aligner",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=MEDICAL_COLORS["light_blue"],
        ).pack(pady=8)
        ctk.CTkLabel(
            header_frame,
            text="Professional Edition",
            font=ctk.CTkFont(size=10),
            text_color=MEDICAL_COLORS["text_tertiary"],
        ).pack()

        # Botones compactos
        h = 30       # altura real compacta
        fs = 11      # tamaño de fuente
        nav_items = [
            ("🏠 Dashboard", self.app.show_home),
            ("👥 Patients", self.app.show_patients),
            ("📅 Appointments", self.app.show_appointments),
        ]

        for i, (text, command) in enumerate(nav_items):
            btn = ctk.CTkButton(
                self,
                text=text,
                command=command,
                height=h,
                width=80,
                fg_color=MEDICAL_COLORS["navy"],
                hover_color=MEDICAL_COLORS["navy_hover"],
                text_color="#f1f5f9",
                font=ctk.CTkFont(size=fs, weight="bold"),
                border_width=0,
                corner_radius=6,
            )
            btn.grid(row=i + 1, column=0, sticky="ew", padx=16, pady=4)

        ctk.CTkLabel(
            self,
            text=f"v{Config.APP_VERSION}",
            font=ctk.CTkFont(size=10),
            text_color=MEDICAL_COLORS["text_tertiary"],
        ).grid(row=4, column=0, pady=(10,10), padx=16)
