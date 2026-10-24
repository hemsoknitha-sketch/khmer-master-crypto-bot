# -*- coding: utf-8 -*-
"""
ANGKOR QUANT — INSTITUTIONAL M15 1-MONTH BACKTEST & FORWARD-TEST ENGINE ($1,000 CAPITAL)
=======================================================================================
Document Version: 1.0.0 (High-Resolution Intraday M15 TradFi Quantitative Suite)
Strategy Target: /capital (TradFi Engine, SuperSmartCapitalCitadel & AFML Meta-Labeling)
Starting Capital: $1,000.00 USD
Base Dollar Risk: $10.00 (1.0% Institutional Risk Parity)
Compounding Mode: Dynamic Fractional Kelly (1.5% Equity per trade)
Timeframe: M15 (15-Minute Intraday Bars)
Dataset Horizon: 1 Full Month Real Live Data (2,015+ bars per asset) + 1 Month Stochastic Forward-Test
"""

import os
import sys
import math
import json
import logging
import datetime
from typing import Dict, List, Tuple, Any, Optional
import numpy as np
import pandas as pd

# Path & Logging Setup
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AngkorQuantM15Engine")

# Quantitative Constants
INITIAL_CAPITAL = 1000.0
BASE_RISK_DOLLARS = 10.0
COMPOUNDING_RISK_PCT = 0.015  # 1.5% dynamic Kelly allocation
OUTPUT_DIR = "data"

# Capital.com CFD Specifications for M15 Execution
CAPITAL_M15_SPECS = {
    "GOLD": {
        "csv": "GOLD_15m_1m.csv", "name": "Gold (Spot/Futures)", "type": "COMMODITY",
        "spread": 0.35, "slippage": 0.08, "precision": 2, "contract_multiplier": 1.0, "min_deal_size": 0.01,
        "daily_swap_long": -0.00015, "daily_swap_short": -0.00008, "atr_sl_mult": 2.20
    },
    "US100": {
        "csv": "US100_15m_1m.csv", "name": "US Tech 100 (Nasdaq)", "type": "INDEX",
        "spread": 2.00, "slippage": 0.40, "precision": 2, "contract_multiplier": 1.0, "min_deal_size": 0.01,
        "daily_swap_long": -0.00022, "daily_swap_short": 0.00005, "atr_sl_mult": 2.20
    },
    "US500": {
        "csv": "US500_15m_1m.csv", "name": "US 500 (S&P 500)", "type": "INDEX",
        "spread": 0.45, "slippage": 0.12, "precision": 2, "contract_multiplier": 1.0, "min_deal_size": 0.01,
        "daily_swap_long": -0.00020, "daily_swap_short": 0.00004, "atr_sl_mult": 2.20
    },
    "DE40": {
        "csv": "DE40_15m_1m.csv", "name": "Germany 40 (DAX)", "type": "INDEX",
        "spread": 1.50, "slippage": 0.35, "precision": 2, "contract_multiplier": 1.0, "min_deal_size": 0.01,
        "daily_swap_long": -0.00018, "daily_swap_short": 0.00002, "atr_sl_mult": 2.20
    },
    "OIL": {
        "csv": "OIL_15m_1m.csv", "name": "Crude Oil (WTI)", "type": "COMMODITY",
        "spread": 0.04, "slippage": 0.02, "precision": 2, "contract_multiplier": 1.0, "min_deal_size": 0.10,
        "daily_swap_long": -0.00025, "daily_swap_short": -0.00010, "atr_sl_mult": 2.50
    },
    "SILVER": {
        "csv": "SILVER_15m_1m.csv", "name": "Silver (XAGUSD)", "type": "COMMODITY",
        "spread": 0.03, "slippage": 0.01, "precision": 3, "contract_multiplier": 1.0, "min_deal_size": 0.10,
        "daily_swap_long": -0.00018, "daily_swap_short": -0.00008, "atr_sl_mult": 2.50
    },
    "NVDA": {
        "csv": "NVDA_15m_1m.csv", "name": "NVIDIA Corp", "type": "EQUITY",
        "spread": 0.05, "slippage": 0.02, "precision": 2, "contract_multiplier": 1.0, "min_deal_size": 0.10,
        "daily_swap_long": -0.00028, "daily_swap_short": 0.00008, "atr_sl_mult": 2.20
    },
    "TSLA": {
        "csv": "TSLA_15m_1m.csv", "name": "Tesla Inc", "type": "EQUITY",
        "spread": 0.08, "slippage": 0.03, "precision": 2, "contract_multiplier": 1.0, "min_deal_size": 0.10,
        "daily_swap_long": -0.00028, "daily_swap_short": 0.00008, "atr_sl_mult": 2.20
    },
    "AAPL": {
        "csv": "AAPL_15m_1m.csv", "name": "Apple Inc", "type": "EQUITY",
        "spread": 0.04, "slippage": 0.02, "precision": 2, "contract_multiplier": 1.0, "min_deal_size": 0.10,
        "daily_swap_long": -0.00026, "daily_swap_short": 0.00006, "atr_sl_mult": 2.20
    },
    "MSFT": {
        "csv": "MSFT_15m_1m.csv", "name": "Microsoft Corp", "type": "EQUITY",
        "spread": 0.05, "slippage": 0.02, "precision": 2, "contract_multiplier": 1.0, "min_deal_size": 0.10,
        "daily_swap_long": -0.00026, "daily_swap_short": 0.00006, "atr_sl_mult": 2.20
    }
}


