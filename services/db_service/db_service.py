import sqlite3
from datetime import datetime


class DBWorker:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
    
    def __enter__(self):
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self.conn.commit()
        else:
            self.conn.rollback()



class DBService:
    def __init__(self, db_path):
        self.db_path = db_path
        self.init_db()
        self.conn = None

    def __del__(self):
        if self.conn:
            self.conn.close()   
    
    def init_db(self):
        try:
            self.conn = sqlite3.connect(self.db_path)
            with DBWorker(self.conn) as c:
                c.execute(
                    """
                CREATE TABLE IF NOT EXISTS logged_time (
                    index INTEGER PRIMARY KEY AUTOINCREMENT,
                    issue_key TEXT,
                    date TEXT,
                    time_spent TEXT,
                    comment TEXT
                    chat_id TEXT
                )
                """
                )
                c.execute(
                    """
                CREATE TABLE IF NOT EXISTS users (
                    index INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT,
                    jira_username TEXT,
                    chat_id TEXT PRIMARY KEY
                )
                """
                )
        except sqlite3.Error as e:
            print(f"Database error: {e} rollback transaction")
        except Exception as e:
            print(f"Error: {e}")

    def insert_log(self, issue_key, time_spent, comment):
        with DBWorker(self.conn) as c:
            c.execute(
                """
            INSERT INTO logged_time (issue_key, date, time_spent, comment, chat_id) 
            VALUES (?, ?, ?, ?, ?)
            """,
                (issue_key, datetime.now().isoformat(), time_spent, comment),
            )

    def create_user(self, chat_id, username, jira_username):
        with DBWorker(self.conn) as c:
            c.execute(
               """
            INSERT INTO users (username, jira_username, chat_id)
            VALUES (?, ?, ?)
            """,
            (username, jira_username, chat_id),
            )
    
    def get_username(self, chat_id) -> list[str]:
        with DBWorker(self.conn) as c:
            c.execute(
                """
            SELECT username FROM users WHERE chat_id = ?
            """,
                (chat_id,),
            )
            return c.fetchone()

    def get_jira_username(self, chat_id) -> list[str]:
        with DBWorker(self.conn) as c:
            c.execute(
                """
            SELECT jira_username FROM users WHERE chat_id = ?
            """,
                (chat_id,),
            )
            return c.fetchone()

    def get_chat_id(self, chat_id) -> list[str]:
        with DBWorker(self.conn) as c:
            c.execute(
                """
            SELECT chat_id FROM users WHERE chat_id = ?
            """,
                (chat_id,),
            )
            return c.fetchone()
    

    def save_chat_id(self, chat_id):
        with DBWorker(self.conn) as c:
            c.execute(
                """
            INSERT INTO users (chat_id)
            VALUES (?)
            """,
                (chat_id),
            )