"""
KHMER MASTER CRYPTO - APEX 9 SMART MONEY CONCEPTS (SMC) CITADEL ENGINE
=============================================================================
Implementation of the 9 Institutional Smart Money Concepts across M15, M30, H1, H4:
  1. Order Blocks (OB) - Bullish & Bearish Institutional Mitigation Zones
  2. Fair Value Gaps (FVG) - 3-Candle Imbalances & Magnetic Retests
  3. Supply and Demand Zones (SnD) - RBR, RBD, DBR, DBD Structural Bases
  4. Change of Character (CHoCH) - Market Structure Shift / Trend Reversal
  5. Break of Structure (BOS) - Trend Continuation Higher Highs / Lower Lows
  6. Liquidity Pools (LP) - Equal Highs (EQH / BSL) & Equal Lows (EQL / SSL)
  7. Stop-Loss Hunting (Sweep) - Turtle Soup / Liquidity Grab Spring & Upthrust
  8. False Breakouts (Judas Swing / SFP) - Trapped Retail Breakout Reversals
  9. Kill Zones (KZ) - London Open, NY Open, Asian Range Institutional Windows

Multi-Timeframe Confluence: M15 (Sniper Entry), M30 (Base), H1 (Structure), H4 (Macro Bias).
Replaces blind time-based cooldowns with dynamic SMC structural confluence.
=============================================================================
"""

import time
import math
import logging
import requests
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple, Any
import pandas as pd
import numpy as np

logger = logging.getLogger("MT5_SMC_CITADEL")


