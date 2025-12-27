# gui/patients.py
import customtkinter as ctk
from tkinter import messagebox
from core.database import Database

class PatientsView:
    def __init__(self, parent):  
        self.parent = parent
        self.db = parent.master.db
        self.create_patients_view()
    
    def create_patients_view(self):
        self.main_frame = ctk.CTkFrame(self.app, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        
        # Search
        search_frame = ctk.CTkFrame(self.main_frame)
        search_frame.pack(fill="x", pady=(0,20))
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search patients by name...", width=400)
        self.search_entry.pack(side="left", padx=20, pady=15)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        # Patients list
        self.patients_frame = ctk.CTkScrollableFrame(self.main_frame)
        self.patients_frame.pack(fill="both", expand=True, pady=(0,20))
        
        # Add button
        add_btn = ctk.CTkButton(self.main_frame, text="➕ Add New Patient", 
                               command=self.add_patient, width=200, height=45, 
                               font=ctk.CTkFont(size=16, weight="bold"))
        add_btn.pack(pady=10)
        
        self.load_patients()
    
    def load_patients(self, search=""):
        # Clear existing
        for child in self.patients_frame.winfo_children():
            child.destroy()
        
        patients = self.db.get_patients(search)
        
        for patient in patients:
            self.create_patient_card(patient)
    
    def create_patient_card(self, patient):
        card = ctk.CTkFrame(self.patients_frame, fg_color="#f8fafc", 
                          border_width=1, corner_radius=12)
        card.pack(fill="x", padx=20, pady=10)
        
        # Left info
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)
        
        ctk.CTkLabel(info_frame, text=f"👤 {patient[1]}", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"📱 {patient[2]}", 
                    font=ctk.CTkFont(size=13)).pack(anchor="w")
        ctk.CTkLabel(info_frame, text=f"✉️ {patient[3] or 'No email'}", 
                    font=ctk.CTkFont(size=13)).pack(anchor="w")
        
        # Right actions
        actions_frame = ctk.CTkFrame(card, fg_color="transparent")
        actions_frame.pack(side="right", padx=20, pady=15)
        
        view_btn = ctk.CTkButton(actions_frame, text="👁️ View", 
                               width=80, height=35, command=lambda: self.view_patient(patient))
        view_btn.pack(side="left", padx=(0,10))
        
        edit_btn = ctk.CTkButton(actions_frame, text="✏️ Edit", 
                               width=80, height=35, fg_color="#f59e0b")
        edit_btn.pack(side="left")
    
    def on_search(self, event=None):
        self.load_patients(self.search_entry.get())
    
    def add_patient(self):
        from gui.dialogs import PatientDialog
        PatientDialog(self.app, self.load_patients)
    
    def view_patient(self, patient):
        messagebox.showinfo("Patient View", f"Viewing patient: {patient[1]}\nImplement full view here")
