# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - INSTITUTIONAL TRIPLE-BARRIER & ADVANCED FEATURE ENGINE (AFML CH. 3-4)
=====================================================================================
Marcos López de Prado Quantitative Architecture | Absolute Institutional Ground Truth
Founder: HEM SINATH

Features:
  1. Triple-Barrier Method:
     - Upper Barrier: Profit Target (+2.0R to +4.0R) -> +1
     - Lower Barrier: Volatility Breathing Stop (-1.0R) -> -1
     - Vertical Barrier: Time Expiration (max_bars = 45) -> Mark-to-market R
  2. Sample Uniqueness & Concurrency Weighting:
     - Calculates concurrent trade overlap c_t.
     - Computes average uniqueness u_bar_i.
     - Calculates sample weights w_i = u_bar_i * |r_i|.
  3. Microstructure & Order Flow Proxies:
     - Cumulative Volume Delta (CVD)
     - Bid-Ask Volume Imbalance (BAVI)
     - Volume Profile (VPVR): Point of Control (POC), Value Area High/Low (VAH/VAL)
     - Anchored VWAP + Standard Deviation Bands
  4. Macro Cross-Asset Ratios:
     - Gold/Silver Ratio (XAU/XAG)
     - Copper/Gold Ratio (HG/GC)
     - Real Yield (TIPS 10Y Proxy)
     - Yield Curve Slope (2s10s Proxy)
     - VIX Term Structure Contango/Backwardation
  5. Technical & Statistical Suite:
     - MACD, Ichimoku Cloud, Supertrend, Bollinger Bands, Keltner Channels,
       Stochastic RSI, Williams %R, CCI, ROC, OBV, MFI, CMF,
       Hurst Exponent (R/S), Shannon Entropy, Variance Ratio Test.
"""

import os
import math
import logging
from datetime import datetime
from typing import Dict, Any, Tuple, Optional, List

import numpy as np
import pandas as pd
from scipy import stats

logger = logging.getLogger("InstitutionalTripleBarrierEngine")

DEFAULT_LEDGER_PATH = os.path.join(os.path.dirname(__file__), "data", "capital_1000_trades_triple_barrier_ledger.csv")


# -----------------------------------------------------------------------------
# 1. Advanced Technical & Statistical Indicators
# -----------------------------------------------------------------------------
def compute_macd(series: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Computes MACD line, signal line, and MACD histogram."""
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    sig_line = macd_line.ewm(span=signal, adjust=False).mean()
    hist = macd_line - sig_line
    return macd_line, sig_line, hist


def compute_ichimoku(df: pd.DataFrame) -> Dict[str, pd.Series]:
    """Computes Ichimoku Kinko Hyo Cloud lines."""
    high = df["high"]
    low = df["low"]
    tenkan = (high.rolling(9).max() + low.rolling(9).min()) / 2.0
    kijun = (high.rolling(26).max() + low.rolling(26).min()) / 2.0
    senkou_a = ((tenkan + kijun) / 2.0).shift(26)
    senkou_b = ((high.rolling(52).max() + low.rolling(52).min()) / 2.0).shift(26)
    return {
        "tenkan_sen": tenkan,
        "kijun_sen": kijun,
        "senkou_span_a": senkou_a,
        "senkou_span_b": senkou_b,
        "cloud_green": senkou_a > senkou_b
    }


def compute_supertrend(df: pd.DataFrame, period: int = 10, multiplier: float = 3.0) -> Tuple[pd.Series, pd.Series]:
    """Computes ATR-based Supertrend line and directional signal (+1 bull, -1 bear)."""
    high = df["high"]
    low = df["low"]
    close = df["close"]
    tr = np.maximum(high - low, np.maximum(abs(high - close.shift(1)), abs(low - close.shift(1))))
    atr = tr.rolling(period).mean()

    hl2 = (high + low) / 2.0
    upper_band = hl2 + (multiplier * atr)
    lower_band = hl2 - (multiplier * atr)

    supertrend = pd.Series(index=df.index, dtype=float)
    direction = pd.Series(1, index=df.index, dtype=int)

    for i in range(period, len(df)):
        c = close.iloc[i]
        prev_st = supertrend.iloc[i-1] if i > period else lower_band.iloc[i]
        prev_dir = direction.iloc[i-1] if i > period else 1

        if prev_dir == 1:
            if c < lower_band.iloc[i]:
                direction.iloc[i] = -1
                supertrend.iloc[i] = upper_band.iloc[i]
            else:
                direction.iloc[i] = 1
                supertrend.iloc[i] = max(lower_band.iloc[i], prev_st)
        else:
            if c > upper_band.iloc[i]:
                direction.iloc[i] = 1
                supertrend.iloc[i] = lower_band.iloc[i]
            else:
                direction.iloc[i] = -1
                supertrend.iloc[i] = min(upper_band.iloc[i], prev_st)

    return supertrend, direction


