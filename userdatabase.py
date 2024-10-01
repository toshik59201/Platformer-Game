import sqlite3

def initialize_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        difficulty TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()

initialize_database()


def add_user(name, difficulty):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (name, difficulty) VALUES (?, ?)', (name, difficulty))
    conn.commit()
    conn.close()
