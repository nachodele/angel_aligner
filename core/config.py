import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

class Config:
    APP_NAME = os.getenv("APP_NAME", "Angel Aligner")
    APP_VERSION = os.getenv("APP_VERSION", "1.0.0")
    DB_PATH = Path("angel_aligner.db")
    WHATSAPP_PHONE = os.getenv("WHATSAPP_PHONE")
    BACKUP_PATH = Path(os.getenv("BACKUP_PATH", "./backups"))
    LICENSE_KEY = os.getenv("LICENSE_KEY", "TRIAL")
    
    BACKUP_PATH.mkdir(exist_ok=True)
