# ============================================
# MARKET CONDITION DASHBOARD - ENTERPRISE EDITION
# Professional styling, animations, and visual appeal
# ============================================

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import time
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests

# ============================================
# PAGE CONFIG
# ============================================

st.set_page_config(
    page_title="Market Dashboard Pro",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS - Professional Dark Theme
# ============================================

st.markdown("""
<style>
    /* Global dark theme */
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
    /* Main container */
    .main {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 20px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Metric cards */
    .metric-card {
        background: rgba(255,255,255,0.08);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 48px rgba(0,0,0,0.5);
        border-color: rgba(255,255,255,0.2);
    }
    
    /* Signal cards */
    .signal-bull {
        background: linear-gradient(135deg, #00b894, #00cec9);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0,206,201,0.3);
        animation: pulse-green 2s infinite;
    }
    
    .signal-bear {
        background: linear-gradient(135deg, #e17055, #d63031);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(214,48,49,0.3);
        animation: pulse-red 2s infinite;
    }
    
    .signal-neutral {
        background: linear-gradient(135deg, #fdcb6e, #e17055);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(225,112,85,0.3);
        animation: pulse-orange 2s infinite;
    }
    
    /* Animations */
    @keyframes pulse-green {
        0% { box-shadow: 0 8px 32px rgba(0,206,201,0.3); }
        50% { box-shadow: 0 8px 48px rgba(0,206,201,0.6); }
        100% { box-shadow: 0 8px 32px rgba(0,206,201,0.3); }
    }
    
    @keyframes pulse-red {
        0% { box-shadow: 0 8px 32px rgba(214,48,49,0.3); }
        50% { box-shadow: 0 8px 48px rgba(214,48,49,0.6); }
        100% { box-shadow: 0 8px 32px rgba(214,48,49,0.3); }
    }
    
    @keyframes pulse-orange {
        0% { box-shadow: 0 8px 32px rgba(225,112,85,0.3); }
        50% { box-shadow: 0 8px 48px rgba(225,112,85,0.6); }
        100% { box-shadow: 0 8px 32px rgba(225,112,85,0.3); }
    }
    
    /* Gauge chart container */
    .gauge-container {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.1);
    }
    
    /* Status badges */
    .badge-online {
        background: #00b894;
        border-radius: 20px;
        padding: 4px 12px;
        font-size: 12px;
        color: white;
        display: inline-block;
    }
    
    /* Divider with glow */
    .glow-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        margin: 30px 0;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(255,255,255,0.05);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255,255,255,0.2);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: rgba(255,255,255,0.3);
    }
    
    /* Title styling */
    .main-title {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #00cec9, #6c5ce7, #fd79a8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
    }
    
    .subtitle {
        color: rgba(255,255,255,0.5);
        font-size: 14px;
        letter-spacing: 2px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<p class="subtitle" style="text-align:center;">⚡ REAL-TIME MARKET INTELLIGENCE</p>', unsafe_allow_html=True)
    st.markdown('<h1 class="main-title" style="text-align:center;">📈 Market Dashboard</h1>', unsafe_allow_html=True)
    st.markdown(f'<p style="text-align:center; color: rgba(255,255,255,0.4);">Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ET</p>', unsafe_allow_html=True)

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ============================================
# DATA FETCHING
# ============================================

@st.cache_data(ttl=1800)
def fetch_market_data():
    """Fetch market data with fallbacks"""
    try:
        import yfinance as yf
        
        # SPY
        spy = yf.Ticker("SPY")
        spy_hist = spy.history(period="1y")
        
        if len(spy_hist) == 0:
            return None
        
        spy_close = spy_hist['Close'].iloc[-1]
        spy_sma_200 = spy_hist['Close'].rolling(200).mean().iloc[-1]
        spy_high = spy_hist['Close'].max()
        spy_low = spy_hist['Close'].min()
        spy_volume = spy_hist['Volume'].iloc[-1]
        
        # VIX
        vix = yf.Ticker("^VIX")
        vix_hist = vix.history(period="1mo")
        vix_close = vix_hist['Close'].iloc[-1] if len(vix_hist) > 0 else 20
        
        return {
            'spy_close': float(spy_close),
            'spy_sma_200': float(spy_sma_200),
            'spy_high': float(spy_high),
            'spy_low': float(spy_low),
            'spy_volume': float(spy_volume),
            'vix_close': float(vix_close),
            'spy_hist': spy_hist,
            'vix_hist': vix_hist,
            'success': True
        }
    except:
        return None

with st.spinner("🔮 Loading market data..."):
    data = fetch_market_data()

if data is None:
    st.error("❌ Failed to fetch data")
    st.stop()

# ============================================
# CALCULATE SIGNALS
# ============================================

spy_close = data['spy_close']
spy_sma_200 = data['spy_sma_200']
vix_close = data['vix_close']
spy_high = data['spy_high']
spy_low = data['spy_low']
spy_volume = data['spy_volume']
spy_hist = data['spy_hist']
vix_hist = data['vix_hist']

# Determine market regime
if spy_close < spy_sma_200:
    target = 0
    signal = "BEAR"
    signal_emoji = "🐻"
    signal_color = "#e74c3c"
    signal_label = "SELL ALL"
    action_text = "Exit all positions immediately"
elif vix_close > 30:
    target = 50
    signal = "NEUTRAL"
    signal_emoji = "⚠️"
    signal_color = "#f39c12"
    signal_label = "REDUCE TO 50%"
    action_text = "Reduce exposure to 50%"
else:
    target = 100
    signal = "BULL"
    signal_emoji = "🐂"
    signal_color = "#2ecc71"
    signal_label = "HOLD 100%"
    action_text = "Continue holding positions"

# ============================================
# TOP METRICS ROW (Fancy Cards)
# ============================================

st.markdown("""
<style>
.metric-value {
    font-size: 32px;
    font-weight: 700;
    background: linear-gradient(135deg, #fff, rgba(255,255,255,0.7));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.metric-label {
    color: rgba(255,255,255,0.5);
    font-size: 14px;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.metric-change {
    font-size: 16px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# Row 1: Main metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">S&P 500 (SPY)</div>
        <div class="metric-value">${spy_close:.2f}</div>
        <div style="display:flex; justify-content:space-between; margin-top:10px;">
            <span style="color:rgba(255,255,255,0.3); font-size:12px;">52W H: ${spy_high:.2f}</span>
            <span style="color:rgba(255,255,255,0.3); font-size:12px;">52W L: ${spy_low:.2f}</span>
        </div>
        <div style="margin-top:8px;">
            <span style="color:rgba(255,255,255,0.4); font-size:12px;">Volume: {spy_volume/1e6:.1f}M</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    pct_from_sma = ((spy_close / spy_sma_200) - 1) * 100
    color = "#2ecc71" if pct_from_sma > 0 else "#e74c3c"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">200-day SMA</div>
        <div class="metric-value">${spy_sma_200:.2f}</div>
        <div class="metric-change" style="color:{color};">
            {pct_from_sma:+.2f}% from SMA
        </div>
        <div style="margin-top:8px;">
            <span style="color:rgba(255,255,255,0.3); font-size:12px;">
                {'🟢 Above' if pct_from_sma > 0 else '🔴 Below'} 200-day average
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    vix_color = "#e74c3c" if vix_close > 30 else "#f39c12" if vix_close > 20 else "#2ecc71"
    vix_level = "Extreme Fear" if vix_close > 30 else "Elevated" if vix_close > 20 else "Normal"
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">VIX (Fear Index)</div>
        <div class="metric-value" style="color:{vix_color};">{vix_close:.1f}</div>
        <div class="metric-change" style="color:{vix_color};">
            {vix_level}
        </div>
        <div style="margin-top:8px;">
            <span style="color:rgba(255,255,255,0.3); font-size:12px;">
                {'🔴 > 30 (High Risk)' if vix_close > 30 else '🟢 < 30 (Normal)'}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">🎯 Target Exposure</div>
        <div class="metric-value" style="color:{signal_color};">{target}%</div>
        <div style="margin-top:8px;">
            <span style="color:rgba(255,255,255,0.3); font-size:12px;">
                Signal: {signal_label}
            </span>
        </div>
        <div style="margin-top:4px;">
            <span style="color:rgba(255,255,255,0.2); font-size:11px;">
                {action_text}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# SIGNAL CARD (Large, Animated)
# ============================================

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

if signal == "BULL":
    signal_class = "signal-bull"
    signal_icon = "🚀"
    signal_text = "BULL MARKET"
    signal_desc = "All indicators positive. Maintain full exposure."
elif signal == "BEAR":
    signal_class = "signal-bear"
    signal_icon = "⚠️"
    signal_text = "BEAR MARKET"
    signal_desc = "S&P 500 below 200-day SMA. Reduce exposure."
else:
    signal_class = "signal-neutral"
    signal_icon = "⚡"
    signal_text = "CAUTION"
    signal_desc = "VIX elevated. Consider reducing exposure."

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div class="{signal_class}" style="text-align:center; color:white;">
        <div style="font-size:48px; margin-bottom:10px;">{signal_icon}</div>
        <div style="font-size:28px; font-weight:700; letter-spacing:2px;">{signal_text}</div>
        <div style="font-size:16px; opacity:0.9; margin-top:8px;">{signal_desc}</div>
        <div style="font-size:14px; opacity:0.7; margin-top:12px;">
            Target Exposure: <strong>{target}%</strong> | {action_text}
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ============================================
# CHARTS SECTION
# ============================================

st.markdown("### 📊 Market Charts")

# Create professional charts with Plotly
fig = make_subplots(
    rows=3, cols=2,
    shared_xaxes=True,
    vertical_spacing=0.08,
    horizontal_spacing=0.12,
    row_heights=[0.4, 0.3, 0.3],
    subplot_titles=(
        "S&P 500 (SPY) with 200-day SMA",
        "Gauge: Target Exposure",
        "VIX (Fear Index)",
        "Market Regime",
        "Volume",
        "Signal Strength"
    )
)

# 1. SPY Chart
fig.add_trace(
    go.Scatter(
        x=spy_hist.index,
        y=spy_hist['Close'],
        name="SPY Close",
        line=dict(color='#00cec9', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(0,206,201,0.1)'
    ),
    row=1, col=1
)

fig.add_trace(
    go.Scatter(
        x=spy_hist.index,
        y=spy_hist['Close'].rolling(200).mean(),
        name="200-day SMA",
        line=dict(color='#fd79a8', width=2, dash='dash')
    ),
    row=1, col=1
)

# Add shaded regions for buy/sell zones
fig.add_hrect(
    y0=spy_sma_200 * 1.02,
    y1=spy_sma_200 * 1.30,
    fillcolor="rgba(46,204,113,0.05)",
    line_width=0,
    row=1, col=1
)
fig.add_hrect(
    y0=spy_sma_200 * 0.70,
    y1=spy_sma_200 * 0.98,
    fillcolor="rgba(231,76,60,0.05)",
    line_width=0,
    row=1, col=1
)

# 2. Gauge Chart
fig.add_trace(
    go.Indicator(
        mode="gauge+number+delta",
        value=target,
        title={'text': "Exposure", 'font': {'size': 14, 'color': 'white'}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "white"},
            'bar': {'color': signal_color},
            'steps': [
                {'range': [0, 30], 'color': "rgba(231,76,60,0.2)"},
                {'range': [30, 70], 'color': "rgba(241,196,15,0.2)"},
                {'range': [70, 100], 'color': "rgba(46,204,113,0.2)"}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': target
            }
        }
    ),
    row=1, col=2
)

# 3. VIX Chart
fig.add_trace(
    go.Scatter(
        x=vix_hist.index,
        y=vix_hist['Close'],
        name="VIX",
        line=dict(color='#e17055', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(225,112,85,0.1)'
    ),
    row=2, col=1
)

fig.add_hline(
    y=30,
    line_dash="dash",
    line_color="#d63031",
    annotation_text="Risk Threshold (30)",
    row=2, col=1
)

# 4. Market Regime (Heatmap-style)
regime_colors = ['#2ecc71', '#f1c40f', '#e74c3c']
regime_labels = ['Bull', 'Neutral', 'Bear']
regime_value = 0 if signal == "BULL" else 1 if signal == "NEUTRAL" else 2

fig.add_trace(
    go.Indicator(
        mode="number",
        value=regime_value,
        title={'text': "Regime", 'font': {'size': 14, 'color': 'white'}},
        number={'font': {'size': 0}},
        domain={'x': [0, 1], 'y': [0, 1]}
    ),
    row=2, col=2
)

# Add a colored box for regime
fig.add_annotation(
    x=0.5, y=0.5,
    text=f"{signal_emoji} {signal_text}",
    font=dict(size=24, color='white'),
    showarrow=False,
    row=2, col=2,
    bgcolor=signal_color,
    bordercolor='white',
    borderwidth=2,
    borderpad=10,
    opacity=0.8
)

# 5. Volume Chart
fig.add_trace(
    go.Bar(
        x=spy_hist.index[-60:],
        y=spy_hist['Volume'].iloc[-60:] / 1e6,
        name="Volume (M)",
        marker_color='rgba(108,92,231,0.6)'
    ),
    row=3, col=1
)

# 6. Signal Strength
signal_strength = 0
if signal == "BULL":
    signal_strength = min(100, 70 + (100 - vix_close) / 2)
elif signal == "BEAR":
    signal_strength = min(100, 70 + (spy_sma_200 - spy_close) / 10)
else:
    signal_strength = 50

fig.add_trace(
    go.Indicator(
        mode="gauge+number",
        value=signal_strength,
        title={'text': "Signal Strength", 'font': {'size': 14, 'color': 'white'}},
        domain={'x': [0, 1], 'y': [0, 1]},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': "white"},
            'bar': {'color': '#6c5ce7'},
            'steps': [
                {'range': [0, 30], 'color': "rgba(231,76,60,0.2)"},
                {'range': [30, 70], 'color': "rgba(241,196,15,0.2)"},
                {'range': [70, 100], 'color': "rgba(46,204,113,0.2)"}
            ]
        }
    ),
    row=3, col=2
)

# Update layout
fig.update_layout(
    height=900,
    showlegend=True,
    template="plotly_dark",
    hovermode="x unified",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.05)',
    font=dict(color='white'),
    legend=dict(
        bgcolor='rgba(0,0,0,0.3)',
        bordercolor='rgba(255,255,255,0.1)',
        borderwidth=1
    )
)

fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================
# SIDEBAR - Detailed Information
# ============================================

with st.sidebar:
    st.markdown("### 📋 Strategy Dashboard")
    
    st.markdown("---")
    
    # Current snapshot
    st.markdown("#### 🔍 Current Snapshot")
    st.write(f"**S&P 500:** ${spy_close:.2f}")
    st.write(f"**200-day SMA:** ${spy_sma_200:.2f}")
    st.write(f"**VIX:** {vix_close:.1f}")
    st.write(f"**Target Exposure:** **{target}%**")
    st.write(f"**Regime:** {signal_emoji} **{signal_text}**")
    
    st.markdown("---")
    
    # Strategy rules
    st.markdown("#### 📋 Strategy Rules")
    st.markdown("""
    | Condition | Action |
    |-----------|--------|
    | SPY < 200 SMA | 🔴 **SELL 100%** |
    | SPY > 200 SMA + VIX > 30 | 🟠 **SELL 50%** |
    | SPY > 200 SMA + VIX < 30 | 🟢 **HOLD 100%** |
    """)
    
    st.markdown("---")
    
    # Status indicators
    st.markdown("#### 📊 Status")
    
    # SPY status
    if spy_close >= spy_sma_200:
        st.success("🟢 S&P 500: Above 200-day SMA")
    else:
        st.error("🔴 S&P 500: Below 200-day SMA")
    
    # VIX status
    if vix_close <= 20:
        st.success(f"🟢 VIX: {vix_close:.1f} (Normal)")
    elif vix_close <= 30:
        st.warning(f"🟡 VIX: {vix_close:.1f} (Elevated)")
    else:
        st.error(f"🔴 VIX: {vix_close:.1f} (Extreme)")
    
    # Target exposure
    if target == 100:
        st.success(f"🎯 Target: {target}% (Full Invested)")
    elif target == 50:
        st.warning(f"🎯 Target: {target}% (Half Invested)")
    else:
        st.error(f"🎯 Target: {target}% (Cash)")
    
    st.markdown("---")
    
    # Action required
    st.markdown("#### 🎯 Action Required")
    if target == 100:
        st.info("✅ No action needed. Continue holding.")
    elif target == 50:
        st.warning("⚠️ Reduce exposure to 50% at next market open.")
    else:
        st.error("🚨 Exit all positions at next market open.")
    
    st.markdown("---")
    
    # Footer
    st.caption(f"Data: Yahoo Finance")
    st.caption(f"Strategy: v4 - Backtest Faithful")
    st.caption(f"Updated: {datetime.now().strftime('%H:%M:%S')} ET")
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ============================================
# FOOTER
# ============================================

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown("""
    <div style="text-align:center; color:rgba(255,255,255,0.2); font-size:12px; padding:20px;">
        ⚡ Powered by Streamlit & Yahoo Finance<br>
        Max Sharpe + Value Blend Strategy (v4) • Backtest Faithful
    </div>
    """, unsafe_allow_html=True)
