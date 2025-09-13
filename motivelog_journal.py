import sqlite3
from datetime import date

DB_NAME = "motivelog.db"

def init_journal_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS journals (
            id INTEGER PRIMARY KEY,
            entry_date TEXT,
            title TEXT,
            content TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_journal_entry(title, content):
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO journals (entry_date, title, content) VALUES (?, ?, ?)",
              (today, title, content))
    conn.commit()
    conn.close()

def get_journal_entries():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT entry_date, title, content FROM journals ORDER BY entry_date DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def get_journal_by_date(entry_date):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT title, content FROM journals WHERE entry_date = ?", (entry_date,))
    result = c.fetchone()
    conn.close()
    return result