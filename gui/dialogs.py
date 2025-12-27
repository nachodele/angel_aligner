# gui/dialogs.py
import customtkinter as ctk
from tkinter import messagebox
from core.database import Database

class PatientDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback=None):
        super().__init__(parent)
        self.title("Add Patient")
        self.geometry("500x650")
        self.grab_set()
        self.callback = callback
        self.db = parent.db
        
        self.create_form()
    
    def create_form(self):
        # Title
        ctk.CTkLabel(self, text="👤 New Patient", 
                    font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)
        
        # Form fields
        self.entries = {}
        fields = [
            ("Full Name *", "name"),
            ("Phone", "phone"), 
            ("Email", "email"),
            ("Birth Date (YYYY-MM-DD)", "birth_date"),
            ("Address", "address"),
            ("Gender", "gender")
        ]
        
        for label, key in fields:
            frame = ctk.CTkFrame(self)
            frame.pack(fill="x", padx=40, pady=8)
            
            ctk.CTkLabel(frame, text=label, width=120).pack(anchor="w")
            entry = ctk.CTkEntry(frame, width=300)
            entry.pack(fill="x", padx=(120,0))
            self.entries[key] = entry
        
        # Gender dropdown
        self.entries["gender"] = ctk.CTkOptionMenu(self.entries["gender"].master, 
                                                 values=["Male", "Female", "Other"])
        self.entries["gender"].pack(fill="x", padx=(120,0))
        
        # Buttons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=30)
        
        ctk.CTkButton(btn_frame, text="💾 Save", width=100, 
                     command=self.save_patient).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="❌ Cancel", width=100, fg_color="gray").pack(side="left")
    
    def save_patient(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not data["name"]:
            messagebox.showerror("Error", "Name is required!")
            return
        
        patient_id = self.db.add_patient(**data)
        messagebox.showinfo("Success", f"Patient {data['name']} added! ID: {patient_id}")
        self.destroy()
        if self.callback:
            self.callback()
