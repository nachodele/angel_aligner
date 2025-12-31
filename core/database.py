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
        
        # Pacientes
        c.execute('''CREATE TABLE IF NOT EXISTS patients 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     name TEXT NOT NULL, phone TEXT, email TEXT, 
                     birth_date TEXT, address TEXT, gender TEXT, 
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        # Appointments
        c.execute('''CREATE TABLE IF NOT EXISTS appointments 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     patient_id INTEGER, 
                     appointment_date TEXT,
                     appointment_time TEXT,
                     status TEXT DEFAULT 'Scheduled', 
                     procedure TEXT, 
                     aligner_number INTEGER, 
                     aligner_type TEXT, 
                     notes TEXT,
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
        # 🔥 VISITS - Historial clínico
        c.execute('''CREATE TABLE IF NOT EXISTS visits 
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                     patient_id INTEGER, visit_date TEXT,
                     procedure TEXT, aligner_number INTEGER, ipr TEXT, 
                     photos BOOLEAN DEFAULT 0, scan BOOLEAN DEFAULT 0, notes TEXT,
                     created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
        
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
    
    def update_patient(self, patient_id, **data):
        """Actualiza paciente existente"""
        fields = []
        values = []
        for key, value in data.items():
            if value:
                fields.append(f"{key}=?")
                values.append(value)
        
        if not fields:
            return False
        
        query = f"UPDATE patients SET {', '.join(fields)} WHERE id=?"
        values.append(patient_id)
        
        self.conn.execute(query, values)
        self.conn.commit()
        return True
    
    def add_appointment(self, patient_id, appointment_date, appointment_time, procedure, notes="", status="Scheduled", aligner_number=None, aligner_type=None):
        """Añade nueva cita para paciente"""
        cursor = self.conn.execute("""
            INSERT INTO appointments (patient_id, appointment_date, appointment_time, procedure, notes, status, aligner_number, aligner_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (patient_id, appointment_date, appointment_time, procedure, notes, status, aligner_number, aligner_type))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_appointments(self, date_filter=""):
        """Obtiene todas las citas, filtradas por fecha opcionalmente"""
        c = self.conn.cursor()
        if date_filter:
            query = "SELECT * FROM appointments WHERE appointment_date LIKE ? ORDER BY appointment_date, appointment_time"
            appointments = c.execute(query, (f"%{date_filter}%",)).fetchall()
        else:
            query = "SELECT * FROM appointments ORDER BY appointment_date, appointment_time"
            appointments = c.execute(query, ()).fetchall()
        return appointments
    
    def get_patient_name(self, patient_id):
        """Obtiene nombre del paciente por ID"""
        c = self.conn.cursor()
        c.execute("SELECT name FROM patients WHERE id=?", (patient_id,))
        result = c.fetchone()
        return result[0] if result else "Unknown"
    
    # 🔥 NUEVOS MÉTODOS PARA VISITS
    def add_visit_from_appointment(self, appointment_id):
        """🔥 Convierte appointment COMPLETED → visit en historial"""
        c = self.conn.cursor()
        c.execute("""
            SELECT a.patient_id, a.appointment_date, a.appointment_time, 
                   a.procedure, a.notes, a.aligner_number, a.aligner_type
            FROM appointments a WHERE a.id = ? AND a.status = 'Completed'
        """, (appointment_id,))
        
        appt_data = c.fetchone()
        if not appt_data:
            return False
        
        patient_id, visit_date, visit_time, procedure, notes, aligner_num, aligner_type = appt_data
        visit_date_full = f"{visit_date} {visit_time or '00:00'}"
        
        # Añade a visits
        c.execute("""
            INSERT INTO visits (patient_id, visit_date, procedure, aligner_number, 
                               ipr, photos, scan, notes)
            VALUES (?, ?, ?, ?, '', 0, 0, ?)
        """, (patient_id, visit_date_full, procedure, aligner_num or 0, notes or ""))
        
        # Elimina appointment (ya convertido a visit)
        c.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        self.conn.commit()
        return True
    
    def get_patient_visits(self, patient_id):
        """ Historial de visitas del paciente"""
        c = self.conn.cursor()
        c.execute("""
            SELECT visit_date, procedure, aligner_number, ipr, 
                   CASE WHEN photos=1 THEN '✅' ELSE '❌' END as photos,
                   CASE WHEN scan=1 THEN '✅' ELSE '❌' END as scan,
                   notes 
            FROM visits WHERE patient_id = ? ORDER BY visit_date DESC
        """, (patient_id,))
        return c.fetchall()
    
    def delete_appointment(self, appointment_id):
        """Elimina cita"""
        c = self.conn.cursor()
        c.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
        self.conn.commit()
        return True
    
    def update_appointment_status(self, appointment_id, status, new_date=None, new_time=None):
        """Actualiza status de cita (usado por UI)"""
        c = self.conn.cursor()
        if new_date and new_time:
            c.execute("UPDATE appointments SET status=?, appointment_date=?, appointment_time=? WHERE id=?",
                     (status, new_date, new_time, appointment_id))
        else:
            c.execute("UPDATE appointments SET status=? WHERE id=?", (status, appointment_id))
        self.conn.commit()
        return True
