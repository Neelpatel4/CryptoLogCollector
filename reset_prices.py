import sqlite3
conn = sqlite3.connect("coinbase_logs.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS prices")
conn.commit()
conn.close()
