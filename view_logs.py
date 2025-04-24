import sqlite3

def view_prices(limit=10):
    conn = sqlite3.connect("coinbase_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, base_currency, rate FROM prices ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    print("\n[Latest Prices]")
    for row in rows:
        print(f"{row[0]} | {row[1]} -> {row[2]}")
    conn.close()

def view_alerts(limit=10):
    conn = sqlite3.connect("coinbase_logs.db")
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, base_currency, change_percent, severity, message FROM alerts ORDER BY timestamp DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    print("\\n[Recent Alerts]")
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[3]} | {row[2]:.2f}% | {row[4]}")
    conn.close()

if __name__ == "__main__":
    view_prices()
    view_alerts()
