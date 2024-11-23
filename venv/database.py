import sqlite3
from hashlib import sha256

def initialize_db():
    conn = sqlite3.connect('printingapp.db')
    cursor = conn.cursor()

    # Create users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    # Add a default admin user (password: admin)
    admin_password = "admin"
    admin_password_hash = sha256(admin_password.encode()).hexdigest()
    try:
        cursor.execute("INSERT INTO users (username, password_hash) VALUES (?, ?)", ("admin", admin_password_hash))
    except sqlite3.IntegrityError:
        pass  # Admin user already exists

    conn.commit()
    conn.close()

if __name__ == "__main__":
    initialize_db()
