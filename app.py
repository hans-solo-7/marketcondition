# ============================================
# MARKET CONDITION DASHBOARD - S6 STRATEGY
# Complete implementation with asymmetric re-entry logic
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
    page_title="S6 Market Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================
# CUSTOM CSS — CLASSIC FINANCIAL ADVISORY STYLE
# ============================================

st.markdown("""
<style>
    .stApp {
        background: #f5f5f2;
        color: #151515;
    }

    .block-container {
        max-width: 1380px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    [data-testid="stHeader"] { background: transparent; }
    [data-testid="stToolbar"] { visibility: hidden; }

    h1, h2, h3, h4, p, div, span, label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif; }

    .masthead {
        display: flex;
        justify-content: space-between;
        align-items: flex-end;
        border-bottom: 1px solid #cfcfc8;
        padding-bottom: 18px;
        margin-bottom: 24px;
    }
    .brand {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 30px;
        font-weight: 700;
        letter-spacing: -0.5px;
        color: #111;
    }
    .brand-sub {
        margin-top: 3px;
        font-size: 12px;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: #77776f;
    }
    .asof {
        text-align: right;
        font-size: 11px;
        color: #77776f;
        line-height: 1.6;
    }

    .section-kicker {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.8px;
        text-transform: uppercase;
        color: #77776f;
        margin-bottom: 7px;
    }

    .decision-card {
        background: #ffffff;
        border: 1px solid #d4d4ce;
        border-left: 5px solid #1d5b46;
        padding: 28px 32px;
        box-shadow: 0 8px 28px rgba(0,0,0,0.045);
        margin-bottom: 18px;
    }
    .decision-label {
        font-size: 11px;
        letter-spacing: 1.7px;
        text-transform: uppercase;
        color: #77776f;
    }
    .decision-target {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 44px;
        line-height: 1;
        font-weight: 700;
        color: #111;
        margin: 8px 0 10px;
    }
    .decision-title {
        font-size: 16px;
        font-weight: 600;
        color: #1d5b46;
    }
    .decision-copy {
        color: #5f5f59;
        font-size: 13px;
        margin-top: 7px;
        line-height: 1.55;
    }
    .decision-rule {
        color: #8a8a82;
        font-size: 11px;
        margin-top: 15px;
        padding-top: 12px;
        border-top: 1px solid #e3e3dd;
    }

    .panel {
        background: #fff;
        border: 1px solid #d8d8d2;
        padding: 22px 24px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.035);
        height: 100%;
    }
    .panel-title {
        font-family: Georgia, "Times New Roman", serif;
        font-size: 20px;
        font-weight: 700;
        color: #151515;
        margin-bottom: 14px;
    }
    .panel-note {
        color: #77776f;
        font-size: 11px;
        line-height: 1.55;
    }

    .regime-box {
        background: #111;
        color: #fff;
        padding: 24px;
        min-height: 205px;
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .regime-box .label { color: #bdbdb5; font-size: 10px; letter-spacing: 1.6px; text-transform: uppercase; }
    .regime-box .headline { font-family: Georgia, "Times New Roman", serif; font-size: 31px; font-weight: 700; margin: 8px 0; }
    .regime-box .detail { color: #d5d5cf; font-size: 13px; line-height: 1.5; }
    .regime-box .exposure { color: #fff; font-size: 13px; font-weight: 700; margin-top: 18px; }

    .metric-strip {
        background: #fff;
        border-top: 1px solid #d8d8d2;
        border-bottom: 1px solid #d8d8d2;
        padding: 0;
        margin: 20px 0 28px;
    }
    .metric-label { font-size: 10px; text-transform: uppercase; letter-spacing: 1.4px; color: #888880; }
    .metric-value { font-family: Georgia, "Times New Roman", serif; font-size: 25px; font-weight: 700; color: #151515; }

    .execution-highlight {
        background: #f1f5f2;
        border: 1px solid #cbd8d1;
        padding: 17px 19px;
        margin-top: 14px;
    }
    .execution-highlight .ticker { font-family: Georgia, "Times New Roman", serif; font-size: 28px; font-weight: 700; }
    .execution-highlight .price { font-size: 18px; font-weight: 700; color: #1d5b46; }
    .execution-highlight .meta { color: #707069; font-size: 11px; margin-top: 4px; }

    .order-plan {
        background: #fff;
        border: 1px solid #d1d1ca;
        padding: 22px 24px;
        margin-top: 12px;
    }
    .order-plan table { width:100%; border-collapse:collapse; color:#222; font-size:13px; }
    .order-plan th { background:#f0f0ec; padding:10px 12px; text-align:left; font-size:10px; letter-spacing:1px; text-transform:uppercase; color:#6d6d66; border-bottom:1px solid #d5d5ce; }
    .order-plan td { padding:10px 12px; border-bottom:1px solid #e6e6e1; }
    .order-plan .action-buy { color:#1d5b46; font-weight:800; }

    .source-badge {
        display:inline-block;
        padding:4px 10px;
        border:1px solid #c7c7c0;
        color:#5e5e58;
        background:#fff;
        font-size:10px;
        letter-spacing:1.1px;
        text-transform:uppercase;
    }

    .rule-card {
        background:#fff;
        border:1px solid #d8d8d2;
        padding:20px 22px;
    }
    .rule-card .rule-title { font-family:Georgia, "Times New Roman", serif; font-size:18px; font-weight:700; }
    .rule-card .rule-text { color:#64645e; font-size:12px; line-height:1.6; margin-top:6px; }

    .footer-note { color:#8a8a83; font-size:10px; border-top:1px solid #d4d4ce; padding-top:14px; margin-top:28px; }

    /* Streamlit native elements */
    [data-testid="stMetric"] { background:#fff; border:0; padding:15px 18px; }
    [data-testid="stMetricLabel"] { color:#77776f !important; font-size:10px !important; text-transform:uppercase; letter-spacing:1.2px; }
    [data-testid="stMetricValue"] { color:#151515 !important; font-family:Georgia, "Times New Roman", serif; }
    .stButton > button { border:1px solid #aaa9a2; background:#fff; color:#222; border-radius:2px; }
    .stButton > button:hover { border-color:#111; color:#111; }
    .stDataFrame { border:1px solid #d8d8d2; }
</style>
""", unsafe_allow_html=True)

