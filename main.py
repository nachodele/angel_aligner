#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import customtkinter as ctk
from core.config import Config
from core.database import Database
from core.theme import apply_medical_theme, MEDICAL_COLORS

# Aplica theme ANTES de cualquier widget
apply_medical_theme()

from gui.navbar import Navbar
from gui.dashboard import HomeView
from gui.patients import PatientsView

class AngelAligner(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title(f"{Config.APP_NAME} v{Config.APP_VERSION}")
        self.geometry("1600x1000")
        self.minsize(1200, 800)
        self.db = Database()
        
        self.current_view = None
        self.create_layout()
        self.show_home()
    
    def create_layout(self):
        """Layout principal: navbar + content_frame"""
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        
        # Navbar
        self.navbar = Navbar(self, self)
        self.navbar.grid(row=0, column=0, sticky="ns", padx=(10,15), pady=10)
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=(0,10), pady=10)
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)
    
    def show_home(self):
        self.clear_content()
        self.current_view = HomeView(self.content_frame)
    
    def show_patients(self):
        self.clear_content()
        self.current_view = PatientsView(self.content_frame)
    
    def show_appointments(self):
        self.clear_content()
        from gui.appointments import AppointmentsView
        self.current_view = AppointmentsView(self.content_frame, self.db)
    
    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        self.current_view = None

if __name__ == "__main__":
    print("🚀 Iniciando Angel Aligner...")
    app = AngelAligner()
    app.mainloop()