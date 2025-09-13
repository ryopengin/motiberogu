import sqlite3

DB_NAME = "motivelog.db"

def init_tasks_table():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY,
            subject TEXT,
            description TEXT,
            deadline TEXT,
            priority TEXT,
            completed INTEGER DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

def add_task(subject, description, deadline, priority):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO tasks (subject, description, deadline, priority) VALUES (?, ?, ?, ?)",
              (subject, description, deadline, priority))
    conn.commit()
    conn.close()

def update_task(task_id, subject, description, deadline, priority):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        UPDATE tasks
        SET subject = ?, description = ?, deadline = ?, priority = ?
        WHERE id = ?
    ''', (subject, description, deadline, priority, task_id))
    conn.commit()
    conn.close()

def mark_task_completed(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("UPDATE tasks SET completed = 1 WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

def delete_all_completed_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("DELETE FROM tasks WHERE completed = 1")
    conn.commit()
    conn.close()

def get_all_incomplete_tasks_detailed():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, subject, description, deadline, priority FROM tasks WHERE completed = 0")
    tasks = c.fetchall()
    conn.close()
    return tasks

def get_completed_tasks():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, subject, description, deadline, priority FROM tasks WHERE completed = 1")
    tasks = c.fetchall()
    conn.close()
    return tasks

def search_tasks_by_keyword(keyword):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    like_query = f"%{keyword}%"
    c.execute('''
        SELECT id, subject, description, deadline, priority
        FROM tasks
        WHERE completed = 0 AND (subject LIKE ? OR description LIKE ?)
    ''', (like_query, like_query))
    results = c.fetchall()
    conn.close()
    return results