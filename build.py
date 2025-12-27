import subprocess
import sys
import shutil

def build_exe():
    cmd = [
        "pyinstaller", "main.py",
        "--onefile",
        "--windowed",
        "--name", "AngelAligner-Pro",
        "--icon=assets/icon.ico",
        "--add-data", "angel_aligner.db;.",
        "--add-data", "templates;templates",
        "--add-data", ".env;.env",
        "--hidden-import", "customtkinter",
        "--collect-all", "customtkinter"
    ]
    
    subprocess.run(cmd)
    print("✅ Build completado: dist/AngelAligner-Pro.exe")

if __name__ == "__main__":
    build_exe()
