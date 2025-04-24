import sqlite3
import requests
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

LOW = 3.0
MEDIUM = 5.0
HIGH = 10.0

def classify(change_percent):
    abs_change = abs(change_percent)
    if abs_change >= HIGH:
        return "HIGH", "🔴"
    elif abs_change >= MEDIUM:
        return "MEDIUM", "🟡"
    elif abs_change >= LOW:
        return "LOW", "🔵"
    return "NONE", ""

def send_discord_alert(message, severity):
    if severity != "NONE" and WEBHOOK_URL:
        try:
            response = requests.post(WEBHOOK_URL, json={"content": f"**SIEM Alert ({severity})**\\n{message}"})
            if response.status_code == 204:
                print("[+] Discord alert sent.")
            else:
                print(f"[-] Discord alert failed: {response.status_code}")
        except Exception as e:
            print("[-] Error sending Discord alert:", str(e))

def log_alert(timestamp, base, change, severity, icon, db_path="coinbase_logs.db"):
    message = f"{icon} {severity} alert for {base}: {change:.2f}% at {timestamp}"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS alerts (" 
        "id INTEGER PRIMARY KEY AUTOINCREMENT, " 
        "timestamp TEXT NOT NULL, " 
        "base_currency TEXT NOT NULL,"
        "change_percent REAL NOT NULL" 
        "severity TEXT NOT NULL, " 
        "message TEXT NOT NULL)"
    )

    cursor.execute(
        "INSERT INTO alerts (timestamp, base_currency, change_percent, severity, message) "
        "VALUES (?, ?, ?, ?, ?)", 
        (timestamp, base, change, severity, message)
    )

    conn.commit()
    conn.close()
    print(f"[ALERT LOGGED] {message}")
    send_discord_alert(message, severity)

def analyze_currency(base_currency):
    conn = sqlite3.connect("coinbase_logs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT timestamp, rate FROM prices WHERE base_currency=? ORDER BY timestamp DESC LIMIT 2", (base_currency,))
    rows = cursor.fetchall()
    conn.close()

    if len(rows) < 2:
        return
    
    latest_time, latest_rate = rows[0]
    _, previous_rate = rows[1]

    try:
        latest = float(latest_rate)
        previous = float(previous_rate)
        change = ((latest - previous) / previous)
    except:
        return
    
    severity, icon = classify(change)
    if severity != "NONE":
        log_alert(latest_time, base_currency, change, severity, icon)

def run_alert_engine():
    print("[+] Running alert engine for all currencies...")
    conn = sqlite3.connect("coinbase_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT base_currency FROM prices")
    symbols = [row[0] for row in cursor.fetchall()]
    conn.close()

    for symbol in symbols:
        analyze_currency(symbol)

if __name__ == "__main__":
    run_alert_engine()


