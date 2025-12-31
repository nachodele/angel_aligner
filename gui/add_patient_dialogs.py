# gui/dialogs.py
import customtkinter as ctk
from tkinter import messagebox
from core.theme import MEDICAL_COLORS

class PatientDialog(ctk.CTkToplevel):
    def __init__(self, parent, callback=None, patient=None, mode="add"):
        """
        mode: "add" (nuevo) o "edit" (editar)
        patient: datos del paciente (solo para edit)
        """
        super().__init__(parent)
        self.title("Add Patient" if mode == "add" else "Edit Patient")
        self.geometry("550x700")
        self.grab_set()
        self.callback = callback
        self.db = parent.db
        self.mode = mode
        self.patient_id = patient[0] if patient else None
        self.patient_data = patient
        
        self.entries = {}
        self.create_form()
    
    def create_form(self):
        # Header dinámico
        title = "👤 New Patient" if self.mode == "add" else "✏️ Edit Patient"
        ctk.CTkLabel(self, text=title, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=30)
        
        # Form fields
        fields = [
            ("Full Name *", "name"),
            ("Phone", "phone"), 
            ("Email", "email"),
            ("Birth Date (YYYY-MM-DD)", "birth_date"),
            ("Address", "address")
        ]
        
        for label, key in fields:
            frame = ctk.CTkFrame(self)
            frame.pack(fill="x", padx=40, pady=8)
            
            ctk.CTkLabel(frame, text=label, width=120).pack(anchor="w")
            
            # Pre-rellenar si es edit
            default_value = self.patient_data[fields.index((label, key)) + 1] if self.mode == "edit" and self.patient_data else ""
            entry = ctk.CTkEntry(frame, width=300)
            entry.insert(0, default_value)
            entry.pack(fill="x", padx=(120,0))
            self.entries[key] = entry
        
        # Gender dropdown (siempre al final)
        gender_frame = ctk.CTkFrame(self)
        gender_frame.pack(fill="x", padx=40, pady=8)
        
        ctk.CTkLabel(gender_frame, text="Gender", width=120).pack(anchor="w")
        
        # Pre-rellenar gender si edit
        default_gender = self.patient_data[7] if self.mode == "edit" and len(self.patient_data) > 7 else "Male"
        self.entries["gender"] = ctk.CTkOptionMenu(
            gender_frame, 
            values=["Male", "Female", "Other"],
            width=300
        )
        self.entries["gender"].set(default_gender)
        self.entries["gender"].pack(fill="x", padx=(120,0))
        
        # Buttons dinámicos
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=30)
        
        btn_text = "💾 Save" if self.mode == "add" else "💾 Update"
        ctk.CTkButton(btn_frame, text=btn_text, width=120, 
                     command=self.save_patient).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="❌ Cancel", width=120, 
                     fg_color="gray", command=self.destroy).pack(side="left")
    
    def save_patient(self):
        data = {k: v.get() for k, v in self.entries.items()}
        if not data["name"]:
            messagebox.showerror("Error", "Name is required!")
            return
        
        try:
            if self.mode == "add":
                patient_id = self.db.add_patient(**data)
                messagebox.showinfo("Success", f"Patient {data['name']} added! ID: {patient_id}")
            else:  # edit
                self.db.update_patient(self.patient_id, **data)
                messagebox.showinfo("Success", f"Patient {data['name']} updated!")
            
            self.destroy()
            if self.callback:
                self.callback()
        except Exception as e:
            messagebox.showerror("Error", f"Operation failed: {str(e)}")
