import requests 
import sqlite3
from datetime import datetime, timezone
import time

MAINSTREAM = [
    "BTC", "ETH", "SOL", "ADA", "DOGE", "XRP", "LTC", "BCH", "AVAX", "LINK",
    "MATIC", "DOT", "ATOM", "UNI", "SHIB", "ETC", "XLM", "FIL", "APT", "NEAR"
]

def fetch_coinbase_currencies():
    url = "https://api.coinbase.com/v2/currencies"
    response = requests.get(url)
    if response.status_code == 200:
        return list(set(MAINSTREAM +[currency["id"] for currency in response.json()["data"]]))
    else:
        print("[-] Failed to fetch currency list.")
        return []
    
def fetch_usd_rate_for_currency(base_currency): 
    url = f"https://api.coinbase.com/v2/exchange-rates?currency={base_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json().get("data", {})
        rates = data.get("rates", {})
        usd_rate = rates.get("USD")
        return usd_rate
    return None

def save_price(base, usd_rate):
    if usd_rate is None:
        print(f"[!] No USD rate found for {base}")
        return
    conn = sqlite3.connect("coinbase_logs.db")
    cursor = conn.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS prices ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT, "
        "timestamp TEXT NOT NULL, "
        "base_currency TEXT NOT NULL, "
        "rate_currency TEXT NOT NULL, "
        "rate TEXT NOT NULL)"
    )

    cursor.execute(
        "INSERT INTO prices (timestamp, base_currency, rate_currency, rate) VALUES (?, ?, ?, ?)",
        (datetime.now(timezone.utc).isoformat(), base, "USD", usd_rate)
    )

    conn.commit()
    conn.close()
    print(f"[+] Logged {base} -> USD = {usd_rate}")

def run_collector():
    print("[+] Starting full crypto price collector (vs USD)")
    currencies = fetch_coinbase_currencies()
    if not currencies:
        return
    
    for base_currency in currencies:
        usd_rate = fetch_usd_rate_for_currency(base_currency)
        save_price(base_currency, usd_rate)
        time.sleep(0.25)

if __name__ == "__main__":
    run_collector()