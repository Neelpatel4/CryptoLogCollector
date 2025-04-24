import sqlite3
import pandas as pd

conn = sqlite3.connect("coinbase_logs.db")
cursor = conn.cursor()

# Check if BTC, ETH, SOL are in the database
query = """
SELECT base_currency, timestamp, rate FROM prices
WHERE base_currency IN ('BTC', 'ETH', 'SOL')
ORDER BY timestamp DESC
LIMIT 10
"""

df = pd.read_sql_query(query, conn)
conn.close()

print("\n[🔎 DEBUG] Top Coin Price Logs (BTC, ETH, SOL)")
print(df.to_string(index=False))