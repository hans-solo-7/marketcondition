# ============================================
# MARKET CONDITION DASHBOARD - WITH ORDER BOOK PLAN
# Includes portfolio size input and execution plan
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
    
    .order-plan {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        border: 1px solid rgba(255,255,255,0.08);
        margin-top: 15px;
    }
    
    .order-plan table {
        width: 100%;
        border-collapse: collapse;
        color: rgba(255,255,255,0.9);
        font-size: 13px;
    }
    
    .order-plan th {
        background: rgba(255,255,255,0.1);
        padding: 10px 12px;
        text-align: left;
        font-weight: 600;
        color: rgba(255,255,255,0.7);
        border-bottom: 2px solid rgba(255,255,255,0.1);
    }
    
    .order-plan td {
        padding: 8px 12px;
        border-bottom: 1px solid rgba(255,255,255,0.05);
    }
    
    .order-plan .action-buy {
        color: #2ecc71;
        font-weight: 600;
    }
    
    .order-plan .action-sell {
        color: #e74c3c;
        font-weight: 600;
    }
    
    .order-plan .action-hold {
        color: #fdcb6e;
        font-weight: 600;
    }
    
    .signal-tag {
        display: inline-block;
        padding: 2px 10px;
        border-radius: 12px;
        font-size: 11px;
        font-weight: 600;
    }
    
    .tag-qqq { background: rgba(108,92,231,0.3); color: #a29bfe; }
    .tag-spy { background: rgba(0,206,201,0.3); color: #00cec9; }
    .tag-gld { background: rgba(243,156,18,0.3); color: #fdcb6e; }
    .tag-bil { background: rgba(9,132,227,0.3); color: #74b9ff; }
    
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
# ETF CONFIGURATION
# ============================================

ETF_CONFIG = {
    'QQQ': {
        'name': 'Nasdaq-100 (Tech)',
        'ticker': 'CNDX',
        'isin': 'IE00B53SZB19',
        'ter': '0.30%',
        'price': 1688.00,
        'exchange': 'LSE',
        'currency': 'USD',
        'description': 'iShares Nasdaq 100 UCITS ETF (Acc)',
        'signal': 'Calm Bull',
        'condition': 'SPY > SMA200 & VIX < 20',
        'tag': 'tag-qqq'
    },
    'SPY': {
        'name': 'S&P 500 (Core)',
        'ticker': 'CSPX',
        'isin': 'IE00B5BMR087',
        'ter': '0.07%',
        'price': 830.56,
        'exchange': 'LSE',
        'currency': 'USD',
        'description': 'iShares Core S&P 500 UCITS ETF (Acc)',
        'signal': 'Elevated Bull',
        'condition': 'SPY > SMA200 & 20 <= VIX < 30',
        'tag': 'tag-spy'
    },
    'GLD': {
        'name': 'Physical Gold',
        'ticker': 'IGLN',
        'isin': 'IE00B4ND3602',
        'ter': '0.12%',
        'price': 86.97,
        'exchange': 'LSE',
        'currency': 'USD',
        'description': 'iShares Physical Gold ETC',
        'signal': 'Defensive (Gold)',
        'condition': 'GLD 60d Momentum > 0',
        'tag': 'tag-gld'
    },
    'BIL': {
        'name': 'Cash / T-Bills',
        'ticker': 'IB01',
        'isin': 'IE00BGSF1X88',
        'ter': '0.07%',
        'price': 121.60,
        'exchange': 'LSE',
        'currency': 'USD',
        'description': 'iShares $ Treasury 0-1yr UCITS ETF (Acc)',
        'signal': 'Defensive (Cash)',
        'condition': 'GLD 60d Momentum <= 0',
        'tag': 'tag-bil'
    }
}

def get_etf_config(s6_target):
    return ETF_CONFIG.get(s6_target, None)

# ============================================
# ORDER BOOK PLAN GENERATOR
# ============================================

def generate_order_plan(target_etf, portfolio_size, current_holdings=None):
    """
    Generate order book plan based on target ETF and portfolio size.
    
    Parameters:
    - target_etf: The ETF config dict
    - portfolio_size: Total portfolio value in USD
    - current_holdings: Dict of current holdings (ticker -> shares)
    
    Returns:
    - Dict with order plan details
    """
    if target_etf is None:
        return None
    
    # Default: assume we're starting from zero (no current holdings)
    if current_holdings is None:
        current_holdings = {}
    
    # Get target ETF details
    ticker = target_etf['ticker']
    price = target_etf['price']
    name = target_etf['name']
    currency = target_etf['currency']
    ter = target_etf['ter']
    isin = target_etf['isin']
    exchange = target_etf['exchange']
    
    # Calculate target shares (use 100% of portfolio)
    target_shares = portfolio_size / price
    
    # Get current shares (if any)
    current_shares = current_holdings.get(ticker, 0)
    
    # Calculate difference
    diff_shares = target_shares - current_shares
    
    # Determine action
    if diff_shares > 0.01:
        action = "BUY"
        action_class = "action-buy"
        shares_to_trade = diff_shares
        estimated_cost = shares_to_trade * price
    elif diff_shares < -0.01:
        action = "SELL"
        action_class = "action-sell"
        shares_to_trade = abs(diff_shares)
        estimated_cost = shares_to_trade * price
    else:
        action = "HOLD"
        action_class = "action-hold"
        shares_to_trade = 0
        estimated_cost = 0
    
    return {
        'ticker': ticker,
        'name': name,
        'price': price,
        'currency': currency,
        'ter': ter,
        'isin': isin,
        'exchange': exchange,
        'current_shares': current_shares,
        'target_shares': target_shares,
        'shares_to_trade': shares_to_trade,
        'action': action,
        'action_class': action_class,
        'estimated_cost': estimated_cost,
        'portfolio_size': portfolio_size,
        'target_allocation': portfolio_size
    }

def generate_full_order_book(s6_target, portfolio_size, current_holdings=None):
    """
    Generate full order book plan for all ETFs based on S6 target.
    Only the target ETF gets the full allocation, others get 0.
    """
    order_book = []
    
    # Get the target ETF config
    target_etf = get_etf_config(s6_target)
    
    if target_etf is None:
        return []
    
    # Generate plan for the target ETF (100% allocation)
    plan = generate_order_plan(target_etf, portfolio_size, current_holdings)
    if plan:
        order_book.append(plan)
    
    return order_book

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
                s6_reason = "Elevated Bull (SPY > 200 SMA, 20 <= VIX < 30) -> Broad Equity"
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
    etf = get_etf_config(data['s6_target'])
    
    if etf:
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
            <div style="margin-top:10px; padding:10px; background:rgba(108,92,231,0.1); border-radius:8px; text-align:center; border:1px solid {data['s6_color']};">
                <div style="font-size:12px; color:rgba(255,255,255,0.4);">ETF to Execute</div>
                <div style="font-size:22px; font-weight:700; color:{data['s6_color']};">{etf['ticker']}</div>
                <div style="font-size:12px; color:rgba(255,255,255,0.6);">{etf['name']}</div>
                <div style="font-size:10px; color:rgba(255,255,255,0.3);">{etf['exchange']} | {etf['currency']} | TER: {etf['ter']}</div>
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

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ============================================
# PORTFOLIO SIZE & ORDER BOOK PLAN
# ============================================

st.markdown("""
<div class="strategy-description">
    <h3 style="color:white; margin-top:0;">📋 Order Book Plan</h3>
    <p style="color:rgba(255,255,255,0.7); font-size:14px;">
        Enter your portfolio size below to generate today's execution plan.
    </p>
</div>
""", unsafe_allow_html=True)

# Portfolio size input
col1, col2 = st.columns([1, 2])

with col1:
    portfolio_size = st.number_input(
        "💰 Portfolio Size (USD)",
        min_value=1000,
        max_value=1000000,
        value=25000,
        step=1000,
        help="Enter your total portfolio value in USD"
    )

with col2:
    st.markdown(f"""
    <div style="background:rgba(255,255,255,0.05); border-radius:10px; padding:15px; margin-top:25px;">
        <div style="color:rgba(255,255,255,0.5); font-size:12px; text-transform:uppercase; letter-spacing:1px;">Target Allocation</div>
        <div style="font-size:24px; font-weight:700; color:{data['s6_color']};">100% → {data['s6_target']}</div>
        <div style="font-size:12px; color:rgba(255,255,255,0.4);">{data['s6_reason'][:60]}...</div>
    </div>
    """, unsafe_allow_html=True)

# Generate order book plan
order_book = generate_full_order_book(data['s6_target'], portfolio_size)

if order_book and len(order_book) > 0:
    plan = order_book[0]
    
    st.markdown(f"""
    <div class="order-plan">
        <h4 style="color:white; margin-top:0;">📊 Execution Plan</h4>
        <table>
            <thead>
                <tr>
                    <th>Action</th>
                    <th>ETF</th>
                    <th>Ticker</th>
                    <th>Price</th>
                    <th>Shares</th>
                    <th>Total Cost</th>
                    <th>Allocation</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td><span class="{plan['action_class']}">{plan['action']}</span></td>
                    <td>{plan['name']}</td>
                    <td><strong>{plan['ticker']}</strong></td>
                    <td>${plan['price']:.2f}</td>
                    <td>{plan['shares_to_trade']:.2f}</td>
                    <td>${plan['estimated_cost']:,.2f}</td>
                    <td>{plan['target_allocation']/portfolio_size*100:.1f}%</td>
                </tr>
            </tbody>
        </table>
        <div style="margin-top:15px; padding:10px; background:rgba(255,255,255,0.03); border-radius:8px; display:flex; justify-content:space-between; flex-wrap:wrap;">
            <span style="color:rgba(255,255,255,0.5); font-size:12px;">
                ISIN: {plan['isin']} | Exchange: {plan['exchange']}
            </span>
            <span style="color:rgba(255,255,255,0.5); font-size:12px;">
                TER: {plan['ter']} | Currency: {plan['currency']}
            </span>
            <span style="color:rgba(255,255,255,0.5); font-size:12px;">
                Portfolio: ${portfolio_size:,.2f} → Target: ${plan['target_allocation']:,.2f}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Execution instructions
    if plan['action'] == "BUY":
        st.info(f"📈 **BUY Order:** Place a **limit order** for {plan['shares_to_trade']:.2f} shares of {plan['ticker']} at or near ${plan['price']:.2f}. Total cost: ${plan['estimated_cost']:,.2f}.")
    elif plan['action'] == "SELL":
        st.warning(f"📉 **SELL Order:** Place a **limit order** to sell {plan['shares_to_trade']:.2f} shares of {plan['ticker']} at or near ${plan['price']:.2f}. Total proceeds: ${plan['estimated_cost']:,.2f}.")
    else:
        st.success(f"✅ **HOLD:** No action needed. Current position matches target allocation for {plan['ticker']}.")

else:
    st.warning("⚠️ No order book plan generated. Please check your configuration.")

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ============================================
# EXECUTION MATRIX TABLE
# ============================================

st.markdown("""
<div class="strategy-description">
    <h3 style="color:white; margin-top:0;">📋 Cleaned Execution Matrix</h3>
    <p style="color:rgba(255,255,255,0.7); font-size:14px;">
        <strong>Key Operational Observations:</strong>
    </p>
    <ul style="color:rgba(255,255,255,0.7); font-size:13px;">
        <li><strong>Acc (Accumulating) Advantage:</strong> All four selections automatically reinvest dividends/yields. In Germany, this streamlines tax reporting under the <em>Vorabpauschale</em> rules and eliminates manual cash reinvestment overhead.</li>
        <li><strong>TER / Cost Efficiency:</strong> An average Total Expense Ratio under 0.15% matches institutional pricing with near-zero drag.</li>
        <li><strong>LSE USD Liquidity:</strong> The LSE listings trade in USD directly during European market hours.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# Create DataFrame for the execution matrix
matrix_data = []
for target, config in ETF_CONFIG.items():
    if target == 'QQQ':
        condition = 'Calm Bull (SPY > SMA200 & VIX < 20)'
    elif target == 'SPY':
        condition = 'Elevated Bull (SPY > SMA200 & 20 <= VIX < 30)'
    elif target == 'GLD':
        condition = 'Defensive Regime (GLD 60d Mom > 0)'
    else:
        condition = 'Defensive Regime (GLD 60d Mom <= 0)'
    
    is_current = target == data['s6_target']
    
    matrix_data.append({
        'Signal': target,
        'Asset': config['name'],
        'ETF Name': config['description'],
        'Ticker': config['ticker'],
        'Curr': config['currency'],
        'TER': config['ter'],
        'Role': condition,
        '✅': '✅ Current' if is_current else ''
    })

df_matrix = pd.DataFrame(matrix_data)

st.dataframe(
    df_matrix,
    column_config={
        "Signal": st.column_config.TextColumn("Strategy Signal", width="small"),
        "Asset": st.column_config.TextColumn("Target Asset", width="medium"),
        "ETF Name": st.column_config.TextColumn("European UCITS ETF", width="large"),
        "Ticker": st.column_config.TextColumn("Ticker", width="small"),
        "Curr": st.column_config.TextColumn("Currency", width="small"),
        "TER": st.column_config.TextColumn("TER", width="small"),
        "Role": st.column_config.TextColumn("Role in Strategy 6", width="large"),
        "✅": st.column_config.TextColumn("", width="small"),
    },
    hide_index=True,
    use_container_width=True
)

# ============================================
# EXECUTION RULES
# ============================================

st.markdown("""
<div class="strategy-description" style="margin-top:15px;">
    <h4 style="color:#6c5ce7; margin-top:0;">⏰ Execution Rule on IBKR</h4>
    <div style="background:rgba(108,92,231,0.1); border-left:3px solid #6c5ce7; padding:15px; margin:10px 0; border-radius:5px;">
        <p style="color:rgba(255,255,255,0.9); margin:0;">
            <strong>Execution Window:</strong> Place your trades between <strong>15:30 and 17:30 CET</strong> 
            (09:30 to 11:30 EST). This window covers the simultaneous open of the London Stock Exchange and the 
            New York market, ensuring maximum market-maker liquidity and penny-wide spreads on all four tickers.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ============================================
# CHARTS
# ============================================

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
    if i < len(data['vix_hist']):
        spy_val = data['spy_hist'].iloc[i]
        sma_val = data['spy_hist'].rolling(200).mean().iloc[i]
        vix_val = data['vix_hist'].iloc[i]
        
        if pd.isna(sma_val) or pd.isna(vix_val):
            continue
        
        if vix_val >= 30 or spy_val < sma_val:
            s6_exposure.iloc[i] = 0.0
        else:
            s6_exposure.iloc[i] = 1.0

fig.add_trace(go.Scatter(x=s6_exposure.index, y=s6_exposure, name="S6 Target Exposure", line=dict(color='#6c5ce7', width=2), fill='tozeroy', fillcolor='rgba(108,92,231,0.2)'), row=3, col=1)
fig.add_hline(y=1.0, line_dash="dot", line_color="#2ecc71", annotation_text="100%", row=3, col=1)
fig.add_hline(y=0.0, line_dash="dot", line_color="#e74c3c", annotation_text="0% (Cash)", row=3, col=1)

# 6. BIL
fig.add_trace(go.Scatter(x=data['bil_hist'].index, y=data['bil_hist'], name="BIL (Cash)", line=dict(color='#0984e3', width=2)), row=3, col=2)

fig.update_layout(
    height=900,
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
