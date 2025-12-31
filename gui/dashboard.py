import customtkinter as ctk
from datetime import date, datetime, time, timedelta
from core.theme import MEDICAL_COLORS
from gui.components import create_stat_card
from tkcalendar import DateEntry
import tkinter as tk

class HomeView:
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.master.db
        self.create_medical_home()
    
    def create_medical_home(self):
        # 1. HEADER (fila 0)
        header = ctk.CTkFrame(self.parent, corner_radius=20, fg_color=MEDICAL_COLORS["navy_hover"])
        header.configure(width=400, height=100)
        header.pack_propagate(False)
        header.pack(pady=(10, 20), anchor="center")

        ctk.CTkLabel(header, text="👋 Good Morning", font=ctk.CTkFont(size=16, weight="bold"), text_color="white").place(x=30, y=20)
        ctk.CTkLabel(header, text="Check available appointment slots", font=ctk.CTkFont(size=13), text_color=MEDICAL_COLORS["light_blue"]).place(x=30, y=55)

        today = date.today().isoformat()
        total_patients = self.db.conn.execute("SELECT COUNT(*) FROM patients").fetchone()[0]
        today_appts = self.db.conn.execute("SELECT COUNT(*) FROM appointments WHERE appointment_date=?", (today,)).fetchone()[0]

        # Stats GRID 2x3
        stats_grid = ctk.CTkFrame(self.parent, fg_color="transparent")
        stats_grid.configure(width=950, height=220)
        stats_grid.pack_propagate(False)
        stats_grid.pack(pady=(0, 30), anchor="center")

        # Configurar columnas
        for i in range(3):
            stats_grid.grid_columnconfigure(i, weight=1)
        stats_grid.grid_rowconfigure(0, weight=1)
        stats_grid.grid_rowconfigure(1, weight=1)

        # Fila 1
        create_stat_card(stats_grid, "Total Patients", total_patients, "text_primary", "👥", 0, 0)
        create_stat_card(stats_grid, "Today's Appts", today_appts, "navy_hover", "📅", 0, 1)
        create_stat_card(stats_grid, "Active Treatments", 24, "text_primary", "⚙️", 0, 2)

        # Fila 2 
        create_stat_card(stats_grid, "Pending Claims", 3, "warning", "💰", 1, 0)
        create_stat_card(stats_grid, "Revenue YTD", "$45,230", "success", "📈", 1, 1)
        create_stat_card(stats_grid, "Avg Rating", "4.8⭐", "primary", "⭐", 1, 2)

        # 3. AVAILABLE SLOTS SECTION (reemplaza Recent Activity)
        self.slots_section = ctk.CTkFrame(self.parent)
        self.slots_section.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        ctk.CTkLabel(self.slots_section, text="🕒 Available Time Slots", font=ctk.CTkFont(size=22, weight="bold"), text_color=MEDICAL_COLORS["text_primary"]).pack(pady=(25, 15))

        # Filtro por día
        filter_frame = ctk.CTkFrame(self.slots_section)
        filter_frame.pack(fill="x", padx=20, pady=(0, 20))

        ctk.CTkLabel(filter_frame, text="📅 Select date:", font=ctk.CTkFont(weight="bold")).pack(side="left", padx=(20, 10), pady=15)
        
        self.slot_date_entry = DateEntry(
            filter_frame, 
            width=12, 
            background=MEDICAL_COLORS["primary"],
            foreground="white", 
            borderwidth=2, 
            date_pattern="yyyy-mm-dd"
        )
        self.slot_date_entry.set_date(date.today())
        self.slot_date_entry.pack(side="left", padx=10, pady=15)

        ctk.CTkButton(
            filter_frame, 
            text="🔍 Check Availability", 
            width=160, height=35,
            command=self.load_available_slots,
            font=ctk.CTkFont(weight="bold")
        ).pack(side="left", padx=10, pady=15)

        # SCROLL area con altura FIJA para tabla
        self.slots_scroll = ctk.CTkScrollableFrame(
            self.slots_section,
            fg_color=MEDICAL_COLORS["background"],
            corner_radius=12,
            height=500
        )
        self.slots_scroll.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Primera carga automática
        self.load_available_slots()

    def get_day_appointments(self, day_str: str):
        """Devuelve diccionario { 'HH:MM': (procedure, patient_name) } para citas del día"""
        c = self.db.conn.cursor()
        c.execute("""
            SELECT appointment_time, procedure, 
                   COALESCE(p.name, 'Unknown') as patient_name
            FROM appointments a 
            LEFT JOIN patients p ON a.patient_id = p.id
            WHERE appointment_date = ? AND status IN ('Scheduled', 'Confirmed')
        """, (day_str,))
        rows = c.fetchall()
        slots = {}
        for time_slot, proc, name in rows:
            if time_slot:  # Solo si tiene hora
                slots[time_slot] = (proc or "Procedure", name)
        return slots

    def generate_time_slots(self, start_hour=7, end_hour=21, step_minutes=20):
        """Genera slots cada 20 min: 07:00, 07:20, 07:40...20:40"""
        slots = []
        current = datetime.combine(date.today(), time(start_hour, 0))
        end = datetime.combine(date.today(), time(end_hour, 0))
        delta = timedelta(minutes=step_minutes)
        
        while current < end:
            slots.append(current.strftime("%H:%M"))
            current += delta
        return slots

    def load_available_slots(self):
        """Carga y muestra tabla de slots disponibles"""
        # Limpiar contenido anterior
        for widget in self.slots_scroll.winfo_children():
            widget.destroy()

        # Fecha seleccionada
        selected_date = self.slot_date_entry.get_date().strftime("%Y-%m-%d")

        # Obtener citas del día
        booked_slots = self.get_day_appointments(selected_date)

        # Generar todos los slots posibles (7:00-21:00 cada 20 min)
        all_slots = self.generate_time_slots(7, 21, 20)

        # HEADER de la tabla
        header_frame = ctk.CTkFrame(self.slots_scroll, fg_color=MEDICAL_COLORS["navy_hover"])
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(header_frame, text="Time Slot", width=120, font=ctk.CTkFont(weight="bold", size=13), 
                    text_color="white", anchor="w").grid(row=0, column=0, padx=20, pady=12, sticky="w")
        ctk.CTkLabel(header_frame, text="Status", width=120, font=ctk.CTkFont(weight="bold", size=13), 
                    text_color="white", anchor="center").grid(row=0, column=1, padx=10, pady=12)
        ctk.CTkLabel(header_frame, text="Patient / Procedure", font=ctk.CTkFont(weight="bold", size=13), 
                    text_color="white", anchor="w").grid(row=0, column=2, padx=10, pady=12, sticky="w")

        # FILAS de slots
        for i, slot_time in enumerate(all_slots):
            row_frame = ctk.CTkFrame(self.slots_scroll)
            row_frame.pack(fill="x", padx=20, pady=4)

            # Columna 1: Hora
            ctk.CTkLabel(row_frame, text=slot_time, width=120, anchor="w", 
                        font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=0, sticky="w", padx=20, pady=8)

            # Columna 2: Status
            if slot_time in booked_slots:
                status_text = "Booked"
                status_color = MEDICAL_COLORS["danger"]
                proc, patient = booked_slots[slot_time]
                info_text = f"{patient} - {proc}"
            else:
                status_text = "Available"
                status_color = MEDICAL_COLORS["success"]
                info_text = "Ready to book"

            status_label = ctk.CTkLabel(
                row_frame, 
                text=status_text, 
                width=120, 
                fg_color=status_color, 
                text_color="white",
                corner_radius=8,
                anchor="center",
                font=ctk.CTkFont(size=11, weight="bold")
            )
            status_label.grid(row=0, column=1, sticky="w", padx=10, pady=8)

            # Columna 3: Info
            info_label = ctk.CTkLabel(
                row_frame, 
                text=info_text, 
                anchor="w",
                font=ctk.CTkFont(size=11)
            )
            info_label.grid(row=0, column=2, sticky="w", padx=10, pady=8)

        # Info final
        summary_frame = ctk.CTkFrame(self.slots_scroll, fg_color="transparent")
        summary_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        available_count = len([s for s in all_slots if s not in booked_slots])
        ctk.CTkLabel(
            summary_frame,
            text=f"✅ {available_count} slots available on {selected_date}",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color=MEDICAL_COLORS["success"]
        ).pack(anchor="e", padx=20, pady=10)