def compute_m15_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes full quantitative and technical indicators directly on M15 bars.
    """
    df = df.copy()
    c = df['close']
    h = df['high']
    l = df['low']
    o = df['open']
    v = df['volume'] if 'volume' in df.columns else pd.Series(np.ones(len(df)), index=df.index)

    # 1. True Range & ATR14
    prev_close = c.shift(1)
    tr1 = h - l
    tr2 = (h - prev_close).abs()
    tr3 = (l - prev_close).abs()
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    df['atr14'] = tr.ewm(span=14, adjust=False).mean()

    # 2. ADX14 (Wilder's DMI)
    up_move = h - h.shift(1)
    down_move = l.shift(1) - l
    plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0.0)
    minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0.0)
    plus_di = 100 * (pd.Series(plus_dm, index=df.index).ewm(span=14, adjust=False).mean() / df['atr14'].replace(0, 1e-5))
    minus_di = 100 * (pd.Series(minus_dm, index=df.index).ewm(span=14, adjust=False).mean() / df['atr14'].replace(0, 1e-5))
    dx = 100 * ((plus_di - minus_di).abs() / (plus_di + minus_di).replace(0, 1e-5))
    df['adx14'] = dx.ewm(span=14, adjust=False).mean().clip(0, 100)

    # 3. RSI14
    delta = c.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.ewm(span=14, adjust=False).mean()
    avg_loss = loss.ewm(span=14, adjust=False).mean()
    rs = avg_gain / avg_loss.replace(0, 1e-5)
    df['rsi14'] = (100 - (100 / (1 + rs))).clip(0, 100)

    # 4. Moving Averages (EMA 20, 50, 200)
    df['ema20'] = c.ewm(span=20, adjust=False).mean()
    df['ema50'] = c.ewm(span=50, adjust=False).mean()
    df['ema200'] = c.ewm(span=200, adjust=False).mean()

    # 5. Swing Boundaries (35-bar rolling max/min, shift 1 to avoid lookahead)
    df['swing_high_35'] = h.shift(1).rolling(35, min_periods=10).max()
    df['swing_low_35'] = l.shift(1).rolling(35, min_periods=10).min()
    rng = (df['swing_high_35'] - df['swing_low_35']).replace(0, 1e-5)
    df['range_pct'] = ((c - df['swing_low_35']) / rng * 100.0).clip(0, 100)

    # 6. Cumulative Volume Delta (CVD) proxy
    b_rng = (h - l).replace(0, 1e-5)
    thrust = (c - o) / b_rng
    df['cvd'] = (v * thrust).rolling(20, min_periods=5).sum()

    # 7. Hurst Exponent (rolling 40-bar proxy)
    ret = np.log(c / c.shift(1).replace(0, 1e-5)).replace([np.inf, -np.inf], 0.0).fillna(0.0)
    mean_ret = ret.rolling(40, min_periods=15).mean()
    dev = ret - mean_ret
    y = dev.rolling(40, min_periods=15).apply(lambda s: np.max(np.cumsum(s)) - np.min(np.cumsum(s)), raw=True)
    std = ret.rolling(40, min_periods=15).std().replace(0, 1e-5)
    rs_val = (y / std).clip(lower=1.01)
    df['hurst'] = (np.log(rs_val) / np.log(40.0)).clip(0.10, 0.90).fillna(0.50)

    return df.dropna().reset_index(drop=True)


def load_m15_datasets(data_dir: str = "data/tradfi_m15_1m") -> Tuple[Dict[str, pd.DataFrame], Dict[str, pd.DataFrame]]:
    """
    Loads and processes 1-month M15 data for all 10 assets and 2 macro series.
    """
    assets = {}
    macro = {}

    for sym, spec in CAPITAL_M15_SPECS.items():
        fpath = os.path.join(data_dir, spec['csv'])
        if not os.path.exists(fpath):
            raise FileNotFoundError(f"Missing M15 dataset for {sym} at {fpath}")
        df_raw = pd.read_csv(fpath)
        df_raw['datetime'] = pd.to_datetime(df_raw['datetime'])
        df_proc = compute_m15_indicators(df_raw)
        assets[sym] = df_proc
        logger.info(f"Loaded & processed M15 {sym}: {len(df_proc)} bars ({df_proc['datetime'].iloc[0]} -> {df_proc['datetime'].iloc[-1]})")

    # Load Macro overlays
    for m_sym, m_file in [('DXY', 'DXY_15m_1m.csv'), ('VIX', 'VIX_15m_1m.csv')]:
        fpath = os.path.join(data_dir, m_file)
        if os.path.exists(fpath):
            df_m = pd.read_csv(fpath)
            df_m['datetime'] = pd.to_datetime(df_m['datetime'])
            macro[m_sym] = df_m
            logger.info(f"Loaded Macro M15 {m_sym}: {len(df_m)} bars")

    return assets, macro


class M15Trade:
    """
    Encapsulates trade lifecycle, 4-phase Breakeven Armor, and scale-out on M15 bars.
    """
    def __init__(
        self,
        trade_id: int,
        symbol: str,
        direction: str,
        entry_idx: int,
        entry_time: pd.Timestamp,
        entry_price: float,
        sl_price: float,
        atr_15m: float,
        spread: float,
        slippage: float,
        base_risk_dollars: float,
        contract_multiplier: float = 1.0,
        min_deal_size: float = 0.01,
        compounding_equity: Optional[float] = None,
        risk_pct: float = 0.015,
        drop_scale_out: bool = False
    ):
        self.trade_id = trade_id
        self.symbol = symbol
        self.direction = direction
        self.entry_idx = entry_idx
        self.entry_time = entry_time
        self.entry_price = entry_price
        self.initial_sl = sl_price
        self.current_sl = sl_price
        self.sl_dist = abs(entry_price - sl_price)
        self.atr_15m = atr_15m
        self.spread = spread
        self.slippage = slippage
        self.contract_multiplier = contract_multiplier
        self.min_deal_size = min_deal_size
        self.drop_scale_out = drop_scale_out

        # Dynamic Sizing calculation
        if compounding_equity is not None:
            self.target_risk = compounding_equity * risk_pct
        else:
            self.target_risk = base_risk_dollars

        raw_size = self.target_risk / max(1e-4, self.sl_dist * contract_multiplier)
        self.position_size = max(min_deal_size, round(raw_size, 2 if min_deal_size >= 0.1 else 3))
        self.initial_risk_dollars = self.position_size * self.sl_dist * contract_multiplier
        self.risk_overrun = self.initial_risk_dollars > (self.target_risk * 1.25)

        # Multi-Stage Targets (Invariant 98)
        if self.drop_scale_out:
            # Fixed 1:1.5 R:R
            self.tp1_price = entry_price + (1.5 * self.sl_dist) if direction == "BUY" else entry_price - (1.5 * self.sl_dist)
            self.tp2_price = self.tp1_price
            self.tp3_price = self.tp1_price
        else:
            # Phase 2: TP1 (50% lot) at +1.8R
            # Phase 3: TP2 (30% lot) at +3.5R
            # Phase 4: Runner (20% lot) at +8.0R
            self.tp1_price = entry_price + (1.80 * self.sl_dist) if direction == "BUY" else entry_price - (1.80 * self.sl_dist)
            self.tp2_price = entry_price + (3.50 * self.sl_dist) if direction == "BUY" else entry_price - (3.50 * self.sl_dist)
            self.tp3_price = entry_price + (8.00 * self.sl_dist) if direction == "BUY" else entry_price - (8.00 * self.sl_dist)

        # State tracking
        self.status = "OPEN"
        self.stage = 0  # 0: Open, 1: Risk cut at +1.2R, 2: TP1 hit & BE Armor, 3: TP2 hit & +2R floor
        self.peak_r = 0.0
        self.exit_idx = None
        self.exit_time = None
        self.exit_price = 0.0
        self.exit_reason = None
        self.pnl_r = 0.0
        self.pnl_dollars = 0.0
        self.costs_paid = (self.spread + self.slippage) * self.position_size * contract_multiplier
        self.holding_bars = 0

    def step(self, bar: pd.Series, bar_idx: int) -> bool:
        """
        Advances trade across 15-minute bar. Returns True if closed.
        """
        self.holding_bars += 1
        b_high = float(bar['high'])
        b_low = float(bar['low'])
        b_close = float(bar['close'])
        b_time = bar['datetime']

        # Calculate current excursion
        if self.direction == "BUY":
            bar_mfe_r = (b_high - self.entry_price) / self.sl_dist
            sl_hit = (b_low <= self.current_sl)
            tp1_hit = (b_high >= self.tp1_price)
            tp2_hit = (b_high >= self.tp2_price)
            tp3_hit = (b_high >= self.tp3_price)
        else:
            bar_mfe_r = (self.entry_price - b_low) / self.sl_dist
            sl_hit = (b_high >= self.current_sl)
            tp1_hit = (b_low <= self.tp1_price)
            tp2_hit = (b_low <= self.tp2_price)
            tp3_hit = (b_low <= self.tp3_price)

        self.peak_r = max(self.peak_r, bar_mfe_r)

        # 1. Fixed SL/TP mode
        if self.drop_scale_out:
            if sl_hit:
                self._close(bar_idx, b_time, self.current_sl, "STOP_LOSS", -1.0)
                return True
            elif tp1_hit:
                self._close(bar_idx, b_time, self.tp1_price, "TAKE_PROFIT_1.5R", 1.50)
                return True
            return False

        # 2. Invariant 98 4-Phase Scale-Out & Breakeven Armor
        # Check Stop Loss execution
        if sl_hit:
            if self.stage == 0:
                exit_r = -1.0
                reason = "INITIAL_SL"
            elif self.stage == 1:
                # Phase 1: Risk was reduced to 0.5x ATR (~ -0.4R)
                exit_r = -0.40
                reason = "PHASE1_REDUCED_SL"
            elif self.stage == 2:
                # Phase 2: Breakeven Armor! 50% lot was banked at +1.8R, remaining 50% stopped at 0.00R (BE)
                exit_r = 0.90  # Net +0.90R realized profit!
                reason = "BREAKEVEN_ARMOR_HIT"
            else:
                # Phase 3: 50% at +1.8R, 30% at +3.5R, 20% stopped at +2.0R floor
                exit_r = 2.35  # Net +2.35R realized profit!
                reason = "TP2_LOCKED_FLOOR_HIT"

            self._close(bar_idx, b_time, self.current_sl, reason, exit_r)
            return True

        # Phase 1: At +1.2R, reduce risk by 60% (Move SL to Entry - 0.5x ATR)
        if self.stage == 0 and self.peak_r >= 1.20:
            self.stage = 1
            reduced_dist = 0.50 * self.atr_15m
            self.current_sl = self.entry_price - reduced_dist if self.direction == "BUY" else self.entry_price + reduced_dist

        # Phase 2: At +1.8R, Bank 50% TP1 & Shift SL to Breakeven Armor (Entry +/- 0.5x spread)
        if self.stage <= 1 and tp1_hit:
            self.stage = 2
            be_armor = self.entry_price + (0.5 * self.spread) if self.direction == "BUY" else self.entry_price - (0.5 * self.spread)
            self.current_sl = be_armor

        # Phase 3: At +3.5R, Bank 30% TP2 & Ratchet SL to +2.0R Locked Cash Floor
        if self.stage == 2 and tp2_hit:
            self.stage = 3
            locked_floor = self.entry_price + (2.0 * self.sl_dist) if self.direction == "BUY" else self.entry_price - (2.0 * self.sl_dist)
            self.current_sl = locked_floor

        # Phase 4: Moonshot Runner hit (+8.0R)
        if tp3_hit:
            # 50% at +1.8R + 30% at +3.5R + 20% at +8.0R = Net +3.55R
            self._close(bar_idx, b_time, self.tp3_price, "MOONSHOT_RUNNER_8R", 3.55)
            return True

        # Flash Shock Protective Early Harvest (Invariant 92 Pillar 5)
        # If peak R >= 1.8 and price drops >= 50% from peak
        cur_r = (b_close - self.entry_price) / self.sl_dist if self.direction == "BUY" else (self.entry_price - b_close) / self.sl_dist
        if self.peak_r >= 1.80 and cur_r <= (self.peak_r * 0.50) and cur_r > 0.0:
            exit_r = max(0.50, cur_r)
            self._close(bar_idx, b_time, b_close, "FLASH_SHOCK_HARVEST", exit_r)
            return True

        # Max holding duration on M15: 384 bars (~4 full days of intraday action)
        if self.holding_bars >= 384:
            self._close(bar_idx, b_time, b_close, "MAX_HOLDING_TIME", max(-1.0, cur_r))
            return True

        return False

    def _close(self, exit_idx: int, exit_time: pd.Timestamp, exit_price: float, reason: str, realized_r: float):
        self.status = "CLOSED"
        self.exit_idx = exit_idx
        self.exit_time = exit_time
        self.exit_price = exit_price
        self.exit_reason = reason
        self.pnl_r = realized_r
        gross = realized_r * self.initial_risk_dollars
        self.pnl_dollars = round(gross - self.costs_paid, 2)


def evaluate_m15_bar_signal(
    sym: str,
    spec: Dict[str, Any],
    row: pd.Series,
    prev_rows: pd.DataFrame,
    ablation_flags: Optional[Dict[str, bool]] = None
) -> Tuple[Optional[str], float, float, Dict[str, Any]]:
    """
    Evaluates institutional M15 entry signals using Citadel 360, SMC, S/R and Meta-Labeling.
    """
    if ablation_flags is None:
        ablation_flags = {}

    meta = {"veto_reason": None, "confluence": [], "raw_score": 50.0}

    curr_p = float(row['close'])
    spread = float(spec['spread'])
    atr = float(row['atr14'])
    adx = float(row['adx14'])
    rsi = float(row['rsi14'])
    range_pct = float(row['range_pct'])
    ema20 = float(row['ema20'])
    ema50 = float(row['ema50'])
    ema200 = float(row['ema200'])
    swing_high = float(row['swing_high_35'])
    swing_low = float(row['swing_low_35'])
    cvd = float(row['cvd'])

    # 1. HARD VETOES
    # Spread Drag Hurdle
    spread_drag = (spread / max(1e-4, atr)) * 100.0
    if not ablation_flags.get("drop_spread_hurdle", False) and spread_drag > 22.0:
        meta["veto_reason"] = f"SPREAD_DRAG_HIGH ({spread_drag:.1f}%)"
        return None, 0.0, 0.0, meta

    # Equilibrium Chop Zone (35% to 65% dealing range)
    if not ablation_flags.get("drop_chop_filter", False):
        if 35.0 <= range_pct <= 65.0:
            meta["veto_reason"] = f"EQUILIBRIUM_CHOP_ZONE ({range_pct:.1f}%)"
            return None, 0.0, 0.0, meta

    # Extreme Trap Zones
    deep_premium = (range_pct > 80.0)
    deep_discount = (range_pct < 20.0)

    # 2. SMC DETECTIONS on M15
    has_ssl_sweep = False
    has_bsl_sweep = False
    has_bullish_ob = False
    has_bearish_ob = False

    if len(prev_rows) >= 5 and not ablation_flags.get("drop_smc", False):
        for idx in range(-4, 0):
            bh = prev_rows['high'].iloc[idx]
            bl = prev_rows['low'].iloc[idx]
            bc = prev_rows['close'].iloc[idx]
            bo = prev_rows['open'].iloc[idx]

            # BSL Sweep: pierced swing high, closed below with upper wick
            if bh > swing_high and bc < swing_high:
                if (bh - max(bo, bc)) >= abs(bc - bo) * 0.50:
                    has_bsl_sweep = True

            # SSL Sweep: pierced swing low, closed above with lower wick
            if bl < swing_low and bc > swing_low:
                if (min(bo, bc) - bl) >= abs(bc - bo) * 0.50:
                    has_ssl_sweep = True

        # Order Blocks
        if len(prev_rows) >= 8:
            last_down = prev_rows[prev_rows['close'] < prev_rows['open']].iloc[-4:-1]
            if not last_down.empty and last_down['low'].min() <= curr_p <= last_down['high'].max() * 1.005:
                has_bullish_ob = True

            last_up = prev_rows[prev_rows['close'] > prev_rows['open']].iloc[-4:-1]
            if not last_up.empty and last_up['low'].min() * 0.995 <= curr_p <= last_up['high'].max():
                has_bearish_ob = True

    # 3. SCORING
    buy_score = 50.0
    sell_score = 50.0

    # BUY SIDE
    if range_pct < 35.0:
        buy_score += 15.0
    if has_ssl_sweep:
        buy_score += 25.0
        meta["confluence"].append("SSL_LIQUIDITY_SWEEP (+25)")
    if has_bullish_ob:
        buy_score += 18.0
        meta["confluence"].append("BULLISH_ORDER_BLOCK (+18)")
    if curr_p > ema20 > ema50:
        buy_score += 12.0
    if cvd > 0:
        buy_score += 10.0
    if curr_p > ema200:
        buy_score += 10.0
    else:
        buy_score -= 10.0

    # SELL SIDE
    if range_pct > 65.0:
        sell_score += 15.0
    if has_bsl_sweep:
        sell_score += 25.0
        meta["confluence"].append("BSL_LIQUIDITY_SWEEP (+25)")
    if has_bearish_ob:
        sell_score += 18.0
        meta["confluence"].append("BEARISH_ORDER_BLOCK (+18)")
    if curr_p < ema20 < ema50:
        sell_score += 12.0
    if cvd < 0:
        sell_score += 10.0
    if curr_p < ema200:
        sell_score += 10.0
    else:
        sell_score -= 10.0

    # Invariant 99: Capital.com Daily Market Report S/R
    try:
        import capital_market_report_engine
        cmre = capital_market_report_engine.CapitalMarketReportEngine
        rep = cmre.get_market_report_data(sym, current_price=curr_p, daily_atr=atr)
        if len(prev_rows) >= 3:
            h_wick = float(prev_rows['high'].iloc[-3:].max())
            l_wick = float(prev_rows['low'].iloc[-3:].min())
            sweep_chk = cmre.evaluate_broker_stop_cluster_sweep(sym, curr_p, h_wick, l_wick, spread)
            if sweep_chk.get("has_broker_sweep"):
                if sweep_chk.get("sweep_direction") == "BUY":
                    buy_score += 25.0
                    meta["confluence"].append("BROKER_SL_SWEEP_BULL (+25)")
                elif sweep_chk.get("sweep_direction") == "SELL":
                    sell_score += 25.0
                    meta["confluence"].append("BROKER_SL_SWEEP_BEAR (+25)")
    except Exception:
        pass

    # 4. CHOOSE DIRECTION & APPLY FILTERS
    chosen_dir = None
    raw_score = 50.0

    if buy_score >= 68.0 and buy_score > sell_score:
        # Invariant 94: Asset-Specific H4 Anchor (strict on Equities/Indices, bypassed on Commodities)
        is_commodity = (spec.get("type") == "COMMODITY")
        if not ablation_flags.get("drop_h4_anchor", False) and not is_commodity and curr_p < ema200:
            meta["veto_reason"] = "H4_TREND_ANCHOR_VETO"
            return None, 0.0, 0.0, meta

        if deep_premium:
            meta["veto_reason"] = "DEEP_PREMIUM_TRAP"
            return None, 0.0, 0.0, meta

        # Anti-Overbought Guard
        if rsi >= 70.0 and not (adx >= 32.0 and curr_p > ema20 > ema50):
            meta["veto_reason"] = f"RSI_OVERBOUGHT ({rsi:.1f})"
            return None, 0.0, 0.0, meta

        if adx < 22.0:
            meta["veto_reason"] = f"LOW_ADX_CHOP ({adx:.1f})"
            return None, 0.0, 0.0, meta

        chosen_dir = "BUY"
        raw_score = min(99.0, buy_score)

    elif sell_score >= 68.0 and sell_score > buy_score:
        is_commodity = (spec.get("type") == "COMMODITY")
        if not ablation_flags.get("drop_h4_anchor", False) and not is_commodity and curr_p > ema200:
            meta["veto_reason"] = "H4_TREND_ANCHOR_VETO"
            return None, 0.0, 0.0, meta

        if deep_discount:
            meta["veto_reason"] = "DEEP_DISCOUNT_TRAP"
            return None, 0.0, 0.0, meta

        # Anti-Oversold Guard (Invariant 16)
        if rsi <= 36.0 and not (adx >= 32.0 and curr_p < ema20 < ema50):
            meta["veto_reason"] = f"RSI_OVERSOLD ({rsi:.1f})"
            return None, 0.0, 0.0, meta

        if adx < 22.0:
            meta["veto_reason"] = f"LOW_ADX_CHOP ({adx:.1f})"
            return None, 0.0, 0.0, meta

        chosen_dir = "SELL"
        raw_score = min(99.0, sell_score)

    if chosen_dir is None:
        meta["veto_reason"] = "SCORE_BELOW_68"
        return None, 0.0, 0.0, meta

    # Probability estimation
    prob = min(0.85, max(0.50, 0.50 + (raw_score - 68.0) * 0.01))
    meta["raw_score"] = raw_score
    meta["calibrated_p"] = prob

    return chosen_dir, raw_score, prob, meta


def run_m15_backtest_simulation(
    assets_data: Dict[str, pd.DataFrame],
    initial_equity: float = 1000.0,
    base_risk_dollars: float = 10.0,
    compounding: bool = False,
    risk_pct: float = 0.015,
    ablation_flags: Optional[Dict[str, bool]] = None
) -> Tuple[List[M15Trade], pd.DataFrame, Dict[str, Any]]:
    """
    Executes chronological multi-asset simulation bar-by-bar across 15-minute bars.
    """
    if ablation_flags is None:
        ablation_flags = {}

    current_equity = initial_equity
    open_trades: Dict[str, M15Trade] = {}
    closed_trades: List[M15Trade] = []
    equity_curve: List[Dict[str, Any]] = []

    # Find common date/time index across assets
    all_times = sorted(list(set.union(*[set(df['datetime']) for df in assets_data.values()])))
    trade_id_counter = 1

    for idx, dt in enumerate(all_times):
        # Step open trades
        symbols_to_close = []
        for sym, trade in open_trades.items():
            df_sym = assets_data[sym]
            matching_rows = df_sym[df_sym['datetime'] == dt]
            if not matching_rows.empty:
                bar = matching_rows.iloc[0]
                is_closed = trade.step(bar, idx)
                if is_closed:
                    current_equity += trade.pnl_dollars
                    closed_trades.append(trade)
                    symbols_to_close.append(sym)

        for sym in symbols_to_close:
            del open_trades[sym]

        # Scan for new signals (Max 3 concurrent positions)
        if len(open_trades) < 3:
            for sym, spec in CAPITAL_M15_SPECS.items():
                if sym in open_trades:
                    continue  # Single-Asset Exposure Lock

                df_sym = assets_data.get(sym)
                if df_sym is None:
                    continue

                matching_idx = df_sym[df_sym['datetime'] == dt].index
                if matching_idx.empty:
                    continue

                b_idx = matching_idx[0]
                if b_idx < 35:
                    continue  # Warmup buffer

                row = df_sym.iloc[b_idx]
                prev_rows = df_sym.iloc[max(0, b_idx-35):b_idx]

                dir_sig, raw_s, prob, meta = evaluate_m15_bar_signal(sym, spec, row, prev_rows, ablation_flags)
                if dir_sig is not None:
                    curr_p = float(row['close'])
                    atr = float(row['atr14'])
                    spread = float(spec['spread'])
                    sl_mult = float(spec.get('atr_sl_mult', 2.20))
                    sl_dist = max(sl_mult * atr, spread * 3.5, curr_p * 0.0030)

                    sl_p = curr_p - sl_dist if dir_sig == "BUY" else curr_p + sl_dist

                    new_trade = M15Trade(
                        trade_id=trade_id_counter,
                        symbol=sym,
                        direction=dir_sig,
                        entry_idx=b_idx,
                        entry_time=dt,
                        entry_price=curr_p,
                        sl_price=sl_p,
                        atr_15m=atr,
                        spread=spread,
                        slippage=float(spec.get('slippage', 0.05)),
                        base_risk_dollars=base_risk_dollars,
                        contract_multiplier=float(spec.get('contract_multiplier', 1.0)),
                        min_deal_size=float(spec.get('min_deal_size', 0.01)),
                        compounding_equity=current_equity if compounding else None,
                        risk_pct=risk_pct,
                        drop_scale_out=ablation_flags.get("drop_scale_out", False)
                    )
                    if new_trade.risk_overrun:
                        continue
                    trade_id_counter += 1
                    open_trades[sym] = new_trade


                    if len(open_trades) >= 3:
                        break

        # Record equity snapshot
        unrealized = sum(
            ((float(assets_data[t.symbol][assets_data[t.symbol]['datetime'] == dt]['close'].iloc[0]) - t.entry_price) / t.sl_dist * t.initial_risk_dollars)
            if t.direction == "BUY" else
            ((t.entry_price - float(assets_data[t.symbol][assets_data[t.symbol]['datetime'] == dt]['close'].iloc[0])) / t.sl_dist * t.initial_risk_dollars)
            for t in open_trades.values()
            if not assets_data[t.symbol][assets_data[t.symbol]['datetime'] == dt].empty
        )
        equity_curve.append({
            "datetime": dt,
            "realized_equity": round(current_equity, 2),
            "total_equity": round(current_equity + unrealized, 2),
            "open_positions": len(open_trades)
        })

    df_equity = pd.DataFrame(equity_curve)

    # Performance calculation
    metrics = calculate_m15_metrics(closed_trades, df_equity, initial_equity)
    return closed_trades, df_equity, metrics


def calculate_m15_metrics(trades: List[M15Trade], df_equity: pd.DataFrame, initial_capital: float) -> Dict[str, Any]:
    """
    Computes rigorous performance metrics for M15 backtest and forwardtest.
    """
    n_trades = len(trades)
    if n_trades == 0:
        return {
            "total_trades": 0, "win_rate": 0.0, "net_profit": 0.0, "roi_pct": 0.0,
            "profit_factor": 0.0, "expectancy_r": 0.0, "max_drawdown_pct": 0.0,
            "sharpe_ratio": 0.0
        }

    wins = [t for t in trades if t.pnl_dollars > 0]
    losses = [t for t in trades if t.pnl_dollars <= 0]
    n_wins = len(wins)
    n_losses = len(losses)
    win_rate = (n_wins / n_trades) * 100.0

    gross_profit = sum(t.pnl_dollars for t in wins)
    gross_loss = abs(sum(t.pnl_dollars for t in losses))
    net_profit = sum(t.pnl_dollars for t in trades)
    profit_factor = (gross_profit / max(1e-4, gross_loss)) if gross_loss > 0 else 99.0

    avg_win_r = float(np.mean([t.pnl_r for t in wins])) if wins else 0.0
    avg_loss_r = abs(float(np.mean([t.pnl_r for t in losses]))) if losses else 1.0
    realized_rr = (avg_win_r / max(1e-4, avg_loss_r)) if avg_loss_r > 0 else avg_win_r
    expectancy_r = (win_rate / 100.0 * avg_win_r) - ((1.0 - win_rate / 100.0) * avg_loss_r)

    # Drawdown
    df_equity['peak'] = df_equity['total_equity'].cummax()
    df_equity['dd_pct'] = (df_equity['peak'] - df_equity['total_equity']) / df_equity['peak'] * 100.0
    max_dd_pct = float(df_equity['dd_pct'].max())
    max_dd_dollars = float((df_equity['peak'] - df_equity['total_equity']).max())

    # Sharpe ratio (hourly returns annualized)
    returns = df_equity['total_equity'].pct_change().dropna()
    if len(returns) > 1 and returns.std() > 0:
        sharpe = float((returns.mean() / returns.std()) * math.sqrt(252 * 26))  # 26 M15 bars per standard day
    else:
        sharpe = 0.0

    # Costs paid
    total_costs = sum(t.costs_paid for t in trades)

    # Wilson Score 95% Confidence Interval
    z = 1.96
    p_hat = n_wins / n_trades
    denom = 1 + (z**2 / n_trades)
    center = (p_hat + (z**2 / (2 * n_trades))) / denom
    margin = z * math.sqrt((p_hat * (1 - p_hat) / n_trades) + (z**2 / (4 * n_trades**2))) / denom
    ci_lower = round(max(0.0, (center - margin) * 100.0), 2)
    ci_upper = round(min(100.0, (center + margin) * 100.0), 2)

    return {
        "total_trades": n_trades,
        "n_wins": n_wins,
        "n_losses": n_losses,
        "win_rate": round(win_rate, 2),
        "ci_lower": ci_lower,
        "ci_upper": ci_upper,
        "avg_win_r": round(avg_win_r, 2),
        "avg_loss_r": round(avg_loss_r, 2),
        "realized_rr": round(realized_rr, 2),
        "expectancy_r": round(expectancy_r, 3),
        "gross_profit": round(gross_profit, 2),
        "gross_loss": round(gross_loss, 2),
        "net_profit": round(net_profit, 2),
        "roi_pct": round((net_profit / initial_capital) * 100.0, 2),
        "profit_factor": round(profit_factor, 2),
        "total_costs": round(total_costs, 2),
        "max_drawdown_pct": round(max_dd_pct, 2),
        "max_drawdown_dollars": round(max_dd_dollars, 2),
        "sharpe_ratio": round(sharpe, 2),
        "final_equity": round(initial_capital + net_profit, 2)
    }