def compute_bollinger_bands(series: pd.Series, period: int = 20, num_std: float = 2.0) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series]:
    """Computes Bollinger Bands, %B, and Bandwidth."""
    sma = series.rolling(period).mean()
    rstd = series.rolling(period).std()
    upper = sma + (num_std * rstd)
    lower = sma - (num_std * rstd)
    pct_b = (series - lower) / np.maximum(1e-5, upper - lower)
    bandwidth = (upper - lower) / np.maximum(1e-5, sma)
    return upper, lower, pct_b, bandwidth


def compute_stochastic_rsi(series: pd.Series, rsi_period: int = 14, stoch_period: int = 14, k_period: int = 3) -> Tuple[pd.Series, pd.Series]:
    """Computes Stochastic RSI (%K and %D)."""
    delta = series.diff()
    gain = np.where(delta > 0, delta, 0.0)
    loss = np.where(delta < 0, -delta, 0.0)
    avg_gain = pd.Series(gain, index=series.index).rolling(rsi_period).mean()
    avg_loss = pd.Series(loss, index=series.index).rolling(rsi_period).mean()
    rs = avg_gain / np.maximum(1e-5, avg_loss)
    rsi = 100.0 - (100.0 / (1.0 + rs))

    rsi_low = rsi.rolling(stoch_period).min()
    rsi_high = rsi.rolling(stoch_period).max()
    stoch_rsi = (rsi - rsi_low) / np.maximum(1e-5, rsi_high - rsi_low) * 100.0
    k = stoch_rsi.rolling(k_period).mean()
    d = k.rolling(3).mean()
    return k, d


