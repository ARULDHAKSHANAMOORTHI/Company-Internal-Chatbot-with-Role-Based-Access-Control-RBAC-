# import sqlite3

# conn = sqlite3.connect("users.db", check_same_thread=False)
# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE IF NOT EXISTS users (
#     id INTEGER PRIMARY KEY,
#     username TEXT,
#     password TEXT,
#     role TEXT
# )
# """)

# cursor.execute("""
# INSERT OR IGNORE INTO users VALUES
# (1,'finance_user','123','finance'),
# (2,'hr_user','123','hr'),
# (3,'ceo','123','c_level')
# """)

# conn.commit()

import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

# Users table
cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT NOT NULL,
    role TEXT NOT NULL
)
""")

# Chat history table
cur.execute("""
CREATE TABLE IF NOT EXISTS chat_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    query TEXT,
    answer TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()
