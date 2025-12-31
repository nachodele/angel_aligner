# gui/patients.py - FIJADO NameError
import customtkinter as ctk
from tkinter import messagebox
from core.database import Database
from core.theme import MEDICAL_COLORS

class PatientsView:
    def __init__(self, parent):  
        self.parent = parent
        self.db = parent.master.db
        self.current_mode = "list"
        self.selected_patient = None
        self.detail_container = None 
        self.create_patients_view()
    
    def create_patients_view(self):
        self.main_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Search + Back (siempre visible)
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(10, 20))
        
        search_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        search_frame.pack(side="left")
        
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="🔍 Search patients...", width=400)
        self.search_entry.pack(pady=15, padx=20)
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        back_btn = ctk.CTkButton(header_frame, text="⬅️ Back", width=150, height=45,
                                command=self.show_list_view, fg_color="transparent",
                                text_color=MEDICAL_COLORS["text_primary"])
        back_btn.pack(side="right", pady=15)
        
        # Contenido principal
        self.content_frame = ctk.CTkFrame(self.main_frame)
        self.content_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        self.show_list_view()
    
    def show_list_view(self):
        """Muestra lista de pacientes"""
        self.current_mode = "list"
        self.selected_patient = None
        
        for child in self.content_frame.winfo_children():
            child.destroy()
        
        self.patients_frame = ctk.CTkScrollableFrame(self.content_frame)
        self.patients_frame.pack(fill="both", expand=True)
        
        add_btn = ctk.CTkButton(self.content_frame, text="➕ Add New Patient", 
                               command=self.add_patient, width=250, height=50,
                               font=ctk.CTkFont(size=16, weight="bold"))
        add_btn.pack(pady=20)
        
        self.load_patients()
    
    def show_patient_detail(self, patient):
        """Vista detalle del paciente"""
        self.current_mode = "detail"
        self.selected_patient = patient
        self.render_patient_view(patient)
    
    def show_clinic_history(self, patient):
        """Muestra historial clínico EN LA MISMA VISTA"""
        self.current_mode = "history"
        self.selected_patient = patient
        self.render_patient_view(patient)
    
    def render_patient_view(self, patient):
        """Renderiza vista completa (header + contenido dinámico)"""
        # Limpiar contenido anterior
        for child in self.content_frame.winfo_children():
            child.destroy()
        
        # Panel principal
        self.detail_container = ctk.CTkFrame(self.content_frame, fg_color=MEDICAL_COLORS["surface"], 
                                           corner_radius=20)
        self.detail_container.pack(fill="both", expand=True, padx=40, pady=20)
        
        # Header paciente (siempre visible)
        header = ctk.CTkFrame(self.detail_container, fg_color=MEDICAL_COLORS["primary"], 
                             corner_radius=20)
        header.pack(fill="x", padx=30, pady=30)
        
        ctk.CTkLabel(header, text="👤", width=60, height=60, corner_radius=30,
                    fg_color="white", font=ctk.CTkFont(size=24)).pack(side="left", padx=20, pady=15)
        ctk.CTkLabel(header, text=patient[1], font=ctk.CTkFont(size=24, weight="bold"),
                    text_color="white").pack(side="left", pady=22)
        
        # Botones acción (dinámicos)
        self.btn_frame = ctk.CTkFrame(self.detail_container)
        self.btn_frame.pack(fill="x", padx=30, pady=20)
        
        if self.current_mode == "detail":
            ctk.CTkButton(self.btn_frame, text="📋 Clinic History", width=140, height=45,
                         command=lambda: self.show_clinic_history(patient),
                         fg_color=MEDICAL_COLORS["success"]).pack(side="left", padx=10)
            ctk.CTkButton(self.btn_frame, text="✏️ Edit Patient", width=140, height=45,
                         command=lambda: self.edit_patient(patient), 
                         fg_color="#f59e0b").pack(side="left", padx=10)
        else:  # history
            ctk.CTkButton(self.btn_frame, text="👤 Patient Details", width=140, height=45,
                         command=lambda: self.show_patient_detail(patient),
                         fg_color=MEDICAL_COLORS["primary"]).pack(side="left", padx=10)
        
        # Contenido dinámico
        if self.current_mode == "detail":
            self.render_patient_info(patient)
        else:
            self.render_clinic_history(patient)
    
    def render_patient_info(self, patient):
        """Renderiza información del paciente"""
        info_scroll = ctk.CTkScrollableFrame(self.detail_container)
        info_scroll.pack(fill="both", expand=True, padx=30, pady=(0, 0))
        
        fields = [
            ("Patient ID", patient[0]),
            ("Phone", patient[2] or "No phone"),
            ("Email", patient[3] or "No email"),
            ("Birth Date", patient[4] or "No date"),
            ("Address", patient[5] or "No address"),
            ("Gender", patient[6] or "Not specified")
        ]
        
        for i, (label, value) in enumerate(fields):
            row = ctk.CTkFrame(info_scroll, fg_color=MEDICAL_COLORS["background"])
            row.grid(row=i, column=0, sticky="ew", padx=20, pady=8)
            
            row.grid_columnconfigure(0, weight=0)
            row.grid_columnconfigure(1, weight=1)
            
            ctk.CTkLabel(row, text=f"{label}:", font=ctk.CTkFont(size=14, weight="bold"),
                        width=120).grid(row=0, column=0, sticky="w", padx=(15, 5), pady=10)
            
            ctk.CTkLabel(row, text=value, font=ctk.CTkFont(size=13), 
                        text_color=MEDICAL_COLORS["text_secondary"]).grid(row=0, column=1, sticky="w", padx=(0, 15), pady=10)
    
    def render_clinic_history(self, patient):
        """Renderiza tabla de historial clínico"""
        table_frame = ctk.CTkScrollableFrame(self.detail_container)
        table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 0))
        
        # Headers - ANCHO EXACTO
        headers_frame = ctk.CTkFrame(table_frame, fg_color=MEDICAL_COLORS["glass"])
        headers_frame.pack(fill="x", pady=(20,10))
        
        # headers = ["Date", "Procedure", "Aligner #", "IPR", "Photos", "Scan", "Notes"]
        headers = ["Date", "Procedure", "Notes"]
        
        # ANCHOS EXACTOS para alineación perfecta
        header_widths = [150, 250, 400]
        for i, header_text in enumerate(headers):
            lbl = ctk.CTkLabel(headers_frame, text=header_text, 
                            font=ctk.CTkFont(weight="bold", size=13),
                            width=header_widths[i],  # ← EXACTO
                            anchor="w")
            lbl.pack(side="left", padx=(0, 10) if i < 2 else (0, 0))
        
        # Carga visitas
        visits = self.db.get_patient_visits(patient[0])
        
        if not visits:
            no_history = ctk.CTkLabel(table_frame, text="📭 No clinic history yet", 
                                    font=ctk.CTkFont(size=18), 
                                    text_color=MEDICAL_COLORS["text_secondary"])
            no_history.pack(expand=True, pady=50)
        else:
            for visit in visits:
                row_frame = ctk.CTkFrame(table_frame, fg_color=MEDICAL_COLORS["glass"], height=60)
                row_frame.pack(fill="x", pady=4)
                row_frame.pack_propagate(False)
                
                '''
                for i, data in enumerate(visit):
                    lbl = ctk.CTkLabel(row_frame, text=str(data), 
                                    font=ctk.CTkFont(size=12),
                                    width=120 if i < 6 else 250,
                                    anchor="w")
                    lbl.pack(side="left", padx=8, pady=8)
                '''
                # SOLO date (indice 0),procedure (índice 1), notes (índice 6)
                # DATE - ancho exacto + bold
                ctk.CTkLabel(row_frame, text=visit[0] or "-",  
                            font=ctk.CTkFont(size=12, weight="bold"),
                            width=header_widths[0], height=60,  # ← height para centrar vertical
                            anchor="w", justify="left").pack(side="left", padx=15, pady=0, fill="y")
                
                # PROCEDURE - ancho exacto + bold
                ctk.CTkLabel(row_frame, text=visit[1] or "-",  
                            font=ctk.CTkFont(size=12, weight="bold"),
                            width=header_widths[1], height=60,
                            anchor="w", justify="left").pack(side="left", padx=0, pady=0, fill="y")
                
                # NOTES - ancho exacto + MULTILÍNEA
                notes_label = ctk.CTkLabel(row_frame, text=visit[6] or "-",  
                                        font=ctk.CTkFont(size=12),
                                        width=header_widths[2], height=60,
                                        anchor="w", justify="left", wraplength=380)  # ← WRAPLINEA
                notes_label.pack(side="left", padx=0, pady=0, fill="y")


            
    def load_patients(self, search=""):
        if self.current_mode != "list":
            return
        
        for child in self.patients_frame.winfo_children():
            child.destroy()
        
        patients = self.db.get_patients(search)
        for patient in patients:
            self.create_patient_card(patient)
    
    def create_patient_card(self, patient):
        card = ctk.CTkFrame(self.patients_frame, fg_color="#f8fafc", 
                          border_width=3, corner_radius=12, height=60)
        card.pack_propagate(False)
        card.pack(fill="x", padx=20, pady=10)
        card.patient_data = patient
        
        info_frame = ctk.CTkFrame(card, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=20, pady=15)
        
        ctk.CTkLabel(info_frame, text=f"👤 {patient[1]}", 
                    font=ctk.CTkFont(size=16, weight="bold")).pack(anchor="w")
        
        view_btn = ctk.CTkButton(card, text="👁️ View", width=100, height=35,
                                command=lambda c=card: self.show_patient_detail(c.patient_data),
                                fg_color=MEDICAL_COLORS["primary"])
        view_btn.pack(side="right", padx=20, pady=15)
    
    def on_search(self, event=None):
        self.load_patients(self.search_entry.get())
    
    def add_patient(self):
        from gui.add_patient_dialogs import PatientDialog
        PatientDialog(self.parent.master, self.load_patients, mode="add")
    
    def edit_patient(self, patient):
        from gui.add_patient_dialogs import PatientDialog
        PatientDialog(self.parent.master, self.show_list_view, patient=patient, mode="edit")
