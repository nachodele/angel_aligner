# gui/components.py
import customtkinter as ctk
from core.theme import MEDICAL_COLORS

def create_stat_card(parent, title, value, color_key="primary", icon="📊", row=0, col=0):
    """Stat card para GRID 2x3 - NO usa pack()"""
    color = MEDICAL_COLORS.get(color_key, MEDICAL_COLORS["primary"])

    card = ctk.CTkFrame(
        parent,
        width=300,
        height=100,
        corner_radius=12,
        fg_color=color,
        border_width=0,
    )
    
    # ✅ SOLO GRID, NUNCA pack()
    card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")
    card.grid_propagate(False)

    ctk.CTkLabel(
        card,
        text=icon,
        font=ctk.CTkFont(size=22),
        text_color="white",
    ).place(x=18, y=18)

    ctk.CTkLabel(
        card,
        text=str(value),
        font=ctk.CTkFont(size=18, weight="bold"),
        text_color="white",
    ).place(x=70, y=16)

    ctk.CTkLabel(
        card,
        text=title,
        font=ctk.CTkFont(size=11),
        text_color=MEDICAL_COLORS["light_blue"],
    ).place(x=70, y=40)

    return card

def create_patient_card(parent, patient, on_view):
    """Patient card (usa pack porque es lista vertical)"""
    card = ctk.CTkFrame(
        parent,
        height=85,
        corner_radius=12,
        fg_color=MEDICAL_COLORS["surface"],
        border_width=1,
        border_color=MEDICAL_COLORS["border"],
    )
    card.pack(fill="x", padx=20, pady=8)
    card.pack_propagate(False)

    avatar = ctk.CTkLabel(
        card,
        text="👤",
        width=32,
        height=32,
        corner_radius=16,
        fg_color=MEDICAL_COLORS.get("glass", "#e2e8f0"),
        font=ctk.CTkFont(size=16),
    )
    avatar.place(x=18, y=18)

    ctk.CTkLabel(
        card,
        text=patient[1],
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color=MEDICAL_COLORS["text_primary"],
    ).place(x=70, y=18)

    ctk.CTkLabel(
        card,
        text=f"📱 {patient[2] or 'No phone'}",
        font=ctk.CTkFont(size=11),
        text_color=MEDICAL_COLORS["text_secondary"],
    ).place(x=70, y=40)

    view_btn = ctk.CTkButton(
        card,
        text="View",
        width=60,
        height=24,
        corner_radius=6,
        fg_color=MEDICAL_COLORS["primary"],
        hover_color=MEDICAL_COLORS["primary_hover"],
        text_color="white",
        font=ctk.CTkFont(size=10, weight="bold"),
        command=lambda: on_view(patient),
    )
    view_btn.place(x=300, y=24)  # ← Posición fija

    return card
