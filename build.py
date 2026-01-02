# build.py - TU CÓDIGO MEJORADO
import subprocess
import sys
import os
import shutil

def build_exe():
    # 🧹 Limpieza previa
    for path in ["build", "dist", "AngelAligner-Pro.spec"]:
        if os.path.exists(path):
            shutil.rmtree(path) if os.path.isdir(path) else os.remove(path)
    
    cmd = [
        "pyinstaller", "main.py",
        "--onefile",
        "--windowed",
        "--name", "AngelAligner-Pro",
        "--icon=assets/icon.ico",
        "--add-data", "angel_aligner.db;.",
        "--add-data", "templates;templates",
        "--add-data", ".env;.",  # ← ya lo tienes perfecto
        "--hidden-import", "customtkinter",
        "--collect-all", "customtkinter",
        "--noconfirm",  # no pregunta antes de borrar
        "--clean"       # limpia cache PyInstaller
    ]
    
    print("🚀 Build iniciado...")
    print("Ejecutando:", " ".join(cmd))
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ Build completado: dist/AngelAligner-Pro.exe")
        print("📦 Tamaño:", os.path.getsize("dist/AngelAligner-Pro.exe") / (1024*1024), "MB")
    else:
        print("❌ Error:", result.stderr)

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    build_exe()
