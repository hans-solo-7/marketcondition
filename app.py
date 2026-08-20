# Create the streamlit app file
with open('market_dashboard.py', 'w') as f:
    f.write("""
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Market Dashboard", layout="wide")
st.title("📊 Market Condition Dashboard")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

@st.cache_data(ttl=3600)
def fetch_market_data():
    spy = yf.Ticker("SPY")
    spy_hist = spy.history(period="1y")
    spy_close = spy_hist['Close'].iloc[-1]
    spy_sma_200 = spy_hist['Close'].rolling(200).mean().iloc[-1]
    
    vix = yf.Ticker("^VIX")
    vix_hist = vix.history(period="5d")
    vix_close = vix_hist['Close'].iloc[-1]
    
    return {
        'spy': {'price': spy_close, 'sma_200': spy_sma_200},
        'vix': {'price': vix_close},
        'spy_hist': spy_hist
    }

data = fetch_market_data()
spy = data['spy']
vix = data['vix']

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("S&P 500 (SPY)", f"${spy['price']:.2f}")
with col2:
    st.metric("200-day SMA", f"${spy['sma_200']:.2f}")
with col3:
    st.metric("VIX", f"{vix['price']:.1f}")
with col4:
    # Signal
    if spy['price'] < spy['sma_200']:
        target, color = "🔴 0%", "red"
    elif vix['price'] > 30:
        target, color = "🟠 50%", "orange"
    else:
        target, color = "🟢 100%", "green"
    st.metric("Target Exposure", target)

# Chart
fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)
fig.add_trace(go.Scatter(x=data['spy_hist'].index, y=data['spy_hist']['Close'], name="SPY"), row=1, col=1)
fig.add_trace(go.Scatter(x=data['spy_hist'].index, y=data['spy_hist']['Close'].rolling(200).mean(), name="200-day SMA"), row=1, col=1)
st.plotly_chart(fig, use_container_width=True)

st.markdown("### 🎯 Action Required")
if spy['price'] < spy['sma_200']:
    st.error("🔴 SELL ALL - Bear Market")
elif vix['price'] > 30:
    st.warning("🟠 REDUCE TO 50% - High Volatility")
else:
    st.success("🟢 HOLD - Bull Market")
""")