# ============================================
# HEADER
# ============================================

st.markdown("""
<div class="masthead">
    <div>
        <div class="brand">S6 Investment Dashboard</div>
        <div class="brand-sub">Systematic Allocation · Decision Support</div>
    </div>
    <div class="asof">
        <span class="source-badge">Verified daily data</span><br>
        Signal engine · US market close
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# ETF CONFIGURATION
# ============================================

ETF_CONFIG = {
    'QQQ': {
        'name': 'Nasdaq-100 (Tech)',
        'ticker': 'SXRV',
        'isin': 'IE00B53SZB19',
        'ter': '0.30%',
        'exchange': 'Xetra',
        'currency': 'EUR',
        'description': 'iShares Nasdaq 100 UCITS ETF (Acc)',
        'signal': 'Calm Bull',
        'condition': 'SPY > SMA200 & VIX < 20',
        'tag': 'tag-qqq'
    },
    'SPY': {
        'name': 'S&P 500 (Core)',
        'ticker': 'SXR8',
        'isin': 'IE00B5BMR087',
        'ter': '0.07%',
        'exchange': 'Xetra',
        'currency': 'EUR',
        'description': 'iShares Core S&P 500 UCITS ETF (Acc)',
        'signal': 'Elevated Bull',
        'condition': 'SPY > SMA200 & 20 <= VIX < 30',
        'tag': 'tag-spy'
    },
    'GLD': {
        'name': 'Physical Gold',
        'ticker': 'EGLN',
        'isin': 'IE00B4ND3602',
        'ter': '0.12%',
        'exchange': 'LSE',
        'currency': 'EUR',
        'description': 'iShares Physical Gold ETC',
        'signal': 'Defensive (Gold)',
        'condition': 'GLD 60d Momentum > 0',
        'tag': 'tag-gld'
    },
    'BIL': {
        'name': 'Cash / T-Bills',
        'ticker': 'IBC1',
        'isin': 'IE00BGSF1X88',
        'ter': '0.07%',
        'exchange': 'gettex',
        'currency': 'EUR',
        'description': 'iShares $ Treasury 0-1yr UCITS ETF (Acc)',
        'signal': 'Defensive (Cash)',
        'condition': 'GLD 60d Momentum <= 0',
        'tag': 'tag-bil'
    }
}

def get_etf_config(s6_target):
    return ETF_CONFIG.get(s6_target, None)

# ============================================
# DATA FETCHING / VALIDATION
# ============================================

# IMPORTANT:
# Signal instruments are US-market proxies: SPY, QQQ, GLD and ^VIX.
# Execution instruments are their European UCITS counterparts:
# SXRV, SXR8, EGLN and IBC1.
#
# Signal data is daily and intentionally based on the latest COMPLETED
# US trading session. It is not labelled as real-time.
# Execution prices are fetched separately and are never silently replaced
# by hard-coded fallback prices.

SIGNAL_TICKERS = ["SPY", "QQQ", "GLD", "BIL", "^VIX"]
EXECUTION_TICKERS = {
    # Confirmed by the user as tradable in their IBKR account.
    "SXRV": ["SXRV.DE"],   # Xetra / EUR
    "SXR8": ["SXR8.DE"],   # Xetra / EUR
    "EGLN": ["EGLN.L"],    # LSE / EUR
    "IBC1": ["IBC1.DE"],   # gettex / EUR
}


@st.cache_data(ttl=86400)
def fetch_10y_backtest():
    """
    10-year S6 proxy backtest.

    Methodology:
    - Signal rules use unadjusted daily closes for SPY / QQQ / GLD / BIL / VIX.
    - Investment returns use adjusted closes for SPY / QQQ / GLD / BIL so
      distributions are included.
    - The signal calculated after the US close on day t is applied to the
      return on day t+1. This avoids same-day look-ahead.
    - The strategy is 100% invested in exactly one of QQQ, SPY, GLD or BIL.
    - No transaction costs, slippage, taxes, FX effects, bid/ask spread or
      differences between US signal proxies and the European execution lines
      are included.
    """
    tickers = ["SPY", "QQQ", "GLD", "BIL", "^VIX"]

    raw = yf.download(
        tickers,
        period="15y",
        interval="1d",
        auto_adjust=False,
        progress=False,
        threads=True
    )

    if raw.empty:
        raise ValueError("Yahoo Finance returned no backtest data.")

    if not isinstance(raw.columns, pd.MultiIndex):
        raise ValueError("Unexpected Yahoo Finance backtest column format.")

    if "Close" not in raw.columns.get_level_values(0):
        raise ValueError("Backtest data has no Close field.")

    if "Adj Close" not in raw.columns.get_level_values(0):
        raise ValueError("Backtest data has no Adj Close field.")

    close = raw["Close"].copy()
    adj = raw["Adj Close"].copy()

    required = ["SPY", "QQQ", "GLD", "BIL", "^VIX"]
    missing = [t for t in required if t not in close.columns]
    if missing:
        raise ValueError(f"Missing backtest tickers: {', '.join(missing)}")

    close = close[required].dropna(how="any")
    adj_assets = adj[["SPY", "QQQ", "GLD", "BIL"]].reindex(close.index)
    adj_assets = adj_assets.dropna(how="any")

    common_index = close.index.intersection(adj_assets.index)
    close = close.loc[common_index]
    adj_assets = adj_assets.loc[common_index]

    if len(close) < 10 * 252:
        raise ValueError(
            f"Insufficient history for 10-year backtest: {len(close)} sessions."
        )

    spy = close["SPY"]
    qqq = close["QQQ"]
    gld = close["GLD"]
    vix = close["^VIX"]

    sma200 = spy.rolling(200, min_periods=200).mean()
    ema50 = spy.ewm(span=50, adjust=False, min_periods=50).mean()
    gld_mom = gld.pct_change(60)

    # Same asymmetric state machine as the live strategy.
    equity_state = 1
    states = pd.Series(np.nan, index=close.index, dtype=float)
    targets = pd.Series(index=close.index, dtype="object")

    for i in range(len(close)):
        if pd.isna(sma200.iloc[i]) or pd.isna(ema50.iloc[i]) or pd.isna(gld_mom.iloc[i]):
            continue

        p = float(spy.iloc[i])
        s200 = float(sma200.iloc[i])
        e50 = float(ema50.iloc[i])
        v = float(vix.iloc[i])

        if equity_state == 1:
            if p < s200 or v >= 30:
                equity_state = 0
        else:
            if p > e50 and v < 25:
                equity_state = 1

        states.iloc[i] = float(equity_state)

        if equity_state == 0:
            targets.iloc[i] = "GLD" if gld_mom.iloc[i] > 0 else "BIL"
        else:
            targets.iloc[i] = "QQQ" if v < 20 else "SPY"

    # Keep only the requested 10-year window, while retaining warm-up
    # history before the window so the indicators are fully formed.
    end_date = close.index[-1]
    start_date = end_date - pd.DateOffset(years=10)

    bt_dates = close.index[close.index >= start_date]
    if len(bt_dates) < 2:
        raise ValueError("Unable to construct the 10-year backtest window.")

    # Signal on t -> hold selected asset during t+1.
    next_day_returns = adj_assets.pct_change().shift(-1)

    strategy_returns = pd.Series(np.nan, index=bt_dates, dtype=float)
    benchmark_returns = pd.Series(np.nan, index=bt_dates, dtype=float)

    for date in bt_dates:
        target = targets.loc[date]
        if pd.isna(target):
            continue
        strategy_returns.loc[date] = next_day_returns.loc[date, target]
        benchmark_returns.loc[date] = next_day_returns.loc[date, "SPY"]

    valid = strategy_returns.notna() & benchmark_returns.notna()
    strategy_returns = strategy_returns.loc[valid]
    benchmark_returns = benchmark_returns.loc[valid]

    if len(strategy_returns) < 9 * 252:
        raise ValueError(
            f"Backtest window contains only {len(strategy_returns)} usable sessions."
        )

    strategy_curve = (1 + strategy_returns).cumprod() * 100.0
    spy_curve = (1 + benchmark_returns).cumprod() * 100.0

    def metrics(returns, curve):
        years = len(returns) / 252.0
        total_return = float(curve.iloc[-1] / 100.0 - 1.0)
        cagr = float((curve.iloc[-1] / 100.0) ** (1.0 / years) - 1.0)
        vol = float(returns.std(ddof=1) * np.sqrt(252))
        sharpe = float(
            (returns.mean() / returns.std(ddof=1)) * np.sqrt(252)
        ) if returns.std(ddof=1) > 0 else np.nan

        drawdown = curve / curve.cummax() - 1.0
        max_dd = float(drawdown.min())

        return {
            "total_return": total_return,
            "cagr": cagr,
            "volatility": vol,
            "sharpe": sharpe,
            "max_drawdown": max_dd,
            "ending_value": float(curve.iloc[-1]),
        }

    s6_metrics = metrics(strategy_returns, strategy_curve)
    spy_metrics = metrics(benchmark_returns, spy_curve)

    # Calendar-year returns for the compact results table.
    annual = pd.DataFrame({
        "S6": strategy_returns,
        "SPY": benchmark_returns
    })
    annual.index = pd.to_datetime(annual.index)
    annual_returns = annual.groupby(annual.index.year).apply(
        lambda x: (1 + x).prod() - 1
    )

    return {
        "start_date": strategy_returns.index[0],
        "end_date": strategy_returns.index[-1],
        "strategy_returns": strategy_returns,
        "benchmark_returns": benchmark_returns,
        "strategy_curve": strategy_curve,
        "spy_curve": spy_curve,
        "s6_metrics": s6_metrics,
        "spy_metrics": spy_metrics,
        "annual_returns": annual_returns,
    }

@st.cache_data(ttl=900)
def fetch_market_data():
    try:
        raw = yf.download(
            SIGNAL_TICKERS,
            period="2y",
            interval="1d",
            auto_adjust=False,
            progress=False,
            threads=True
        )

        if raw.empty:
            raise ValueError("Yahoo Finance returned no signal data.")

        if isinstance(raw.columns, pd.MultiIndex):
            if "Close" not in raw.columns.get_level_values(0):
                raise ValueError("Signal data has no Close field.")
            closes = raw["Close"].copy()
        else:
            closes = raw.copy()

        required = ["SPY", "QQQ", "GLD", "BIL", "^VIX"]
        missing = [t for t in required if t not in closes.columns]
        if missing:
            raise ValueError(f"Missing signal tickers: {', '.join(missing)}")

        # Do NOT forward-fill market prices. Each signal is evaluated on
        # observations where all required instruments actually have data.
        closes = closes[required].dropna(how="any")

        if len(closes) < 250:
            raise ValueError(
                f"Insufficient history ({len(closes)} sessions). Need at least 250."
            )

        spy = closes["SPY"]
        qqq = closes["QQQ"]
        gld = closes["GLD"]
        bil = closes["BIL"]
        vix = closes["^VIX"]

        sma200_spy = spy.rolling(window=200, min_periods=200).mean()
        ema50_spy = spy.ewm(span=50, adjust=False, min_periods=50).mean()
        gld_mom = gld.pct_change(60)

        # Latest completed common US session.
        last_date = closes.index[-1]

        current_spy = float(spy.iloc[-1])
        current_qqq = float(qqq.iloc[-1])
        current_gld = float(gld.iloc[-1])
        current_bil = float(bil.iloc[-1])
        current_vix = float(vix.iloc[-1])
        current_sma200 = float(sma200_spy.iloc[-1])
        current_ema50 = float(ema50_spy.iloc[-1])
        current_gld_mom = float(gld_mom.iloc[-1])

        if any(pd.isna(x) for x in [
            current_sma200, current_ema50, current_gld_mom
        ]):
            raise ValueError("Required indicators are not available for latest session.")

        # ========================================
        # ASYMMETRIC RE-ENTRY STATE MACHINE
        # ========================================
        # EXIT:     SPY < 200 SMA OR VIX >= 30
        # RE-ENTER: SPY > 50 EMA AND VIX < 25
        #
        # Signals are generated from completed daily bars. The resulting
        # state is therefore actionable on the NEXT execution session.
        # ========================================

        in_equity_state = 1
        exposure_history = pd.Series(np.nan, index=closes.index, dtype=float)

        for i in range(len(closes)):
            s200 = sma200_spy.iloc[i]
            e50 = ema50_spy.iloc[i]
            v = vix.iloc[i]
            p = spy.iloc[i]

            if pd.isna(s200) or pd.isna(e50):
                continue

            if in_equity_state == 1:
                if p < s200 or v >= 30:
                    in_equity_state = 0
            else:
                if p > e50 and v < 25:
                    in_equity_state = 1

            exposure_history.iloc[i] = float(in_equity_state)

        is_above_sma200 = current_spy > current_sma200
        is_above_ema50 = current_spy > current_ema50

        # ========================================
        # S6 SIGNAL ALLOCATION LOGIC
        # ========================================
        if in_equity_state == 0:
            if current_gld_mom > 0:
                s6_target = "GLD"
                s6_reason = (
                    f"Defensive State active -> Gold 60d momentum positive "
                    f"({current_gld_mom*100:+.1f}%)"
                )
                s6_color = "#9a7b2f"
                s6_class = "signal-gld"
                s6_emoji = "🪙"
            else:
                s6_target = "BIL"
                s6_reason = (
                    f"Defensive State active -> Gold 60d momentum negative "
                    f"({current_gld_mom*100:+.1f}%)"
                )
                s6_color = "#666666"
                s6_class = "signal-bil"
                s6_emoji = "🏦"
        else:
            if current_vix < 20:
                s6_target = "QQQ"
                s6_reason = (
                    f"Calm Bull active (VIX < 20: {current_vix:.1f}) "
                    "-> 100% Tech Exposure"
                )
                s6_color = "#222222"
                s6_class = "signal-qqq"
                s6_emoji = "🚀"
            else:
                s6_target = "SPY"
                s6_reason = (
                    f"Elevated Bull active (20 <= VIX < 30: {current_vix:.1f}) "
                    "-> 100% Core Equity"
                )
                s6_color = "#1d5b46"
                s6_class = "regime-bull"
                s6_emoji = "🐂"

        # ========================================
        # ORIGINAL REGIME (for comparison)
        # ========================================
        if current_spy < current_sma200:
            target = 0
            signal_emoji = "🐻"
            signal_color = "#333333"
            signal_label = "BEAR MARKET"
            signal_desc = "S&P 500 below 200-day SMA"
            action_text = "SELL ALL - Exit all positions"
            regime_class = "regime-bear"
        elif current_vix > 30:
            target = 50
            signal_emoji = "⚠️"
            signal_color = "#9a7b2f"
            signal_label = "CAUTION"
            signal_desc = "VIX above 30 (elevated volatility)"
            action_text = "REDUCE TO 50% - Sell half"
            regime_class = "regime-neutral"
        else:
            target = 100
            signal_emoji = "🐂"
            signal_color = "#1d5b46"
            signal_label = "BULL MARKET"
            signal_desc = "All indicators normal"
            action_text = "HOLD 100% - Continue holding"
            regime_class = "regime-bull"

        # ========================================
        # EXECUTION PRICES — SEPARATE FROM SIGNAL DATA
        # ========================================
        live_prices = {}
        execution_meta = {}

        for ticker, candidates in EXECUTION_TICKERS.items():
            found = False

            for t in candidates:
                try:
                    hist = yf.Ticker(t).history(
                        period="5d",
                        interval="1d",
                        auto_adjust=False
                    )

                    if hist.empty or "Close" not in hist.columns:
                        continue

                    close_series = hist["Close"].dropna()
                    if close_series.empty:
                        continue

                    execution_price = float(close_series.iloc[-1])
                    execution_date = close_series.index[-1]

                    if not np.isfinite(execution_price) or execution_price <= 0:
                        continue

                    live_prices[ticker] = execution_price
                    execution_meta[ticker] = {
                        "symbol": t,
                        "date": execution_date,
                        "source": "Yahoo Finance",
                        "status": "latest available daily close"
                    }
                    found = True
                    break

                except Exception:
                    continue

            if not found:
                # Never use the old hard-coded prices as a fallback.
                live_prices[ticker] = None
                execution_meta[ticker] = {
                    "symbol": candidates[0],
                    "date": None,
                    "source": "Yahoo Finance",
                    "status": "UNAVAILABLE"
                }

        # Translate strategy signal names to the confirmed EUR execution
        # instruments available in the user's IBKR account.
        #
        # IMPORTANT:
        # These are EUR trading lines, NOT EUR-hedged versions.
        # The strategy still derives its signals from SPY / QQQ / GLD / VIX.
        execution_map = {
            "QQQ": "SXRV",   # Xetra / EUR
            "SPY": "SXR8",   # Xetra / EUR
            "GLD": "EGLN",   # LSE / EUR
            "BIL": "IBC1"    # gettex / EUR
        }

        execution_ticker = execution_map[s6_target]
        execution_price = live_prices.get(execution_ticker)

        return {
            # Signal market
            "spy_close": current_spy,
            "qqq_close": current_qqq,
            "gld_close": current_gld,
            "bil_close": current_bil,
            "vix_close": current_vix,
            "sma200": current_sma200,
            "ema50": current_ema50,
            "gld_mom": current_gld_mom,
            "date": last_date,

            "spy_hist": spy,
            "qqq_hist": qqq,
            "gld_hist": gld,
            "vix_hist": vix,
            "bil_hist": bil,

            # One source of truth for historical S6 state
            "s6_exposure_hist": exposure_history,

            # Current strategy state
            "s6_target": s6_target,
            "s6_reason": s6_reason,
            "s6_color": s6_color,
            "s6_class": s6_class,
            "s6_emoji": s6_emoji,
            "is_above_sma200": is_above_sma200,
            "is_above_ema50": is_above_ema50,
            "in_equity_state": in_equity_state,

            # Execution instruments
            "live_prices": live_prices,
            "execution_meta": execution_meta,
            "execution_ticker": execution_ticker,
            "execution_price": execution_price,

            # Original regime
            "target": target,
            "signal_emoji": signal_emoji,
            "signal_color": signal_color,
            "signal_label": signal_label,
            "signal_desc": signal_desc,
            "action_text": action_text,
            "regime_class": regime_class,

            "success": True,
            "data_source": "Yahoo Finance",
            "data_status": "latest completed US session for signals"
        }

    except Exception as e:
        st.error(f"Data Fetch Error: {e}")
        return None

with st.spinner("Loading market data..."):
    data = fetch_market_data()

if data is None:
    st.error("Failed to fetch data. Please try again.")
    st.stop()

with st.spinner("Building 10-year S6 backtest..."):
    try:
        backtest = fetch_10y_backtest()
    except Exception as e:
        backtest = None
        st.warning(f"10-year backtest unavailable: {e}")

# ============================================
# DATA STATUS
# ============================================

st.markdown(f"""
<div style="display:flex; justify-content:space-between; align-items:center; margin:4px 0 18px; color:#77776f; font-size:11px;">
    <div>Signal data: <strong>{data['date'].strftime('%d %b %Y')} US close</strong> · Yahoo Finance · Daily observations</div>
    <div>Execution data: latest available market price</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# S6 DECISION
# ============================================

state_display = "EQUITY" if data['in_equity_state'] == 1 else "DEFENSIVE"
etf = get_etf_config(data['s6_target'])
execution_price = data.get('execution_price')

st.markdown(f"""
<div class="decision-card">
    <div class="decision-label">S6 Current Allocation</div>
    <div class="decision-target">{data['s6_target']}</div>
    <div class="decision-title">{etf['name'] if etf else data['s6_target']} · {etf['ticker'] if etf else ''}</div>
    <div class="decision-copy">{data['s6_reason']}</div>
    <div class="decision-copy">
        Signal state: <strong>{state_display}</strong> ·
        SPY {data['spy_close']:.2f} vs 200-day SMA {data['sma200']:.2f} ·
        50-day EMA {data['ema50']:.2f} · VIX {data['vix_close']:.1f}
    </div>
    <div class="decision-rule">
        Exit: SPY &lt; 200 SMA or VIX ≥ 30 &nbsp; | &nbsp;
        Re-enter: SPY &gt; 50 EMA and VIX &lt; 25
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================
# DECISION CONTEXT
# ============================================

col1, col2 = st.columns([0.82, 1.18], gap="large")

with col1:
    st.markdown('<div class="section-kicker">Market Regime</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="regime-box">
        <div class="label">Reference regime</div>
        <div class="headline">{data['signal_label']}</div>
        <div class="detail">{data['signal_desc']}</div>
        <div class="exposure">Reference exposure: {data['target']}%</div>
        <div class="detail" style="margin-top:6px;">{data['action_text']}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown('<div class="section-kicker">Signal Diagnostics</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="panel">
        <div class="panel-title">Why the model is here</div>
        <div class="metric-strip" style="border-top:0; margin:0;">
            <div style="display:grid; grid-template-columns:1fr 1fr;">
                <div style="padding:14px 10px; border-right:1px solid #e0e0da; border-bottom:1px solid #e0e0da;">
                    <div class="metric-label">SPY close</div><div class="metric-value">${data['spy_close']:.2f}</div>
                </div>
                <div style="padding:14px 10px; border-bottom:1px solid #e0e0da;">
                    <div class="metric-label">200-day SMA</div><div class="metric-value">${data['sma200']:.2f}</div>
                </div>
                <div style="padding:14px 10px; border-right:1px solid #e0e0da;">
                    <div class="metric-label">50-day EMA</div><div class="metric-value">${data['ema50']:.2f}</div>
                </div>
                <div style="padding:14px 10px;">
                    <div class="metric-label">VIX</div><div class="metric-value">{data['vix_close']:.1f}</div>
                </div>
            </div>
        </div>
        <div class="execution-highlight">
            <div class="metric-label">European execution instrument</div>
            <div class="ticker">{etf['ticker'] if etf else '—'}</div>
            <div class="price">{('€' + format(execution_price, '.2f')) if execution_price is not None else 'PRICE UNAVAILABLE'}</div>
            <div class="meta">{etf['description'] if etf else ''} · {etf['exchange'] if etf else ''} · {etf['currency'] if etf else ''}</div>
            <div class="meta">Latest available market price · Yahoo Finance</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================
# EXECUTION INSTRUMENT STATUS
# ============================================

st.markdown('<div class="section-kicker" style="margin-top:28px;">Execution Universe</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-title" style="margin-bottom:4px;">EUR UCITS trading lines</div>', unsafe_allow_html=True)
st.caption("Signal instruments are US proxies. Trades are executed in the corresponding European instruments.")

exec_rows = []
for strategy_key, execution_key in {"QQQ": "SXRV", "SPY": "SXR8", "GLD": "EGLN", "BIL": "IBC1"}.items():
    p = data["live_prices"].get(execution_key)
    meta = data["execution_meta"].get(execution_key, {})
    exec_rows.append({
        "Signal": strategy_key,
        "Execution ETF": execution_key,
        "Latest Price": f"€{p:.2f}" if p is not None else "UNAVAILABLE",
        "Data Status": meta.get("status", "UNAVAILABLE"),
        "Yahoo Symbol": meta.get("symbol", execution_key),
    })

st.dataframe(pd.DataFrame(exec_rows), hide_index=True, use_container_width=True)

# ============================================
# MARKET SNAPSHOT
# ============================================

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("SPY", f"${data['spy_close']:.2f}", "Above 200 SMA" if data['is_above_sma200'] else "Below 200 SMA")
with col2:
    st.metric("QQQ", f"${data['qqq_close']:.2f}")
with col3:
    st.metric("GLD", f"${data['gld_close']:.2f}", f"{data['gld_mom']*100:+.1f}% / 60d")
with col4:
    st.metric("VIX", f"{data['vix_close']:.1f}", "Calm" if data['vix_close'] < 20 else ("Elevated" if data['vix_close'] < 30 else "Extreme"))

# ============================================
# PORTFOLIO & ORDER PLAN
# ============================================

st.markdown('<div class="section-kicker" style="margin-top:30px;">Execution Planning</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-title">Order sizing</div>', unsafe_allow_html=True)

col1, col2 = st.columns([0.7, 1.3], gap="large")
with col1:
    portfolio_size = st.number_input(
        "Portfolio Size (EUR)", min_value=1000, max_value=1000000,
        value=25000, step=1000, help="Enter total portfolio value in EUR"
    )
with col2:
    st.markdown(f"""
    <div class="panel" style="padding:17px 20px;">
        <div class="metric-label">Current S6 target</div>
        <div class="metric-value">100% → {data['s6_target']}</div>
        <div class="panel-note">{data['s6_reason']}</div>
    </div>
    """, unsafe_allow_html=True)

target_etf = get_etf_config(data['s6_target'])

if target_etf:
    ticker = target_etf['ticker']
    name = target_etf['name']
    price = data.get('execution_price')

    if price is None:
        st.error(
            f"🔴 Execution price unavailable for {ticker}. "
            "No order calculation is generated."
        )
    else:
        shares = portfolio_size / price
        total_cost = shares * price

        st.markdown(f"""
        <div class="order-plan">
            <h4 style="color:#151515; margin-top:0; font-family:Georgia, 'Times New Roman', serif;">Execution Plan</h4>
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
                        <td><span class="action-buy">BUY</span></td>
                        <td>{name}</td>
                        <td><strong>{ticker}</strong></td>
                        <td>€{price:.2f}</td>
                        <td>{shares:.2f}</td>
                        <td>€{total_cost:,.2f}</td>
                        <td>100.0%</td>
                    </tr>
                </tbody>
            </table>
            <div style="margin-top:15px; padding:10px; background:#f5f5f2; border-radius:2px; display:flex; justify-content:space-between; flex-wrap:wrap;">
                <span style="color:#6d6d66; font-size:12px;">
                    ISIN: {target_etf['isin']} | Exchange: {target_etf['exchange']}
                </span>
                <span style="color:#6d6d66; font-size:12px;">
                    TER: {target_etf['ter']} | Currency: {target_etf['currency']}
                </span>
                <span style="color:#6d6d66; font-size:12px;">
                    Portfolio: €{portfolio_size:,.2f} → Target: €{total_cost:,.2f}
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.info(
            f"📈 **BUY Order:** Place a **limit order** for {shares:.2f} shares "
            f"of {ticker} at or near €{price:.2f}. Total cost: €{total_cost:,.2f}. "
            f"Price source: Yahoo Finance · latest available market price (not a live bid/ask quote)."
        )
else:
    st.warning("⚠️ No order book plan generated. Please check your configuration.")

st.markdown('<div class="glow-divider"></div>', unsafe_allow_html=True)

# ============================================
# STRATEGY REFERENCE
# ============================================

st.markdown('<div class="section-kicker" style="margin-top:32px;">Strategy Reference</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-title">Signal → execution map</div>', unsafe_allow_html=True)

matrix_data = []
for target, config in ETF_CONFIG.items():
    if target == 'QQQ':
        condition = 'Equity state + VIX < 20'
    elif target == 'SPY':
        condition = 'Equity state + 20 ≤ VIX < 30'
    elif target == 'GLD':
        condition = 'Defensive state + GLD 60d momentum > 0'
    else:
        condition = 'Defensive state + GLD 60d momentum ≤ 0'
    is_current = target == data['s6_target']
    p = data['live_prices'].get(config['ticker'])
    matrix_data.append({
        'Signal': target,
        'Execution ETF': config['ticker'],
        'Latest Price': f"${p:.2f}" if p is not None else "UNAVAILABLE",
        'TER': config['ter'],
        'Model Role': condition,
        'Current': 'YES' if is_current else ''
    })

st.dataframe(
    pd.DataFrame(matrix_data), hide_index=True, use_container_width=True,
    column_config={
        "Signal": st.column_config.TextColumn("Signal", width="small"),
        "Execution ETF": st.column_config.TextColumn("Execution ETF", width="small"),
        "Latest Price": st.column_config.TextColumn("Latest Price", width="small"),
        "TER": st.column_config.TextColumn("TER", width="small"),
        "Model Role": st.column_config.TextColumn("Model Role", width="large"),
        "Current": st.column_config.TextColumn("Current", width="small"),
    }
)

col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("""
    <div class="rule-card">
        <div class="rule-title">Asymmetric re-entry</div>
        <div class="rule-text"><strong>Exit:</strong> SPY below 200-day SMA OR VIX ≥ 30.</div>
        <div class="rule-text"><strong>Re-enter:</strong> SPY above 50-day EMA AND VIX &lt; 25.</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="rule-card">
        <div class="rule-title">Execution discipline</div>
        <div class="rule-text"><strong>Signal:</strong> calculated after the completed US session.</div>
        <div class="rule-text"><strong>Trade:</strong> use the European UCITS counterpart during the chosen execution window.</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-kicker" style="margin-top:30px;">Execution Window</div>', unsafe_allow_html=True)
st.markdown("""
<div class="rule-card">
    <div class="rule-title">IBKR execution guidance</div>
    <div class="rule-text">15:30–17:30 CEST in summer / 14:30–16:30 CET in winter (09:30–11:30 ET). This captures the New York open and the liquid London/New York overlap. Actual bid/ask spreads and liquidity should be checked before placing an order.</div>
</div>
""", unsafe_allow_html=True)

# ============================================
# CHARTS
# ============================================

st.markdown('<div class="section-kicker" style="margin-top:34px;">Historical Context</div>', unsafe_allow_html=True)
st.markdown('<div class="panel-title">Market regime and signal history</div>', unsafe_allow_html=True)

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
fig.add_trace(go.Scatter(x=data['spy_hist'].index, y=data['spy_hist'], name="SPY", line=dict(color='#1d5b46', width=2.5)), row=1, col=1)
fig.add_trace(go.Scatter(x=data['spy_hist'].index, y=data['spy_hist'].rolling(200).mean(), name="200-day SMA", line=dict(color='#77776f', width=2, dash='dash')), row=1, col=1)
fig.add_trace(go.Scatter(x=data['spy_hist'].index, y=data['spy_hist'].ewm(span=50, adjust=False).mean(), name="50-day EMA", line=dict(color='#9a7b2f', width=2, dash='dot')), row=1, col=1)

# 2. QQQ
fig.add_trace(go.Scatter(x=data['qqq_hist'].index, y=data['qqq_hist'], name="QQQ", line=dict(color='#222222', width=2.5)), row=1, col=2)

# 3. GLD + Momentum
fig.add_trace(go.Scatter(x=data['gld_hist'].index, y=data['gld_hist'], name="GLD", line=dict(color='#9a7b2f', width=2.5)), row=2, col=1)
gld_mom_series = data['gld_hist'].pct_change(60) * 100
fig.add_trace(go.Scatter(x=gld_mom_series.index, y=gld_mom_series, name="GLD 60d Momentum %", line=dict(color='#555555', width=1.5, dash='dash')), row=2, col=1)
fig.add_hline(y=0, line_dash="dot", line_color="white", opacity=0.3, row=2, col=1)

# 4. VIX
fig.add_trace(go.Scatter(x=data['vix_hist'].index, y=data['vix_hist'], name="VIX", line=dict(color='#555555', width=2.5)), row=2, col=2)
fig.add_hline(y=30, line_dash="dash", line_color="#333333", annotation_text="Risk Threshold (30)", row=2, col=2)
fig.add_hline(y=20, line_dash="dot", line_color="#9a7b2f", annotation_text="Calm Threshold (20)", row=2, col=2)

# 5. S6 Exposure — exact same state machine used by the live signal
s6_exposure = data['s6_exposure_hist']

fig.add_trace(
    go.Scatter(
        x=s6_exposure.index,
        y=s6_exposure,
        name="S6 Equity State",
        line=dict(color='#222222', width=2),
        fill='tozeroy',
        fillcolor='rgba(108,92,231,0.2)',
        connectgaps=False
    ),
    row=3, col=1
)
fig.add_hline(
    y=1.0, line_dash="dot", line_color="#1d5b46",
    annotation_text="Equity", row=3, col=1
)
fig.add_hline(
    y=0.0, line_dash="dot", line_color="#333333",
    annotation_text="Defensive", row=3, col=1
)

# 6. BIL
fig.add_trace(go.Scatter(x=data['bil_hist'].index, y=data['bil_hist'], name="BIL (Cash)", line=dict(color='#666666', width=2)), row=3, col=2)

fig.update_layout(
    height=900,
    showlegend=True,
    template="plotly_white",
    hovermode="x unified",
    paper_bgcolor='#f5f5f2',
    plot_bgcolor='#ffffff',
    font=dict(color='#222222'),
    legend=dict(bgcolor='#ffffff', bordercolor='#d8d8d2', borderwidth=1)
)

fig.update_xaxes(showgrid=True, gridcolor='#e7e7e1')
fig.update_yaxes(showgrid=True, gridcolor='#e7e7e1')

st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# ============================================
# STRATEGY METHOD & 10-YEAR BACKTEST
# ============================================

st.markdown(
    '<div class="section-kicker" style="margin-top:38px;">Strategy Method & Evidence</div>',
    unsafe_allow_html=True
)
st.markdown(
    '<div class="panel-title">How S6 works — and how it has behaved historically</div>',
    unsafe_allow_html=True
)

method_col, results_col = st.columns([1.0, 1.25], gap="large")

with method_col:
    st.markdown("""
    <div class="rule-card" style="height:100%;">
        <div class="rule-title">The S6 decision sequence</div>

        <div class="rule-text"><strong>1 · Determine the regime.</strong>
        The model remains in EQUITY state until either SPY falls below its
        200-day SMA or VIX reaches 30.</div>

        <div class="rule-text"><strong>2 · Re-entry is deliberately harder.</strong>
        Once defensive, the model returns to EQUITY only when SPY is above its
        50-day EMA and VIX is below 25.</div>

        <div class="rule-text"><strong>3 · Choose the exposure.</strong>
        In EQUITY state, VIX &lt; 20 selects QQQ; 20 ≤ VIX &lt; 30 selects SPY.
        In DEFENSIVE state, positive 60-day GLD momentum selects GLD;
        otherwise BIL.</div>

        <div class="rule-text"><strong>4 · Execute in EUR.</strong>
        The signal is calculated from US-market proxies. The corresponding
        trade is placed in the confirmed EUR IBKR trading line:
        QQQ → SXRV · SPY → SXR8 · GLD → EGLN · BIL → IBC1.</div>

        <div class="rule-text"><strong>5 · Timing.</strong>
        A completed US-session signal is actionable on the following execution
        session. The model does not use the next day's information to create
        the signal.</div>
    </div>
    """, unsafe_allow_html=True)

if backtest is not None:
    s6m = backtest["s6_metrics"]
    spym = backtest["spy_metrics"]

    with results_col:
        st.markdown("""
        <div class="rule-card">
            <div class="rule-title">10-year proxy backtest vs SPY</div>
            <div class="rule-text">
                Signal rules use SPY / QQQ / GLD / VIX. Performance uses adjusted
                total-return prices for SPY / QQQ / GLD / BIL. The signal on day t
                is applied to day t+1.
            </div>
        </div>
        """, unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        with m1:
            st.metric("S6 CAGR", f"{s6m['cagr']*100:.1f}%")
        with m2:
            st.metric("SPY CAGR", f"{spym['cagr']*100:.1f}%")
        with m3:
            st.metric("S6 Max DD", f"{s6m['max_drawdown']*100:.1f}%")
        with m4:
            st.metric("SPY Max DD", f"{spym['max_drawdown']*100:.1f}%")

        m5, m6, m7, m8 = st.columns(4)
        with m5:
            st.metric("S6 Volatility", f"{s6m['volatility']*100:.1f}%")
        with m6:
            st.metric("SPY Volatility", f"{spym['volatility']*100:.1f}%")
        with m7:
            st.metric("S6 Sharpe", f"{s6m['sharpe']:.2f}")
        with m8:
            st.metric("SPY Sharpe", f"{spym['sharpe']:.2f}")

    # Growth of $100 — normalized comparison.
    bt_fig = go.Figure()
    bt_fig.add_trace(go.Scatter(
        x=backtest["strategy_curve"].index,
        y=backtest["strategy_curve"],
        name="S6",
        line=dict(color="#1d5b46", width=2.5)
    ))
    bt_fig.add_trace(go.Scatter(
        x=backtest["spy_curve"].index,
        y=backtest["spy_curve"],
        name="SPY",
        line=dict(color="#77776f", width=2),
        dash="dash"
    ))
    bt_fig.update_layout(
        height=430,
        template="plotly_white",
        title=f"Growth of $100 · {backtest['start_date'].strftime('%d %b %Y')} – {backtest['end_date'].strftime('%d %b %Y')}",
        yaxis_title="Portfolio value ($)",
        xaxis_title="",
        hovermode="x unified",
        paper_bgcolor="#f5f5f2",
        plot_bgcolor="#ffffff",
        font=dict(color="#222222"),
        legend=dict(bgcolor="#ffffff", bordercolor="#d8d8d2", borderwidth=1)
    )
    bt_fig.update_xaxes(showgrid=True, gridcolor="#e7e7e1")
    bt_fig.update_yaxes(showgrid=True, gridcolor="#e7e7e1")
    st.plotly_chart(bt_fig, use_container_width=True, config={"displayModeBar": False})

    annual_display = backtest["annual_returns"].copy()
    annual_display.index.name = "Year"
    annual_display = annual_display.rename(columns={"S6": "S6", "SPY": "SPY"})
    annual_display = annual_display.sort_index(ascending=False)
    for col in annual_display.columns:
        annual_display[col] = annual_display[col].map(lambda x: f"{x*100:.1f}%")

    st.dataframe(
        annual_display,
        use_container_width=True,
        hide_index=False
    )

    st.caption(
        "Backtest period is the latest rolling 10 years available in Yahoo Finance. "
        "Returns include distributions through adjusted prices. No fees, slippage, "
        "taxes, FX conversion costs, bid/ask spreads or execution-price differences "
        "between the US signal proxies and the EUR trading lines are modeled. "
        "Historical results are not a guarantee of future performance."
    )
else:
    st.info(
        "The 10-year backtest could not be calculated from the current market-data feed. "
        "The live S6 signal remains available."
    )

# ============================================
# SIDEBAR — COMPACT CONTROLS
# ============================================

with st.sidebar:
    st.markdown("### S6")
    st.caption("Systematic allocation dashboard")
    st.markdown("---")
    st.markdown(f"""
    **Current target**

    ## {data['s6_target']}
    """)
    st.caption(data['s6_reason'])
    st.markdown("---")
    st.markdown("**Signal snapshot**")
    st.write(f"SPY  ${data['spy_close']:.2f}")
    st.write(f"200 SMA  ${data['sma200']:.2f}")
    st.write(f"50 EMA  ${data['ema50']:.2f}")
    st.write(f"VIX  {data['vix_close']:.1f}")
    st.markdown("---")
    st.markdown("**S6 rules**")
    st.caption("Equity: VIX < 20 → QQQ; 20–30 → SPY")
    st.caption("Defensive: GLD momentum > 0 → GLD; otherwise BIL")
    st.caption("Exit: SPY < 200 SMA OR VIX ≥ 30")
    st.caption("Re-enter: SPY > 50 EMA AND VIX < 25")
    st.markdown("---")
    if st.button("Refresh market data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()

st.markdown(f"""
<div class="footer-note">
    S6 is a rules-based decision-support system. Signal data uses US-market proxy instruments; execution uses European UCITS counterparts. Signal values represent the latest completed US session. Execution prices are the latest available market observations from Yahoo Finance and are not live bid/ask quotes.
</div>
""", unsafe_allow_html=True)

