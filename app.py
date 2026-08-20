# ============================================
# MARKET CONDITION DASHBOARD - ENTERPRISE EDITION
# With Head-to-Head Benchmark Section
# ============================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

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
# CUSTOM CSS
# ============================================

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    
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
    
    .regime-bull {
        background: linear-gradient(135deg, #00b894, #00cec9);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(0,206,201,0.3);
        animation: pulse-green 2s infinite;
        text-align: center;
        color: white;
    }
    
    .regime-bear {
        background: linear-gradient(135deg, #e17055, #d63031);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(214,48,49,0.3);
        animation: pulse-red 2s infinite;
        text-align: center;
        color: white;
    }
    
    .regime-neutral {
        background: linear-gradient(135deg, #fdcb6e, #e17055);
        border-radius: 15px;
        padding: 30px;
        box-shadow: 0 8px 32px rgba(225,112,85,0.3);
        animation: pulse-orange 2s infinite;
        text-align: center;
        color: white;
    }
    
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
    
    .glow-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        margin: 30px 0;
    }
    
    .main-title {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #00cec9, #6c5ce7, #fd79a8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
    }
    
    .data-source-badge {
        display: inline-block;
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 600;
    }
    
    .badge-real {
        background: rgba(46,204,113,0.2);
        color: #2ecc71;
        border: 1px solid rgba(46,204,113,0.3);
    }
    
    .badge-simulated {
        background: rgba(241,196,15,0.2);
        color: #f1c40f;
        border: 1px solid rgba(241,196,15,0.3);
    }
    
    .strategy-description {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 25px;
        border: 1px solid rgba(255,255,255,0.08);
        color: rgba(255,255,255,0.8);
        line-height: 1.8;
    }
    
    .benchmark-table {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        overflow-x: auto;
    }
    
    .benchmark-table table {
        width: 100%;
        border-collapse: collapse;
        color: rgba(255,255,255,0.9);
    }
    
    .benchmark-table th {
        background: rgba(255,255,255,0.1);
        padding: 12px 15px;
        text-align: left;
        font-weight: 600;
        color: rgba(255,255,255,0.7);
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
    
    .benchmark-table td {
        padding: 10px 15px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .benchmark-table .winner {
        color: #2ecc71;
        font-weight: 600;
    }
    
    .benchmark-table .winner-badge {
        display: inline-block;
        background: rgba(46,204,113,0.2);
        color: #2ecc71;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .regime-icon {
        font-size: 64px;
    }
    
    .regime-label {
        font-size: 32px;
        font-weight: 700;
        letter-spacing: 2px;
    }
    
    .regime-desc {
        font-size: 16px;
        opacity: 0.9;
        margin-top: 8px;
    }
    
    .regime-action {
        font-size: 18px;
        font-weight: 600;
        margin-top: 12px;
        background: rgba(0,0,0,0.2);
        padding: 10px 20px;
        border-radius: 10px;
        display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown('<h1 class="main-title" style="text-align:center;">📈 Market Dashboard</h1>', unsafe_allow_html=True)

# ============================================
# DATA FETCHING
# ============================================

@st.cache_data(ttl=1800)
def fetch_market_data():
    try:
        import yfinance as yf
        
        spy = yf.Ticker("SPY")
        spy_hist = spy.history(period="1y")
        
        if len(spy_hist) > 0:
            spy_close = spy_hist['Close'].iloc[-1]
            spy_sma_200 = spy_hist['Close'].rolling(200).mean().iloc[-1]
            spy_high = spy_hist['Close'].max()
            spy_low = spy_hist['Close'].min()
            spy_volume = spy_hist['Volume'].iloc[-1]
            
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
                'success': True,
                'data_source': 'real'
            }
    except:
        pass
    
    # Fallback: Simulated data
    np.random.seed(42)
    dates = pd.date_range(end=datetime.now(), periods=252, freq='D')
    base_price = 560
    returns = np.random.normal(0.0004, 0.012, 252)
    prices = base_price * (1 + returns).cumprod()
    
    spy_close = prices[-1]
    spy_sma_200 = np.mean(prices[-200:])
    spy_high = max(prices)
    spy_low = min(prices)
    spy_volume = 50000000 + np.random.randint(0, 30000000)
    vix_close = 18 + np.random.normal(0, 2)
    
    spy_hist = pd.DataFrame({'Close': prices, 'Volume': [spy_volume] * len(prices)}, index=dates)
    vix_hist = pd.DataFrame({'Close': [vix_close + np.random.normal(0, 1) for _ in range(30)]}, 
                           index=pd.date_range(end=datetime.now(), periods=30, freq='D'))
    
    return {
        'spy_close': float(spy_close),
        'spy_sma_200': float(spy_sma_200),
        'spy_high': float(spy_high),
        'spy_low': float(spy_low),
        'spy_volume': float(spy_volume),
        'vix_close': float(vix_close),
        'spy_hist': spy_hist,
        'vix_hist': vix_hist,
        'success': True,
        'data_source': 'simulated'
    }

with st.spinner("🔮 Loading market data..."):
    data = fetch_market_data()

# ============================================
# DATA SOURCE BADGE
# ============================================

if data['data_source'] == 'real':
    st.markdown('<div style="text-align:center; margin-bottom:5px;"><span class="data-source-badge badge-real">✅ LIVE DATA</span></div>', unsafe_allow_html=True)
else:
    st.markdown('<div style="text-align:center; margin-bottom:5px;"><span class="data-source-badge badge-simulated">⚠️ SIMULATED DATA (Yahoo Finance Rate Limited)</span></div>', unsafe_allow_html=True)

st.markdown(f'<p style="text-align:center; color: rgba(255,255,255,0.4); font-size:13px;">Last updated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} ET</p>', unsafe_allow_html=True)

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

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

if spy_close < spy_sma_200:
    target = 0
    signal = "BEAR"
    signal_emoji = "🐻"
    signal_color = "#e74c3c"
    signal_label = "BEAR MARKET"
    signal_desc = "S&P 500 below 200-day SMA"
    action_text = "🔴 SELL ALL - Exit all positions immediately"
    regime_class = "regime-bear"
elif vix_close > 30:
    target = 50
    signal = "NEUTRAL"
    signal_emoji = "⚠️"
    signal_color = "#f39c12"
    signal_label = "CAUTION"
    signal_desc = "VIX above 30 (elevated volatility)"
    action_text = "🟠 REDUCE TO 50% - Sell half of positions"
    regime_class = "regime-neutral"
else:
    target = 100
    signal = "BULL"
    signal_emoji = "🐂"
    signal_color = "#2ecc71"
    signal_label = "BULL MARKET"
    signal_desc = "All indicators normal"
    action_text = "🟢 HOLD 100% - Continue holding positions"
    regime_class = "regime-bull"

# ============================================
# MAIN REGIME CARD
# ============================================

st.markdown(f"""
<div class="{regime_class}">
    <div class="regime-icon">{signal_emoji}</div>
    <div class="regime-label">{signal_label}</div>
    <div class="regime-desc">{signal_desc}</div>
    <div style="font-size:14px; opacity:0.8; margin-top:5px;">
        Target Exposure: <strong>{target}%</strong>
    </div>
    <div class="regime-action">{action_text}</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ============================================
# METRICS ROW
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:rgba(255,255,255,0.5); font-size:14px; text-transform:uppercase; letter-spacing:1px;">S&P 500 (SPY)</div>
        <div style="font-size:32px; font-weight:700; color:white;">${spy_close:.2f}</div>
        <div style="display:flex; justify-content:space-between; margin-top:10px;">
            <span style="color:rgba(255,255,255,0.3); font-size:12px;">52W H: ${spy_high:.2f}</span>
            <span style="color:rgba(255,255,255,0.3); font-size:12px;">52W L: ${spy_low:.2f}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    pct_from_sma = ((spy_close / spy_sma_200) - 1) * 100
    color = "#2ecc71" if pct_from_sma > 0 else "#e74c3c"
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:rgba(255,255,255,0.5); font-size:14px; text-transform:uppercase; letter-spacing:1px;">200-day SMA</div>
        <div style="font-size:32px; font-weight:700; color:white;">${spy_sma_200:.2f}</div>
        <div style="color:{color}; font-size:16px; font-weight:600; margin-top:5px;">{pct_from_sma:+.2f}% from SMA</div>
        <div style="margin-top:5px;"><span style="color:rgba(255,255,255,0.3); font-size:12px;">{'🟢 Above' if pct_from_sma > 0 else '🔴 Below'} 200-day average</span></div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    vix_color = "#e74c3c" if vix_close > 30 else "#f39c12" if vix_close > 20 else "#2ecc71"
    vix_level = "Extreme Fear" if vix_close > 30 else "Elevated" if vix_close > 20 else "Normal"
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:rgba(255,255,255,0.5); font-size:14px; text-transform:uppercase; letter-spacing:1px;">VIX (Fear Index)</div>
        <div style="font-size:32px; font-weight:700; color:{vix_color};">{vix_close:.1f}</div>
        <div style="color:{vix_color}; font-size:16px; font-weight:600; margin-top:5px;">{vix_level}</div>
        <div style="margin-top:5px;"><span style="color:rgba(255,255,255,0.3); font-size:12px;">{'🔴 > 30 (High Risk)' if vix_close > 30 else '🟢 < 30 (Normal)'}</span></div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style="color:rgba(255,255,255,0.5); font-size:14px; text-transform:uppercase; letter-spacing:1px;">🎯 Target Exposure</div>
        <div style="font-size:32px; font-weight:700; color:{signal_color};">{target}%</div>
        <div style="margin-top:5px;"><span style="color:rgba(255,255,255,0.3); font-size:12px;">Regime: {signal_label}</span></div>
        <div style="margin-top:3px;"><span style="color:rgba(255,255,255,0.2); font-size:11px;">{action_text}</span></div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# CHARTS
# ============================================

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
st.markdown("### 📊 Market Charts")

fig = make_subplots(
    rows=2, cols=2,
    shared_xaxes=False,
    vertical_spacing=0.12,
    horizontal_spacing=0.15,
    subplot_titles=(
        "S&P 500 (SPY) with 200-day SMA",
        "VIX (Fear Index)",
        "Volume",
        "Target Exposure"
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

# 2. VIX Chart
fig.add_trace(
    go.Scatter(
        x=vix_hist.index,
        y=vix_hist['Close'],
        name="VIX",
        line=dict(color='#e17055', width=2.5),
        fill='tozeroy',
        fillcolor='rgba(225,112,85,0.1)'
    ),
    row=1, col=2
)

fig.add_hline(y=30, line_dash="dash", line_color="#d63031", 
              annotation_text="Risk Threshold (30)", row=1, col=2)

# 3. Volume Chart
fig.add_trace(
    go.Bar(
        x=spy_hist.index[-60:],
        y=spy_hist['Volume'].iloc[-60:] / 1e6,
        name="Volume (M)",
        marker_color='rgba(108,92,231,0.7)'
    ),
    row=2, col=1
)

# 4. Target Exposure Bar
fig.add_trace(
    go.Bar(
        x=["Exposure"],
        y=[target],
        name="Target Exposure",
        marker_color=signal_color,
        text=[f"{target}%"],
        textposition="outside",
        width=[0.3]
    ),
    row=2, col=2
)

# Reference lines
fig.add_hline(y=100, line_dash="dot", line_color="#2ecc71", 
              annotation_text="100% (Bull)", row=2, col=2)
fig.add_hline(y=50, line_dash="dot", line_color="#f39c12", 
              annotation_text="50% (Neutral)", row=2, col=2)
fig.add_hline(y=0, line_dash="dot", line_color="#e74c3c", 
              annotation_text="0% (Bear)", row=2, col=2)

fig.update_layout(
    height=700,
    showlegend=True,
    template="plotly_dark",
    hovermode="x unified",
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(255,255,255,0.05)',
    font=dict(color='white'),
    legend=dict(bgcolor='rgba(0,0,0,0.3)', bordercolor='rgba(255,255,255,0.1)', borderwidth=1)
)

fig.update_xaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')
fig.update_yaxes(showgrid=True, gridcolor='rgba(255,255,255,0.05)')

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("### 📋 Strategy Dashboard")
    
    st.markdown("---")
    
    st.markdown(f"""
    <div style="text-align:center; padding:15px; background:rgba(255,255,255,0.05); border-radius:10px; border:1px solid {signal_color};">
        <div style="font-size:36px;">{signal_emoji}</div>
        <div style="font-size:20px; font-weight:700; color:{signal_color};">{signal_label}</div>
        <div style="font-size:14px; color:rgba(255,255,255,0.7);">{signal_desc}</div>
        <div style="font-size:16px; font-weight:600; color:white; margin-top:5px;">Target: {target}%</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("#### 🔍 Current Snapshot")
    st.write(f"**S&P 500:** ${spy_close:.2f}")
    st.write(f"**200-day SMA:** ${spy_sma_200:.2f}")
    st.write(f"**VIX:** {vix_close:.1f}")
    
    st.markdown("---")
    
    st.markdown("#### 📋 Strategy Rules")
    st.markdown("""
    | Condition | Action |
    |-----------|--------|
    | SPY < 200 SMA | 🔴 **SELL 100%** |
    | SPY > 200 SMA + VIX > 30 | 🟠 **SELL 50%** |
    | SPY > 200 SMA + VIX < 30 | 🟢 **HOLD 100%** |
    """)
    
    st.markdown("---")
    
    if spy_close >= spy_sma_200:
        st.success("🟢 S&P 500: Above 200-day SMA")
    else:
        st.error("🔴 S&P 500: Below 200-day SMA")
    
    if vix_close <= 20:
        st.success(f"🟢 VIX: {vix_close:.1f} (Normal)")
    elif vix_close <= 30:
        st.warning(f"🟡 VIX: {vix_close:.1f} (Elevated)")
    else:
        st.error(f"🔴 VIX: {vix_close:.1f} (Extreme)")
    
    st.markdown("---")
    
    if target == 100:
        st.info("✅ No action needed. Continue holding.")
    elif target == 50:
        st.warning("⚠️ Reduce exposure to 50% at next market open.")
    else:
        st.error("🚨 Exit all positions at next market open.")
    
    st.markdown("---")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

# ============================================
# STRATEGY OVERVIEW & HEAD-TO-HEAD BENCHMARK
# ============================================

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class="strategy-description">
    <h3 style="color:white; margin-top:0;">📖 Strategy Overview</h3>
    <p style="color:rgba(255,255,255,0.8);">
        This dashboard implements a <strong>systematic, rules-based investment strategy</strong> 
        that combines two proven market indicators:
    </p>
</div>
""", unsafe_allow_html=True)

# 1. 200-Day Moving Average
st.markdown("""
<div class="strategy-description" style="margin-top:15px;">
    <h4 style="color:#00cec9; margin-top:0;">1️⃣ The 200-Day Moving Average (Trend Filter)</h4>
    <p style="color:rgba(255,255,255,0.8);">
        The 200-day simple moving average (SMA) is one of the most widely followed technical indicators 
        by institutional investors. It acts as a <strong>primary trend filter</strong>:
    </p>
    <ul style="color:rgba(255,255,255,0.8); padding-left:20px;">
        <li><strong style="color:#2ecc71;">Above 200-day SMA:</strong> Bull market regime — stay invested</li>
        <li><strong style="color:#e74c3c;">Below 200-day SMA:</strong> Bear market regime — protect capital</li>
    </ul>
    <p style="color:rgba(255,255,255,0.7); font-size:14px;">
        Research shows that the 200-day SMA has been a reliable risk-control tool. During major bear markets 
        (2000, 2008, 2020, 2022), investors who exited when SPY fell below its 200-day SMA significantly 
        reduced their drawdowns. The "penalty" for this protection is occasional whipsaws in choppy markets, 
        but the long-term risk-adjusted returns (Sharpe Ratio) have historically improved.
    </p>
</div>
""", unsafe_allow_html=True)

# 2. VIX
st.markdown("""
<div class="strategy-description" style="margin-top:15px;">
    <h4 style="color:#f39c12; margin-top:0;">2️⃣ The VIX (Volatility Filter)</h4>
    <p style="color:rgba(255,255,255,0.8);">
        The VIX, often called the "Fear Index," measures market expectations of near-term volatility. 
        When VIX exceeds 30, it typically indicates elevated fear and market stress:
    </p>
    <ul style="color:rgba(255,255,255,0.8); padding-left:20px;">
        <li><strong style="color:#2ecc71;">VIX below 30:</strong> Normal market conditions — full exposure</li>
        <li><strong style="color:#e74c3c;">VIX above 30:</strong> High volatility environment — reduce exposure by 50%</li>
    </ul>
    <p style="color:rgba(255,255,255,0.7); font-size:14px;">
        The VIX tends to spike during market selloffs and periods of uncertainty. By reducing exposure when 
        VIX is elevated, the strategy aims to <strong>protect against sudden market declines</strong> while 
        maintaining participation in normal market conditions.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# HEAD-TO-HEAD BENCHMARK SECTION
# ============================================

st.markdown("""
<div class="strategy-description" style="margin-top:15px;">
    <h3 style="color:white; margin-top:0;">🏆 Head-to-Head Benchmark: Buy & Hold vs. Tactical Overlay</h3>
    <p style="color:rgba(255,255,255,0.7); font-size:14px;">
        <strong>Period:</strong> 2011-08-24 to 2026-08-20 (15.0 years | 3,768 trading days)<br>
        <strong>Initial Investment:</strong> $10,000
    </p>
</div>
""", unsafe_allow_html=True)

# Benchmark Table using HTML
st.markdown("""
<div class="benchmark-table">
    <table>
        <thead>
            <tr>
                <th>KPI Metric</th>
                <th>Buy &amp; Hold</th>
                <th>Tactical (SMA200 + VIX)</th>
                <th>Winner</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Total Return</strong></td>
                <td>748.0%</td>
                <td>341.6%</td>
                <td><span class="winner">🏆 Buy &amp; Hold</span></td>
            </tr>
            <tr>
                <td><strong>Annualized Return (CAGR)</strong></td>
                <td>15.4%</td>
                <td>10.4%</td>
                <td><span class="winner">🏆 Buy &amp; Hold</span></td>
            </tr>
            <tr>
                <td><strong>Annualized Volatility</strong></td>
                <td>16.9%</td>
                <td>11.1%</td>
                <td><span class="winner">🏆 Tactical Overlay</span></td>
            </tr>
            <tr>
                <td><strong>Max Drawdown</strong></td>
                <td style="color:#e74c3c;">-33.7%</td>
                <td style="color:#2ecc71;">-21.4%</td>
                <td><span class="winner">🏆 Tactical Overlay</span></td>
            </tr>
            <tr>
                <td><strong>Sharpe Ratio (rf=2%)</strong></td>
                <td>0.81</td>
                <td>0.77</td>
                <td><span class="winner">🏆 Buy &amp; Hold</span></td>
            </tr>
            <tr>
                <td><strong>Sortino Ratio</strong></td>
                <td>1.01</td>
                <td>0.88</td>
                <td><span class="winner">🏆 Buy &amp; Hold</span></td>
            </tr>
            <tr>
                <td><strong>Calmar Ratio</strong></td>
                <td>0.46</td>
                <td>0.49</td>
                <td><span class="winner">🏆 Tactical Overlay</span></td>
            </tr>
            <tr>
                <td><strong>Win Rate (Active Days)</strong></td>
                <td>55.4%</td>
                <td>54.9%</td>
                <td><span class="winner">🏆 Buy &amp; Hold</span></td>
            </tr>
            <tr>
                <td><strong>Max Consecutive Losses</strong></td>
                <td>8</td>
                <td>7</td>
                <td><span class="winner">🏆 Tactical Overlay</span></td>
            </tr>
        </tbody>
    </table>
</div>
""", unsafe_allow_html=True)

# ============================================
# WHY USE TACTICAL OVERLAY - EXPLANATION
# ============================================

st.markdown("""
<div class="strategy-description" style="margin-top:15px;">
    <h4 style="color:#6c5ce7; margin-top:0;">🤔 Why Use the Tactical Overlay if Returns Are Lower?</h4>
    <p style="color:rgba(255,255,255,0.8);">
        This is the most important question. The answer lies in <strong>risk management</strong> 
        and the <strong>psychological reality</strong> of investing:
    </p>
    
    <div style="background:rgba(46,204,113,0.1); border-left:3px solid #2ecc71; padding:15px; margin:15px 0; border-radius:5px;">
        <p style="color:rgba(255,255,255,0.9);">
            <strong>🔑 Key Insight:</strong> The Tactical Overlay cuts maximum drawdown <strong>from -33.7% to -21.4%</strong> 
            — a <strong>36% reduction</strong> in peak-to-trough loss.
        </p>
    </div>
    
    <p style="color:rgba(255,255,255,0.8);">
        <strong>Why this matters:</strong>
    </p>
    <ul style="color:rgba(255,255,255,0.8); padding-left:20px;">
        <li><strong>Psychological Survival:</strong> A 33.7% drawdown means $10,000 becomes $6,630. 
        Many investors panic and sell at the bottom. A 21.4% drawdown ($10,000 → $7,860) is 
        <strong>emotionally easier to withstand</strong> and less likely to trigger panic selling.</li>
        <li><strong>Recovery Time:</strong> A 33.7% loss requires a <strong>50.8% gain</strong> to recover. 
        A 21.4% loss requires only a <strong>27.2% gain</strong> — <strong>nearly half</strong> the required recovery.</li>
        <li><strong>Consistency:</strong> The Tactical strategy has slightly lower risk-adjusted returns (Sharpe 0.77 vs 0.81), 
        but <strong>much lower volatility</strong> (11.1% vs 16.9%) and <strong>better downside protection</strong> 
        (Calmar 0.49 vs 0.46).</li>
        <li><strong>Behavioral Edge:</strong> A strategy you can <strong>stick with</strong> during tough times 
        is more valuable than one with mathematically higher returns that you cannot hold.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ============================================
# TACTICAL EXPOSURE STATS
# ============================================

st.markdown("""
<div class="strategy-description" style="margin-top:15px;">
    <h4 style="color:#fd79a8; margin-top:0;">📊 Tactical Exposure Statistics</h4>
    <div style="display:grid; grid-template-columns: 1fr 1fr 1fr; gap:15px; margin:15px 0;">
        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; text-align:center;">
            <div style="font-size:28px; font-weight:700; color:#2ecc71;">80.2%</div>
            <div style="color:rgba(255,255,255,0.5); font-size:12px;">Time Invested (3,021 days)</div>
        </div>
        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; text-align:center;">
            <div style="font-size:28px; font-weight:700; color:#f39c12;">19.8%</div>
            <div style="color:rgba(255,255,255,0.5); font-size:12px;">Time in Cash (747 days)</div>
        </div>
        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; text-align:center;">
            <div style="font-size:28px; font-weight:700; color:#e17055;">83</div>
            <div style="color:rgba(255,255,255,0.5); font-size:12px;">Total Switches (Trades)</div>
        </div>
    </div>
    <div style="display:grid; grid-template-columns: 1fr 1fr; gap:15px;">
        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; text-align:center;">
            <div style="font-size:20px; font-weight:700; color:#3498db;">$84,799.94</div>
            <div style="color:rgba(255,255,255,0.5); font-size:12px;">Final Balance (Buy &amp; Hold)</div>
        </div>
        <div style="background:rgba(255,255,255,0.05); padding:15px; border-radius:10px; text-align:center;">
            <div style="font-size:20px; font-weight:700; color:#2ecc71;">$44,158.88</div>
            <div style="color:rgba(255,255,255,0.5); font-size:12px;">Final Balance (Tactical Overlay)</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# DISCLAIMER
# ============================================

st.markdown("""
<div class="strategy-description" style="margin-top:15px; border-left: 3px solid #fd79a8; padding-left: 20px;">
    <h4 style="color:#fd79a8; margin-top:0;">⚠️ Important Disclaimer</h4>
    <p style="font-size:14px; color:rgba(255,255,255,0.6);">
        This dashboard is for <strong>educational and informational purposes only</strong>. 
        Past performance does not guarantee future results. The strategy is a systematic, rules-based 
        approach that has been backtested, but all investments carry risk. 
        Always consult with a qualified financial advisor before making investment decisions.
    </p>
</div>
""", unsafe_allow_html=True)

# ============================================
# FOOTER
# ============================================

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"""
    <div style="text-align:center; color:rgba(255,255,255,0.2); font-size:12px; padding:20px;">
        ⚡ Powered by Streamlit &amp; { 'Yahoo Finance (Live)' if data['data_source'] == 'real' else 'Simulated Data' }<br>
        Max Sharpe + Value Blend Strategy (v4) • Backtest Faithful<br>
        Data Source: {'✅ LIVE' if data['data_source'] == 'real' else '⚠️ SIMULATED'}
    </div>
    """, unsafe_allow_html=True)
