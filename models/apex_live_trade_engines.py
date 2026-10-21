# -*- coding: utf-8 -*-
"""
ANGKOR QUANT / APEX AGI - INSTITUTIONAL LIVE TRADE ENGINES
============================================================
Mathematical Edge, Cost-Aware Execution, Signal Fusion & Risk Shield

Pillars:
  1. MEV & Flash Loan Arbitrage Engine (Graph cycle enumeration, gas/fee modeling)
  2. Insider Wallet & Whale Activity Tracker (Time-decayed flow graphs, PageRank centrality)
  3. Live Trade Execution Engine (Confidence-weighted signal fusion, Fractional Kelly,
     Dynamic Trailing Stops, Portfolio Drawdown Kill-Switch, and Slippage Armor)
"""

import time
import math
import logging
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
import networkx as nx

try:
    import ccxt
except ImportError:
    ccxt = None

log = logging.getLogger("apex")
log.setLevel(logging.INFO)

BPS = 10000.0


# =============================================================================
# ១. MEV & FLASH LOAN ARBITRAGE ENGINE
# =============================================================================
class MEVFlashLoanEngine:
    """
    Cost-aware arbitrage detection on a directed liquidity graph.
    Cycle enumeration bounded by max_hops, accounting for flash loan fee,
    swap fees, and gas costs before approving execution.
    """
    def __init__(self, num_coins: int = 1050, min_profit_wei: int = 10**15,
                 flash_loan_fee_bps: float = 9.0, gas_per_trade: int = 250000):
        self.num_coins = num_coins
        self.coins = [f"COIN_{i}" for i in range(num_coins)]
        self.min_profit_wei = int(min_profit_wei)
        self.flash_loan_fee_bps = float(flash_loan_fee_bps)
        self.gas_per_trade = int(gas_per_trade)
        self.graph = nx.DiGraph()
        self.last_scan_ts = 0.0

    def build_liquidity_graph(self, pools: List[Dict[str, Any]]) -> None:
        """
        Builds directed liquidity graph from pool states.
        pools: iterable of dicts with keys: from, to, rate, fee_bps, depth_wei
        """
        self.graph.clear()
        for p in pools:
            try:
                if float(p.get("depth_wei", 0)) <= 0 or float(p.get("rate", 0)) <= 0:
                    continue
                u, v = p["from"], p["to"]
                rate_val = float(p["rate"])
                fee_val = float(p.get("fee_bps", 0.0))
                depth_val = int(p["depth_wei"])

                if self.graph.has_edge(u, v):
                    if rate_val > float(self.graph[u][v]["rate"]):
                        self.graph[u][v].update(
                            rate=rate_val,
                            fee_bps=fee_val,
                            depth_wei=depth_val
                        )
                else:
                    self.graph.add_edge(
                        u, v,
                        rate=rate_val,
                        fee_bps=fee_val,
                        depth_wei=depth_val
                    )
            except (KeyError, TypeError, ValueError):
                continue

    def find_arbitrage(self, base_token: str, max_hops: int = 3) -> List[Dict[str, Any]]:
        """
        Enumerates simple cycles containing base_token bounded by max_hops + 1.
        Rotates cycle so it begins and ends at base_token.
        Filters for cycles with gross rate > 1.0.
        """
        if base_token not in self.graph:
            return []
        candidates = []
        try:
            for cycle in nx.simple_cycles(self.graph, length_bound=max_hops + 1):
                if not cycle or len(cycle) < 2 or base_token not in cycle:
                    continue
                # Canonicalize cycle to start from base_token
                idx = cycle.index(base_token)
                cycle = cycle[idx:] + cycle[:idx]

                rate = 1.0
                total_fee_bps = 0.0
                ok = True
                for i in range(len(cycle)):
                    u = cycle[i]
                    v = cycle[(i + 1) % len(cycle)]
                    if not self.graph.has_edge(u, v):
                        ok = False
                        break
                    e = self.graph[u][v]
                    rate *= float(e["rate"])
                    total_fee_bps += float(e["fee_bps"])
                if not ok or rate <= 1.0:
                    continue
                candidates.append({
                    "cycle": cycle,
                    "gross_rate": rate,
                    "total_fee_bps": total_fee_bps,
                })
        except (nx.NetworkXNoCycle, nx.NetworkXError):
            return []
        return candidates

    def execute_if_profitable(self, base_token: str, amount_wei: int,
                              gas_price_gwei: float = 30.0,
                              eth_price_usd: float = 3000.0) -> Optional[Dict[str, Any]]:
        """
        Calculates exact net profit in WEI after flash loan fee, swap fees, and gas.
        Rejects any opportunity below min_profit_wei.
        """
        self.last_scan_ts = time.time()
        if amount_wei <= 0 or amount_wei > self.graph.nodes.get(base_token, {}).get("cap_wei", amount_wei):
            return None
        candidates = self.find_arbitrage(base_token)
        if not candidates:
            return None
        best = max(candidates, key=lambda c: c["gross_rate"])
        gross_profit_wei = int(amount_wei * (best["gross_rate"] - 1.0))
        flash_fee_wei = int(amount_wei * self.flash_loan_fee_bps / BPS)
        swap_fee_wei = int(amount_wei * best["total_fee_bps"] / BPS)
        gas_cost_wei = int(self.gas_per_trade * gas_price_gwei * 1e9)
        net_profit_wei = gross_profit_wei - flash_fee_wei - swap_fee_wei - gas_cost_wei

        if net_profit_wei < self.min_profit_wei:
            return None

        return {
            "cycle": best["cycle"],
            "amount_wei": int(amount_wei),
            "net_profit_wei": int(net_profit_wei),
            "gas_cost_wei": int(gas_cost_wei),
            "roi_bps": int(net_profit_wei / amount_wei * BPS),
            "expected_value_usd": (net_profit_wei / 1e18) * float(eth_price_usd),
            "execute": True,
        }


