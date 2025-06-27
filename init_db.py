import sqlite3

# Connect or create database
conn = sqlite3.connect('database.db')

# Create tables
conn.executescript("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    subject TEXT,
    rating INTEGER,
    comments TEXT,
    FOREIGN KEY(student_id) REFERENCES users(id)
);
""")

conn.commit()
conn.close()
print("✅ Database tables created successfully.")