def compute_williams_r(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Computes Williams %R oscillator (-100 to 0)."""
    hh = df["high"].rolling(period).max()
    ll = df["low"].rolling(period).min()
    wr = ((hh - df["close"]) / np.maximum(1e-5, hh - ll)) * -100.0
    return wr


def compute_cci(df: pd.DataFrame, period: int = 20) -> pd.Series:
    """Computes Commodity Channel Index (CCI)."""
    tp = (df["high"] + df["low"] + df["close"]) / 3.0
    sma = tp.rolling(period).mean()
    mad = tp.rolling(period).apply(lambda x: np.mean(np.abs(x - np.mean(x))), raw=True)
    cci = (tp - sma) / np.maximum(1e-5, 0.015 * mad)
    return cci


def compute_obv_and_mfi(df: pd.DataFrame, period: int = 14) -> Tuple[pd.Series, pd.Series]:
    """Computes On-Balance Volume (OBV) and Money Flow Index (MFI)."""
    close = df["close"]
    vol = df["volume"]
    obv = (np.sign(close.diff()).fillna(0) * vol).cumsum()

    tp = (df["high"] + df["low"] + close) / 3.0
    raw_money_flow = tp * vol
    pos_flow = pd.Series(np.where(tp > tp.shift(1), raw_money_flow, 0.0), index=df.index)
    neg_flow = pd.Series(np.where(tp < tp.shift(1), raw_money_flow, 0.0), index=df.index)

    pos_mf = pos_flow.rolling(period).sum()
    neg_mf = neg_flow.rolling(period).sum()
    mfr = pos_mf / np.maximum(1e-5, neg_mf)
    mfi = 100.0 - (100.0 / (1.0 + mfr))
    return obv, mfi


def compute_hurst_exponent_rs(series: pd.Series, max_lag: int = 30) -> float:
    """
    Computes Rescaled Range (R/S) Hurst Exponent.
    H > 0.5: Persistent/trending
    H = 0.5: Brownian random walk
    H < 0.5: Mean-reverting
    """
    vals = series.dropna().values
    if len(vals) < max_lag * 2:
        return 0.50

    lags = [l for l in [10, 15, 20, 25, 30] if l < len(vals) // 2]
    if len(lags) < 3:
        return 0.50

    rs_values = []
    for lag in lags:
        sub_returns = np.diff(vals[-lag*2:])
        mean_r = np.mean(sub_returns)
        cum_dev = np.cumsum(sub_returns - mean_r)
        r_range = np.max(cum_dev) - np.min(cum_dev)
        s_std = np.std(sub_returns)
        if s_std > 1e-6:
            rs_values.append(r_range / s_std)
        else:
            rs_values.append(1.0)

    try:
        poly = np.polyfit(np.log(lags), np.log(rs_values), 1)
        hurst = float(np.clip(poly[0], 0.05, 0.95))
        return hurst
    except Exception:
        return 0.50


def compute_shannon_entropy(series: pd.Series, bins: int = 10) -> float:
    """Computes Shannon Entropy of return distribution (Information Content)."""
    returns = series.pct_change().dropna().values
    if len(returns) < bins:
        return 0.0
    counts, _ = np.histogram(returns, bins=bins, density=True)
    counts = counts[counts > 0]
    p = counts / np.sum(counts)
    entropy = -np.sum(p * np.log2(p))
    return float(entropy)


def compute_variance_ratio_test(series: pd.Series, q: int = 5) -> Tuple[float, float]:
    """
    Computes Lo-MacKinlay Variance Ratio Test for Random Walk.
    VR = Var(q-period returns) / (q * Var(1-period returns))
    """
    returns_1 = np.diff(np.log(series.dropna().values))
    if len(returns_1) < q * 10:
        return 1.0, 0.0

    var_1 = np.var(returns_1, ddof=1)
    returns_q = np.diff(np.log(series.dropna().values[::q]))
    var_q = np.var(returns_q, ddof=1)

    if var_1 < 1e-9:
        return 1.0, 0.0

    vr = float(var_q / (q * var_1))
    # Test statistic under homoskedasticity
    n = len(returns_1)
    stat = (vr - 1.0) / np.sqrt((2.0 * (2 * q - 1) * (q - 1)) / (3.0 * q * n))
    return vr, float(stat)


# -----------------------------------------------------------------------------
# 2. Microstructure & Order Flow Proxies
# -----------------------------------------------------------------------------
def compute_microstructure_proxies(df: pd.DataFrame) -> Dict[str, pd.Series]:
    """
    Computes Cumulative Volume Delta (CVD), Bid-Ask Volume Imbalance (BAVI),
    and Anchored VWAP from standard OHLCV bars.
    """
    high = df["high"]
    low = df["low"]
    open_p = df["open"]
    close = df["close"]
    vol = df["volume"]

    # Bar directional intra-bar thrust
    bar_range = np.maximum(1e-5, high - low)
    directional_weight = (close - open_p) / bar_range

    # Volume Delta & CVD
    vol_delta = vol * directional_weight
    cvd = vol_delta.cumsum()

    # BAVI: Bid-Ask Volume Imbalance proxy
    buyer_vol = vol * np.clip(0.5 + 0.5 * directional_weight, 0.0, 1.0)
    seller_vol = vol * np.clip(0.5 - 0.5 * directional_weight, 0.0, 1.0)
    bavi = (buyer_vol - seller_vol) / np.maximum(1e-5, buyer_vol + seller_vol)

    # Anchored VWAP (rolling 60 bars anchor)
    cum_pv = (close * vol).rolling(60).sum()
    cum_v = vol.rolling(60).sum()
    avwap = cum_pv / np.maximum(1e-5, cum_v)
    avwap_std = ((close - avwap) ** 2 * vol).rolling(60).sum() / np.maximum(1e-5, cum_v)
    avwap_std = np.sqrt(np.maximum(0.0, avwap_std))

    return {
        "cvd": cvd,
        "bavi": bavi,
        "avwap": avwap,
        "avwap_upper": avwap + (1.5 * avwap_std),
        "avwap_lower": avwap - (1.5 * avwap_std)
    }


def compute_volume_profile_poc(df: pd.DataFrame, lookback: int = 40, bins: int = 15) -> Tuple[float, float, float]:
    """
    Computes Point of Control (POC), Value Area High (VAH), and Value Area Low (VAL).
    Value Area covers 70% of total volume around POC.
    """
    sub = df.iloc[-lookback:]
    if len(sub) < 10:
        p = float(df["close"].iloc[-1])
        return p, p * 1.01, p * 0.99

    prices = sub["close"].values
    volumes = sub["volume"].values

    hist, bin_edges = np.histogram(prices, bins=bins, weights=volumes)
    poc_idx = np.argmax(hist)
    poc_price = (bin_edges[poc_idx] + bin_edges[poc_idx + 1]) / 2.0

    total_vol = np.sum(hist)
    target_vol = total_vol * 0.70
    current_vol = hist[poc_idx]

    left = poc_idx
    right = poc_idx

    while current_vol < target_vol and (left > 0 or right < bins - 1):
        left_vol = hist[left - 1] if left > 0 else 0
        right_vol = hist[right + 1] if right < bins - 1 else 0

        if right_vol >= left_vol and right < bins - 1:
            right += 1
            current_vol += hist[right]
        elif left > 0:
            left -= 1
            current_vol += hist[left]
        else:
            break

    val_price = bin_edges[left]
    vah_price = bin_edges[right + 1]
    return float(poc_price), float(vah_price), float(val_price)


# -----------------------------------------------------------------------------
# 3. Triple-Barrier Method & Sample Uniqueness (AFML Ch. 3 & 4)
# -----------------------------------------------------------------------------
class InstitutionalTripleBarrierEngine:
    """
    Marcos López de Prado Triple-Barrier Quantitative Framework.
    """

    @staticmethod
    def triple_barrier_label(
        entry_price: float,
        sl_price: float,
        tp1_price: float,
        tp2_price: float,
        direction: str,
        forward_bars: pd.DataFrame,
        daily_swap: float = 0.0,
        spread: float = 0.0,
        max_bars: int = 45
    ) -> Dict[str, Any]:
        """
        Labels a trade using Triple-Barrier:
        - Barrier 1 (Upper): Target TP1 (+2.5R) or TP2 (+4.0R) hit -> Label +1
        - Barrier 2 (Lower): Stop Loss hit -> Label -1
        - Barrier 3 (Vertical): Time expiration (max_bars) -> Mark-to-market realized R
        """
        dir_clean = str(direction or "").upper().strip()
        sl_dist = abs(entry_price - sl_price)
        if sl_dist <= 1e-5:
            sl_dist = entry_price * 0.015

        n_bars = min(len(forward_bars), max_bars)
        if n_bars == 0:
            return {
                "label": 0,
                "realized_r": 0.0,
                "holding_bars": 0,
                "barrier_hit": "VERTICAL_EXPIRY",
                "exit_price": entry_price
            }

        sl_hit = False
        tp1_hit = False
        tp2_hit = False
        breakeven_active = False
        active_sl = sl_price
        exit_price = entry_price
        exit_idx = n_bars - 1
        barrier_hit = "VERTICAL_EXPIRY"
        swap_accrued = 0.0

        for idx in range(n_bars):
            bar = forward_bars.iloc[idx]
            b_high = float(bar["high"])
            b_low = float(bar["low"])
            b_close = float(bar["close"])
            swap_accrued += daily_swap

            # 1. Check Stop Loss
            if dir_clean == "BUY":
                if b_low <= active_sl:
                    sl_hit = True
                    exit_price = active_sl
                    exit_idx = idx
                    barrier_hit = "LOWER_STOP_LOSS"
                    break
                # Check TP1 -> activates Breakeven Armor (Entry + 0.5*Spread) or exits if single TP
                if not tp1_hit and b_high >= tp1_price:
                    tp1_hit = True
                    if tp2_price <= tp1_price:
                        exit_price = tp1_price
                        exit_idx = idx
                        barrier_hit = "UPPER_PROFIT_TARGET"
                        break
                    breakeven_active = True
                    active_sl = entry_price + (0.5 * spread)
                # Check TP2
                if tp1_hit and b_high >= tp2_price:
                    tp2_hit = True
                    exit_price = tp2_price
                    exit_idx = idx
                    barrier_hit = "UPPER_PROFIT_TARGET_TP2"
                    break
            else:  # SELL
                if b_high >= active_sl:
                    sl_hit = True
                    exit_price = active_sl
                    exit_idx = idx
                    barrier_hit = "LOWER_STOP_LOSS"
                    break
                if not tp1_hit and b_low <= tp1_price:
                    tp1_hit = True
                    if tp2_price >= tp1_price:
                        exit_price = tp1_price
                        exit_idx = idx
                        barrier_hit = "UPPER_PROFIT_TARGET"
                        break
                    breakeven_active = True
                    active_sl = entry_price - (0.5 * spread)
                if tp1_hit and b_low <= tp2_price:
                    tp2_hit = True
                    exit_price = tp2_price
                    exit_idx = idx
                    barrier_hit = "UPPER_PROFIT_TARGET_TP2"
                    break

        holding_bars = exit_idx + 1

        if barrier_hit == "VERTICAL_EXPIRY":
            exit_price = float(forward_bars["close"].iloc[exit_idx])

        # Compute Net Realized R
        gross_diff = (exit_price - entry_price) if dir_clean == "BUY" else (entry_price - exit_price)
        net_diff = gross_diff - spread - (swap_accrued * entry_price)
        realized_r = float(net_diff / sl_dist)

        # Label: +1 for winning trade, -1 for loss, 0 for scratch/neutral
        if realized_r > 0.05:
            label = 1
        elif realized_r < -0.05:
            label = -1
        else:
            label = 0

        return {
            "label": int(label),
            "binary_win": 1 if realized_r > 0.0 else 0,
            "realized_r": round(realized_r, 4),
            "holding_bars": holding_bars,
            "barrier_hit": barrier_hit,
            "exit_price": exit_price,
            "breakeven_armored": breakeven_active
        }

    @classmethod
    def compute_sample_uniqueness(cls, trades_df: pd.DataFrame) -> pd.Series:
        """
        Computes sample uniqueness u_bar_i for each trade based on concurrency overlap c_t.
        Follows Marcos López de Prado AFML Chapter 4.
        """
        if len(trades_df) == 0:
            return pd.Series([], dtype=float)

        trades_df = trades_df.copy()
        trades_df["entry_idx"] = pd.to_datetime(trades_df["entry_date"])
        trades_df["exit_idx"] = pd.to_datetime(trades_df["exit_date"])

        # Build timeline of concurrent active trades c_t
        all_dates = pd.date_range(trades_df["entry_idx"].min(), trades_df["exit_idx"].max())
        concurrency = pd.Series(0, index=all_dates)

        for _, row in trades_df.iterrows():
            concurrency.loc[row["entry_idx"]:row["exit_idx"]] += 1

        concurrency = np.maximum(1, concurrency)

        # Compute average uniqueness u_bar for each trade
        uniqueness_list = []
        for _, row in trades_df.iterrows():
            sub_c = concurrency.loc[row["entry_idx"]:row["exit_idx"]]
            u_t = 1.0 / sub_c
            u_bar = float(u_t.mean())
            uniqueness_list.append(u_bar)

        return pd.Series(uniqueness_list, index=trades_df.index)

    @classmethod
    def build_1000_trade_universe(
        cls,
        save_csv: str = DEFAULT_LEDGER_PATH,
        min_trades: int = 1000
    ) -> pd.DataFrame:
        """
        Generates 1,000+ real trade simulations across top institutional TradFi assets
        with full triple-barrier labeling, microstructural flow, macro overlays, and sample weights.
        """
        import capital_10y_backtester as bt

        logger.info("Initializing 1,000+ Trade Institutional Triple-Barrier Generation...")

        # 30 Prime Institutional Assets across Commodities, US/Euro/Asian Indices, and Mega-Cap Stocks
        prime_assets = [
            "GCF", "SIF", "CLF", "BZF", "HGF", "NGF",
            "ESF", "NQF", "YMF", "RTYF", "GDAXI", "FTSE", "FCHI", "STOXX50E", "N225", "HSI", "AXJO",
            "AAPL", "MSFT", "NVDA", "TSLA", "AMZN", "GOOGL", "META", "AMD", "AVGO", "BABA", "TSM",
            "JPM", "XOM"
        ]

        # Load Macro Ratios
        gold_df = pd.read_csv("data/tradfi_10y_dna/GCF_1d_10y.csv")
        silver_df = pd.read_csv("data/tradfi_10y_dna/SIF_1d_10y.csv")
        copper_df = pd.read_csv("data/tradfi_10y_dna/HGF_1d_10y.csv")
        tnx_df = pd.read_csv("data/tradfi_10y_dna/TNX_1d_10y.csv")
        vix_df = pd.read_csv("data/tradfi_10y_dna/VIX_1d_10y.csv")
        dxy_df = pd.read_csv("data/tradfi_10y_dna/DX-Y.NYB_1d_10y.csv")

        def _load_optional_macro_map(filename: str) -> Dict[Any, float]:
            path = os.path.join("data", "tradfi_10y_dna", filename)
            if not os.path.exists(path):
                return {}
            try:
                opt_df = pd.read_csv(path)
                opt_df["Date"] = pd.to_datetime(opt_df["Date"])
                return dict(zip(opt_df["Date"], opt_df["close"]))
            except Exception as exc:
                logger.warning(f"Optional macro file {filename} could not be loaded: {exc}")
                return {}

        gold_df["Date"] = pd.to_datetime(gold_df["Date"])
        silver_df["Date"] = pd.to_datetime(silver_df["Date"])
        copper_df["Date"] = pd.to_datetime(copper_df["Date"])
        tnx_df["Date"] = pd.to_datetime(tnx_df["Date"])
        vix_df["Date"] = pd.to_datetime(vix_df["Date"])
        dxy_df["Date"] = pd.to_datetime(dxy_df["Date"])

        # Macro Maps
        gold_map = dict(zip(gold_df["Date"], gold_df["close"]))
        silver_map = dict(zip(silver_df["Date"], silver_df["close"]))
        copper_map = dict(zip(copper_df["Date"], copper_df["close"]))
        tnx_map = dict(zip(tnx_df["Date"], tnx_df["close"]))
        vix_map = dict(zip(vix_df["Date"], vix_df["close"]))
        dxy_map = dict(zip(dxy_df["Date"], dxy_df["close"]))
        tips_map = _load_optional_macro_map("DFII10_1d_10y.csv")
        yield_curve_map = _load_optional_macro_map("T10Y2Y_1d_10y.csv")
        credit_spread_map = _load_optional_macro_map("BAMLH0A0HYM2_1d_10y.csv")
        put_call_map = _load_optional_macro_map("CPC_1d_10y.csv")
        vix3m_map = _load_optional_macro_map("VIX3M_1d_10y.csv")

        # VIX 60-day moving average for term structure proxy
        vix_df["vix_sma60"] = vix_df["close"].rolling(60).mean()
        vix_ts_map = dict(zip(vix_df["Date"], vix_df["close"] / np.maximum(1e-5, vix_df["vix_sma60"])))

        records = []

        for epic in prime_assets:
            csv_path = f"data/tradfi_10y_dna/{epic}_1d_10y.csv"
            if not os.path.exists(csv_path):
                continue

            df = pd.read_csv(csv_path)
            df["Date"] = pd.to_datetime(df["Date"])
            if len(df) < 250:
                continue

            # Core Technical Indicators
            tr = np.maximum(df["high"] - df["low"], np.maximum(abs(df["high"] - df["close"].shift(1)), abs(df["low"] - df["close"].shift(1))))
            df["atr14"] = tr.rolling(14).mean()
            df["ema20"] = df["close"].ewm(span=20, adjust=False).mean()
            df["ema50"] = df["close"].ewm(span=50, adjust=False).mean()
            df["ema200"] = df["close"].ewm(span=200, adjust=False).mean()
            df["swing_high_35"] = df["high"].rolling(35).max().shift(1)
            df["swing_low_35"] = df["low"].rolling(35).min().shift(1)
            df["range_pct"] = ((df["close"] - df["swing_low_35"]) / np.maximum(1e-5, df["swing_high_35"] - df["swing_low_35"])) * 100.0

            # Momentum
            delta = df["close"].diff()
            gain = np.where(delta > 0, delta, 0.0)
            loss = np.where(delta < 0, -delta, 0.0)
            avg_g = pd.Series(gain, index=df.index).rolling(14).mean()
            avg_l = pd.Series(loss, index=df.index).rolling(14).mean()
            df["rsi14"] = 100.0 - (100.0 / (1.0 + (avg_g / np.maximum(1e-5, avg_l))))

            # ADX
            up_move = df["high"] - df["high"].shift(1)
            down_move = df["low"].shift(1) - df["low"]
            plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
            minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
            plus_di = 100.0 * (pd.Series(plus_dm, index=df.index).rolling(14).mean() / np.maximum(1e-5, df["atr14"]))
            minus_di = 100.0 * (pd.Series(minus_dm, index=df.index).rolling(14).mean() / np.maximum(1e-5, df["atr14"]))
            dx = 100.0 * (abs(plus_di - minus_di) / np.maximum(1e-5, plus_di + minus_di))
            df["adx14"] = dx.rolling(14).mean()

            # Microstructure Proxies
            micro = compute_microstructure_proxies(df)
            df["cvd"] = micro["cvd"]
            df["bavi"] = micro["bavi"]
            df["avwap"] = micro["avwap"]

            # Additional Technicals
            df["macd"], df["macd_sig"], df["macd_hist"] = compute_macd(df["close"])
            df["boll_up"], df["boll_dn"], df["boll_pct_b"], df["boll_bw"] = compute_bollinger_bands(df["close"])
            df["stoch_k"], df["stoch_d"] = compute_stochastic_rsi(df["close"])
            df["williams_r"] = compute_williams_r(df)
            df["cci"] = compute_cci(df)

            # Asset Spread Estimation
            ref_p = float(df["close"].iloc[-1])
            if "GC" in epic:
                spread = 0.35
            elif "SI" in epic:
                spread = 0.02
            elif "CL" in epic or "BZ" in epic:
                spread = 0.04
            elif "NQ" in epic or "ES" in epic or "YM" in epic:
                spread = 1.25
            else:
                spread = max(0.05, round(ref_p * 0.00015, 2))

            for i in range(200, len(df) - 45):
                row = df.iloc[i]
                curr_p = float(row["close"])
                curr_d = row["Date"]
                atr_val = float(row["atr14"])
                if pd.isna(atr_val) or atr_val <= 0:
                    continue

                # Multi-Factor Citadel Scoring
                is_uptrend = (curr_p >= row["ema200"]) and (row["ema20"] >= row["ema50"])
                is_downtrend = (curr_p <= row["ema200"]) and (row["ema20"] <= row["ema50"])
                rng_p = float(row["range_pct"]) if not pd.isna(row["range_pct"]) else 50.0

                # Chop avoidance (35% to 65% equilibrium injunction)
                if 38.0 <= rng_p <= 62.0:
                    continue

                dir_signal = None
                raw_score = 50.0

                if is_uptrend and rng_p < 38.0 and row["rsi14"] > 38.0 and row["adx14"] >= 22.0:
                    dir_signal = "BUY"
                    raw_score = 72.0 + (5.0 if row["cvd"] > df["cvd"].iloc[i-5] else 0.0) + (5.0 if curr_p > row["avwap"] else 0.0)
                elif is_downtrend and rng_p > 62.0 and row["rsi14"] < 68.0 and row["adx14"] >= 22.0:
                    dir_signal = "SELL"
                    raw_score = 72.0 + (5.0 if row["cvd"] < df["cvd"].iloc[i-5] else 0.0) + (5.0 if curr_p < row["avwap"] else 0.0)

                if dir_signal is not None and raw_score >= 68.0:
                    next_b = df.iloc[i+1]
                    entry_p = float(next_b["open"])
                    sl_dist = max(2.20 * atr_val, 3.5 * spread, entry_p * 0.0035)
                    sl_p = entry_p - sl_dist if dir_signal == "BUY" else entry_p + sl_dist
                    tp1_p = entry_p + (2.5 * sl_dist) if dir_signal == "BUY" else entry_p - (2.5 * sl_dist)
                    tp2_p = entry_p + (4.0 * sl_dist) if dir_signal == "BUY" else entry_p - (4.0 * sl_dist)

                    forward_bars = df.iloc[i+1:i+46]

                    # Triple-Barrier Evaluation
                    barrier_res = cls.triple_barrier_label(
                        entry_price=entry_p,
                        sl_price=sl_p,
                        tp1_price=tp1_p,
                        tp2_price=tp2_p,
                        direction=dir_signal,
                        forward_bars=forward_bars,
                        daily_swap=-0.0001,
                        spread=spread,
                        max_bars=45
                    )

                    exit_date = df["Date"].iloc[min(len(df)-1, i + barrier_res["holding_bars"])]

                    # Macro Cross Ratios
                    g_price = gold_map.get(curr_d, 2000.0)
                    s_price = silver_map.get(curr_d, 25.0)
                    c_price = copper_map.get(curr_d, 4.0)
                    gs_ratio = g_price / max(1e-5, s_price)
                    cg_ratio = (c_price / max(1e-5, g_price)) * 1000.0
                    tips_real_yield = tnx_map.get(curr_d, 4.0) - 2.20
                    vix_val = vix_map.get(curr_d, 20.0)
                    vix3m_val = vix3m_map.get(curr_d)
                    if vix3m_val:
                        vix_ts = vix_val / max(1e-5, vix3m_val)
                    else:
                        vix_ts = vix_ts_map.get(curr_d, 1.0)
                    dxy_val = dxy_map.get(curr_d, 102.0)
                    yield_curve_2s10s = yield_curve_map.get(curr_d, 0.0)
                    credit_spread_hy = credit_spread_map.get(curr_d, 0.0)
                    put_call_ratio = put_call_map.get(curr_d, 1.0)
                    if curr_d in tips_map:
                        tips_real_yield = tips_map[curr_d]

                    # Statistical Features
                    hurst = compute_hurst_exponent_rs(df["close"].iloc[max(0, i-60):i])
                    entropy = compute_shannon_entropy(df["close"].iloc[max(0, i-60):i])
                    volume_profile_poc, volume_profile_vah, volume_profile_val = compute_volume_profile_poc(
                        df.iloc[:i+1],
                        lookback=40,
                        bins=15
                    )

                    records.append({
                        "trade_id": len(records) + 1,
                        "symbol": epic,
                        "entry_date": curr_d.strftime("%Y-%m-%d"),
                        "exit_date": exit_date.strftime("%Y-%m-%d"),
                        "direction": dir_signal,
                        "direction_num": 1 if dir_signal == "BUY" else -1,
                        "entry_price": round(entry_p, 4),
                        "exit_price": round(barrier_res["exit_price"], 4),
                        "sl_price": round(sl_p, 4),
                        "tp1_price": round(tp1_p, 4),
                        "tp2_price": round(tp2_p, 4),
                        "holding_bars": barrier_res["holding_bars"],
                        "barrier_hit": barrier_res["barrier_hit"],
                        "triple_barrier_label": barrier_res["label"],
                        "binary_win": barrier_res["binary_win"],
                        "realized_r": barrier_res["realized_r"],
                        # Microstructure
                        "raw_score": raw_score,
                        "adx14": round(float(row["adx14"]), 2),
                        "rsi14": round(float(row["rsi14"]), 2),
                        "range_pct": round(rng_p, 2),
                        "atr14": round(atr_val, 4),
                        "spread_drag_pct": round((spread / atr_val) * 100.0, 2),
                        "ema20_dist_pct": round(((curr_p / max(1e-5, row["ema20"])) - 1.0) * 100.0, 4),
                        "ema50_dist_pct": round(((curr_p / max(1e-5, row["ema50"])) - 1.0) * 100.0, 4),
                        "ema200_dist_pct": round(((curr_p / max(1e-5, row["ema200"])) - 1.0) * 100.0, 4),
                        "cvd": round(float(row["cvd"]), 1),
                        "bavi": round(float(row["bavi"]), 4),
                        "avwap_dist_pct": round(((curr_p / max(1e-5, row["avwap"])) - 1.0) * 100.0, 2),
                        "volume_profile_poc": round(volume_profile_poc, 4),
                        "volume_profile_vah": round(volume_profile_vah, 4),
                        "volume_profile_val": round(volume_profile_val, 4),
                        "boll_pct_b": round(float(row["boll_pct_b"]), 2),
                        "stoch_k": round(float(row["stoch_k"]), 2),
                        "williams_r": round(float(row["williams_r"]), 2),
                        "cci": round(float(row["cci"]), 2),
                        # Macro Overlays
                        "gold_silver_ratio": round(gs_ratio, 2),
                        "copper_gold_ratio": round(cg_ratio, 4),
                        "tips_real_yield": round(tips_real_yield, 2),
                        "yield_curve_2s10s": round(float(yield_curve_2s10s), 4),
                        "credit_spread_hy": round(float(credit_spread_hy), 4),
                        "vix": round(vix_val, 2),
                        "vix_term_structure": round(vix_ts, 4),
                        "put_call_ratio": round(float(put_call_ratio), 4),
                        "dxy": round(dxy_val, 2),
                        # Statistics
                        "hurst_exponent": round(hurst, 3),
                        "shannon_entropy": round(entropy, 3),
                        "day_of_week": curr_d.weekday()
                    })

        df_trades = pd.DataFrame(records).sort_values("entry_date").reset_index(drop=True)
        df_trades["trade_id"] = np.arange(1, len(df_trades) + 1)

        # Compute Sample Uniqueness and Weights (AFML Ch. 4)
        logger.info(f"Computing sample uniqueness across {len(df_trades)} historical trades...")
        uniqueness = cls.compute_sample_uniqueness(df_trades)
        df_trades["sample_uniqueness"] = uniqueness.round(4)

        abs_r = np.abs(df_trades["realized_r"])
        sample_weights = uniqueness * abs_r
        sample_weights = (sample_weights / max(1e-5, sample_weights.sum())) * len(df_trades)
        df_trades["sample_weight"] = sample_weights.round(4)

        if save_csv:
            os.makedirs(os.path.dirname(save_csv), exist_ok=True)
            df_trades.to_csv(save_csv, index=False)
            logger.info(f"Saved {len(df_trades)} institutional trades to {save_csv}")

        return df_trades


def label_triple_barrier_with_weights(
    entry_price: float,
    future_highs: Any,
    future_lows: Any,
    future_closes: Any,
    tp_price: float,
    sl_price: float,
    direction: str = "BUY",
    holding_period_bars: int = 45,
    spread: float = 0.0,
    daily_swap: float = 0.0
) -> Tuple[int, float, float]:
    """
    Convenience function to label a trade using Triple-Barrier from numpy arrays or series.
    Returns: (label, realized_r, sample_weight)
      - label: +1 (profit target hit), -1 (stop loss hit), 0 (vertical expiry)
      - realized_r: actual realized R value post-costs
      - sample_weight: volatility & uniqueness-adjusted sample weight
    """
    highs = np.asarray(future_highs, dtype=float)
    lows = np.asarray(future_lows, dtype=float)
    closes = np.asarray(future_closes, dtype=float)

    n_bars = min(len(highs), holding_period_bars)
    if n_bars == 0:
        return 0, 0.0, 1.0

    df_forward = pd.DataFrame({
        "high": highs[:n_bars],
        "low": lows[:n_bars],
        "close": closes[:n_bars]
    })

    res = InstitutionalTripleBarrierEngine.triple_barrier_label(
        entry_price=entry_price,
        sl_price=sl_price,
        tp1_price=tp_price,
        tp2_price=tp_price,
        direction=direction,
        forward_bars=df_forward,
        daily_swap=daily_swap,
        spread=spread,
        max_bars=holding_period_bars
    )

    label = int(res["label"])
    realized_r = float(res["realized_r"])
    sample_weight = float(max(0.1, min(3.0, 1.0 + abs(realized_r) * 0.5)))
    return label, realized_r, sample_weight


def calculate_sample_uniqueness_weights(trades_df: pd.DataFrame) -> pd.Series:
    """Wrapper around InstitutionalTripleBarrierEngine.compute_sample_uniqueness."""
    return InstitutionalTripleBarrierEngine.compute_sample_uniqueness(trades_df)


def extract_institutional_feature_vector(df: pd.DataFrame, idx: int) -> Dict[str, float]:
    """Extracts institutional feature vector at bar idx."""
    sub = df.iloc[:idx+1]
    last_row = sub.iloc[-1]
    return {
        "close": float(last_row.get("close", 0.0)),
        "rsi": float(last_row.get("rsi", 50.0)),
        "adx": float(last_row.get("adx", 25.0)),
        "atr": float(last_row.get("atr", 1.0))
    }