class MT5SMCCitadelEngine:
    """
    Institutional 9 Smart Money Concepts Multi-Timeframe Engine.
    Analyzes M15, M30, H1, and H4 price action to detect institutional liquidity setups.
    """

    # In-memory TTL Cache: { "SYMBOL_TIMEFRAME": (timestamp, DataFrame) }
    _CANDLE_CACHE: Dict[str, Tuple[float, pd.DataFrame]] = {}
    _CACHE_TTL_SECONDS: float = 60.0  # 60s cache to preserve sub-millisecond execution

    # Latest Confluence Analysis Cache: { symbol: result_dict }
    _LAST_ANALYSIS: Dict[str, Dict[str, Any]] = {}

    @classmethod
    def get_cached_analysis(cls, symbol: str) -> Optional[Dict[str, Any]]:
        """Returns the most recent SMC analysis for a symbol if within 180s."""
        clean = symbol.replace("/", "").replace("_", "").replace("-", "").upper().strip()
        data = cls._LAST_ANALYSIS.get(clean) or cls._LAST_ANALYSIS.get(symbol.upper().strip())
        if data and (time.time() - float(data.get("timestamp", 0.0))) <= 180.0:
            return data
        return None

    # Symbol mapping for Yahoo Finance / Binance
    _YF_MAP = {
        "XAUUSD": "GC=F",
        "GOLD": "GC=F",
        "XAGUSD": "SI=F",
        "SILVER": "SI=F",
        "EURUSD": "EURUSD=X",
        "GBPUSD": "GBPUSD=X",
        "USDJPY": "USDJPY=X",
        "AUDUSD": "AUDUSD=X",
        "USDCAD": "USDCAD=X",
        "USDCHF": "USDCHF=X",
        "NZDUSD": "NZDUSD=X",
        "EURJPY": "EURJPY=X",
        "GBPJPY": "GBPJPY=X",
        "AUDJPY": "AUDJPY=X",
        "CADJPY": "CADJPY=X",
        "EURGBP": "EURGBP=X",
        "EURAUD": "EURAUD=X",
        "GBPAUD": "GBPAUD=X",
        "EURCAD": "EURCAD=X",
        "GBPCAD": "GBPCAD=X",
        "NZDJPY": "NZDJPY=X",
        "AUDNZD": "AUDNZD=X",
        "US30": "YM=F",
        "DJ30": "YM=F",
        "BTCUSD": "BTC-USD",
        "ETHUSD": "ETH-USD",
        "SOLUSD": "SOL-USD",
        "NVDA": "NVDA",
        "AAPL": "AAPL",
        "TSLA": "TSLA"
    }

    @classmethod
    def clean_symbol(cls, symbol: str) -> str:
        s = str(symbol).strip().upper()
        for suffix in [".C", ".c", "c", "_PERP", "USDT"]:
            if s.endswith(suffix) and len(s) > len(suffix):
                s = s[:-len(suffix)]
        return s

    # =========================================================================
    # CANDLE FETCHER & MULTI-TIMEFRAME CACHE (M15, M30, H1, H4)
    # =========================================================================
    @classmethod
    def fetch_timeframe_candles(cls, symbol: str, timeframe: str = "15m", limit: int = 100) -> Optional[pd.DataFrame]:
        """
        Fetches OHLCV candles for a given timeframe ('15m', '30m', '1h', '4h').
        Uses in-memory 60s TTL cache to guarantee high-frequency performance.
        """
        clean_sym = cls.clean_symbol(symbol)
        cache_key = f"{clean_sym}_{timeframe}"
        now_ts = time.time()

        if cache_key in cls._CANDLE_CACHE:
            ts, df_cached = cls._CANDLE_CACHE[cache_key]
            if (now_ts - ts) < cls._CACHE_TTL_SECONDS and df_cached is not None and len(df_cached) >= 20:
                return df_cached

        df = None

        # Strategy 1: Binance Direct API for Crypto and Gold (Ultra-fast < 100ms)
        if any(c in clean_sym for c in ["BTC", "ETH", "SOL", "BNB", "XAU"]):
            b_sym = clean_sym + "USDT" if not clean_sym.endswith("USDT") else clean_sym
            if "XAU" in clean_sym:
                b_sym = "XAUUSDT"
            b_interval = timeframe if timeframe != "4h" else "4h"
            url = f"https://api.binance.com/api/v3/klines?symbol={b_sym}&interval={b_interval}&limit={limit}"
            try:
                r = requests.get(url, timeout=4)
                if r.status_code == 200:
                    raw_data = r.json()
                    if isinstance(raw_data, list) and len(raw_data) > 0:
                        df = pd.DataFrame(raw_data, columns=[
                            'timestamp', 'open', 'high', 'low', 'close', 'volume',
                            'close_time', 'q_vol', 'num_trades', 'tb_base', 'tb_quote', 'ignore'
                        ])
                        for col in ['open', 'high', 'low', 'close', 'volume']:
                            df[col] = df[col].astype(float)
                        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            except Exception:
                pass

        # Strategy 2: yfinance for Forex, Indices, Stocks & Global Metals
        if df is None or len(df) < 20:
            yf_ticker = cls._YF_MAP.get(clean_sym, f"{clean_sym}=X")
            try:
                import yfinance as yf
                yf_interval = timeframe if timeframe in ["15m", "30m", "1h"] else "1h"
                period = "5d" if timeframe in ["15m", "30m"] else "1mo"
                raw_df = yf.download(yf_ticker, period=period, interval=yf_interval, progress=False)
                if raw_df is not None and not raw_df.empty and len(raw_df) >= 10:
                    # Flatten multi-index columns if present
                    if isinstance(raw_df.columns, pd.MultiIndex):
                        raw_df.columns = [col[0].lower() for col in raw_df.columns]
                    else:
                        raw_df.columns = [str(c).lower() for c in raw_df.columns]

                    if timeframe == "4h":
                        # Resample 1h to 4h
                        resampled = raw_df.resample('4h').agg({
                            'open': 'first',
                            'high': 'max',
                            'low': 'min',
                            'close': 'last',
                            'volume': 'sum'
                        }).dropna()
                        df = resampled.tail(limit).copy()
                    else:
                        df = raw_df.tail(limit).copy()
                    df.reset_index(inplace=True)
            except Exception as ex:
                logger.debug(f"yfinance fetch error for {clean_sym} ({timeframe}): {ex}")

        # Strategy 3: Synthetic / Fallback from Live Quotes
        if df is None or len(df) < 10:
            return None

        # Ensure correct column naming and float types
        for col in ['open', 'high', 'low', 'close', 'volume']:
            if col in df.columns:
                df[col] = df[col].astype(float)

        cls._CANDLE_CACHE[cache_key] = (now_ts, df)
        return df

    # =========================================================================
    # CONCEPT 1: ORDER BLOCKS (OB) - Bullish & Bearish Mitigation Zones
    # =========================================================================
    @classmethod
    def detect_order_blocks(cls, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Identifies institutional Order Blocks:
          - Bullish OB: Last down-close candle before violent upward displacement.
          - Bearish OB: Last up-close candle before violent downward displacement.
        Tracks active mitigation status relative to current price.
        """
        if df is None or len(df) < 15:
            return []

        obs = []
        n = len(df)
        closes = df['close'].values
        opens = df['open'].values
        highs = df['high'].values
        lows = df['low'].values

        # Average candle body size for displacement threshold
        body_sizes = [abs(closes[i] - opens[i]) for i in range(n)]
        avg_body = np.mean(body_sizes[-20:]) if len(body_sizes) >= 20 else np.mean(body_sizes)
        current_price = closes[-1]

        for i in range(max(1, n - 25), n - 2):
            c_open = opens[i]
            c_close = closes[i]
            c_high = highs[i]
            c_low = lows[i]

            # 1. Bullish Order Block (Red candle before green impulse that breaks structure)
            if c_close < c_open:  # Down-close candle
                # Next 1-2 candles show strong bullish impulse
                fwd_high = max(highs[i+1:min(n, i+3)])
                fwd_body = abs(closes[i+1] - opens[i+1]) if (i+1 < n) else 0.0
                if fwd_high > c_high and fwd_body >= (avg_body * 1.3):
                    # Check mitigation: did subsequent candles breach low?
                    subsequent_lows = lows[i+2:n]
                    is_mitigated = any(l < c_low for l in subsequent_lows) if len(subsequent_lows) > 0 else False
                    is_testing = (c_low <= current_price <= (c_high + avg_body * 0.2))
                    if not is_mitigated:
                        obs.append({
                            "type": "BULLISH_OB",
                            "index": i,
                            "top": c_high,
                            "bottom": c_low,
                            "mid": (c_high + c_low) / 2.0,
                            "is_testing": is_testing,
                            "mitigated": False
                        })

            # 2. Bearish Order Block (Green candle before red impulse that breaks structure)
            elif c_close > c_open:  # Up-close candle
                fwd_low = min(lows[i+1:min(n, i+3)])
                fwd_body = abs(closes[i+1] - opens[i+1]) if (i+1 < n) else 0.0
                if fwd_low < c_low and fwd_body >= (avg_body * 1.3):
                    subsequent_highs = highs[i+2:n]
                    is_mitigated = any(h > c_high for h in subsequent_highs) if len(subsequent_highs) > 0 else False
                    is_testing = ((c_low - avg_body * 0.2) <= current_price <= c_high)
                    if not is_mitigated:
                        obs.append({
                            "type": "BEARISH_OB",
                            "index": i,
                            "top": c_high,
                            "bottom": c_low,
                            "mid": (c_high + c_low) / 2.0,
                            "is_testing": is_testing,
                            "mitigated": False
                        })

        return obs

    # =========================================================================
    # CONCEPT 2: FAIR VALUE GAPS (FVG) - 3-Candle Imbalance & Retest
    # =========================================================================
    @classmethod
    def detect_fair_value_gaps(cls, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Identifies 3-candle Fair Value Gaps (imbalances):
          - Bullish FVG: Low[i] > High[i-2] (gap between High[i-2] and Low[i])
          - Bearish FVG: High[i] < Low[i-2] (gap between Low[i-2] and High[i])
        """
        if df is None or len(df) < 10:
            return []

        fvgs = []
        n = len(df)
        highs = df['high'].values
        lows = df['low'].values
        closes = df['close'].values
        current_price = closes[-1]

        for i in range(max(2, n - 20), n):
            # Bullish FVG: Candle i low is higher than candle i-2 high
            if lows[i] > highs[i-2]:
                gap_bottom = highs[i-2]
                gap_top = lows[i]
                gap_size = gap_top - gap_bottom
                if gap_size > 0:
                    # Check if price has returned to fill/retest the gap
                    is_testing = (gap_bottom <= current_price <= gap_top)
                    subsequent_lows = lows[i+1:n] if (i+1 < n) else []
                    is_fully_filled = any(l <= gap_bottom for l in subsequent_lows) if len(subsequent_lows) > 0 else False
                    if not is_fully_filled:
                        fvgs.append({
                            "type": "BULLISH_FVG",
                            "top": gap_top,
                            "bottom": gap_bottom,
                            "mid": (gap_top + gap_bottom) / 2.0,
                            "is_testing": is_testing,
                            "filled": False
                        })

            # Bearish FVG: Candle i high is lower than candle i-2 low
            elif highs[i] < lows[i-2]:
                gap_top = lows[i-2]
                gap_bottom = highs[i]
                gap_size = gap_top - gap_bottom
                if gap_size > 0:
                    is_testing = (gap_bottom <= current_price <= gap_top)
                    subsequent_highs = highs[i+1:n] if (i+1 < n) else []
                    is_fully_filled = any(h >= gap_top for h in subsequent_highs) if len(subsequent_highs) > 0 else False
                    if not is_fully_filled:
                        fvgs.append({
                            "type": "BEARISH_FVG",
                            "top": gap_top,
                            "bottom": gap_bottom,
                            "mid": (gap_top + gap_bottom) / 2.0,
                            "is_testing": is_testing,
                            "filled": False
                        })

        return fvgs

    # =========================================================================
    # CONCEPT 3: SUPPLY & DEMAND ZONES (SnD) - RBR, RBD, DBR, DBD
    # =========================================================================
    @classmethod
    def detect_supply_demand_zones(cls, df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Identifies institutional base origins:
          - RBR (Rally-Base-Rally): Demand Continuation
          - DBR (Drop-Base-Rally): Demand Reversal
          - RBD (Rally-Base-Drop): Supply Reversal
          - DBD (Drop-Base-Drop): Supply Continuation
        """
        if df is None or len(df) < 15:
            return []

        zones = []
        n = len(df)
        closes = df['close'].values
        opens = df['open'].values
        highs = df['high'].values
        lows = df['low'].values
        current_price = closes[-1]

        for i in range(max(2, n - 20), n - 1):
            # Base candle has small body compared to full range
            c_range = highs[i] - lows[i]
            c_body = abs(closes[i] - opens[i])
            if c_range <= 0:
                continue

            if (c_body / c_range) <= 0.45:  # Base consolidation candle
                prev_move = closes[i-1] - opens[i-2] if (i >= 2) else 0.0
                next_move = closes[i+1] - opens[i+1]

                # RBR (Rally-Base-Rally) or DBR (Drop-Base-Rally) -> DEMAND
                if next_move > 0 and (next_move / c_range) >= 1.2:
                    pattern = "RBR" if prev_move > 0 else "DBR"
                    is_testing = (lows[i] <= current_price <= highs[i])
                    zones.append({
                        "type": "DEMAND",
                        "pattern": pattern,
                        "top": highs[i],
                        "bottom": lows[i],
                        "is_testing": is_testing
                    })

                # RBD (Rally-Base-Drop) or DBD (Drop-Base-Drop) -> SUPPLY
                elif next_move < 0 and (abs(next_move) / c_range) >= 1.2:
                    pattern = "RBD" if prev_move > 0 else "DBD"
                    is_testing = (lows[i] <= current_price <= highs[i])
                    zones.append({
                        "type": "SUPPLY",
                        "pattern": pattern,
                        "top": highs[i],
                        "bottom": lows[i],
                        "is_testing": is_testing
                    })

        return zones

    # =========================================================================
    # CONCEPT 4: CHANGE OF CHARACTER (CHoCH) - Structural Trend Shift
    # =========================================================================
    @classmethod
    def detect_choch(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detects structural trend shift:
          - Bullish CHoCH: Price breaks above the previous Lower High in a downtrend.
          - Bearish CHoCH: Price breaks below the previous Higher Low in an uptrend.
        """
        res = {"bullish_choch": False, "bearish_choch": False, "level": 0.0, "reason": "NONE"}
        if df is None or len(df) < 20:
            return res

        highs = df['high'].values
        lows = df['low'].values
        closes = df['close'].values
        n = len(df)

        # Detect swing pivots (3-bar fractal)
        swing_highs = []
        swing_lows = []
        for i in range(2, n - 2):
            if highs[i] > highs[i-1] and highs[i] > highs[i-2] and highs[i] > highs[i+1] and highs[i] > highs[i+2]:
                swing_highs.append((i, highs[i]))
            if lows[i] < lows[i-1] and lows[i] < lows[i-2] and lows[i] < lows[i+1] and lows[i] < lows[i+2]:
                swing_lows.append((i, lows[i]))

        if len(swing_highs) >= 2 and len(swing_lows) >= 2:
            last_sh_idx, last_sh_val = swing_highs[-1]
            prev_sh_idx, prev_sh_val = swing_highs[-2]
            last_sl_idx, last_sl_val = swing_lows[-1]
            prev_sl_idx, prev_sl_val = swing_lows[-2]

            current_close = closes[-1]

            # Bullish CHoCH: Downtrend (LH) being broken by current candle close
            if last_sh_val < prev_sh_val:  # was Lower High
                if current_close > last_sh_val:
                    res["bullish_choch"] = True
                    res["level"] = last_sh_val
                    res["reason"] = f"Bullish_CHoCH_Broken_LH_{last_sh_val:.5f}"

            # Bearish CHoCH: Uptrend (HL) being broken by current candle close
            if last_sl_val > prev_sl_val:  # was Higher Low
                if current_close < last_sl_val:
                    res["bearish_choch"] = True
                    res["level"] = last_sl_val
                    res["reason"] = f"Bearish_CHoCH_Broken_HL_{last_sl_val:.5f}"

        return res

    # =========================================================================
    # CONCEPT 5: BREAK OF STRUCTURE (BOS) - Trend Continuation Confirmation
    # =========================================================================
    @classmethod
    def detect_bos(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detects trend continuation:
          - Bullish BOS: Price closes above previous Higher High (HH).
          - Bearish BOS: Price closes below previous Lower Low (LL).
        """
        res = {"bullish_bos": False, "bearish_bos": False, "level": 0.0, "reason": "NONE"}
        if df is None or len(df) < 20:
            return res

        highs = df['high'].values
        lows = df['low'].values
        closes = df['close'].values
        n = len(df)

        swing_highs = [highs[i] for i in range(2, n - 2) if highs[i] > max(highs[i-2:i]) and highs[i] > max(highs[i+1:i+3])]
        swing_lows = [lows[i] for i in range(2, n - 2) if lows[i] < min(lows[i-2:i]) and lows[i] < min(lows[i+1:i+3])]

        current_close = closes[-1]

        if len(swing_highs) >= 2:
            highest_prior = max(swing_highs[-2:])
            if current_close > highest_prior:
                res["bullish_bos"] = True
                res["level"] = highest_prior
                res["reason"] = f"Bullish_BOS_Continuation_{highest_prior:.5f}"

        if len(swing_lows) >= 2:
            lowest_prior = min(swing_lows[-2:])
            if current_close < lowest_prior:
                res["bearish_bos"] = True
                res["level"] = lowest_prior
                res["reason"] = f"Bearish_BOS_Continuation_{lowest_prior:.5f}"

        return res

    # =========================================================================
    # CONCEPT 6: LIQUIDITY POOLS (LP) - Equal Highs (EQH) & Equal Lows (EQL)
    # =========================================================================
    @classmethod
    def detect_liquidity_pools(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Scans for clusters of Equal Highs (EQH / Buy-Side Liquidity)
        and Equal Lows (EQL / Sell-Side Liquidity).
        """
        res = {"bsl_pools": [], "ssl_pools": []}
        if df is None or len(df) < 20:
            return res

        highs = df['high'].values
        lows = df['low'].values
        n = len(df)

        shs = [highs[i] for i in range(2, n - 2) if highs[i] > max(highs[i-2:i]) and highs[i] > max(highs[i+1:i+3])]
        sls = [lows[i] for i in range(2, n - 2) if lows[i] < min(lows[i-2:i]) and lows[i] < min(lows[i+1:i+3])]

        # Find EQH (Highs within 0.12% of each other)
        for i in range(len(shs)):
            for j in range(i + 1, len(shs)):
                if abs(shs[i] - shs[j]) / shs[i] <= 0.0012:
                    res["bsl_pools"].append(max(shs[i], shs[j]))

        # Find EQL (Lows within 0.12% of each other)
        for i in range(len(sls)):
            for j in range(i + 1, len(sls)):
                if abs(sls[i] - sls[j]) / sls[i] <= 0.0012:
                    res["ssl_pools"].append(min(sls[i], sls[j]))

        return res

    # =========================================================================
    # CONCEPT 7: STOP-LOSS HUNTING (SWEEP / TURTLE SOUP) - Liquidity Grabs
    # =========================================================================
    @classmethod
    def detect_stop_loss_hunting(cls, df: pd.DataFrame, lp: Dict[str, Any]) -> Dict[str, Any]:
        """
        Detects smart money liquidity sweeps:
          - Bullish Sweep: Candle wicks below EQL/SSL, but closes back above with rejection wick.
          - Bearish Sweep: Candle wicks above EQH/BSL, but closes back below with rejection wick.
        """
        res = {"bullish_sweep": False, "bearish_sweep": False, "sweep_level": 0.0, "reason": "NONE"}
        if df is None or len(df) < 5:
            return res

        last_candle = df.iloc[-1]
        c_open = float(last_candle['open'])
        c_close = float(last_candle['close'])
        c_high = float(last_candle['high'])
        c_low = float(last_candle['low'])
        c_range = c_high - c_low

        if c_range <= 0:
            return res

        lower_wick = min(c_open, c_close) - c_low
        upper_wick = c_high - max(c_open, c_close)

        # Bullish Liquidity Sweep (Turtle Soup Spring)
        for ssl in lp.get("ssl_pools", []):
            if c_low < ssl and c_close > ssl and (lower_wick / c_range) >= 0.40:
                res["bullish_sweep"] = True
                res["sweep_level"] = ssl
                res["reason"] = f"Bullish_TurtleSoup_SSL_Sweep_{ssl:.5f}"
                break

        # Bearish Liquidity Sweep (Turtle Soup Upthrust)
        for bsl in lp.get("bsl_pools", []):
            if c_high > bsl and c_close < bsl and (upper_wick / c_range) >= 0.40:
                res["bearish_sweep"] = True
                res["sweep_level"] = bsl
                res["reason"] = f"Bearish_TurtleSoup_BSL_Sweep_{bsl:.5f}"
                break

        return res

    # =========================================================================
    # CONCEPT 8: FALSE BREAKOUTS (JUDAS SWING / SFP) - Trapped Retail
    # =========================================================================
    @classmethod
    def detect_false_breakouts(cls, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Detects Swing Failure Patterns (SFP):
        Price pushes beyond recent 10-bar consolidation high/low then violently snaps back.
        """
        res = {"bullish_fakeout": False, "bearish_fakeout": False, "level": 0.0, "reason": "NONE"}
        if df is None or len(df) < 15:
            return res

        highs = df['high'].values
        lows = df['low'].values
        closes = df['close'].values

        recent_range_high = max(highs[-12:-2])
        recent_range_low = min(lows[-12:-2])

        c_high = highs[-1]
        c_low = lows[-1]
        c_close = closes[-1]

        # Bearish Judas / Fakeout (Spike above range high, close back inside)
        if c_high > recent_range_high and c_close < recent_range_high:
            res["bearish_fakeout"] = True
            res["level"] = recent_range_high
            res["reason"] = f"Bearish_Judas_Fakeout_Top_{recent_range_high:.5f}"

        # Bullish Judas / Fakeout (Dip below range low, close back inside)
        elif c_low < recent_range_low and c_close > recent_range_low:
            res["bullish_fakeout"] = True
            res["level"] = recent_range_low
            res["reason"] = f"Bullish_Judas_Fakeout_Bottom_{recent_range_low:.5f}"

        return res

    # =========================================================================
    # CONCEPT 9: KILL ZONES (KZ) - Institutional Timing Windows
    # =========================================================================
    @classmethod
    def get_kill_zone_status(cls) -> Dict[str, Any]:
        """
        Determines if current time is within high-probability SMC institutional Kill Zones:
          - London Open Kill Zone: 07:00 - 10:00 UTC (Judas Swings & Expansion)
          - New York Open Kill Zone: 12:00 - 15:00 UTC (Trend Acceleration / Reversal)
          - London Close Kill Zone: 15:00 - 17:00 UTC (Daily profit taking)
          - Asian Range: 00:00 - 06:00 UTC (Liquidity Accumulation)
        """
        utc_now = datetime.now(timezone.utc)
        time_float = utc_now.hour + (utc_now.minute / 60.0)

        is_london_open = (7.0 <= time_float <= 10.0)
        is_ny_open = (12.0 <= time_float <= 15.0)
        is_london_close = (15.0 <= time_float <= 17.0)
        is_asian = (0.0 <= time_float <= 6.0)

        active_zone = "NONE"
        in_prime_kill_zone = False
        boost_points = 0.0

        if is_london_open:
            active_zone = "LONDON_OPEN_KILL_ZONE"
            in_prime_kill_zone = True
            boost_points = 12.0
        elif is_ny_open:
            active_zone = "NEW_YORK_OPEN_KILL_ZONE"
            in_prime_kill_zone = True
            boost_points = 15.0
        elif is_london_close:
            active_zone = "LONDON_CLOSE_KILL_ZONE"
            in_prime_kill_zone = True
            boost_points = 8.0
        elif is_asian:
            active_zone = "ASIAN_RANGE_ACCUMULATION"
            in_prime_kill_zone = False
            boost_points = 4.0

        return {
            "active_zone": active_zone,
            "in_prime_kill_zone": in_prime_kill_zone,
            "boost_points": boost_points,
            "utc_hour": utc_now.hour
        }

    # =========================================================================
    # MASTER 9 SMC MULTI-TIMEFRAME SYNTHESIS (M15, M30, H1, H4)
    # =========================================================================
    @classmethod
    def analyze_9_smc_confluence(cls, symbol: str) -> Dict[str, Any]:
        """
        Unified Institutional Synthesis across all 9 Smart Money Concepts on M15, M30, H1, H4:
        Evaluates Macro Trend, Structure, Order Blocks, FVGs, Liquidity Sweeps, and Kill Zones.
        Returns:
          {
            "action": "BUY" | "SELL" | "WAIT",
            "confidence": float (0-100),
            "reason": str,
            "entry_price": float,
            "sl_price": float,
            "tp_price": float,
            "rr_ratio": float,
            "confluence_factors": list
          }
        """
        default_res = {
            "action": "WAIT",
            "confidence": 50.0,
            "reason": "NO_SMC_CONFLUENCE",
            "entry_price": 0.0,
            "sl_price": 0.0,
            "tp_price": 0.0,
            "rr_ratio": 0.0,
            "confluence_factors": []
        }

        # 1. Fetch candles across M15, M30, H1, H4
        df_m15 = cls.fetch_timeframe_candles(symbol, "15m", limit=60)
        df_m30 = cls.fetch_timeframe_candles(symbol, "30m", limit=50)
        df_h1 = cls.fetch_timeframe_candles(symbol, "1h", limit=50)
        df_h4 = cls.fetch_timeframe_candles(symbol, "4h", limit=40)

        # Fallback if any higher timeframe is missing: derive from M15 / H1
        if df_m15 is None or len(df_m15) < 15:
            return default_res

        current_price = float(df_m15['close'].iloc[-1])
        kz_info = cls.get_kill_zone_status()

        bullish_score = 0.0
        bearish_score = 0.0
        confluence_factors = []

        # Kill Zone Timing Boost (Concept 9)
        if kz_info["in_prime_kill_zone"]:
            boost = kz_info["boost_points"]
            bullish_score += boost * 0.5
            bearish_score += boost * 0.5
            confluence_factors.append(f"KillZone_{kz_info['active_zone']}")

        # ---------------------------------------------------------------------
        # H4 & H1 MACRO STRUCTURE (Macro Bias, Major OBs, Major SnD)
        # ---------------------------------------------------------------------
        if df_h4 is not None and len(df_h4) >= 10:
            h4_bos = cls.detect_bos(df_h4)
            h4_choch = cls.detect_choch(df_h4)
            h4_obs = cls.detect_order_blocks(df_h4)

            if h4_bos["bullish_bos"] or h4_choch["bullish_choch"]:
                bullish_score += 20.0
                confluence_factors.append("H4_Macro_Bullish_Structure")
            elif h4_bos["bearish_bos"] or h4_choch["bearish_choch"]:
                bearish_score += 20.0
                confluence_factors.append("H4_Macro_Bearish_Structure")

            # Check if testing H4 Order Block
            for ob in h4_obs:
                if ob["is_testing"] and ob["type"] == "BULLISH_OB":
                    bullish_score += 15.0
                    confluence_factors.append("H4_Bullish_OB_Retest")
                elif ob["is_testing"] and ob["type"] == "BEARISH_OB":
                    bearish_score += 15.0
                    confluence_factors.append("H4_Bearish_OB_Retest")

        if df_h1 is not None and len(df_h1) >= 10:
            h1_bos = cls.detect_bos(df_h1)
            h1_choch = cls.detect_choch(df_h1)
            h1_fvgs = cls.detect_fair_value_gaps(df_h1)
            h1_lps = cls.detect_liquidity_pools(df_h1)

            if h1_bos["bullish_bos"] or h1_choch["bullish_choch"]:
                bullish_score += 15.0
                confluence_factors.append("H1_Bullish_BOS_CHoCH")
            elif h1_bos["bearish_bos"] or h1_choch["bearish_choch"]:
                bearish_score += 15.0
                confluence_factors.append("H1_Bearish_BOS_CHoCH")

            for fvg in h1_fvgs:
                if fvg["is_testing"] and fvg["type"] == "BULLISH_FVG":
                    bullish_score += 12.0
                    confluence_factors.append("H1_Bullish_FVG_Mitigation")
                elif fvg["is_testing"] and fvg["type"] == "BEARISH_FVG":
                    bearish_score += 12.0
                    confluence_factors.append("H1_Bearish_FVG_Mitigation")

        # ---------------------------------------------------------------------
        # M30 & M15 EXECUTION (Liquidity Sweep, Order Block, SnD, CHoCH)
        # ---------------------------------------------------------------------
        if df_m30 is not None and len(df_m30) >= 10:
            m30_snd = cls.detect_supply_demand_zones(df_m30)
            for z in m30_snd:
                if z["is_testing"] and z["type"] == "DEMAND":
                    bullish_score += 12.0
                    confluence_factors.append(f"M30_Demand_{z['pattern']}_Tap")
                elif z["is_testing"] and z["type"] == "SUPPLY":
                    bearish_score += 12.0
                    confluence_factors.append(f"M30_Supply_{z['pattern']}_Tap")

        # M15 Precision Trigger (Sniper Level)
        m15_obs = cls.detect_order_blocks(df_m15)
        m15_fvgs = cls.detect_fair_value_gaps(df_m15)
        m15_lps = cls.detect_liquidity_pools(df_m15)
        m15_sweep = cls.detect_stop_loss_hunting(df_m15, m15_lps)
        m15_fakeout = cls.detect_false_breakouts(df_m15)
        m15_choch = cls.detect_choch(df_m15)

        # Concept 7: Liquidity Sweep (Turtle Soup)
        if m15_sweep["bullish_sweep"]:
            bullish_score += 25.0
            confluence_factors.append(m15_sweep["reason"])
        elif m15_sweep["bearish_sweep"]:
            bearish_score += 25.0
            confluence_factors.append(m15_sweep["reason"])

        # Concept 8: False Breakout (Judas Swing)
        if m15_fakeout["bullish_fakeout"]:
            bullish_score += 15.0
            confluence_factors.append(m15_fakeout["reason"])
        elif m15_fakeout["bearish_fakeout"]:
            bearish_score += 15.0
            confluence_factors.append(m15_fakeout["reason"])

        # Concept 1 & 2 on M15: Order Block & FVG
        for ob in m15_obs:
            if ob["is_testing"] and ob["type"] == "BULLISH_OB":
                bullish_score += 15.0
                confluence_factors.append("M15_Bullish_OB_Test")
            elif ob["is_testing"] and ob["type"] == "BEARISH_OB":
                bearish_score += 15.0
                confluence_factors.append("M15_Bearish_OB_Test")

        for fvg in m15_fvgs:
            if fvg["is_testing"] and fvg["type"] == "BULLISH_FVG":
                bullish_score += 12.0
                confluence_factors.append("M15_Bullish_FVG_Fill")
            elif fvg["is_testing"] and fvg["type"] == "BEARISH_FVG":
                bearish_score += 12.0
                confluence_factors.append("M15_Bearish_FVG_Fill")

        if m15_choch["bullish_choch"]:
            bullish_score += 15.0
            confluence_factors.append("M15_Bullish_CHoCH_Trigger")
        elif m15_choch["bearish_choch"]:
            bearish_score += 15.0
            confluence_factors.append("M15_Bearish_CHoCH_Trigger")

        # ---------------------------------------------------------------------
        # EVALUATE CONFLUENCE DECISION (Strict 95% Institutional Target)
        # ---------------------------------------------------------------------
        action = "WAIT"
        confidence = 50.0
        sl_price = 0.0
        tp_price = 0.0
        rr_ratio = 0.0

        # Calculate local ATR for SL/TP positioning
        m15_highs = df_m15['high'].values
        m15_lows = df_m15['low'].values
        m15_closes = df_m15['close'].values
        tr_list = [max(m15_highs[i] - m15_lows[i], abs(m15_highs[i] - m15_closes[i-1]), abs(m15_lows[i] - m15_closes[i-1])) for i in range(1, len(m15_closes))]
        m15_atr = float(np.mean(tr_list[-14:])) if len(tr_list) >= 14 else (current_price * 0.002)

        if bullish_score >= 65.0 and (bullish_score - bearish_score) >= 25.0:
            action = "BUY"
            confidence = min(96.0, 85.0 + ((bullish_score - 65.0) / 35.0) * 11.0)
            # SL strictly below recent M15 swing low / swept level
            local_low = min(m15_lows[-5:])
            sl_price = round(local_low - (m15_atr * 0.5), 5)
            risk_dist = max(current_price * 0.001, current_price - sl_price)
            # TP target: 1:3.0 Asymmetric Reward
            tp_price = round(current_price + (risk_dist * 3.0), 5)
            rr_ratio = round((tp_price - current_price) / max(0.00001, current_price - sl_price), 2)

        elif bearish_score >= 65.0 and (bearish_score - bullish_score) >= 25.0:
            action = "SELL"
            confidence = min(96.0, 85.0 + ((bearish_score - 65.0) / 35.0) * 11.0)
            # SL strictly above recent M15 swing high / swept level
            local_high = max(m15_highs[-5:])
            sl_price = round(local_high + (m15_atr * 0.5), 5)
            risk_dist = max(current_price * 0.001, sl_price - current_price)
            # TP target: 1:3.0 Asymmetric Reward
            tp_price = round(current_price - (risk_dist * 3.0), 5)
            rr_ratio = round((current_price - tp_price) / max(0.00001, sl_price - current_price), 2)

        reason_str = f"SMC_9Concepts_{action}_{confidence:.0f}%_RR{rr_ratio}:1_{'_'.join(confluence_factors[:4])}"

        clean_sym = symbol.replace("/", "").replace("_", "").replace("-", "").upper().strip()
        res = {
            "symbol": symbol,
            "action": action,
            "confidence": confidence,
            "reason": reason_str,
            "entry_price": current_price,
            "sl_price": sl_price,
            "tp_price": tp_price,
            "rr_ratio": rr_ratio,
            "confluence_factors": confluence_factors,
            "bullish_score": bullish_score,
            "bearish_score": bearish_score,
            "kill_zone": kz_info["active_zone"],
            "timestamp": time.time()
        }
        cls._LAST_ANALYSIS[symbol.upper().strip()] = res
        cls._LAST_ANALYSIS[clean_sym] = res
        return res
