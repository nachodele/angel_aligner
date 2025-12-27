# gui/components.py
import customtkinter as ctk
from core.theme import MEDICAL_COLORS, BUTTON_SIZES


def create_stat_card(parent, title, value, color_key="primary", icon="📊"):
    color = MEDICAL_COLORS.get(color_key, MEDICAL_COLORS["primary"])

    card = ctk.CTkFrame(
        parent,
        height=70,
        corner_radius=12,
        fg_color=color,
        border_width=0,
    )
    card.configure(width=400, height=100)            # largo del panel
    card.pack(padx=0, pady=6)           # IMPORTANTE: pack
    card.pack_propagate(False)

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
    card = ctk.CTkFrame(
        parent,
        height=72,
        corner_radius=12,
        fg_color=MEDICAL_COLORS["surface"],
        border_width=1,
        border_color=MEDICAL_COLORS["border"],
    )
    card.configure(width=400, height=100)
    card.pack(padx=20, pady=8)          # IMPORTANTE: pack
    card.pack_propagate(False)

    avatar = ctk.CTkLabel(
        card,
        text="👤",
        width=32,
        height=32,
        corner_radius=16,
        fg_color=MEDICAL_COLORS["glass"],
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
    view_btn.place(x=card.winfo_reqwidth() - 90, y=24)

    return card
