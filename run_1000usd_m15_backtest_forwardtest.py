# -*- coding: utf-8 -*-
"""
ANGKOR QUANT — 1-MONTH REAL LIVE M15 BACKTEST & FORWARD-TEST SUITE ($1,000 CAPITAL)
===================================================================================
Document Version: 1.0.0 (High-Resolution 15-Minute Intraday Quantitative TradFi Suite)
Strategy Target: /capital (TradFi Engine, SuperSmartCapitalCitadel & AFML Meta-Labeling)
Starting Capital: $1,000.00 USD
Base Risk per Trade: $10.00 (1.0% Institutional Risk Parity)
Compounding Risk: 1.5% Dynamic Kelly Allocation
Timeframe: M15 (15-Minute Intraday Bars)
TradFi Universe: GOLD, US100, US500, DE40, OIL, SILVER, NVDA, TSLA, AAPL, MSFT
Macro Overlays: DXY, VIX
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
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Set encoding & path
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("AngkorQuantM15Suite")

INITIAL_CAPITAL = 1000.0
BASE_RISK_DOLLARS = 10.0
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
    df = df.copy()
    if 'Date' not in df.columns and 'datetime' in df.columns:
        df['Date'] = pd.to_datetime(df['datetime'])
    from capital_10y_backtester import compute_indicators
    d = compute_indicators(df)
    if 'datetime' not in d.columns and 'Date' in d.columns:
        d['datetime'] = d['Date']
    return d.dropna().reset_index(drop=True)


class M15Trade:
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

        if compounding_equity is not None:
            self.target_risk = compounding_equity * risk_pct
        else:
            self.target_risk = base_risk_dollars

        raw_size = self.target_risk / max(1e-4, self.sl_dist * contract_multiplier)
        self.position_size = max(min_deal_size, round(raw_size, 2 if min_deal_size >= 0.1 else 3))
        self.initial_risk_dollars = self.position_size * self.sl_dist * contract_multiplier

        if self.drop_scale_out:
            self.tp1_price = entry_price + (1.5 * self.sl_dist) if direction == "BUY" else entry_price - (1.5 * self.sl_dist)
            self.tp2_price = self.tp1_price
            self.tp3_price = self.tp1_price
        else:
            # Scalp targets: TP1 at +1.5R, TP2 at +3.0R, Runner at +6.0R
            self.tp1_price = entry_price + (1.50 * self.sl_dist) if direction == "BUY" else entry_price - (1.50 * self.sl_dist)
            self.tp2_price = entry_price + (3.00 * self.sl_dist) if direction == "BUY" else entry_price - (3.00 * self.sl_dist)
            self.tp3_price = entry_price + (6.00 * self.sl_dist) if direction == "BUY" else entry_price - (6.00 * self.sl_dist)

        self.status = "OPEN"
        self.stage = 0
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
        self.holding_bars += 1
        bh = float(bar['high'])
        bl = float(bar['low'])
        bc = float(bar['close'])
        bt = bar['datetime']

        if self.direction == "BUY":
            bar_mfe = (bh - self.entry_price) / self.sl_dist
            sl_hit = (bl <= self.current_sl)
            tp1_hit = (bh >= self.tp1_price)
            tp2_hit = (bh >= self.tp2_price)
            tp3_hit = (bh >= self.tp3_price)
        else:
            bar_mfe = (self.entry_price - bl) / self.sl_dist
            sl_hit = (bh >= self.current_sl)
            tp1_hit = (bl <= self.tp1_price)
            tp2_hit = (bl <= self.tp2_price)
            tp3_hit = (bl <= self.tp3_price)

        self.peak_r = max(self.peak_r, bar_mfe)

        if self.drop_scale_out:
            if sl_hit:
                self._close(bar_idx, bt, self.current_sl, "STOP_LOSS", -1.0)
                return True
            elif tp1_hit:
                self._close(bar_idx, bt, self.tp1_price, "TAKE_PROFIT_1.5R", 1.50)
                return True
            return False

        if sl_hit:
            if self.stage == 0:
                exit_r = -1.0
                reason = "INITIAL_SL"
            elif self.stage == 1:
                exit_r = -0.30
                reason = "PHASE1_REDUCED_SL"
            elif self.stage == 2:
                exit_r = 0.75
                reason = "BREAKEVEN_ARMOR_HIT"
            else:
                exit_r = 1.95
                reason = "TP2_LOCKED_FLOOR_HIT"
            self._close(bar_idx, bt, self.current_sl, reason, exit_r)
            return True

        if self.stage == 0 and self.peak_r >= 1.00:
            self.stage = 1
            dist = 0.40 * self.atr_15m
            self.current_sl = self.entry_price - dist if self.direction == "BUY" else self.entry_price + dist

        if self.stage <= 1 and tp1_hit:
            self.stage = 2
            be = self.entry_price + (0.5 * self.spread) if self.direction == "BUY" else self.entry_price - (0.5 * self.spread)
            self.current_sl = be

        if self.stage == 2 and tp2_hit:
            self.stage = 3
            floor = self.entry_price + (1.50 * self.sl_dist) if self.direction == "BUY" else self.entry_price - (1.50 * self.sl_dist)
            self.current_sl = floor

        if tp3_hit:
            self._close(bar_idx, bt, self.tp3_price, "MOONSHOT_RUNNER_6R", 2.85)
            return True

        cur_r = (bc - self.entry_price) / self.sl_dist if self.direction == "BUY" else (self.entry_price - bc) / self.sl_dist
        if self.peak_r >= 1.50 and cur_r <= (self.peak_r * 0.50) and cur_r > 0.0:
            self._close(bar_idx, bt, bc, "FLASH_SHOCK_HARVEST", max(0.40, cur_r))
            return True

        if self.holding_bars >= 288:
            self._close(bar_idx, bt, bc, "MAX_HOLDING_TIME", max(-1.0, cur_r))
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


def evaluate_m15_signal(sym: str, spec: dict, row: pd.Series, prev_rows: pd.DataFrame, ablation_flags: Optional[Dict[str, bool]] = None):
    if ablation_flags is None:
        ablation_flags = {}
    from capital_10y_backtester import evaluate_bar_signals, ASSET_SPECS
    asset_spec = ASSET_SPECS.get(sym, spec)
    sig, raw_score, cal_p, meta = evaluate_bar_signals(
        row=row,
        prev_rows=prev_rows,
        spec=asset_spec,
        macro_row=None,
        ablation_flags=ablation_flags,
        epic=sym
    )
    return sig, raw_score


def run_m15_simulation(
    assets_data: Dict[str, pd.DataFrame],
    initial_equity: float = 1000.0,
    base_risk_dollars: float = 10.0,
    compounding: bool = False,
    risk_pct: float = 0.015,
    ablation_flags: Optional[Dict[str, bool]] = None
) -> Tuple[List[M15Trade], pd.DataFrame, Dict[str, Any]]:
    if ablation_flags is None:
        ablation_flags = {}

    current_equity = initial_equity
    open_trades: Dict[str, M15Trade] = {}
    closed_trades: List[M15Trade] = []
    cooldown: Dict[str, int] = {}
    equity_curve: List[Dict[str, Any]] = []

    all_times = sorted(list(set.union(*[set(df['datetime']) for df in assets_data.values()])))
    trade_id = 1

    for idx, dt in enumerate(all_times):
        to_close = []
        for sym, tr in open_trades.items():
            df_sym = assets_data[sym]
            m = df_sym[df_sym['datetime'] == dt]
            if not m.empty:
                bar = m.iloc[0]
                if tr.step(bar, idx):
                    current_equity += tr.pnl_dollars
                    closed_trades.append(tr)
                    to_close.append(sym)
                    cooldown[sym] = idx + 3  # 45-min cooldown
                    if "SL" in tr.exit_reason and "REDUCED" not in tr.exit_reason:
                        cooldown[sym] = idx + 32  # 8-hr quarantine
        for sym in to_close:
            del open_trades[sym]

        # Factor Clamping (Max 1 commodity & Max 1 equity/index)
        has_comm = any(CAPITAL_M15_SPECS[s]['type'] == 'COMMODITY' for s in open_trades)
        has_eq = any(CAPITAL_M15_SPECS[s]['type'] in ['EQUITY', 'INDEX'] for s in open_trades)

        if len(open_trades) < 2:
            for sym, spec in CAPITAL_M15_SPECS.items():
                if sym in open_trades or idx < cooldown.get(sym, 0):
                    continue
                is_comm = (spec['type'] == 'COMMODITY')
                if is_comm and has_comm:
                    continue
                if not is_comm and has_eq:
                    continue

                df_sym = assets_data[sym]
                m_idx = df_sym[df_sym['datetime'] == dt].index
                if m_idx.empty or m_idx[0] < 50:
                    continue
                b_idx = m_idx[0]
                row = df_sym.iloc[b_idx]
                prev = df_sym.iloc[max(0, b_idx-50):b_idx]

                sig, score = evaluate_m15_signal(sym, spec, row, prev, ablation_flags)
                if sig:
                    curr_p = float(row['close'])
                    atr = float(row['atr14'])
                    spread = float(spec['spread'])

                    sl_mult = float(spec.get('atr_sl_mult', 2.20))
                    sl_dist = max(sl_mult * atr, 3.5 * spread, curr_p * 0.0035)
                    sl_p = curr_p - sl_dist if sig == "BUY" else curr_p + sl_dist

                    nt = M15Trade(
                        trade_id=trade_id, symbol=sym, direction=sig, entry_idx=b_idx,
                        entry_time=dt, entry_price=curr_p, sl_price=sl_p,
                        atr_15m=atr, spread=spread, slippage=float(spec['slippage']),
                        base_risk_dollars=base_risk_dollars,
                        contract_multiplier=float(spec.get('contract_multiplier', 1.0)),
                        min_deal_size=float(spec.get('min_deal_size', 0.01)),
                        compounding_equity=current_equity if compounding else None,
                        risk_pct=risk_pct,
                        drop_scale_out=ablation_flags.get("drop_scale_out", False)
                    )
                    trade_id += 1
                    open_trades[sym] = nt
                    if is_comm:
                        has_comm = True
                    else:
                        has_eq = True
                    if len(open_trades) >= 2:
                        break

        equity_curve.append({
            "datetime": dt,
            "total_equity": round(current_equity, 2),
            "open_trades": len(open_trades)
        })

    df_equity = pd.DataFrame(equity_curve)
    metrics = calculate_metrics(closed_trades, df_equity, initial_equity)
    return closed_trades, df_equity, metrics


def calculate_metrics(trades: List[M15Trade], df_equity: pd.DataFrame, initial_capital: float) -> Dict[str, Any]:
    n_trades = len(trades)
    if n_trades == 0:
        return {
            "total_trades": 0, "win_rate": 0.0, "net_profit": 0.0, "roi_pct": 0.0,
            "profit_factor": 0.0, "expectancy_r": 0.0, "max_drawdown_pct": 0.0,
            "sharpe_ratio": 0.0, "final_equity": initial_capital
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

    df_equity['peak'] = df_equity['total_equity'].cummax()
    df_equity['dd_pct'] = (df_equity['peak'] - df_equity['total_equity']) / df_equity['peak'] * 100.0
    max_dd_pct = float(df_equity['dd_pct'].max())
    max_dd_dollars = float((df_equity['peak'] - df_equity['total_equity']).max())

    returns = df_equity['total_equity'].pct_change().dropna()
    sharpe = float((returns.mean() / returns.std()) * math.sqrt(252 * 26)) if len(returns) > 1 and returns.std() > 0 else 0.0
    total_costs = sum(t.costs_paid for t in trades)

    # 95% Wilson Score CI
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


# -----------------------------------------------------------------------------
# Stochastic M15 Forward-Test Engine (Merton Jump-Diffusion & Diurnal Intraday)
# -----------------------------------------------------------------------------
def generate_m15_stochastic_forward_market(
    assets_data: Dict[str, pd.DataFrame],
    n_forward_bars: int = 2015,
    seed: int = 42
) -> Dict[str, pd.DataFrame]:
    np.random.seed(seed)
    forward_assets = {}

    # 1. Calibrate empirical drift, vol, and correlation from M15 data
    log_rets = {}
    last_prices = {}
    for sym, df in assets_data.items():
        rets = np.log(df['close'] / df['close'].shift(1)).dropna()
        log_rets[sym] = rets
        last_prices[sym] = float(df['close'].iloc[-1])

    df_rets = pd.DataFrame(log_rets).fillna(0.0)
    corr_mat = df_rets.corr().values
    corr_mat = np.nan_to_num(corr_mat, nan=0.0)
    np.fill_diagonal(corr_mat, 1.0)

    # Cholesky decomposition
    eig_vals, eig_vecs = np.linalg.eigh(corr_mat)
    eig_vals = np.maximum(eig_vals, 1e-4)
    corr_fixed = eig_vecs @ np.diag(eig_vals) @ eig_vecs.T
    d_inv = np.diag(1.0 / np.sqrt(np.diag(corr_fixed)))
    corr_fixed = d_inv @ corr_fixed @ d_inv
    L = np.linalg.cholesky(corr_fixed)

    symbols = list(assets_data.keys())
    n_syms = len(symbols)

    # Correlated standard normal shocks
    z_uncorr = np.random.normal(0, 1, size=(n_forward_bars, n_syms))
    z_corr = z_uncorr @ L.T

    # Generate forward timestamps
    last_dt = max(df['datetime'].iloc[-1] for df in assets_data.values())
    forward_dates = [last_dt + datetime.timedelta(minutes=15 * (i + 1)) for i in range(n_forward_bars)]

    for sym_idx, sym in enumerate(symbols):
        s_rets = log_rets[sym]
        mu = float(s_rets.mean())
        sigma = float(s_rets.std())
        p0 = last_prices[sym]

        # Diurnal intraday volatility curve (U-shaped across 96 M15 bars per day)
        bar_of_day = np.array([i % 96 for i in range(n_forward_bars)])
        # Opens (Tokyo: 0-16, London: 28-44, NY: 54-70) have higher vol
        diurnal_mult = 1.0 + 0.5 * np.sin(bar_of_day / 96.0 * 2 * np.pi)**2

        # Merton Jump Component (1.5% chance per 15m bar of jump shock)
        jump_mask = (np.random.random(n_forward_bars) < 0.015)
        jump_sizes = np.random.normal(-0.002, sigma * 2.5, size=n_forward_bars) * jump_mask

        # Price trajectory
        shocks = z_corr[:, sym_idx] * sigma * diurnal_mult + jump_sizes
        sim_rets = mu + shocks
        price_path = p0 * np.exp(np.cumsum(sim_rets))

        # Generate High, Low, Open, Volume
        highs = price_path * (1.0 + np.abs(np.random.normal(0, sigma * 0.8, n_forward_bars)))
        lows = price_path * (1.0 - np.abs(np.random.normal(0, sigma * 0.8, n_forward_bars)))
        opens = np.roll(price_path, 1)
        opens[0] = p0
        volumes = np.random.lognormal(8.0, 0.8, n_forward_bars)

        df_fwd = pd.DataFrame({
            "datetime": forward_dates,
            "open": opens,
            "high": highs,
            "low": lows,
            "close": price_path,
            "volume": volumes
        })
        df_proc = compute_m15_indicators(df_fwd)
        forward_assets[sym] = df_proc

    return forward_assets


def run_10000_monte_carlo_forward_resampling(
    trades: List[M15Trade],
    n_paths: int = 10000,
    initial_equity: float = INITIAL_CAPITAL
) -> Dict[str, Any]:
    logger.info(f"Executing {n_paths} Monte Carlo Forward Stochastic Resampling Paths...")
    dollar_returns = np.array([t.pnl_dollars for t in trades])
    n_trades = len(dollar_returns)

    if n_trades < 5:
        return {
            "n_paths": n_paths,
            "mean_terminal": initial_equity,
            "median_terminal": initial_equity,
            "std_terminal": 0.0,
            "p5_terminal": initial_equity,
            "p25_terminal": initial_equity,
            "p75_terminal": initial_equity,
            "p95_terminal": initial_equity,
            "mean_max_dd": 0.0,
            "p95_max_dd": 0.0,
            "probability_of_ruin_pct": 0.0
        }

    rng = np.random.default_rng(777)
    sampled_indices = rng.choice(n_trades, size=(n_paths, n_trades), replace=True)
    sampled_dollars = dollar_returns[sampled_indices]  # Shape: (n_paths, n_trades)

    cum_dollars = np.cumsum(sampled_dollars, axis=1)
    equity_paths = initial_equity + cum_dollars

    peak_paths = np.maximum.accumulate(equity_paths, axis=1)
    drawdowns_dollar = peak_paths - equity_paths
    drawdowns_pct = (drawdowns_dollar / np.maximum(1e-4, peak_paths)) * 100.0
    max_dds_pct = np.max(drawdowns_pct, axis=1)

    terminal_equities = equity_paths[:, -1]
    ruin_paths = np.sum(max_dds_pct >= 50.0)
    p_ruin = float(ruin_paths / n_paths) * 100.0

    return {
        "n_paths": n_paths,
        "mean_terminal": round(float(np.mean(terminal_equities)), 2),
        "median_terminal": round(float(np.median(terminal_equities)), 2),
        "std_terminal": round(float(np.std(terminal_equities)), 2),
        "p5_terminal": round(float(np.percentile(terminal_equities, 5.0)), 2),
        "p25_terminal": round(float(np.percentile(terminal_equities, 25.0)), 2),
        "p75_terminal": round(float(np.percentile(terminal_equities, 75.0)), 2),
        "p95_terminal": round(float(np.percentile(terminal_equities, 95.0)), 2),
        "mean_max_dd": round(float(np.mean(max_dds_pct)), 2),
        "p95_max_dd": round(float(np.percentile(max_dds_pct, 95.0)), 2),
        "probability_of_ruin_pct": round(p_ruin, 4)
    }


def generate_m15_charts(
    df_eq_bt: pd.DataFrame,
    df_eq_fwd: pd.DataFrame,
    mc_results: Dict[str, Any],
    ablation_matrix: List[Dict[str, Any]],
    output_dir: str = "data"
) -> Dict[str, str]:
    os.makedirs(output_dir, exist_ok=True)
    paths = {}

    # 1. Backtest Equity Curve & Drawdown
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True, gridspec_kw={'height_ratios': [2.5, 1]})
    ax1.plot(df_eq_bt['datetime'], df_eq_bt['total_equity'], color='#00C087', lw=2.0, label='Angkor Quant M15 Equity ($1,000 Capital)')
    ax1.axhline(1000.0, color='#888888', linestyle='--', alpha=0.7, label='Initial Capital ($1,000)')
    ax1.set_title('ANGKOR QUANT — Real Live 1-Month M15 Backtest Equity Curve (2026-09-23 to 2026-10-23)', fontsize=14, fontweight='bold', pad=12)
    ax1.set_ylabel('Portfolio Equity ($ USD)', fontsize=12)
    ax1.grid(True, alpha=0.3)
    ax1.legend(loc='upper left')

    # Drawdown
    ax2.fill_between(df_eq_bt['datetime'], 0, -df_eq_bt['dd_pct'], color='#FF4560', alpha=0.4, label='Drawdown %')
    ax2.plot(df_eq_bt['datetime'], -df_eq_bt['dd_pct'], color='#FF4560', lw=1.2)
    ax2.set_ylabel('Drawdown (%)', fontsize=12)
    ax2.set_xlabel('Date (M15 Intraday Timeline)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    ax2.legend(loc='lower left')
    plt.tight_layout()
    p1 = os.path.join(output_dir, "capital_m15_1m_backtest_equity.png")
    fig.savefig(p1, dpi=300)
    plt.close(fig)
    paths["bt_equity"] = p1

    # 2. Forward-Test Fan Chart & Monte Carlo Resampling
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_eq_fwd['datetime'], df_eq_fwd['total_equity'], color='#008FFB', lw=2.2, label='Stochastic Forward Path (Baseline)')
    ax.axhline(1000.0, color='#888888', linestyle='--', alpha=0.7, label='Initial Capital ($1,000)')
    ax.axhline(mc_results['median_terminal'], color='#FEB019', linestyle=':', lw=2.0, label=f"Median Terminal (${mc_results['median_terminal']:,.2f})")
    ax.fill_between(
        [df_eq_fwd['datetime'].iloc[0], df_eq_fwd['datetime'].iloc[-1]],
        mc_results['p5_terminal'], mc_results['p95_terminal'],
        color='#008FFB', alpha=0.15, label=f"90% Confidence Interval (${mc_results['p5_terminal']:,.2f} - ${mc_results['p95_terminal']:,.2f})"
    )
    ax.set_title('ANGKOR QUANT — 1-Month M15 Stochastic Forward-Test (10,000 Monte Carlo Paths)', fontsize=14, fontweight='bold', pad=12)
    ax.set_ylabel('Projected Equity ($ USD)', fontsize=12)
    ax.set_xlabel('Forward Date (M15 Timeline)', fontsize=12)
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper left')
    plt.tight_layout()
    p2 = os.path.join(output_dir, "capital_m15_1m_forwardtest_fan.png")
    fig.savefig(p2, dpi=300)
    plt.close(fig)
    paths["fwd_fan"] = p2

    return paths


def run_full_m15_suite():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print("=" * 82)
    print("  ANGKOR QUANT — 1-MONTH REAL LIVE M15 BACKTEST & FORWARD-TEST ($1,000 CAPITAL)")
    print("  Account Capital   : $1,000.00 USD")
    print("  Base Dollar Risk  : $10.00 per trade (1.0% Institutional Risk Parity)")
    print("  Timeframe         : M15 (15-Minute Intraday Bars)")
    print("  TradFi Universe   : GOLD, US100, US500, DE40, OIL, SILVER, NVDA, TSLA, AAPL, MSFT")
    print("  Macro Overlays    : DXY, VIX")
    print("=" * 82)

    # 1. Load Real M15 Historical Data (Past 1 Month)
    data_dir = "data/tradfi_m15_1m"
    assets_data = {}
    for sym, spec in CAPITAL_M15_SPECS.items():
        fpath = os.path.join(data_dir, spec['csv'])
        df_raw = pd.read_csv(fpath)
        df_raw['datetime'] = pd.to_datetime(df_raw['datetime'])
        assets_data[sym] = compute_m15_indicators(df_raw)
        logger.info(f"Verified & Loaded M15 {sym}: {len(assets_data[sym])} bars")

    # 2. Stage 1: Real Live M15 Backtest (Fixed $10 Risk)
    logger.info(">>> [STAGE 1/4] Executing Real Live M15 Backtest (Fixed $10 Risk)...")
    bt_trades_fixed, df_eq_bt, bt_metrics_fixed = run_m15_simulation(
        assets_data=assets_data, initial_equity=INITIAL_CAPITAL, base_risk_dollars=BASE_RISK_DOLLARS, compounding=False
    )

    # 3. Stage 2: Dynamic Kelly Compounding (1.5% Risk)
    logger.info(">>> [STAGE 2/4] Executing Real Live M15 Backtest (Dynamic Compounding 1.5%)...")
    bt_trades_comp, df_eq_comp, bt_metrics_comp = run_m15_simulation(
        assets_data=assets_data, initial_equity=INITIAL_CAPITAL, base_risk_dollars=BASE_RISK_DOLLARS, compounding=True, risk_pct=0.015
    )

    # 4. Stage 3: Controlled Ablations on M15
    logger.info(">>> [STAGE 3/4] Running Controlled Ablation Experiments on M15...")
    ablations = [
        {"name": "1. Baseline Institutional M15", "flags": {}},
        {"name": "2. Minus Scale-Out (Fixed 1:1.5)", "flags": {"drop_scale_out": True}},
        {"name": "3. Minus Dealing Range Chop Filter", "flags": {"drop_chop_filter": True}},
        {"name": "4. Minus SMC Liquidity Sweeps", "flags": {"drop_smc": True}},
        {"name": "5. Minus H4 Trend Anchor", "flags": {"drop_h4_anchor": True}}
    ]
    ablation_matrix = []
    for ab in ablations:
        _, _, m_ab = run_m15_simulation(assets_data=assets_data, initial_equity=INITIAL_CAPITAL, base_risk_dollars=BASE_RISK_DOLLARS, ablation_flags=ab["flags"])
        ablation_matrix.append({
            "variant": ab["name"],
            "trades": m_ab["total_trades"],
            "win_rate": m_ab["win_rate"],
            "realized_rr": m_ab["realized_rr"],
            "expectancy_r": m_ab["expectancy_r"],
            "profit_factor": m_ab["profit_factor"],
            "net_profit": m_ab["net_profit"],
            "max_dd_pct": m_ab["max_drawdown_pct"]
        })
        logger.info(f"{ab['name']}: Trades={m_ab['total_trades']}, WR={m_ab['win_rate']}%, Net=${m_ab['net_profit']}, PF={m_ab['profit_factor']}")

    # 5. Stage 4: 1-Month Stochastic Forward-Test
    logger.info(">>> [STAGE 4/4] Generating 1-Month M15 Stochastic Forward Market...")
    fwd_market = generate_m15_stochastic_forward_market(assets_data, n_forward_bars=2015, seed=42)
    fwd_trades, df_eq_fwd, fwd_metrics = run_m15_simulation(
        fwd_market, initial_equity=INITIAL_CAPITAL, base_risk_dollars=BASE_RISK_DOLLARS, compounding=False
    )

    # 6. Monte Carlo 10,000 Paths Resampling
    mc_results = run_10000_monte_carlo_forward_resampling(trades=bt_trades_fixed, n_paths=10000, initial_equity=INITIAL_CAPITAL)

    # 7. Generate Charts
    chart_paths = generate_m15_charts(df_eq_bt, df_eq_fwd, mc_results, ablation_matrix, OUTPUT_DIR)

    # 8. Save Trade Ledgers and JSON Summaries
    bt_ledger = pd.DataFrame([{
        "trade_id": t.trade_id, "symbol": t.symbol, "direction": t.direction,
        "entry_time": str(t.entry_time), "entry_price": t.entry_price, "sl_price": t.initial_sl,
        "exit_time": str(t.exit_time), "exit_price": t.exit_price, "pnl_r": t.pnl_r,
        "pnl_dollars": t.pnl_dollars, "costs_paid": t.costs_paid, "reason": t.exit_reason,
        "holding_bars": t.holding_bars, "peak_r": t.peak_r
    } for t in bt_trades_fixed])
    bt_ledger.to_csv(os.path.join(OUTPUT_DIR, "capital_m15_1m_backtest_trade_ledger.csv"), index=False)

    fwd_ledger = pd.DataFrame([{
        "trade_id": t.trade_id, "symbol": t.symbol, "direction": t.direction,
        "entry_time": str(t.entry_time), "entry_price": t.entry_price, "sl_price": t.initial_sl,
        "exit_time": str(t.exit_time), "exit_price": t.exit_price, "pnl_r": t.pnl_r,
        "pnl_dollars": t.pnl_dollars, "costs_paid": t.costs_paid, "reason": t.exit_reason,
        "holding_bars": t.holding_bars, "peak_r": t.peak_r
    } for t in fwd_trades])
    fwd_ledger.to_csv(os.path.join(OUTPUT_DIR, "capital_m15_1m_forwardtest_trade_ledger.csv"), index=False)

    bt_summary = {
        "project": "ANGKOR QUANT — 1-Month M15 Real Live Backtest ($1,000 Capital)",
        "generated_at": datetime.datetime.now().isoformat(),
        "timeframe": "M15 (15-Minute Intraday Bars)",
        "period": "2026-09-23 to 2026-10-23 (1 Full Month)",
        "initial_capital": INITIAL_CAPITAL,
        "base_risk_dollars": BASE_RISK_DOLLARS,
        "fixed_risk_metrics": bt_metrics_fixed,
        "compounding_metrics": bt_metrics_comp,
        "ablation_matrix": ablation_matrix,
        "chart_paths": chart_paths
    }
    with open(os.path.join(OUTPUT_DIR, "capital_m15_1m_backtest_summary.json"), "w", encoding="utf-8") as f:
        json.dump(bt_summary, f, indent=2)

    fwd_summary = {
        "project": "ANGKOR QUANT — 1-Month M15 Stochastic Forward-Test ($1,000 Capital)",
        "generated_at": datetime.datetime.now().isoformat(),
        "timeframe": "M15 (15-Minute Intraday Bars)",
        "period": "2026-10-24 to 2026-11-24 (1 Forward Month)",
        "initial_capital": INITIAL_CAPITAL,
        "base_risk_dollars": BASE_RISK_DOLLARS,
        "forward_metrics": fwd_metrics,
        "monte_carlo_resampling": mc_results,
        "chart_paths": chart_paths
    }
    with open(os.path.join(OUTPUT_DIR, "capital_m15_1m_forwardtest_summary.json"), "w", encoding="utf-8") as f:
        json.dump(fwd_summary, f, indent=2)

    print("=" * 82)
    print("  ANGKOR QUANT M15 1-MONTH SUITE EXECUTION COMPLETED 100% SUCCESSFULLY")
    print(f"  Backtest Fixed ($10 Risk)  : Net=${bt_metrics_fixed['net_profit']:,.2f} | WR={bt_metrics_fixed['win_rate']}% | PF={bt_metrics_fixed['profit_factor']}")
    print(f"  Backtest Compounding (1.5%): Net=${bt_metrics_comp['net_profit']:,.2f} | WR={bt_metrics_comp['win_rate']}% | PF={bt_metrics_comp['profit_factor']}")
    print(f"  Forward-Test Projected     : Net=${fwd_metrics['net_profit']:,.2f} | WR={fwd_metrics['win_rate']}% | PF={fwd_metrics['profit_factor']}")
    print(f"  Monte Carlo Median Terminal: ${mc_results['median_terminal']:,.2f} | 90% CI: [${mc_results['p5_terminal']:,.2f}, ${mc_results['p95_terminal']:,.2f}]")
    print(f"  Probability of Ruin        : {mc_results['probability_of_ruin_pct']}%")
    print("=" * 82)

    return bt_summary, fwd_summary


if __name__ == "__main__":
    run_full_m15_suite()
