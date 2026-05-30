import sqlite3
import hashlib
import os

DB_PATH = "vulnbank.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    conn = get_db()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT DEFAULT 'user'
        )
    """)

    c.execute("""
        CREATE TABLE accounts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            balance REAL DEFAULT 1000.0,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    """)

    c.execute("""
        CREATE TABLE transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            from_account INTEGER,
            to_account INTEGER,
            amount REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Passwords stored as plain MD5 (A02 - crypto failure)
    def md5(p): return hashlib.md5(p.encode()).hexdigest()

    c.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
              ("admin", md5("admin123"), "admin"))
    c.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
              ("alice", md5("password1"), "user"))
    c.execute("INSERT INTO users (username, password, role) VALUES (?,?,?)",
              ("bob", md5("qwerty"), "user"))

    c.execute("INSERT INTO accounts (user_id, balance) VALUES (1, 99999.0)")
    c.execute("INSERT INTO accounts (user_id, balance) VALUES (2, 1500.0)")
    c.execute("INSERT INTO accounts (user_id, balance) VALUES (3, 800.0)")

    conn.commit()
    conn.close()
    print("[+] Database initialised with test users: admin/admin123, alice/password1, bob/qwerty")

if __name__ == "__main__":
    init_db()