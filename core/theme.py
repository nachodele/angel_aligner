# core/theme.py
import customtkinter as ctk

def apply_medical_theme():
    """Aplica tema médico profesional global"""
    
    # Configuración base
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("blue")
    
    # Colores médicos profesionales
    MEDICAL_COLORS = {
        "primary": "#3b82f6",      # Azul médico principal
        "primary_hover": "#1d4ed8",
        "success": "#10b981",      # Verde progreso
        "warning": "#f59e0b",      # Alerta naranja
        "danger": "#ef4444",       # Rojo cancelación
        "background": "#f8fafc",   # Fondo hielo
        "surface": "#ffffff",      # Superficies blancas
        "border": "#e2e8f0",       # Bordes sutiles
        "text_primary": "#1e293b", # Texto principal
        "text_secondary": "#64748b" # Texto secundario
    }

# Constantes de colores para usar en toda la app
MEDICAL_COLORS = {
    "primary": "#3b82f6",
    "primary_hover": "#1d4ed8",
    "success": "#10b981",
    "success_hover": "#059669",
    "warning": "#f59e0b",
    "warning_hover": "#d97706",
    "danger": "#ef4444",
    "danger_hover": "#dc2626",
    "background": "#f8fafc",
    "surface": "#ffffff",
    "glass": "#f1f5f9",
    "border": "#e2e8f0",
    "border_hover": "#cbd5e1",
    "text_primary": "#1e293b",
    "text_secondary": "#64748b",
    "text_tertiary": "#94a3b8",
    "white": "#ffffff",
    "light_blue": "#e0f2fe",
    "dark_navy": "#1e293b",
    "navy": "#334155",
    "navy_hover": "#475569"
}

def get_medical_style(component):
    """Devuelve estilos médicos por componente"""
    styles = {
        "header": {
            "bg": MEDICAL_COLORS["primary"],
            "text": MEDICAL_COLORS["white"],
            "text_secondary": MEDICAL_COLORS["light_blue"]
        },
        "navbar": {
            "bg": MEDICAL_COLORS["dark_navy"],
            "button_bg": MEDICAL_COLORS["navy"],
            "button_hover": MEDICAL_COLORS["navy_hover"],
            "text": "#f1f5f9",
            "accent": "#60a5fa"
        },
        "card": {
            "bg": MEDICAL_COLORS["surface"],
            "border": MEDICAL_COLORS["border"],
            "hover": MEDICAL_COLORS["glass"]
        },
        "button_primary": {
            "bg": MEDICAL_COLORS["primary"],
            "hover": MEDICAL_COLORS["primary_hover"],
            "text": MEDICAL_COLORS["white"]
        },
        "button_secondary": {
            "bg": MEDICAL_COLORS["glass"],
            "hover": MEDICAL_COLORS["surface"],
            "text": MEDICAL_COLORS["text_primary"]
        }
    }
    return styles.get(component, {})

if __name__ == "__main__":
    apply_medical_theme()
