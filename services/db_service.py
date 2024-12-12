import sqlite3
from datetime import datetime

class DBService:
    def __init__(self, db_path):
        self.db_path = db_path

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
        CREATE TABLE IF NOT EXISTS logged_time (
            issue_key TEXT,
            date TEXT,
            time_spent TEXT,
            comment TEXT
        )
        """)
        conn.commit()
        conn.close()

    def insert_log(self, issue_key, time_spent, comment):
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute("""
        INSERT INTO logged_time (issue_key, date, time_spent, comment) 
        VALUES (?, ?, ?, ?)
        """, (issue_key, datetime.now().isoformat(), time_spent, comment))
        conn.commit()
        conn.close()