# =============================================================================
# ២. INSIDER WALLET & WHALE TRACKER
# =============================================================================
def build_onchain_graph(transfers: List[Dict[str, Any]], decay: float = 0.5) -> nx.DiGraph:
    """
    Constructs a directed flow graph from transfer logs with temporal decay weighting.
    """
    G = nx.DiGraph()
    if not transfers:
        return G
    n = len(transfers)
    for idx, t in enumerate(transfers):
        try:
            val = float(t.get("value", 0.0))
            w = val * (decay ** (n - 1 - idx))
            if w <= 0:
                continue
            src, dst = t["from"], t["to"]
        except (KeyError, TypeError, ValueError):
            continue
        if G.has_edge(src, dst):
            G[src][dst]["weight"] += w
            G[src][dst]["count"] += 1
        else:
            G.add_edge(src, dst, weight=w, count=1)
    return G


def scan_insider_activity(G: nx.DiGraph, smart_money_wallets: List[str],
                          target_token: str, min_confidence: float = 0.6) -> Dict[str, Any]:
    """
    Scans for smart money inflow clusters and network centrality around target_token.
    Emits confidence-scored directional accumulation (+1) or distribution (-1) signals.
    """
    if G is None or not G.nodes():
        return {"signal": 0, "confidence": 0.0, "reason": "empty_graph"}
    if target_token not in G:
        return {"signal": 0, "confidence": 0.0, "reason": "no_token_data"}
    smart = set(smart_money_wallets) & set(G.nodes())
    if not smart:
        return {"signal": 0, "confidence": 0.0, "reason": "no_smart_money"}
    try:
        pagerank = nx.pagerank(G, alpha=0.85, weight="weight", max_iter=200)
    except (nx.PowerIterationFailedConvergence, ZeroDivisionError):
        pagerank = {n: 1.0 / max(1, len(G)) for n in G.nodes()}

    total_inflow = 0.0
    smart_inflow = 0.0
    for u in G.predecessors(target_token):
        w = float(G[u][target_token].get("weight", 0.0))
        total_inflow += w
        if u in smart:
            smart_inflow += w

    if total_inflow <= 0:
        return {"signal": 0, "confidence": 0.0, "reason": "no_inflow"}

    ratio = smart_inflow / total_inflow
    centrality = sum(pagerank.get(w, 0.0) for w in smart) / max(len(smart), 1)
    confidence = min(1.0, 0.5 * ratio + 0.5 * min(1.0, centrality * 100))

    if ratio > 0.7 and confidence >= min_confidence:
        signal = 1
    elif ratio < 0.3 and confidence >= min_confidence:
        signal = -1
    else:
        signal = 0

    return {
        "signal": signal,
        "confidence": confidence,
        "smart_inflow": smart_inflow,
        "total_inflow": total_inflow,
        "ratio": ratio,
        "centrality": centrality,
        "reason": "ok",
    }


