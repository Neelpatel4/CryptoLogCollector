import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
from datetime import datetime

st.set_page_config(page_title="Crypto SIEM Dashboard", layout="wide")
st.title("Real-Time Crypto SIEM Dashboard")

DB_PATH = "coinbase_logs.db"
MAINSTREAM = [
    "BTC", "ETH", "SOL", "ADA", "DOGE", "XRP", "LTC", "BCH", "AVAX", "LINK",
    "MATIC", "DOT", "ATOM", "UNI", "SHIB", "ETC", "XLM", "FIL", "APT", "NEAR"
]

@st.cache_data(ttl=60)
def load_prices():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM prices", conn)
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df["rate"] = pd.to_numeric(df["rate"], errors="coerce")
    return df.dropna()

@st.cache_data(ttl=60)
def load_alerts():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM alerts", conn)
    conn.close()
    df["timestamp"] = pd.to_datetime(df["timestamp"])
    return df

prices_df = load_prices()
alerts_df = load_alerts()

st.sidebar.header("Filters")
show_mainstream = st.sidebar.checkbox("Show Mainstream Coins Only", value=True)

coins = prices_df["base_currency"].unique().tolist()
if show_mainstream:
    coins = [coin for coin in coins if coin in MAINSTREAM]

selected_coin = st.sidebar.selectbox("Select Coin", sorted(coins))
time_range = st.sidebar.slider("Time Range (hours)", 1, 48, 1)

now=pd.Timestamp.utcnow()
filtered_prices = prices_df[
    (prices_df["base_currency"] == selected_coin) &
    (prices_df["timestamp"] >= now - pd.Timedelta(hours=time_range))
]

st.subheader(f"📈 {selected_coin} Price over Time (Last {time_range}h)")
fig = px.line(
    filtered_prices,
    x="timestamp",
    y="rate",
    labels={"timestamp": "Time", "rate": "USD"},
    title=f"{selected_coin} -> USD"
)
fig.update_traces(line=dict(width=2))
st.plotly_chart(fig, use_container_width=True)

st.subheader("Recent Alets")
severity_filter = st.multiselect("Filter by Severity", options=["LOW", "MEDIUM", "HIGH"], default=["LOW", "MEDIUM", "HIGH"])
coin_filter = st.multiselect("Filter by Coin", options=alerts_df["base_currency"].unique().tolist(), default=alerts_df["base_currency"].unique().tolist())

filtered_alerts = alerts_df[
    alerts_df["severity"].isin(severity_filter) &
    alerts_df["base_currency"].isin(coin_filter)
].sort_values(by="timestamp", ascending=False)

st.dataframe(filtered_alerts[["timestamp", "base_currency", "change_percent", "severity", "message"]], use_container_width=True, height=400)