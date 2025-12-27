import sqlite3
from datetime import datetime
from core.config import Config

STATUS_CHOICES = ["Scheduled", "Completed", "Cancelled", "No Show"]
PROCEDURE_CHOICES = ["IPR", "Aligner Change", "Adjustment", "Photos Taken", "Intraoral Scan", "Progress Review"]
ALIGNER_TYPE_CHOICES = ["Angel Aligners", "Brackets", "Hybrid"]

class Database:
    def __init__(self):
        self.conn = sqlite3.connect(Config.DB_PATH, check_same_thread=False)
        self.init_tables()
    
    def init_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS patients 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT NOT NULL, phone TEXT, email TEXT, 
                     birth_date TEXT, address TEXT, gender TEXT, 
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS appointments 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     patient_id INTEGER, appointment_date TEXT,
                     status TEXT DEFAULT 'Scheduled', procedure TEXT, 
                     aligner_number INTEGER, aligner_type TEXT, notes TEXT,
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        c.execute('''CREATE TABLE IF NOT EXISTS visits 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     patient_id INTEGER, visit_date TEXT,
                     procedure TEXT, aligner_number INTEGER, ipr TEXT, 
                     photos BOOLEAN DEFAULT 0, scan BOOLEAN DEFAULT 0, notes TEXT)''')
        
        self.conn.commit()
    
    def get_patients(self, search=""):
        c = self.conn.cursor()
        query = "SELECT * FROM patients WHERE name LIKE ? ORDER BY name"
        patients = c.execute(query, (f"%{search}%",)).fetchall()
        return patients
    
    def add_patient(self, **data):
        c = self.conn.cursor()
        c.execute('''INSERT INTO patients (name, phone, email, birth_date, address, gender) 
                    VALUES (?, ?, ?, ?, ?, ?)''', 
                 (data['name'], data['phone'], data['email'], 
                  data['birth_date'], data['address'], data['gender']))
        self.conn.commit()
        return c.lastrowid
