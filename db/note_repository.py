import sqlite3
from datetime import datetime

class NoteRepository:
    def __init__(self, db_path="db/database.db"):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS notes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    transcription TEXT,
                    draft_note TEXT,
                    final_note TEXT,
                    score REAL,
                    created_at TEXT,
                    updated_at TEXT
                )
            """)
            conn.commit()

    def save_note(self, filename, transcription, draft_note, final_note, score):
        now = datetime.now().isoformat()
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO notes (
                    filename, transcription, draft_note, final_note, score, created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (filename, transcription, draft_note, final_note, score, now, now))
            conn.commit()

    def get_note_by_id(self, note_id):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes WHERE id = ?", (note_id,))
            return cursor.fetchone()
### in case we want to check the list on web :) 
    def list_notes(self):
        with self._connect() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM notes ORDER BY created_at DESC")
            return cursor.fetchall()
