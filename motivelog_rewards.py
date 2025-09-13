import sqlite3

DB_NAME = "motivelog.db"

def init_motivation_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS motivation_points (
            id INTEGER PRIMARY KEY,
            total_points INTEGER DEFAULT 0
        )
    ''')
    c.execute("INSERT OR IGNORE INTO motivation_points (id, total_points) VALUES (1, 0)")
    conn.commit()
    conn.close()

def add_motivation_point(amount=1):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE motivation_points SET total_points = total_points + ? WHERE id = 1", (amount,))
    conn.commit()
    conn.close()

def get_total_points():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT total_points FROM motivation_points WHERE id = 1")
    row = c.fetchone()
    conn.close()
    return row[0] if row else 0