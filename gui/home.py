# gui/home.py
import customtkinter as ctk
from datetime import date
from core.theme import MEDICAL_COLORS
from gui.components import create_stat_card


class HomeView:
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.master.db
        self.create_medical_home()
    
    def create_medical_home(self):
        # Header hero
        header = ctk.CTkFrame(
            self.parent,
            corner_radius=20,
            fg_color=MEDICAL_COLORS["navy_hover"],
        )
        header.configure(width=400, height=100)  # largo controlado
        header.pack(pady=(10, 20), anchor="center")  # IMPORTANTE: pack
        header.pack_propagate(False)

        ctk.CTkLabel(
            header,
            text="👋 Good Morning",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="white",
        ).place(x=30, y=20)

        ctk.CTkLabel(
            header,
            text="Here's what's happening with your practice today",
            font=ctk.CTkFont(size=13),
            text_color=MEDICAL_COLORS["light_blue"],
        ).place(x=30, y=55)

        # Stats row
        stats_container = ctk.CTkFrame(self.parent, fg_color="transparent")
        stats_container.configure(width=400, height=100)
        stats_container.pack(pady=(10, 20), anchor="center")  # IMPORTANTE: pack

        today = date.today().isoformat()
        total_patients = self.db.conn.execute(
            "SELECT COUNT(*) FROM patients"
        ).fetchone()[0]
        today_appts = self.db.conn.execute(
            "SELECT COUNT(*) FROM appointments WHERE appointment_date=?",
            (today,),
        ).fetchone()[0]

        create_stat_card(stats_container, "Total Patients", total_patients, "text_primary", "👥")
        create_stat_card(stats_container, "Today's Appts", today_appts, "navy_hover", "📅")
        create_stat_card(stats_container, "Active Treatments", 24, "text_primary", "⚙️")

        # Recent activity (igual que antes)
        activity_section = ctk.CTkFrame(self.parent)
        activity_section.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        title = ctk.CTkLabel(
            activity_section,
            text="Recent Activity",
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=MEDICAL_COLORS["text_primary"],
        )
        title.pack(pady=(25, 15))

        scroll = ctk.CTkScrollableFrame(
            activity_section,
            fg_color=MEDICAL_COLORS["background"],
            corner_radius=12,
        )
        scroll.pack(fill="both", expand=True, pady=10)

        try:
            recent = self.db.conn.execute(
                """
                SELECT a.appointment_date, p.name, a.procedure, a.status 
                FROM appointments a LEFT JOIN patients p ON a.patient_id = p.id 
                ORDER BY a.appointment_date DESC LIMIT 10
                """
            ).fetchall()

            if not recent:
                ctk.CTkLabel(
                    scroll,
                    text="📭 No recent activity. Add your first patient!",
                    font=ctk.CTkFont(size=14),
                    text_color=MEDICAL_COLORS["text_secondary"],
                ).pack(expand=True)
            else:
                for appt in recent:
                    ctk.CTkLabel(
                        scroll,
                        text=f"📅 {appt[0] or 'N/A'} - {appt[1] or 'Unknown'}: {appt[2] or 'N/A'}",
                        font=ctk.CTkFont(size=14),
                        text_color=MEDICAL_COLORS["text_primary"],
                    ).pack(fill="x", padx=20, pady=12)
        except:
            ctk.CTkLabel(
                scroll,
                text="📭 Getting started... Add patients to see activity here",
                font=ctk.CTkFont(size=14),
                text_color=MEDICAL_COLORS["text_secondary"],
            ).pack(expand=True)
