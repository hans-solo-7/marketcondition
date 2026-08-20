# ============================================
# MARKET CONDITION DASHBOARD - WITH S6 SIGNAL
# Complete working version - ALL SYNTAX ERRORS FIXED
# ============================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime
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
    
    .signal-qqq {
        background: linear-gradient(135deg, #6c5ce7, #a29bfe);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(108,92,231,0.4);
        animation: pulse-qqq 2s infinite;
        text-align: center;
        color: white;
    }
    
    .signal-gld {
        background: linear-gradient(135deg, #fdcb6e, #f39c12);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(243,156,18,0.4);
        animation: pulse-gold 2s infinite;
        text-align: center;
        color: white;
    }
    
    .signal-bil {
        background: linear-gradient(135deg, #74b9ff, #0984e3);
        border-radius: 15px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(9,132,227,0.4);
        animation: pulse-blue 2s infinite;
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
    
    @keyframes pulse-qqq {
        0% { box-shadow: 0 8px 32px rgba(108,92,231,0.4); }
        50% { box-shadow: 0 8px 48px rgba(108,92,231,0.7); }
        100% { box-shadow: 0 8px 32px rgba(108,92,231,0.4); }
    }
    
    @keyframes pulse-gold {
        0% { box-shadow: 0 8px 32px rgba(243,156,18,0.4); }
        50% { box-shadow: 0 8px 48px rgba(243,156,18,0.7); }
        100% { box-shadow: 0 8px 32px rgba(243,156,18,0.4); }
    }
    
    @keyframes pulse-blue {
        0% { box-shadow: 0 8px 32px rgba(9,132,227,0.4); }
        50% { box-shadow: 0 8px 48px rgba(9,132,227,0.7); }
        100% { box-shadow: 0 8px 32px rgba(9,132,227,0.4); }
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
        tickers = ["SPY", "QQQ", "GLD", "BIL", "^VIX"]
        df = yf.download(tickers, period="2y", interval="1d", progress=False)
        
        if isinstance(df.columns, pd.MultiIndex):
            closes = df["Close"].copy()
        else:
            closes = df.copy()
        
        closes = closes.ffill().dropna()
        
        spy = closes["SPY"]
        qqq = closes["QQQ"]
        gld = closes["GLD"]
        bil = closes["BIL"]
        vix = closes["^VIX"]
        
        sma200_spy = spy.rolling(window=200).mean()
        ema50_spy = spy.ewm(span=50, adjust=False).mean()
        gld_mom = gld.pct_change(60)
        
        current_spy = float(spy.iloc[-1])
        current_qqq = float(qqq.iloc[-1])
        current_gld = float(gld.iloc[-1])
        current_bil = float(bil.iloc[-1])
        current_vix = float(vix.iloc[-1])
        current_sma200 = float(sma200_spy.iloc[-1])
        current_ema50 = float(ema50_spy.iloc[-1])
        current_gld_mom = float(gld_mom.iloc[-1])
        last_date = closes.index[-1]
        
        is_above_sma200 = current_spy > current_sma200
        is_above_ema50 = current_spy > current_ema50
        
        # S6 Signal
        if current_vix >= 30 or not is_above_sma200:
            if current_gld_mom > 0:
                s6_target = "GLD"
                s6_reason = f"Defensive (VIX >= 30 or SPY < 200 SMA) -> Gold momentum positive ({current_gld_mom*100:+.1f}%)"
                s6_color = "#f39c12"
                s6_class = "signal-gld"
                s6_emoji = "🪙"
            else:
                s6_target = "BIL"
                s6_reason = f"Defensive (VIX >= 30 or SPY < 200 SMA) -> Gold momentum negative ({current_gld_mom*100:+.1f}%)"
                s6_color = "#0984e3"
                s6_class = "signal-bil"
                s6_emoji = "🏦"
        else:
            if current_vix < 20:
                s6_target = "QQQ"
                s6_reason = "Calm Bull (SPY > 200 SMA, VIX < 20) -> Tech Equity"
                s6_color = "#6c5ce7"
                s6_class = "signal-qqq"
                s6_emoji = "🚀"
            else:
                s6_target = "SPY"
                s6_reason = "Moderate Bull (SPY > 200 SMA, 20 <= VIX < 30) -> Broad Equity"
                s6_color = "#00cec9"
                s6_class = "regime-bull"
                s6_emoji = "🐂"
        
        # Original regime
        if current_spy < current_sma200:
            target = 0
            signal_emoji = "🐻"
            signal_color = "#e74c3c"
            signal_label = "BEAR MARKET"
            signal_desc = "S&P 500 below 200-day SMA"
            action_text = "SELL ALL - Exit all positions"
            regime_class = "regime-bear"
        elif current_vix > 30:
            target = 50
            signal_emoji = "⚠️"
            signal_color = "#f39c12"
            signal_label = "CAUTION"
            signal_desc = "VIX above 30 (elevated volatility)"
            action_text = "REDUCE TO 50% - Sell half"
            regime_class = "regime-neutral"
        else:
            target = 100
            signal_emoji = "🐂"
            signal_color = "#2ecc71"
            signal_label = "BULL MARKET"
            signal_desc = "All indicators normal"
            action_text = "HOLD 100% - Continue holding"
            regime_class = "regime-bull"
        
        return {
            'spy_close': current_spy,
            'qqq_close': current_qqq,
            'gld_close': current_gld,
            'bil_close': current_bil,
            'vix_close': current_vix,
            'sma200': current_sma200,
            'ema50': current_ema50,
            'gld_mom': current_gld_mom,
            'date': last_date,
            'spy_hist': closes['SPY'],
            'qqq_hist': closes['QQQ'],
            'gld_hist': closes['GLD'],
            'vix_hist': closes['^VIX'],
            'bil_hist': closes['BIL'],
            's6_target': s6_target,
            's6_reason': s6_reason,
            's6_color': s6_color,
            's6_class': s6_class,
            's6_emoji': s6_emoji,
            'is_above_sma200': is_above_sma200,
            'is_above_ema50': is_above_ema50,
            'target': target,
            'signal_emoji': signal_emoji,
            'signal_color': signal_color,
            'signal_label': signal_label,
            'signal_desc': signal_desc,
            'action_text': action_text,
            'regime_class': regime_class,
            'success': True,
            'data_source': 'real'
        }
    except Exception as e:
        return None

with st.spinner("Loading market data..."):
    data = fetch_market_data()

if data is None:
    st.error("Failed to fetch data. Please try again.")
    st.stop()

# ============================================
# DATA SOURCE BADGE
# ============================================

st.markdown('<div style="text-align:center; margin-bottom:5px;"><span class="data-source-badge badge-real">✅ LIVE DATA</span></div>', unsafe_allow_html=True)
st.markdown(f'<p style="text-align:center; color: rgba(255,255,255,0.4); font-size:13px;">Last updated: {data["date"].strftime("%Y-%m-%d %H:%M")} ET</p>', unsafe_allow_html=True)

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ============================================
# S6 SIGNAL CARD
# ============================================

st.markdown(f"""
<div class="{data['s6_class']}">
    <div style="font-size:48px;">{data['s6_emoji']}</div>
    <div style="font-size:28px; font-weight:700; letter-spacing:1px;">🎯 TARGET: {data['s6_target']}</div>
    <div style="font-size:16px; opacity:0.9; margin-top:8px;">{data['s6_reason']}</div>
    <div style="font-size:14px; opacity:0.7; margin-top:8px;">
        SPY: ${data['spy_close']:.2f} | 200 SMA: ${data['sma200']:.2f} | VIX: {data['vix_close']:.1f}
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ============================================
# TWO COLUMN LAYOUT
# ============================================

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"""
    <div class="{data['regime_class']}" style="padding:20px;">
        <div style="font-size:40px;">{data['signal_emoji']}</div>
        <div style="font-size:24px; font-weight:700;">{data['signal_label']}</div>
        <div style="font-size:14px; opacity:0.8;">{data['signal_desc']}</div>
        <div style="font-size:16px; font-weight:600; margin-top:8px; background:rgba(0,0,0,0.2); padding:8px 16px; border-radius:8px; display:inline-block;">
            Exposure: {data['target']}%
        </div>
        <div style="font-size:13px; margin-top:5px; opacity:0.6;">{data['action_text']}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.05); border-radius:15px; padding:20px; border:1px solid rgba(255,255,255,0.08); height:100%;">
        <div style="color:rgba(255,255,255,0.5); font-size:14px; text-transform:uppercase; letter-spacing:1px; margin-bottom:10px;">📊 S6 Signal Details</div>
        <div style="display:grid; grid-template-columns:1fr 1fr; gap:10px;">
            <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; text-align:center;">
                <div style="font-size:18px; font-weight:700; color:#00cec9;">${data['spy_close']:.2f}</div>
                <div style="font-size:11px; color:rgba(255,255,255,0.4);">SPY Price</div>
            </div>
            <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; text-align:center;">
                <div style="font-size:18px; font-weight:700; color:#fd79a8;">${data['sma200']:.2f}</div>
                <div style="font-size:11px; color:rgba(255,255,255,0.4);">200-day SMA</div>
            </div>
            <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; text-align:center;">
                <div style="font-size:18px; font-weight:700; color:#fdcb6e;">{data['vix_close']:.1f}</div>
                <div style="font-size:11px; color:rgba(255,255,255,0.4);">VIX</div>
            </div>
            <div style="background:rgba(255,255,255,0.05); padding:10px; border-radius:8px; text-align:center;">
                <div style="font-size:18px; font-weight:700; color:#f39c12;">{data['gld_mom']*100:+.1f}%</div>
                <div style="font-size:11px; color:rgba(255,255,255,0.4);">GLD 60d Momentum</div>
            </div>
        </div>
        <div style="margin-top:10px; padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; text-align:center;">
            <span style="color:rgba(255,255,255,0.3); font-size:12px;">
                SPY above 200 SMA: {'✅' if data['is_above_sma200'] else '❌'} | 
                SPY above 50 EMA: {'✅' if data['is_above_ema50'] else '❌'}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ============================================
# METRICS ROW
# ============================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("S&P 500 (SPY)", f"${data['spy_close']:.2f}", 
              "Above 200 SMA" if data['is_above_sma200'] else "Below 200 SMA")

with col2:
    st.metric("NASDAQ (QQQ)", f"${data['qqq_close']:.2f}")

with col3:
    st.metric("Gold (GLD)", f"${data['gld_close']:.2f}", 
              f"{data['gld_mom']*100:+.1f}% (60d)")

with col4:
    st.metric("🎯 S6 Target", data['s6_target'])

# ============================================
# CHARTS
# ============================================

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)
st.markdown("### 📊 Market Charts")

fig = make_subplots(
    rows=3, cols=2,
    shared_xaxes=False,
    vertical_spacing=0.10,
    horizontal_spacing=0.15,
    subplot_titles=(
        "S&P 500 (SPY) with SMA200 & EMA50",
        "NASDAQ (QQQ)",
        "Gold (GLD) with 60-day Momentum",
        "VIX (Fear Index)",
        "S6 Target Exposure",
        "BIL (Cash Equivalent)"
    )
)

# 1. SPY
fig.add_trace(go.Scatter(x=data['spy_hist'].index, y=data['spy_hist'], name="SPY", line=dict(color='#00cec9', width=2.5)), row=1, col=1)
fig.add_trace(go.Scatter(x=data['spy_hist'].index, y=data['spy_hist'].rolling(200).mean(), name="200-day SMA", line=dict(color='#fd79a8', width=2, dash='dash')), row=1, col=1)
fig.add_trace(go.Scatter(x=data['spy_hist'].index, y=data['spy_hist'].ewm(span=50, adjust=False).mean(), name="50-day EMA", line=dict(color='#fdcb6e', width=2, dash='dot')), row=1, col=1)

# 2. QQQ
fig.add_trace(go.Scatter(x=data['qqq_hist'].index, y=data['qqq_hist'], name="QQQ", line=dict(color='#6c5ce7', width=2.5)), row=1, col=2)

# 3. GLD + Momentum
fig.add_trace(go.Scatter(x=data['gld_hist'].index, y=data['gld_hist'], name="GLD", line=dict(color='#f39c12', width=2.5)), row=2, col=1)
gld_mom_series = data['gld_hist'].pct_change(60) * 100
fig.add_trace(go.Scatter(x=gld_mom_series.index, y=gld_mom_series, name="GLD 60d Momentum %", line=dict(color='#e17055', width=1.5, dash='dash')), row=2, col=1)
fig.add_hline(y=0, line_dash="dot", line_color="white", opacity=0.3, row=2, col=1)

# 4. VIX
fig.add_trace(go.Scatter(x=data['vix_hist'].index, y=data['vix_hist'], name="VIX", line=dict(color='#e17055', width=2.5)), row=2, col=2)
fig.add_hline(y=30, line_dash="dash", line_color="#d63031", annotation_text="Risk Threshold (30)", row=2, col=2)
fig.add_hline(y=20, line_dash="dot", line_color="#fdcb6e", annotation_text="Calm Threshold (20)", row=2, col=2)

# 5. S6 Exposure
s6_exposure = pd.Series(1.0, index=data['spy_hist'].index)
for i in range(200, len(data['spy_hist'])):
    spy_val = data['spy_hist'].iloc[i]
    sma_val = data['spy_hist'].rolling(200).mean().iloc[i]
    vix_val = data['vix_hist'].iloc[i] if i < len(data['vix_hist']) else 20
    if pd.isna(sma_val) or pd.isna(vix_val):
        continue
    if vix_val >= 30 or spy_val < sma_val:
        s6_exposure.iloc[i] = 0.0

fig.add_trace(go.Scatter(x=s6_exposure.index, y=s6_exposure, name="S6 Target Exposure", line=dict(color='#6c5ce7', width=2), fill='tozeroy', fillcolor='rgba(108,92,231,0.2)'), row=3, col=1)
fig.add_hline(y=1.0, line_dash="dot", line_color="#2ecc71", annotation_text="100%", row=3, col=1)
fig.add_hline(y=0.0, line_dash="dot", line_color="#e74c3c", annotation_text="0% (Cash)", row=3, col=1)

# 6. BIL
fig.add_trace(go.Scatter(x=data['bil_hist'].index, y=data['bil_hist'], name="BIL (Cash)", line=dict(color='#0984e3', width=2)), row=3, col=2)

fig.update_layout(height=900, showlegend=True, template="plotly_dark", hovermode="x unified", 
                  paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(255,255,255,0.05)',
                  font=dict(color='white'), legend=dict(bgcolor='rgba(0,0,0,0.3)'))
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================
# SIDEBAR
# ============================================

with st.sidebar:
    st.markdown("### 📋 Strategy Dashboard")
    st.markdown("---")
    
    st.markdown(f"""
    <div style="text-align:center; padding:15px; background:rgba(255,255,255,0.05); border-radius:10px; border:1px solid {data['s6_color']};">
        <div style="font-size:36px;">{data['s6_emoji']}</div>
        <div style="font-size:20px; font-weight:700; color:{data['s6_color']};">{data['s6_target']}</div>
        <div style="font-size:12px; color:rgba(255,255,255,0.7);">{data['s6_reason'][:50]}...</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("#### 🔍 Current Snapshot")
    st.write(f"**SPY:** ${data['spy_close']:.2f}")
    st.write(f"**QQQ:** ${data['qqq_close']:.2f}")
    st.write(f"**GLD:** ${data['gld_close']:.2f}")
    st.write(f"**VIX:** {data['vix_close']:.1f}")
    
    st.markdown("---")
    st.markdown("#### 📋 S6 Rules")
    st.markdown("""
    | Condition | Target |
    |-----------|--------|
    | VIX >= 30 OR SPY < 200 SMA | **DEFENSIVE** |
    | -> GLD Momentum > 0 | 🪙 GLD |
    | -> GLD Momentum <= 0 | 🏦 BIL |
    | SPY > 200 SMA + VIX < 20 | 🚀 QQQ |
    | SPY > 200 SMA + 20 <= VIX < 30 | 🐂 SPY |
    """)
    
    st.markdown("---")
    st.markdown("#### 📊 Status")
    if data['is_above_sma200']:
        st.success("🟢 SPY: Above 200-day SMA")
    else:
        st.error("🔴 SPY: Below 200-day SMA")
    
    if data['vix_close'] <= 20:
        st.success(f"🟢 VIX: {data['vix_close']:.1f} (Calm)")
    elif data['vix_close'] <= 30:
        st.warning(f"🟡 VIX: {data['vix_close']:.1f} (Elevated)")
    else:
        st.error(f"🔴 VIX: {data['vix_close']:.1f} (Extreme)")
    
    st.markdown("---")
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
