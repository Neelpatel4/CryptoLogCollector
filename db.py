import sqlite3 

def initialize_db():
    conn = sqlite3.connect("coinbase_logs.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS prices (" 
        "id INTEGER PRIMARY KEY AUTINCREMENT, " 
        "timestamp TEXT NOT NULL, " 
        "base_currency TEXT NOT NULL, " 
        "rate_currency TEXT NOT NULL, " 
        "rate TEXT NOT NULL)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS alerts (" 
        "id INTEGER PRIMARY KEY AUTINCREMENT, " 
        "timestamp TEXT NOT NULL, " 
        "base_currency TEXT NOT NULL, " 
        "change_percent REAL NOT NULL, "
        "severity TEXT NOT NULL, " 
        "message TEXT NOT NULL)"
    )
    conn.commit()
    conn.close()
    print("[+] Database intialized")

if __name__ == "__main__":
    initialize_db()
