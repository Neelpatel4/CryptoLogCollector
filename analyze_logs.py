import sqlite3

def show_recent_price_changes():
    conn = sqlite3.connect("coinbase_logs.db")
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT base_currency FROM prices")
    currencies = [row[0] for row in cursor.fetchall()]
    
    for base in currencies:
        cursor.execute("SELECT timestamp, rate FROM prices WHERE base_currency=? ORDER BY timestamp DESC LIMIT 2", (base,))
        rows = cursor.fetchall()
        if len(rows) == 2:
            t1, r1 = rows
            _, r0 = rows[1]
            try:
                pct = ((float(r1) - float(r0)) / float(r0)) * 100
                print(f"{base}: {pct:.2f}% change (Latest: {r1} at {t1})")
            except:
                continue

    conn.close()

if __name__ == "__main__":
    show_recent_price_changes()


