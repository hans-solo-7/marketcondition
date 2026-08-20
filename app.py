# ============================================
# MARKET CONDITION DASHBOARD - STREAMLIT CLOUD
# Simplified version that works with Python 3.14+
# ============================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="Market Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Market Condition Dashboard")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# ============================================
# DATA FETCHING WITH ERROR HANDLING
# ============================================

@st.cache_data(ttl=1800)  # 30 minutes cache
def fetch_market_data():
    """Fetch SPY and VIX data with error handling"""
    try:
        # SPY
        spy = yf.Ticker("SPY")
        spy_hist = spy.history(period="1y")
        
        if len(spy_hist) == 0:
            return None
        
        spy_close = spy_hist['Close'].iloc[-1]
        spy_sma_200 = spy_hist['Close'].rolling(200).mean().iloc[-1]
        
        # VIX
        vix = yf.Ticker("^VIX")
        vix_hist = vix.history(period="5d")
        
        if len(vix_hist) == 0:
            vix_close = 20.0  # Default if VIX not available
        else:
            vix_close = vix_hist['Close'].iloc[-1]
        
        return {
            'spy_close': float(spy_close),
            'spy_sma_200': float(spy_sma_200),
            'vix_close': float(vix_close),
            'spy_hist': spy_hist,
            'vix_hist': vix_hist,
            'success': True
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }

# ============================================
# FETCH DATA
# ============================================

with st.spinner("Fetching market data..."):
    data = fetch_market_data()

# ============================================
# DISPLAY
# ============================================

if data is None or not data.get('success', False):
    st.error(f"❌ Failed to fetch data: {data.get('error', 'Unknown error')}")
    st.info("Please try refreshing the page in a few minutes.")
else:
    spy_close = data['spy_close']
    spy_sma_200 = data['spy_sma_200']
    vix_close = data['vix_close']
    spy_hist = data['spy_hist']
    vix_hist = data['vix_hist']
    
    # === Determine signal ===
    if spy_close < spy_sma_200:
        target = 0
        signal = "🔴 SELL ALL"
        signal_color = "#e74c3c"
        signal_detail = "S&P 500 below 200-day SMA (Bear Market)"
    elif vix_close > 30:
        target = 50
        signal = "🟠 REDUCE TO 50%"
        signal_color = "#f39c12"
        signal_detail = f"VIX above 30 ({vix_close:.1f})"
    else:
        target = 100
        signal = "🟢 HOLD 100%"
        signal_color = "#2ecc71"
        signal_detail = "All indicators normal (Bull Market)"
    
    # === TOP ROW: Metrics ===
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="S&P 500 (SPY)",
            value=f"${spy_close:.2f}"
        )
    
    with col2:
        st.metric(
            label="200-day SMA",
            value=f"${spy_sma_200:.2f}",
            delta=f"{((spy_close / spy_sma_200) - 1) * 100:.1f}%"
        )
    
    with col3:
        st.metric(
            label="VIX (Fear Index)",
            value=f"{vix_close:.1f}"
        )
    
    with col4:
        st.metric(
            label="🎯 Target Exposure",
            value=f"{target}%",
            delta=signal_detail
        )
    
    # === Signal Box ===
    st.markdown("---")
    st.markdown("### 📋 Signal")
    
    if target == 0:
        st.error(f"**{signal}** - {signal_detail}")
        st.write("**Action:** Exit all positions at next market open.")
    elif target == 50:
        st.warning(f"**{signal}** - {signal_detail}")
        st.write("**Action:** Reduce exposure to 50% at next market open.")
    else:
        st.success(f"**{signal}** - {signal_detail}")
        st.write("**Action:** No action needed. Continue holding.")
    
    # === CHARTS ===
    st.markdown("---")
    st.markdown("### 📈 Charts")
    
    # Create subplots
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.08,
        row_heights=[0.65, 0.35]
    )
    
    # SPY Chart
    fig.add_trace(
        go.Scatter(
            x=spy_hist.index,
            y=spy_hist['Close'],
            name="SPY Close",
            line=dict(color='#2E86C1', width=2)
        ),
        row=1, col=1
    )
    
    # SMA 200
    fig.add_trace(
        go.Scatter(
            x=spy_hist.index,
            y=spy_hist['Close'].rolling(200).mean(),
            name="200-day SMA",
            line=dict(color='#E74C3C', width=2, dash='dash')
        ),
        row=1, col=1
    )
    
    # VIX Chart
    if len(vix_hist) > 0:
        fig.add_trace(
            go.Scatter(
                x=vix_hist.index,
                y=vix_hist['Close'],
                name="VIX",
                line=dict(color='#E67E22', width=2)
            ),
            row=2, col=1
        )
        
        # VIX threshold line
        fig.add_hline(
            y=30,
            line_dash="dash",
            line_color="red",
            annotation_text="VIX > 30 = Reduce",
            row=2, col=1
        )
    
    fig.update_layout(
        height=600,
        showlegend=True,
        template="plotly_white",
        hovermode="x unified"
    )
    
    fig.update_yaxes(title_text="Price", row=1, col=1)
    fig.update_yaxes(title_text="VIX", row=2, col=1)
    
    st.plotly_chart(fig, use_container_width=True)
    
    # === SIDEBAR ===
    st.sidebar.markdown("### 📋 Quick Reference")
    
    st.sidebar.markdown("""
    **Strategy Rules:**
    
    | Condition | Action |
    |-----------|--------|
    | SPY < 200 SMA | 🔴 SELL 100% |
    | SPY > 200 SMA + VIX > 30 | 🟠 SELL 50% |
    | SPY > 200 SMA + VIX < 30 | 🟢 HOLD 100% |
    """)
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("**Current Status:**")
    st.sidebar.write(f"SPY: {'🟢 Above' if spy_close >= spy_sma_200 else '🔴 Below'} 200 SMA")
    st.sidebar.write(f"VIX: {'🔴 High (>30)' if vix_close > 30 else '🟢 Normal'}")
    st.sidebar.write(f"Target: **{target}%**")
    
    st.sidebar.markdown("---")
    st.sidebar.caption("Data Source: Yahoo Finance")
    st.sidebar.caption("Strategy: Max Sharpe + Value Blend (v4)")
