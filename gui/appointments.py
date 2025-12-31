import customtkinter as ctk
from tkinter import messagebox
from tkcalendar import Calendar, DateEntry
from core.theme import MEDICAL_COLORS
from datetime import date
import tkinter as tk

class AppointmentsView(ctk.CTkFrame):
    def __init__(self, parent, db):
        super().__init__(parent)
        self.db = db
        self.app = parent.master
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_calendar_view()

    def create_calendar_view(self):
        # Header con filtros + NEW BUTTON
        header_frame = ctk.CTkFrame(self, corner_radius=15)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Filtro por fecha
        filter_frame = ctk.CTkFrame(header_frame)
        filter_frame.pack(side="left", padx=20, pady=15)
        
        ctk.CTkLabel(filter_frame, text="🔍 Filter by date:", 
                    font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        self.date_filter = DateEntry(
            filter_frame, width=12, background=MEDICAL_COLORS["primary"],
            foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd"
        )
        self.date_filter.set_date(date.today())
        self.date_filter.pack(pady=(5,0))
        
        ctk.CTkButton(filter_frame, text="Filter", width=80,
                     command=self.load_appointments).pack(pady=(10,0))
        
        # BOTÓN NEW APPOINTMENT
        ctk.CTkButton(header_frame, text="➕ New Appointment", width=160, height=35,
                     command=self.open_new_appointment, font=ctk.CTkFont(weight="bold")).pack(side="right", padx=20, pady=15)
        
        # MAIN CONTAINER
        main_container = ctk.CTkFrame(self)
        main_container.pack(fill="both", expand=True)
        
        CALENDAR_WIDTH = 520
        self.calendar_container = ctk.CTkFrame(main_container, width=CALENDAR_WIDTH)
        self.calendar_container.pack(side="left", fill="both", expand=False, padx=(20,15), pady=20)
        self.calendar_container.pack_propagate(False)
        
        ctk.CTkLabel(self.calendar_container, text="📅 Calendar", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=15)
        
        self.calendar = Calendar(self.calendar_container, selectmode="day", date_pattern="y-mm-dd",
                               font="Arial 11", background=MEDICAL_COLORS["primary"],
                               foreground="white", headersbackground=MEDICAL_COLORS["dark_navy"],
                               normalbackground=MEDICAL_COLORS["navy"], selectbackground=MEDICAL_COLORS["success"])
        self.calendar.pack(fill="both", expand=True, padx=15, pady=(0,15))
        self.calendar.bind("<<CalendarSelected>>", self.on_date_selected)
        
        list_container = ctk.CTkFrame(main_container)
        list_container.pack(side="left", fill="both", expand=True, padx=(0,20), pady=20)
        
        ctk.CTkLabel(list_container, text="📋 Appointments", 
                    font=ctk.CTkFont(size=18, weight="bold")).pack(pady=(15,10))
        
        canvas_frame = ctk.CTkFrame(list_container)
        canvas_frame.pack(fill="both", expand=True, padx=15, pady=(0,15))
        canvas_frame.grid_columnconfigure(0, weight=1)
        canvas_frame.grid_rowconfigure(0, weight=1)
        
        self.appointments_canvas = ctk.CTkCanvas(canvas_frame, highlightthickness=0)
        self.scrollbar_v = ctk.CTkScrollbar(canvas_frame, orientation="vertical", command=self.appointments_canvas.yview)
        self.scrollbar_h = ctk.CTkScrollbar(canvas_frame, orientation="horizontal", command=self.appointments_canvas.xview)
        self.scrollable_frame = ctk.CTkFrame(self.appointments_canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.appointments_canvas.configure(scrollregion=self.appointments_canvas.bbox("all"))
        )
        
        self.appointments_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.appointments_canvas.configure(yscrollcommand=self.scrollbar_v.set, xscrollcommand=self.scrollbar_h.set)
        
        self.appointments_canvas.grid(row=0, column=0, sticky="nsew")
        self.scrollbar_v.grid(row=0, column=1, sticky="ns")
        self.scrollbar_h.grid(row=1, column=0, sticky="ew")
        
        self.load_appointments()

    def open_new_appointment(self):
        """Abre diálogo de pacientes para seleccionar"""
        PatientSelectionDialog(self, self.db, self.new_appointment)

    def new_appointment(self, patient):
        """Crea nueva cita para paciente seleccionado"""
        # ✅ after_idle para evitar problemas de foco
        def open_appointment_dialog():
            AppointmentDialog(self.app, patient, self.db, self.load_appointments)
        self.after_idle(open_appointment_dialog)

    def load_appointments(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        try:
            filter_date = self.date_filter.get_date().strftime("%Y-%m-%d")
            appointments = self.db.get_appointments(filter_date)
            
            if not appointments:
                center_frame = ctk.CTkFrame(self.scrollable_frame, width=618)
                center_frame.pack(expand=True)
                center_frame.pack_propagate(False)
                
                no_appts = ctk.CTkLabel(
                    center_frame, 
                    text="📭 No appointments", 
                    font=ctk.CTkFont(size=20, weight="bold"), 
                    text_color="gray"
                )
                no_appts.pack(expand=True)
                return

            header_frame = ctk.CTkFrame(self.scrollable_frame)
            header_frame.pack(fill="x", pady=(0,10))
            
            headers = [("Time", 100), ("Patient", 200), ("Procedure", 180), ("Status", 120), ("Action", 140)]
            for col, (text, width) in enumerate(headers):
                lbl = ctk.CTkLabel(header_frame, text=text, width=width, 
                                 font=ctk.CTkFont(weight="bold", size=12), anchor="w")
                lbl.grid(row=0, column=col, sticky="w", padx=15, pady=12)
            
            for appt in appointments:
                self.create_appointment_row(appt)
            
            self.calendar.selection_set(filter_date)
            
        except Exception as e:
            print(f"Error: {e}")

    def create_appointment_row(self, appt):
        row_frame = ctk.CTkFrame(self.scrollable_frame)
        row_frame.pack(fill="x", pady=2, padx=5)
        
        patient_name = self.db.get_patient_name(appt[1])
        status_color = {"Scheduled": MEDICAL_COLORS["success"], 
                       "Completed": MEDICAL_COLORS["warning"],
                       "Cancelled": MEDICAL_COLORS["danger"],
                       "Rescheduled": MEDICAL_COLORS["primary"],
                       "No Show": "orange"}.get(appt[4], "gray")
        
        ctk.CTkLabel(row_frame, text=appt[3], width=100, anchor="center", 
                    font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", padx=15, pady=10)
        ctk.CTkLabel(row_frame, text=patient_name[:28]+"..." if len(patient_name)>28 else patient_name, 
                    width=200, anchor="w", font=ctk.CTkFont(weight="bold")).grid(row=0, column=1, sticky="w", padx=5, pady=10)
        ctk.CTkLabel(row_frame, text=(appt[5][:25] or "-")+"...", width=180, anchor="w").grid(row=0, column=2, sticky="w", padx=5, pady=10)
        ctk.CTkLabel(row_frame, text=appt[4], width=120, fg_color=status_color, 
                    corner_radius=6, padx=12, anchor="center").grid(row=0, column=3, sticky="w", padx=5, pady=10)
        
        action_frame = ctk.CTkFrame(row_frame)
        action_frame.grid(row=0, column=4, sticky="w", padx=5, pady=10)
        
        ctk.CTkButton(action_frame, text="Edit", width=60, height=30,
                     font=ctk.CTkFont(size=12), command=lambda: self.edit_appointment_status(appt[0])).pack(side="left", padx=(0,5))
        ctk.CTkButton(action_frame, text="Del", width=60, height=30, fg_color=MEDICAL_COLORS["danger"],
                     font=ctk.CTkFont(size=12), command=lambda: self.delete_appointment(appt[0])).pack(side="left")

    def delete_appointment(self, appointment_id):
        if messagebox.askyesno("🗑️ Delete Appointment", "¿Estás seguro de eliminar esta cita?"):
            try:
                c = self.db.conn.cursor()
                c.execute("DELETE FROM appointments WHERE id=?", (appointment_id,))
                self.db.conn.commit()
                self.load_appointments()
                messagebox.showinfo("✅ Deleted", "Cita eliminada correctamente")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {e}")

    def edit_appointment_status(self, appointment_id):
        StatusDialog(self, appointment_id, self.db)

    def on_date_selected(self, event):
        selected_date = self.calendar.selection_get()
        self.date_filter.set_date(selected_date)
        self.load_appointments()

# DIALOGO SELECCIÓN PACIENTE
class PatientSelectionDialog(ctk.CTkToplevel):
    def __init__(self, parent, db, callback):
        super().__init__(parent)
        self.db = db
        self.callback = callback
        self.title("👥 Select Patient")
        self.geometry("600x500")
        self.grab_set()
        
        self.selected_patient = None
        self.create_patient_selector()
    
    def create_patient_selector(self):
        header = ctk.CTkFrame(self, fg_color=MEDICAL_COLORS["primary"])
        header.pack(fill="x", padx=20, pady=20)
        ctk.CTkLabel(header, text="👥 Select Patient for New Appointment", 
                    font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(pady=20)
        
        search_frame = ctk.CTkFrame(self)
        search_frame.pack(fill="x", padx=20, pady=(0,10))
        ctk.CTkLabel(search_frame, text="🔍 Search:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="Enter patient name...")
        self.search_entry.pack(side="left", fill="x", expand=True, padx=(0,10))
        self.search_entry.bind("<KeyRelease>", self.on_search)
        
        list_frame = ctk.CTkFrame(self)
        list_frame.pack(fill="both", expand=True, padx=20, pady=(0,20))
        
        self.patient_listbox = ctk.CTkScrollableFrame(list_frame)
        self.patient_listbox.pack(fill="both", expand=True)
        
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=20, pady=20)
        
        ctk.CTkButton(btn_frame, text="✅ Create Appointment", width=200,
                     command=self.select_patient, font=ctk.CTkFont(weight="bold")).pack(side="right", padx=10)
        ctk.CTkButton(btn_frame, text="❌ Cancel", width=120,
                     fg_color="gray", command=self.destroy).pack(side="right")
        
        self.load_patients()
    
    def load_patients(self, search=""):
        for widget in self.patient_listbox.winfo_children():
            widget.destroy()
        
        patients = self.db.get_patients(search)
        
        if not patients:
            no_patients = ctk.CTkLabel(self.patient_listbox, text="No patients found", 
                                     font=ctk.CTkFont(size=16), text_color="gray")
            no_patients.pack(pady=50)
            return
        
        for patient in patients:
            patient_frame = ctk.CTkFrame(self.patient_listbox)
            patient_frame.pack(fill="x", pady=5, padx=10)
            
            info_label = ctk.CTkLabel(patient_frame, 
                                    text=f"{patient[1]} ({patient[2] if patient[2] else 'No phone'})",
                                    font=ctk.CTkFont(size=14, weight="bold"))
            info_label.pack(anchor="w", padx=15, pady=12)
            
            select_btn = ctk.CTkButton(patient_frame, text="➕ Select", width=100, height=30,
                                     command=lambda p=patient: self.select_patient_direct(p))
            select_btn.pack(anchor="e", padx=15, pady=12)
    
    def on_search(self, event):
        search_term = self.search_entry.get()
        self.load_patients(search_term)
    
    def select_patient_direct(self, patient):
        """Selecciona paciente directamente"""
        self.selected_patient = patient
        self.callback(patient)
        self.destroy()
    
    def select_patient(self):
        """Selecciona paciente del botón principal"""
        if self.selected_patient:
            self.callback(self.selected_patient)
            self.destroy()
        else:
            messagebox.showwarning("Warning", "Please select a patient first")

# APPOINTMENT DIALOG EMBEDDED (SIN ARCHIVO SEPARADO)
class AppointmentDialog(ctk.CTkToplevel):
    def __init__(self, parent, patient, db, callback):
        super().__init__(parent)
        self.patient_id = patient[0]
        self.patient_name = patient[1]
        self.db = db
        self.callback = callback
        self.title("📅 New Appointment")
        self.geometry("550x600")
        self.grab_set()
        self.resizable(False, False)
        
        self.date_selected = None
        self.appointment_time = None
        self.procedure_var = tk.StringVar()
        
        # LISTA DE PROCEDIMIENTOS COMUNES
        self.procedures = [
            "Consulta inicial", "Limpieza dental", "Empaste", "Extracción",
            "Blanqueamiento", "Ortodoncia consulta", "Endodoncia", "Prótesis",
            "Implante consulta", "Cirugía oral", "Revisión", "Emergencia"
        ]
        
        self.create_dialog()
    
    def create_dialog(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=MEDICAL_COLORS["primary"], corner_radius=15)
        header.pack(fill="x", padx=30, pady=30)
        
        ctk.CTkLabel(header, text="📅", font=ctk.CTkFont(size=24), text_color="white").pack(side="left", padx=20)
        ctk.CTkLabel(header, text=f"New Appointment for {self.patient_name}", 
                    font=ctk.CTkFont(size=20, weight="bold"), text_color="white").pack(pady=20)
        
        # Form
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=40, pady=(0,30))
        
        # Fecha
        ctk.CTkLabel(form_frame, text="📅 Date:", font=ctk.CTkFont(weight="bold", size=14)).pack(anchor="w", pady=(20,5))
        self.date_entry = DateEntry(form_frame, width=12, background=MEDICAL_COLORS["primary"],
                                   foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
        self.date_entry.set_date(date.today())
        self.date_entry.pack(pady=(0,20))
        
        # Hora
        ctk.CTkLabel(form_frame, text="⏰ Time:", font=ctk.CTkFont(weight="bold", size=14)).pack(anchor="w", pady=(0,5))
        time_container = ctk.CTkFrame(form_frame)
        time_container.pack(pady=(5,20))
        
        hours = [f"{h:02d}" for h in range(7, 22)]
        self.hour_menu = ctk.CTkOptionMenu(time_container, values=hours, width=80)
        self.hour_menu.set("14")
        self.hour_menu.pack(side="left", padx=(0,8))
        
        ctk.CTkLabel(time_container, text=":", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
        
        minutes = ["00", "10", "20", "30", "40", "50"]
        self.minute_menu = ctk.CTkOptionMenu(time_container, values=minutes, width=80)
        self.minute_menu.set("00")
        self.minute_menu.pack(side="left", padx=(8,0))
        
        # SELECCIÓN DE PROCEDIMIENTO (OptionMenu)
        ctk.CTkLabel(form_frame, text="📋 Procedure:", font=ctk.CTkFont(weight="bold", size=14)).pack(anchor="w", pady=(0,5))
        self.procedure_menu = ctk.CTkOptionMenu(
            form_frame, 
            values=self.procedures, 
            variable=self.procedure_var,
            width=300
        )
        self.procedure_menu.pack(fill="x", pady=(5,25))
        
        # Campo NOTAS opcional
        ctk.CTkLabel(form_frame, text="📝 Notes (optional):", font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(0,5))
        self.notes_entry = ctk.CTkEntry(form_frame, height=35, placeholder_text="Additional notes...")
        self.notes_entry.pack(fill="x", pady=(5,0))
        
        # Botones
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(fill="x", padx=40, pady=30)
        
        ctk.CTkButton(btn_frame, text="✅ Schedule Appointment", width=200, height=45,
                     command=self.save_appointment, font=ctk.CTkFont(weight="bold", size=14)).pack(side="right", padx=10)
        ctk.CTkButton(btn_frame, text="❌ Cancel", width=120, height=45,
                     fg_color="gray", command=self.destroy).pack(side="right")
    
    def check_time_conflict(self, date_str, time_str):
        """VERIFICA CONFLICTO DE TIEMPO EN ESA FECHA/HORA"""
        try:
            c = self.db.conn.cursor()
            c.execute("""
                SELECT id, procedure, 
                       (SELECT name FROM patients WHERE patients.id = appointments.patient_id) as patient_name
                FROM appointments 
                WHERE appointment_date=? AND appointment_time=? AND status IN ('Scheduled', 'Confirmed')
            """, (date_str, time_str))
            conflict = c.fetchone()
            return conflict
        except:
            return None
    
    def save_appointment(self):
        """GUARDA CITA CON VERIFICACIÓN DE CONFLICTOS"""
        self.date_selected = self.date_entry.get_date().strftime("%Y-%m-%d")
        self.appointment_time = f"{self.hour_menu.get()}:{self.minute_menu.get()}"
        procedure = self.procedure_var.get().strip()
        notes = self.notes_entry.get().strip()
        
        if not procedure:
            messagebox.showwarning("⚠️ Warning", "Please select a procedure.")
            return
        
        # VERIFICAR CONFLICTO CON NOMBRE PACIENTE / TIEMPO
        conflict = self.check_time_conflict(self.date_selected, self.appointment_time)
        if conflict:
            conflict_id, conflict_procedure, conflict_patient = conflict
            messagebox.showwarning(
                "⚠️ Time Conflict", 
                f"Ya existe una cita a las {self.appointment_time}:\n\n"
                f"👤 {conflict_patient}\n"
                f"📋 {conflict_procedure}\n\n"
                f"Por favor, elige otro horario."
            )
            return
        
        try:
            self.db.add_appointment(
                patient_id=self.patient_id,
                appointment_date=self.date_selected,
                appointment_time=self.appointment_time,
                procedure=procedure,
                notes=notes,
                status="Scheduled"  # POR DEFECTO
            )
            
            messagebox.showinfo("✅ Success", f"Appointment scheduled!\n\n"
                                        f"👤 {self.patient_name}\n"
                                        f"📅 {self.date_selected}\n"
                                        f"🕒 {self.appointment_time}\n"
                                        f"📋 {procedure}")
            
            self.destroy()
            if self.callback:
                self.callback()
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")

# StatusDialog CORREGIDO (SIN ERRORES DE FOCO)
# StatusDialog CORREGIDO - Botón Update SIEMPRE VISIBLE
class StatusDialog(ctk.CTkToplevel):
    def __init__(self, parent, appointment_id, db):
        super().__init__(parent)
        self.appointment_id = appointment_id
        self.db = db
        self.title("✏️ Edit Appointment Status")
        self.geometry("500x500")  # ✅ Más alto
        self.grab_set()
        self.resizable(False, False)
        
        # Cargar datos actuales
        c = self.db.conn.cursor()
        c.execute("SELECT status, appointment_date, appointment_time FROM appointments WHERE id=?", (appointment_id,))
        current_data = c.fetchone()
        self.current_status = current_data[0]
        self.current_date = current_data[1]
        self.current_time = current_data[2] if current_data[2] else "14:00"
        
        self.status_var = tk.StringVar(value=self.current_status)
        self.date_frame = None
        self.new_date_entry = None
        self.new_time_hour = None
        self.new_time_minute = None
        
        self.create_dialog()
    
    def create_dialog(self):
        # Header
        header = ctk.CTkFrame(self, fg_color=MEDICAL_COLORS["primary"], corner_radius=15)
        header.pack(fill="x", padx=30, pady=30)
        
        ctk.CTkLabel(header, text="✏️", font=ctk.CTkFont(size=24), text_color="white").pack(side="left", padx=20)
        ctk.CTkLabel(header, text="Update Appointment Status", font=ctk.CTkFont(size=20, weight="bold"), 
                    text_color="white").pack(pady=20)
        
        # Form frame
        form_frame = ctk.CTkFrame(self)
        form_frame.pack(fill="both", expand=True, padx=40, pady=(0,30))
        
        # Status selector
        status_frame = ctk.CTkFrame(form_frame)
        status_frame.pack(fill="x", pady=20)
        ctk.CTkLabel(status_frame, text="Status:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
        
        statuses = ["Scheduled", "Completed", "Rescheduled", "Cancelled", "No Show"]
        self.status_menu = ctk.CTkOptionMenu(status_frame, values=statuses, variable=self.status_var,
                                           command=self.on_status_change)
        self.status_menu.pack(pady=(10,0), fill="x")
        
        # Botones
        btn_frame = ctk.CTkFrame(self)
        btn_frame.pack(pady=20)
        
        ctk.CTkButton(btn_frame, text="✅ Update", width=120, height=40,
                     command=self.update_status, font=ctk.CTkFont(weight="bold")).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="❌ Cancel", width=120, height=40,
                     fg_color="gray", command=self.destroy).pack(side="left", padx=10)
    
    def on_status_change(self, status):
        """Muestra/oculta fecha+hora según estado"""
        # ✅ LIMPIA frame anterior
        if hasattr(self, 'date_frame') and self.date_frame:
            self.date_frame.destroy()
        
        if status == "Rescheduled":
            # ✅ CORRECTO: frame en form_frame (self)
            self.date_frame = ctk.CTkFrame(self.children['!ctkframe'])  # form_frame
            self.date_frame.pack(fill="x", pady=20)
            
            # Fecha
            ctk.CTkLabel(self.date_frame, text="📅 New Date:", font=ctk.CTkFont(weight="bold")).pack(anchor="w", pady=(0,5))
            
            self.new_date_entry = DateEntry(self.date_frame, width=12, background=MEDICAL_COLORS["primary"],
                                          foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd")
            self.new_date_entry.set_date(date.today())
            self.new_date_entry.pack(pady=(0,15))
            
            # Hora
            ctk.CTkLabel(self.date_frame, text="⏰ New Time:", font=ctk.CTkFont(weight="bold")).pack(anchor="w")
            
            time_container = ctk.CTkFrame(self.date_frame)
            time_container.pack(pady=(5,0))
            
            # Horas 07-21
            hours = [f"{h:02d}" for h in range(7, 22)]
            self.new_time_hour = ctk.CTkOptionMenu(time_container, values=hours, width=80)
            self.new_time_hour.set(self.current_time[:2])
            self.new_time_hour.pack(side="left", padx=(0,8))
            
            ctk.CTkLabel(time_container, text=":", font=ctk.CTkFont(size=18, weight="bold")).pack(side="left")
            
            # Minutos
            minutes = ["00", "10", "20", "30", "40", "50"]
            self.new_time_minute = ctk.CTkOptionMenu(time_container, values=minutes, width=80)
            self.new_time_minute.set(self.current_time[3:])
            self.new_time_minute.pack(side="left", padx=(8,0))
    
    def update_status(self):
        new_status = self.status_var.get()
        
        try:
            c = self.db.conn.cursor()
            
            if new_status == "Rescheduled" and self.new_date_entry and self.new_time_hour and self.new_time_minute:
                new_date = self.new_date_entry.get_date().strftime("%Y-%m-%d")
                new_time = f"{self.new_time_hour.get()}:{self.new_time_minute.get()}"
                c.execute("UPDATE appointments SET status=?, appointment_date=?, appointment_time=? WHERE id=?",
                        (new_status, new_date, new_time, self.appointment_id))
            else:
                c.execute("UPDATE appointments SET status=? WHERE id=?", 
                        (new_status, self.appointment_id))
            
            # 🔥 NUEVA LÓGICA: Si status=Completed → mover a Visits
            if new_status == "Completed":
                if self.db.add_visit_from_appointment(self.appointment_id):
                    messagebox.showinfo("✅ Completed", "Appointment moved to patient history!")
                else:
                    messagebox.showwarning("⚠️ Warning", "Could not move to history")
            
            self.db.conn.commit()
            self.master.load_appointments()
            self.destroy()
            
        except Exception as e:
            messagebox.showerror("❌ Error", f"Update failed: {str(e)}")

            
        except Exception as e:
            print(f"Update error: {e}")

