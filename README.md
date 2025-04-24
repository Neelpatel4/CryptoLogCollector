# Crypto Log Collector

A lightweight Security Information and Event Management (SIEM) tool built for tracking and visualizing live cryptocurrency prices from Coinbase using their public API. This system alerts on significant price changes, classifies severity, and displays everything on an interactive Streamlit dashboard.

🚀 Features

  🔁 Auto-collects exchange rates for all coins listed on Coinbase
  
  🧠 Alert engine to detect:
  
  🔵 Low severity (3–5% change)
  
  🟡 Medium (5–10%)
  
  🔴 High (10%+)
  
  💾 Stores data in local SQLite database
  
  📊 Interactive Streamlit + Plotly dashboard
  
  🔔 Discord webhook alerts (for high-severity changes)
  
  🧪 Live monitoring with monitor.py


To run this project you will need to run it within the Virtual Environment 
  1st Step
    Run this command in the Terminal 
    .\venv311\Scripts\activate.ps1
    To run the Virtual Environment
  2nd Step
    The run this command 
    streamlit run dashboard.py
    The project should be available within your web browser to use!
    
