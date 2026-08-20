# ============================================
# SIMPLIFIED APP - WITH SIMULATED DATA FALLBACK
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Market Dashboard", layout="wide")
st.title("📊 Market Condition Dashboard")

# Try to fetch real data
try:
    import yfinance as yf
    spy = yf.Ticker("SPY")
    spy_hist = spy.history(period="1y")
    
    if len(spy_hist) > 0:
        # Use real data
        spy_close = spy_hist['Close'].iloc[-1]
        spy_sma = spy_hist['Close'].rolling(200).mean().iloc[-1]
        
        vix = yf.Ticker("^VIX")
        vix_hist = vix.history(period="5d")
        vix_close = vix_hist['Close'].iloc[-1] if len(vix_hist) > 0 else 20
        
        st.success("✅ Using real market data")
    else:
        raise Exception("No data")
        
except:
    # Use simulated data
    st.warning("⚠️ Using simulated data (Yahoo Finance rate-limited)")
    
    # Generate realistic-looking data
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=252, freq='D')
    base_price = 560
    returns = np.random.normal(0.0004, 0.012, 252)
    prices = base_price * (1 + returns).cumprod()
    spy_close = prices[-1]
    spy_sma = np.mean(prices[-200:])
    vix_close = 18 + np.random.normal(0, 2)

# Display metrics
col1, col2, col3 = st.columns(3)
col1.metric("SPY", f"${spy_close:.2f}")
col2.metric("200-day SMA", f"${spy_sma:.2f}")
col3.metric("VIX", f"{vix_close:.1f}")

# Signal
if spy_close < spy_sma:
    st.error("🔴 SELL ALL - Bear Market")
elif vix_close > 30:
    st.warning("🟠 REDUCE TO 50% - High VIX")
else:
    st.success("🟢 HOLD - Bull Market")
