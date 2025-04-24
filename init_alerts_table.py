import sqlite3

conn = sqlite3.connect("coinbase_logs.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        timestamp TEXT NOT NULL,
        base_currency TEXT NOT NULL,
        change_percent REAL NOT NULL,
        severity TEXT NOT NULL,
        message TEXT NOT NULL 
    )
""")

conn.commit()
conn.close()
print("[+] Created 'alerts' table.ini")