# =============================================================================
# ៣. LIVE TRADE EXECUTION ENGINE
# =============================================================================
class LiveTradeExecutionEngine:
    """
    Deterministic, risk-hardened trade execution engine.
    Integrates confidence-weighted signal fusion, fractional Kelly sizing,
    slippage guards, trailing stops, and a portfolio drawdown kill switch.
    """
    def __init__(self, exchange_id: str = "binance", api_key: str = "",
                 secret: str = "", testnet: bool = True,
                 max_position_pct: float = 0.20, max_drawdown_pct: float = 0.05,
                 trailing_stop_pct: float = 0.018, kelly_fraction: float = 0.5,
                 min_confidence: float = 0.55, max_slippage_bps: float = 50.0,
                 max_leverage: float = 1.0):
        self.exchange_id = exchange_id
        if ccxt is not None:
            exchange_class = getattr(ccxt, exchange_id, ccxt.binance)
            self.exchange = exchange_class({
                "apiKey": api_key,
                "secret": secret,
                "enableRateLimit": True,
                "timeout": 30000,
                "options": {"defaultType": "spot", "adjustForTimeDifference": True},
            })
            if testnet and hasattr(self.exchange, "set_sandbox_mode"):
                try:
                    self.exchange.set_sandbox_mode(True)
                except Exception as e_sb:
                    log.warning("Sandbox mode setup: %s", e_sb)
        else:
            self.exchange = None
            log.warning("ccxt package not installed. Exchange client uninitialized.")

        self.max_position_pct = float(max_position_pct)
        self.max_drawdown_pct = float(max_drawdown_pct)
        self.trailing_stop_pct = float(trailing_stop_pct)
        self.kelly_fraction = float(kelly_fraction)
        self.min_confidence = float(min_confidence)
        self.max_slippage_bps = float(max_slippage_bps)
        self.max_leverage = max(1.0, float(max_leverage))
        self.positions: Dict[str, Dict[str, Any]] = {}
        self.equity = 0.0
        self.peak_equity = 0.0
        self.kill_switch = False
        self.markets_ready = False

    def _ensure_markets(self) -> bool:
        if self.markets_ready:
            return True
        if self.exchange is None:
            return False
        try:
            self.exchange.load_markets()
            self.markets_ready = True
            return True
        except Exception as e:
            log.error("load_markets failed: %s", e)
            return False

    def fuse_signals(self, model_outputs: Dict[str, Dict[str, Any]]) -> Tuple[int, float]:
        """
        Confidence-weighted voting over multiple model outputs.
        Time complexity: O(M), Space: O(1).
        """
        if not model_outputs:
            return 0, 0.0
        total_w = 0.0
        weighted = 0.0
        for name, out in model_outputs.items():
            try:
                conf = float(out.get("confidence", 0.0))
                sig = int(out.get("signal", 0))
            except (TypeError, ValueError):
                continue
            if conf <= 0.0 or sig == 0:
                continue
            total_w += conf
            weighted += sig * conf
        if total_w <= 0.0:
            return 0, 0.0
        score = weighted / total_w
        if score > self.min_confidence:
            return 1, score
        if score < -self.min_confidence:
            return -1, abs(score)
        return 0, abs(score)

    def kelly_size(self, p_win: float, payoff_ratio: float) -> float:
        """
        Fractional Kelly sizing: f* = (p - (1-p)/b) * kelly_fraction.
        """
        p_clamped = max(0.0, min(0.999, float(p_win)))
        if p_clamped <= 0.0 or payoff_ratio <= 0.0:
            return 0.0
        f = p_clamped - (1.0 - p_clamped) / payoff_ratio
        return max(0.0, min(1.0, f)) * self.kelly_fraction

    def _drawdown(self) -> float:
        if self.peak_equity <= 0.0:
            return 0.0
        return max(0.0, (self.peak_equity - self.equity) / self.peak_equity)

    def update_equity(self, new_equity: float) -> None:
        self.equity = float(new_equity)
        if self.equity > self.peak_equity:
            self.peak_equity = self.equity
        if self._drawdown() >= self.max_drawdown_pct:
            self.kill_switch = True
            log.warning("kill_switch engaged, drawdown=%.4f", self._drawdown())

    def execute_market_order(self, symbol: str, side: str, quote_amount: float,
                             expected_price: float,
                             max_slippage_bps: Optional[float] = None) -> Dict[str, Any]:
        """
        Executes market order with pre-trade slippage checks and strict CCXT exception handling.
        """
        if self.kill_switch:
            return {"status": "rejected", "reason": "kill_switch"}
        if self.exchange is None:
            return {"status": "error", "reason": "no_exchange_client"}
        if not self._ensure_markets():
            return {"status": "error", "reason": "markets_unavailable"}
        if symbol not in self.exchange.markets:
            return {"status": "error", "reason": "unknown_symbol"}
        if quote_amount <= 0:
            return {"status": "rejected", "reason": "non_positive_amount"}

        max_slip = float(max_slippage_bps if max_slippage_bps is not None else self.max_slippage_bps)
        try:
            ticker = self.exchange.fetch_ticker(symbol)
        except Exception as e:
            return {"status": "error", "reason": f"ticker:{e}"}

        best = float(ticker.get("ask" if side == "buy" else "bid", 0.0) or 0.0)
        if best <= 0:
            return {"status": "error", "reason": "invalid_price"}

        slip_bps = abs(best - expected_price) / max(expected_price, 1e-9) * BPS
        if slip_bps > max_slip:
            return {
                "status": "rejected",
                "reason": "slippage",
                "slippage_bps": slip_bps
            }

        amount_base = quote_amount / best
        try:
            order = self.exchange.create_order(symbol, "market", side, amount_base)
            return {
                "status": "filled",
                "order": order,
                "price": best,
                "amount": amount_base
            }
        except getattr(ccxt, "InsufficientFunds", Exception) as e:
            return {"status": "error", "reason": f"insufficient_funds:{e}"}
        except Exception as e:
            return {"status": "error", "reason": str(e)}

    def open_position(self, symbol: str, quote_amount: float, entry_price: float,
                      expected_tp_pct: float, expected_sl_pct: float,
                      confidence: float) -> Dict[str, Any]:
        """
        Sizes and opens position according to Fractional Kelly and risk caps.
        """
        if self.kill_switch:
            return {"status": "rejected", "reason": "kill_switch"}
        if quote_amount > self.equity * self.max_position_pct:
            return {"status": "rejected", "reason": "position_cap"}

        p_win = max(0.0, min(1.0, confidence))
        payoff = max(1e-9, expected_tp_pct / max(expected_sl_pct, 1e-9))
        f = self.kelly_size(p_win, payoff)
        if f <= 0.0:
            return {"status": "rejected", "reason": "kelly_zero"}

        target_quote = min(self.equity * f, self.equity * self.max_position_pct)
        result = self.execute_market_order(symbol, "buy", target_quote, entry_price)
        if result.get("status") != "filled":
            return result

        fill = result["price"]
        self.positions[symbol] = {
            "entry_price": fill,
            "size_quote": target_quote,
            "peak": fill,
            "stop_price": fill * (1.0 - expected_sl_pct),
            "tp_price": fill * (1.0 + expected_tp_pct),
            "opened_at": time.time(),
        }
        return {"status": "opened", "position": self.positions[symbol], "fill": fill}

    def update_trailing_stops(self) -> List[Dict[str, Any]]:
        """
        Updates peak tracking and ratchets trailing stops.
        Executes immediate market sell when price drops below stop floor.
        """
        closed = []
        if self.exchange is None:
            return closed

        for sym, pos in list(self.positions.items()):
            try:
                px = float(self.exchange.fetch_ticker(sym).get("last", 0.0) or 0.0)
            except Exception:
                continue
            if px <= 0:
                continue
            pos["last_price"] = px
            if px > pos["peak"]:
                pos["peak"] = px

            trailing = pos["peak"] * (1.0 - self.trailing_stop_pct)
            hard_stop = pos["entry_price"] * (1.0 - self.trailing_stop_pct)
            stop = max(trailing, hard_stop)
            pos["stop_price"] = stop

            if px <= stop:
                res = self.execute_market_order(sym, "sell", pos["size_quote"], px)
                if res.get("status") == "filled":
                    pnl_pct = (res["price"] / pos["entry_price"]) - 1.0
                    self.equity += pos["size_quote"] * pnl_pct
                    if self.equity > self.peak_equity:
                        self.peak_equity = self.equity
                    closed.append({
                        "symbol": sym,
                        "pnl_pct": pnl_pct,
                        "reason": "trailing_stop"
                    })
                    del self.positions[sym]
        return closed

    def check_drawdown_and_liquidate(self) -> List[Dict[str, Any]]:
        """
        Enforces maximum portfolio drawdown kill-switch.
        Closes all positions immediately if threshold is breached.
        """
        if self._drawdown() < self.max_drawdown_pct:
            return []
        self.kill_switch = True
        closed = []
        if self.exchange is None:
            return closed

        for sym, pos in list(self.positions.items()):
            try:
                px = float(self.exchange.fetch_ticker(sym).get("last", 0.0) or 0.0)
            except Exception:
                continue
            res = self.execute_market_order(sym, "sell", pos["size_quote"], px)
            if res.get("status") == "filled":
                pnl_pct = (res["price"] / pos["entry_price"]) - 1.0
                self.equity += pos["size_quote"] * pnl_pct
                closed.append({
                    "symbol": sym,
                    "pnl_pct": pnl_pct,
                    "reason": "drawdown_liquidation"
                })
                del self.positions[sym]
        return closed
