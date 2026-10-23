# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - CAPITAL.COM DAILY MARKET REPORT & CONTRARIAN SENTIMENT ARBITRAGE ENGINE
========================================================================================
Document Version: 1.0.0 (Institutional Specification Lock - Invariant 99)
Target Broker: Capital.com (FCA, CySEC, ASIC Regulated Global Multi-Asset Broker)
Instruments: Gold (XAUUSD), US Indices (US500, US100, US30), Commodities, Mega-Cap Tech
Core Capabilities:
  1. Monte Safieddine Market Report Knowledge & Dynamic Volatility S/R Levels
  2. Live Capital.com Client Sentiment Parser (GET /api/v1/clients/sentiment) & In-Memory Cache
  3. Multi-Class Sentiment Arbitrage (Client Herd vs Leveraged Funds vs Asset Managers)
  4. Extreme Retail Herd Liquidity Trap Veto (79.75% Retail Loss Exploitation)
  5. Exact Broker Stop-Loss Cluster Sweep Reversal (Turtle Soup Liquidity Hunt at SL Res/Sup)
  6. Multi-Timeframe Daily & Weekly Regime Synchronizer for Meta-Labeling Model 2
"""

import time
import math
import logging
from typing import Dict, Any, Tuple, Optional, List

logger = logging.getLogger("CapitalMarketReportEngine")
if not logger.handlers:
    h = logging.StreamHandler()
    h.setFormatter(logging.Formatter("[%(asctime)s] [%(levelname)s] [MarketReportEngine] %(message)s"))
    logger.addHandler(h)
    logger.setLevel(logging.INFO)

# ==============================================================================
# 1. MONTE SAFIEDDINE INSTITUTIONAL DAILY MARKET REPORT BENCHMARK KNOWLEDGE
# ==============================================================================
# Exact coordinates transcribed from the Capital.com Daily Market Report:
CAPITAL_DAILY_REPORT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "US500": {
        "daily_regime": "Consolidation - Volatile",
        "weekly_regime": "Bull Average",
        "starting_point": 7720.10,
        "delta": 45.80,
        "res1": 7765.90, "sl_res1": 7788.80,
        "res2": 7811.70, "sl_res2": 7834.60,
        "sup1": 7674.30, "sl_sup1": 7651.40,
        "sup2": 7628.50, "sl_sup2": 7605.60,
        "client_long_pct": 71.0, "client_short_pct": 29.0,
        "institutional_long_pct": 38.0, "institutional_short_pct": 62.0,
        "leveraged_funds_long_pct": 19.0, "leveraged_funds_short_pct": 81.0,
        "asset_managers_long_pct": 85.0, "asset_managers_short_pct": 15.0,
        "indicators": {"adx": "Consolidation", "rsi": "Neutral", "bb": "Neutral", "ma_short": "Neutral", "ma_long": "Bullish"},
    },
    "US100": {
        "daily_regime": "Consolidation - Volatile",
        "weekly_regime": "Consolidation - Volatile",
        "starting_point": 29578.0,
        "delta": 296.0,
        "res1": 29874.0, "sl_res1": 30021.0,
        "res2": 30169.0, "sl_res2": 30317.0,
        "sup1": 29283.0, "sl_sup1": 29135.0,
        "sup2": 28987.0, "sl_sup2": 28840.0,
        "client_long_pct": 67.0, "client_short_pct": 33.0,
        "institutional_long_pct": 68.0, "institutional_short_pct": 32.0,
        "leveraged_funds_long_pct": 40.0, "leveraged_funds_short_pct": 60.0,
        "asset_managers_long_pct": 75.0, "asset_managers_short_pct": 25.0,
        "indicators": {"adx": "Trending", "rsi": "Neutral", "bb": "Lower Extreme", "ma_short": "Neutral", "ma_long": "Neutral"},
    },
    "US30": {
        "daily_regime": "Consolidation - Volatile",
        "weekly_regime": "Cautious Consolidation",
        "starting_point": 52667.0,
        "delta": 351.0,
        "res1": 53018.0, "sl_res1": 53193.0,
        "res2": 53369.0, "sl_res2": 53544.0,
        "sup1": 52316.0, "sl_sup1": 52140.0,
        "sup2": 51965.0, "sl_sup2": 51789.0,
        "client_long_pct": 63.0, "client_short_pct": 37.0,
        "institutional_long_pct": 66.0, "institutional_short_pct": 34.0,
        "leveraged_funds_long_pct": 59.0, "leveraged_funds_short_pct": 41.0,
        "asset_managers_long_pct": 73.0, "asset_managers_short_pct": 27.0,
        "indicators": {"adx": "Trending", "rsi": "Neutral", "bb": "Upper Extreme", "ma_short": "Bullish", "ma_long": "Bullish"},
    },
    "DE40": {
        "daily_regime": "Cautious Consolidation",
        "weekly_regime": "Cautious Consolidation",
        "starting_point": 25522.0,
        "delta": 194.0,
        "res1": 25716.0, "sl_res1": 25814.0,
        "res2": 25911.0, "sl_res2": 26008.0,
        "sup1": 25328.0, "sl_sup1": 25230.0,
        "sup2": 25133.0, "sl_sup2": 25036.0,
        "client_long_pct": 59.0, "client_short_pct": 41.0,
        "indicators": {"adx": "Trending", "rsi": "Neutral", "bb": "Upper Extreme", "ma_short": "Bullish", "ma_long": "Neutral"},
    },
    "GOLD": {
        "daily_regime": "Bear Average",
        "weekly_regime": "Cautious Consolidation",
        "starting_point": 4125.23,
        "delta": 45.77,
        "res1": 4171.00, "sl_res1": 4193.88,
        "res2": 4216.77, "sl_res2": 4239.65,
        "sup1": 4079.46, "sl_sup1": 4056.58,
        "sup2": 4033.69, "sl_sup2": 4010.81,
        "client_long_pct": 79.0, "client_short_pct": 21.0,
        "institutional_long_pct": 87.0, "institutional_short_pct": 13.0,
        "leveraged_funds_long_pct": 13.0, "leveraged_funds_short_pct": 87.0,
        "asset_managers_long_pct": 85.0, "asset_managers_short_pct": 15.0,
        "indicators": {"adx": "Trending", "rsi": "Neutral", "bb": "Neutral", "ma_short": "Bearish", "ma_long": "Bearish"},
    },
    "SILVER": {
        "daily_regime": "Bear Average",
        "weekly_regime": "Cautious Consolidation",
        "starting_point": 57.45,
        "delta": 1.25,
        "res1": 58.70, "sl_res1": 59.33,
        "res2": 59.95, "sl_res2": 60.58,
        "sup1": 56.20, "sl_sup1": 55.58,
        "sup2": 54.95, "sl_sup2": 54.33,
        "client_long_pct": 89.0, "client_short_pct": 11.0,
        "institutional_long_pct": 75.0, "institutional_short_pct": 25.0,
        "indicators": {"adx": "Trending", "rsi": "Neutral", "bb": "Neutral", "ma_short": "Neutral", "ma_long": "Bearish"},
    },
    "OIL_CRUDE": {
        "daily_regime": "Consolidation - Volatile",
        "weekly_regime": "Consolidation - Volatile",
        "starting_point": 97.70,
        "delta": 2.64,
        "res1": 100.34, "sl_res1": 101.66,
        "res2": 102.98, "sl_res2": 104.30,
        "sup1": 95.07, "sl_sup1": 93.75,
        "sup2": 92.43, "sl_sup2": 91.11,
        "client_long_pct": 47.0, "client_short_pct": 53.0,
        "institutional_long_pct": 74.0, "institutional_short_pct": 26.0,
        "indicators": {"adx": "Trending", "rsi": "Neutral", "bb": "Upper Extreme", "ma_short": "Neutral", "ma_long": "Bullish"},
    },
    "NVDA": {
        "daily_regime": "Cautious Consolidation",
        "weekly_regime": "Consolidation - Volatile",
        "starting_point": 219.05,
        "delta": 3.48,
        "res1": 222.53, "sl_res1": 224.26,
        "res2": 226.00, "sl_res2": 227.74,
        "sup1": 215.57, "sl_sup1": 213.84,
        "sup2": 212.10, "sl_sup2": 210.36,
        "client_long_pct": 94.0, "client_short_pct": 6.0,
        "indicators": {"adx": "Consolidation", "rsi": "Neutral", "bb": "Neutral", "ma_short": "Neutral", "ma_long": "Neutral"},
    },
    "TSLA": {
        "daily_regime": "Cautious Consolidation",
        "weekly_regime": "Bear Average",
        "starting_point": 373.47,
        "delta": 7.32,
        "res1": 380.79, "sl_res1": 384.45,
        "res2": 388.11, "sl_res2": 391.76,
        "sup1": 366.15, "sl_sup1": 362.49,
        "sup2": 358.83, "sl_sup2": 355.18,
        "client_long_pct": 84.0, "client_short_pct": 16.0,
        "indicators": {"adx": "Consolidation", "rsi": "Neutral", "bb": "Neutral", "ma_short": "Bullish", "ma_long": "Neutral"},
    },
    "AMZN": {
        "daily_regime": "Consolidation - Volatile",
        "weekly_regime": "Cautious Consolidation",
        "starting_point": 261.10,
        "delta": 3.64,
        "res1": 264.74, "sl_res1": 266.57,
        "res2": 268.39, "sl_res2": 270.21,
        "sup1": 257.46, "sl_sup1": 255.63,
        "sup2": 253.81, "sl_sup2": 251.99,
        "client_long_pct": 95.0, "client_short_pct": 5.0,
        "indicators": {"adx": "Consolidation", "rsi": "Neutral", "bb": "Upper Extreme", "ma_short": "Bullish", "ma_long": "Bullish"},
    },
    "AAPL": {
        "daily_regime": "Cautious Consolidation",
        "weekly_regime": "Bull Average",
        "starting_point": 343.64,
        "delta": 4.35,
        "res1": 347.99, "sl_res1": 350.17,
        "res2": 352.34, "sl_res2": 354.52,
        "sup1": 339.29, "sl_sup1": 337.11,
        "sup2": 334.94, "sl_sup2": 332.76,
        "client_long_pct": 91.0, "client_short_pct": 9.0,
        "indicators": {"adx": "Consolidation", "rsi": "Neutral", "bb": "Upper Extreme", "ma_short": "Bullish", "ma_long": "Bullish"},
    },
    "MSFT": {
        "daily_regime": "Bull Average",
        "weekly_regime": "Bull Average",
        "starting_point": 529.86,
        "delta": 7.12,
        "res1": 536.98, "sl_res1": 540.54,
        "res2": 544.10, "sl_res2": 547.67,
        "sup1": 522.74, "sl_sup1": 519.18,
        "sup2": 515.62, "sl_sup2": 512.05,
        "client_long_pct": 91.0, "client_short_pct": 9.0,
        "indicators": {"adx": "Trending", "rsi": "Neutral", "bb": "Neutral", "ma_short": "Neutral", "ma_long": "Bullish"},
    }
}

# ==============================================================================
# 1.1 MONTE SAFIEDDINE OFFICIAL DAILY MARKET REPORT (FRIDAY, OCTOBER 23, 2026)
# ==============================================================================
# Comprehensive 28-Asset Quantitative Coordinates Transcribed from Capital.com:
CAPITAL_OCT23_2026_REPORT_REGISTRY: Dict[str, Dict[str, Any]] = {
    "US500": {
        "name": "US 500 (S&P 500)", "asset_class": "INDEX",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Bull Average",
        "starting_point": 7667.70, "delta": 46.10,
        "res1": 7713.80, "sl_res1": 7736.85, "res2": 7759.91, "sl_res2": 7782.96,
        "sup1": 7621.60, "sl_sup1": 7598.55, "sup2": 7575.49, "sl_sup2": 7552.44,
        "weekly_starting_point": 7658.00,
        "weekly_res1": 7775.64, "weekly_sl_res1": 7834.46, "weekly_res2": 7893.28, "weekly_sl_res2": 7952.10,
        "weekly_sup1": 7540.36, "weekly_sl_sup1": 7481.54, "weekly_sup2": 7422.72, "weekly_sl_sup2": 7363.90,
        "client_long_pct": 74.0, "client_short_pct": 26.0,
        "institutional_long_pct": 38.0, "institutional_short_pct": 62.0,
        "leveraged_funds_long_pct": 19.0, "leveraged_funds_short_pct": 81.0,
        "asset_managers_long_pct": 85.0, "asset_managers_short_pct": 15.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Neutral", "dmi": "Negative", "adx": "Consolidation", "rsi": "Neutral", "bb": "Lower Extreme"},
        "conformist_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Sell 1st Resistance only after a reversal; Buy 1st Support only after a reversal"
    },
    "US100": {
        "name": "US Tech 100 (Nasdaq 100)", "asset_class": "INDEX",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Consolidation - Volatile",
        "starting_point": 28916.0, "delta": 303.0,
        "res1": 29219.0, "sl_res1": 29370.0, "res2": 29521.0, "sl_res2": 29672.0,
        "sup1": 28614.0, "sl_sup1": 28463.0, "sup2": 28312.0, "sl_sup2": 28160.0,
        "weekly_starting_point": 29194.0,
        "weekly_res1": 29947.0, "weekly_sl_res1": 30324.0, "weekly_res2": 30701.0, "weekly_sl_res2": 31077.0,
        "weekly_sup1": 28440.0, "weekly_sl_sup1": 28064.0, "weekly_sup2": 27687.0, "weekly_sl_sup2": 27310.0,
        "client_long_pct": 76.0, "client_short_pct": 24.0,
        "institutional_long_pct": 68.0, "institutional_short_pct": 32.0,
        "leveraged_funds_long_pct": 40.0, "leveraged_funds_short_pct": 60.0,
        "asset_managers_long_pct": 75.0, "asset_managers_short_pct": 25.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Neutral", "dmi": "Negative", "adx": "Trending", "rsi": "Neutral", "bb": "Lower Extreme"},
        "conformist_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Sell 1st Resistance only after a reversal; Buy 1st Support only after a reversal"
    },
    "US30": {
        "name": "Wall Street 30 (Dow Jones)", "asset_class": "INDEX",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Cautious Consolidation",
        "starting_point": 52944.0, "delta": 348.0,
        "res1": 53292.0, "sl_res1": 53466.0, "res2": 53639.0, "sl_res2": 53813.0,
        "sup1": 52597.0, "sl_sup1": 52423.0, "sup2": 52250.0, "sl_sup2": 52076.0,
        "weekly_starting_point": 51982.0,
        "weekly_res1": 52769.0, "weekly_sl_res1": 53163.0, "weekly_res2": 53557.0, "weekly_sl_res2": 53950.0,
        "weekly_sup1": 51194.0, "weekly_sl_sup1": 50800.0, "weekly_sup2": 50407.0, "weekly_sl_sup2": 50013.0,
        "client_long_pct": 61.0, "client_short_pct": 39.0,
        "institutional_long_pct": 66.0, "institutional_short_pct": 34.0,
        "leveraged_funds_long_pct": 59.0, "leveraged_funds_short_pct": 41.0,
        "asset_managers_long_pct": 73.0, "asset_managers_short_pct": 27.0,
        "indicators": {"ma_short": "Bullish", "ma_long": "Bullish", "dmi": "Neutral", "adx": "Trending", "rsi": "Neutral", "bb": "Upper Extreme"},
        "conformist_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Sell 1st Resistance only after a reversal; Buy 1st Support only after a reversal"
    },
    "US2000": {
        "name": "Russell 2000", "asset_class": "INDEX",
        "daily_regime": "Bear Average", "weekly_regime": "Cautious Consolidation",
        "starting_point": 2786.60, "delta": 20.70,
        "res1": 2807.30, "sl_res1": 2817.70, "res2": 2828.00, "sl_res2": 2838.40,
        "sup1": 2765.90, "sl_sup1": 2755.50, "sup2": 2745.20, "sl_sup2": 2734.80,
        "client_long_pct": 74.0, "client_short_pct": 26.0,
        "institutional_long_pct": 39.0, "institutional_short_pct": 61.0,
        "leveraged_funds_long_pct": 34.0, "leveraged_funds_short_pct": 66.0,
        "asset_managers_long_pct": 56.0, "asset_managers_short_pct": 44.0,
        "indicators": {"ma_short": "Neutral", "ma_long": "Bearish", "dmi": "Neutral", "adx": "Trending", "rsi": "Neutral", "bb": "Neutral"},
        "conformist_strategy": "Sell 1st Resistance level only after significant reversal; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Buy 1st Support only after a reversal; Buy 1st Resistance upon breakout from below"
    },
    "DE40": {
        "name": "Germany 40 (DAX)", "asset_class": "INDEX",
        "daily_regime": "Cautious Consolidation", "weekly_regime": "Cautious Consolidation",
        "starting_point": 25383.0, "delta": 193.0,
        "res1": 25576.0, "sl_res1": 25672.0, "res2": 25768.0, "sl_res2": 25865.0,
        "sup1": 25190.0, "sl_sup1": 25093.0, "sup2": 24997.0, "sl_sup2": 24901.0,
        "weekly_starting_point": 25470.0,
        "weekly_res1": 25972.0, "weekly_sl_res1": 26222.0, "weekly_res2": 26473.0, "weekly_sl_res2": 26723.0,
        "weekly_sup1": 24969.0, "weekly_sl_sup1": 24718.0, "weekly_sup2": 24468.0, "weekly_sl_sup2": 24217.0,
        "client_long_pct": 66.0, "client_short_pct": 34.0,
        "indicators": {"ma_short": "Neutral", "ma_long": "Neutral", "dmi": "Neutral", "adx": "Trending", "rsi": "Neutral", "bb": "Neutral"},
        "conformist_strategy": "Sell 1st Resistance only after significant reversal; Buy 1st Support only after significant reversal",
        "contrarian_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above"
    },
    "UK100": {
        "name": "UK 100 (FTSE 100)", "asset_class": "INDEX",
        "daily_regime": "Cautious Consolidation", "weekly_regime": "Consolidation - Volatile",
        "starting_point": 10738.10, "delta": 71.70,
        "res1": 10809.80, "sl_res1": 10845.60, "res2": 10881.40, "sl_res2": 10917.30,
        "sup1": 10666.40, "sl_sup1": 10630.60, "sup2": 10594.80, "sl_sup2": 10558.90,
        "client_long_pct": 67.0, "client_short_pct": 33.0,
        "indicators": {"ma_short": "Neutral", "ma_long": "Bullish", "dmi": "Neutral", "adx": "Consolidation", "rsi": "Neutral", "bb": "Neutral"},
        "conformist_strategy": "Sell 1st Resistance only after significant reversal; Buy 1st Support only after significant reversal",
        "contrarian_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above"
    },
    "ASX200": {
        "name": "Australia 200 (ASX 200)", "asset_class": "INDEX",
        "daily_regime": "Cautious Consolidation", "weekly_regime": "Cautious Consolidation",
        "starting_point": 8770.20, "delta": 58.90,
        "res1": 8829.10, "sl_res1": 8858.60, "res2": 8888.10, "sl_res2": 8917.60,
        "sup1": 8711.30, "sl_sup1": 8681.80, "sup2": 8652.30, "sl_sup2": 8622.80,
        "client_long_pct": 88.0, "client_short_pct": 12.0,
        "indicators": {"ma_short": "Neutral", "ma_long": "Bearish", "dmi": "Neutral", "adx": "Trending", "rsi": "Neutral", "bb": "Neutral"},
        "conformist_strategy": "Sell 1st Resistance only after significant reversal; Buy 1st Support only after significant reversal",
        "contrarian_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above"
    },
    "HK50": {
        "name": "Hong Kong 50 (Hang Seng)", "asset_class": "INDEX",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Cautious Consolidation",
        "starting_point": 23115.0, "delta": 241.0,
        "res1": 23356.0, "sl_res1": 23476.0, "res2": 23597.0, "sl_res2": 23717.0,
        "sup1": 22875.0, "sl_sup1": 22754.0, "sup2": 22634.0, "sl_sup2": 22513.0,
        "client_long_pct": 88.0, "client_short_pct": 12.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Bearish", "dmi": "Negative", "adx": "Trending", "rsi": "Oversold", "bb": "Lower Extreme"},
        "conformist_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Sell 1st Resistance only after a reversal; Buy 1st Support only after a reversal"
    },
    "JP225": {
        "name": "Japan 225 (Nikkei 225)", "asset_class": "INDEX",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Cautious Consolidation",
        "starting_point": 62112.0, "delta": 977.0,
        "res1": 63089.0, "sl_res1": 63577.0, "res2": 64065.0, "sl_res2": 64554.0,
        "sup1": 61135.0, "sl_sup1": 60646.0, "sup2": 60158.0, "sl_sup2": 59669.0,
        "client_long_pct": 79.0, "client_short_pct": 21.0,
        "institutional_long_pct": 66.0, "institutional_short_pct": 34.0,
        "leveraged_funds_long_pct": 46.0, "leveraged_funds_short_pct": 54.0,
        "asset_managers_long_pct": 95.0, "asset_managers_short_pct": 5.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Bearish", "dmi": "Negative", "adx": "Consolidation", "rsi": "Neutral", "bb": "Lower Extreme"},
        "conformist_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Sell 1st Resistance only after a reversal; Buy 1st Support only after a reversal"
    },
    "NVDA": {
        "name": "NVIDIA Corp", "asset_class": "EQUITY",
        "daily_regime": "Cautious Consolidation", "weekly_regime": "Consolidation - Volatile",
        "starting_point": 212.22, "delta": 3.53,
        "res1": 215.75, "sl_res1": 217.52, "res2": 219.28, "sl_res2": 221.05,
        "sup1": 208.69, "sl_sup1": 206.92, "sup2": 205.16, "sl_sup2": 203.39,
        "client_long_pct": 94.0, "client_short_pct": 6.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Neutral", "dmi": "Negative", "adx": "Consolidation", "rsi": "Neutral", "bb": "Lower Extreme"},
        "conformist_strategy": "Sell 1st Resistance only after significant reversal; Buy 1st Support only after significant reversal",
        "contrarian_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above"
    },
    "TSLA": {
        "name": "Tesla Inc", "asset_class": "EQUITY",
        "daily_regime": "Cautious Consolidation", "weekly_regime": "Bear Average",
        "starting_point": 373.20, "delta": 7.56,
        "res1": 380.76, "sl_res1": 384.54, "res2": 388.32, "sl_res2": 392.10,
        "sup1": 365.64, "sl_sup1": 361.86, "sup2": 358.08, "sl_sup2": 354.30,
        "client_long_pct": 85.0, "client_short_pct": 15.0,
        "indicators": {"ma_short": "Bullish", "ma_long": "Neutral", "dmi": "Positive", "adx": "Consolidation", "rsi": "Neutral", "bb": "Neutral"},
        "conformist_strategy": "Sell 1st Resistance only after significant reversal; Buy 1st Support only after significant reversal",
        "contrarian_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above"
    },
    "AMZN": {
        "name": "Amazon.com Inc", "asset_class": "EQUITY",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Cautious Consolidation",
        "starting_point": 250.70, "delta": 3.85,
        "res1": 254.55, "sl_res1": 256.48, "res2": 258.40, "sl_res2": 260.33,
        "sup1": 246.85, "sl_sup1": 244.92, "sup2": 243.00, "sl_sup2": 241.07,
        "client_long_pct": 96.0, "client_short_pct": 4.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Neutral", "dmi": "Neutral", "adx": "Consolidation", "rsi": "Neutral", "bb": "Neutral"},
        "conformist_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Sell 1st Resistance only after a reversal; Buy 1st Support only after a reversal"
    },
    "AAPL": {
        "name": "Apple Inc", "asset_class": "EQUITY",
        "daily_regime": "Cautious Consolidation", "weekly_regime": "Bull Average",
        "starting_point": 348.42, "delta": 4.27,
        "res1": 352.69, "sl_res1": 354.82, "res2": 356.95, "sl_res2": 359.09,
        "sup1": 344.15, "sl_sup1": 342.02, "sup2": 339.89, "sl_sup2": 337.75,
        "client_long_pct": 91.0, "client_short_pct": 9.0,
        "indicators": {"ma_short": "Bullish", "ma_long": "Bullish", "dmi": "Neutral", "adx": "Consolidation", "rsi": "Neutral", "bb": "Upper Extreme"},
        "conformist_strategy": "Sell 1st Resistance only after significant reversal; Buy 1st Support only after significant reversal",
        "contrarian_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above"
    },
    "MSFT": {
        "name": "Microsoft Corp", "asset_class": "EQUITY",
        "daily_regime": "Cautious Consolidation", "weekly_regime": "Bull Average",
        "starting_point": 520.84, "delta": 7.63,
        "res1": 528.47, "sl_res1": 532.28, "res2": 536.09, "sl_res2": 539.90,
        "sup1": 513.21, "sl_sup1": 509.40, "sup2": 505.59, "sl_sup2": 501.78,
        "client_long_pct": 91.0, "client_short_pct": 9.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Bullish", "dmi": "Neutral", "adx": "Trending", "rsi": "Neutral", "bb": "Neutral"},
        "conformist_strategy": "Sell 1st Resistance only after significant reversal; Buy 1st Support only after significant reversal",
        "contrarian_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above"
    },
    "GOLD": {
        "name": "Gold (Spot / Futures CFD)", "asset_class": "COMMODITY",
        "daily_regime": "Bear Average", "weekly_regime": "Cautious Consolidation",
        "starting_point": 4023.61, "delta": 45.41,
        "res1": 4069.02, "sl_res1": 4091.73, "res2": 4114.43, "sl_res2": 4137.14,
        "sup1": 3978.20, "sl_sup1": 3955.49, "sup2": 3932.79, "sl_sup2": 3910.08,
        "weekly_starting_point": 4165.21,
        "weekly_res1": 4300.15, "weekly_sl_res1": 4367.63, "weekly_res2": 4435.10, "weekly_sl_res2": 4502.57,
        "weekly_sup1": 4030.27, "weekly_sl_sup1": 3962.79, "weekly_sup2": 3895.32, "weekly_sl_sup2": 3827.85,
        "client_long_pct": 84.0, "client_short_pct": 16.0,
        "institutional_long_pct": 87.0, "institutional_short_pct": 13.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Bearish", "dmi": "Negative", "adx": "Trending", "rsi": "Neutral", "bb": "Lower Extreme"},
        "conformist_strategy": "Sell 1st Resistance level only after significant reversal; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Buy 1st Support only after a reversal; Buy 1st Resistance upon breakout from below"
    },
    "SILVER": {
        "name": "Silver (XAGUSD)", "asset_class": "COMMODITY",
        "daily_regime": "Bear Average", "weekly_regime": "Cautious Consolidation",
        "starting_point": 54.56, "delta": 1.22,
        "res1": 55.78, "sl_res1": 56.39, "res2": 57.00, "sl_res2": 57.61,
        "sup1": 53.33, "sl_sup1": 52.72, "sup2": 52.11, "sl_sup2": 51.50,
        "weekly_starting_point": 56.94,
        "weekly_res1": 61.09, "weekly_sl_res1": 63.16, "weekly_res2": 65.23, "weekly_sl_res2": 67.30,
        "weekly_sup1": 52.80, "weekly_sl_sup1": 50.73, "weekly_sup2": 48.65, "weekly_sl_sup2": 46.58,
        "client_long_pct": 92.0, "client_short_pct": 8.0,
        "institutional_long_pct": 75.0, "institutional_short_pct": 25.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Bearish", "dmi": "Negative", "adx": "Trending", "rsi": "Neutral", "bb": "Lower Extreme"},
        "conformist_strategy": "Sell 1st Resistance level only after significant reversal; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Buy 1st Support only after a reversal; Buy 1st Resistance upon breakout from below"
    },
    "OIL_CRUDE": {
        "name": "Crude Oil (WTI)", "asset_class": "COMMODITY",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Consolidation - Volatile",
        "starting_point": 98.88, "delta": 2.52,
        "res1": 101.40, "sl_res1": 102.65, "res2": 103.91, "sl_res2": 105.16,
        "sup1": 96.37, "sl_sup1": 95.11, "sup2": 93.86, "sl_sup2": 92.60,
        "weekly_starting_point": 98.92,
        "weekly_res1": 105.19, "weekly_sl_res1": 108.32, "weekly_res2": 111.46, "weekly_sl_res2": 114.59,
        "weekly_sup1": 92.65, "weekly_sl_sup1": 89.51, "weekly_sup2": 86.38, "weekly_sl_sup2": 83.25,
        "client_long_pct": 39.0, "client_short_pct": 61.0,
        "institutional_long_pct": 74.0, "institutional_short_pct": 26.0,
        "indicators": {"ma_short": "Bullish", "ma_long": "Bullish", "dmi": "Positive", "adx": "Trending", "rsi": "Neutral", "bb": "Upper Extreme"},
        "conformist_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Sell 1st Resistance only after a reversal; Buy 1st Support only after a reversal"
    },
    "NATURAL_GAS": {
        "name": "Natural Gas", "asset_class": "COMMODITY",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Cautious Consolidation",
        "starting_point": 3.167, "delta": 0.078,
        "res1": 3.245, "sl_res1": 3.284, "res2": 3.323, "sl_res2": 3.363,
        "sup1": 3.088, "sl_sup1": 3.049, "sup2": 3.010, "sl_sup2": 2.970,
        "client_long_pct": 79.0, "client_short_pct": 21.0,
        "institutional_long_pct": 35.0, "institutional_short_pct": 65.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Bullish", "dmi": "Neutral", "adx": "Trending", "rsi": "Neutral", "bb": "Neutral"},
        "conformist_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above",
        "contrarian_strategy": "Sell 1st Resistance only after a reversal; Buy 1st Support only after a reversal"
    },
    "EURUSD": {
        "name": "EUR/USD", "asset_class": "FOREX",
        "daily_regime": "Bear Average", "weekly_regime": "Consolidation - Negative Bias",
        "starting_point": 1.1221, "delta": 0.0032,
        "res1": 1.1253, "sl_res1": 1.1269, "res2": 1.1285, "sl_res2": 1.1301,
        "sup1": 1.1189, "sl_sup1": 1.1172, "sup2": 1.1156, "sl_sup2": 1.1140,
        "client_long_pct": 64.0, "client_short_pct": 36.0,
        "institutional_long_pct": 38.0, "institutional_short_pct": 62.0,
        "leveraged_funds_long_pct": 39.0, "leveraged_funds_short_pct": 61.0,
        "asset_managers_long_pct": 62.0, "asset_managers_short_pct": 38.0,
        "indicators": {"ma_short": "Neutral", "ma_long": "Bearish", "dmi": "Negative", "adx": "Trending", "rsi": "Oversold", "bb": "Neutral"}
    },
    "GBPUSD": {
        "name": "GBP/USD", "asset_class": "FOREX",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Cautious Consolidation",
        "starting_point": 1.3403, "delta": 0.0041,
        "res1": 1.3444, "sl_res1": 1.3465, "res2": 1.3486, "sl_res2": 1.3507,
        "sup1": 1.3361, "sl_sup1": 1.3340, "sup2": 1.3320, "sl_sup2": 1.3299,
        "client_long_pct": 63.0, "client_short_pct": 37.0,
        "institutional_long_pct": 23.0, "institutional_short_pct": 77.0,
        "leveraged_funds_long_pct": 55.0, "leveraged_funds_short_pct": 45.0,
        "asset_managers_long_pct": 10.0, "asset_managers_short_pct": 90.0,
        "indicators": {"ma_short": "Bullish", "ma_long": "Neutral", "dmi": "Neutral", "adx": "Trending", "rsi": "Neutral", "bb": "Upper Extreme"}
    },
    "EURGBP": {
        "name": "EUR/GBP", "asset_class": "FOREX",
        "daily_regime": "Bear Average", "weekly_regime": "Consolidation - Volatile",
        "starting_point": 0.8371, "delta": 0.0013,
        "res1": 0.8384, "sl_res1": 0.8390, "res2": 0.8397, "sl_res2": 0.8404,
        "sup1": 0.8358, "sl_sup1": 0.8351, "sup2": 0.8345, "sl_sup2": 0.8338,
        "client_long_pct": 75.0, "client_short_pct": 25.0,
        "institutional_long_pct": 47.0, "institutional_short_pct": 53.0,
        "leveraged_funds_long_pct": 61.0, "leveraged_funds_short_pct": 39.0,
        "asset_managers_long_pct": 77.0, "asset_managers_short_pct": 23.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Bearish", "dmi": "Negative", "adx": "Trending", "rsi": "Oversold", "bb": "Lower Extreme"}
    },
    "USDJPY": {
        "name": "USD/JPY", "asset_class": "FOREX",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Cautious Consolidation",
        "starting_point": 156.54, "delta": 0.62,
        "res1": 157.16, "sl_res1": 157.48, "res2": 157.79, "sl_res2": 158.10,
        "sup1": 155.91, "sl_sup1": 155.60, "sup2": 155.29, "sl_sup2": 154.97,
        "client_long_pct": 54.0, "client_short_pct": 46.0,
        "institutional_long_pct": 42.0, "institutional_short_pct": 58.0,
        "leveraged_funds_long_pct": 60.0, "leveraged_funds_short_pct": 40.0,
        "asset_managers_long_pct": 35.0, "asset_managers_short_pct": 65.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Bearish", "dmi": "Neutral", "adx": "Consolidation", "rsi": "Neutral", "bb": "Lower Extreme"}
    },
    "AUDUSD": {
        "name": "AUD/USD", "asset_class": "FOREX",
        "daily_regime": "Bear Average", "weekly_regime": "Cautious Consolidation",
        "starting_point": 0.7019, "delta": 0.0023,
        "res1": 0.7042, "sl_res1": 0.7054, "res2": 0.7065, "sl_res2": 0.7077,
        "sup1": 0.6996, "sl_sup1": 0.6985, "sup2": 0.6973, "sl_sup2": 0.6962,
        "client_long_pct": 63.0, "client_short_pct": 37.0,
        "institutional_long_pct": 31.0, "institutional_short_pct": 69.0,
        "leveraged_funds_long_pct": 70.0, "leveraged_funds_short_pct": 30.0,
        "asset_managers_long_pct": 30.0, "asset_managers_short_pct": 70.0,
        "indicators": {"ma_short": "Bullish", "ma_long": "Bearish", "dmi": "Neutral", "adx": "Trending", "rsi": "Neutral", "bb": "Upper Extreme"}
    },
    "USDCAD": {
        "name": "USD/CAD", "asset_class": "FOREX",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Consolidation - Positive Bias",
        "starting_point": 1.4002, "delta": 0.0035,
        "res1": 1.4037, "sl_res1": 1.4054, "res2": 1.4072, "sl_res2": 1.4089,
        "sup1": 1.3967, "sl_sup1": 1.3950, "sup2": 1.3932, "sl_sup2": 1.3915,
        "client_long_pct": 45.0, "client_short_pct": 55.0,
        "institutional_long_pct": 67.0, "institutional_short_pct": 33.0,
        "leveraged_funds_long_pct": 82.0, "leveraged_funds_short_pct": 18.0,
        "asset_managers_long_pct": 57.0, "asset_managers_short_pct": 43.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Neutral", "dmi": "Negative", "adx": "Trending", "rsi": "Neutral", "bb": "Lower Extreme"}
    },
    "USDCHF": {
        "name": "USD/CHF", "asset_class": "FOREX",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Consolidation - Positive Bias",
        "starting_point": 0.8199, "delta": 0.0030,
        "res1": 0.8229, "sl_res1": 0.8244, "res2": 0.8259, "sl_res2": 0.8274,
        "sup1": 0.8169, "sl_sup1": 0.8154, "sup2": 0.8139, "sl_sup2": 0.8124,
        "client_long_pct": 72.0, "client_short_pct": 28.0,
        "institutional_long_pct": 64.0, "institutional_short_pct": 36.0,
        "leveraged_funds_long_pct": 71.0, "leveraged_funds_short_pct": 29.0,
        "asset_managers_long_pct": 70.0, "asset_managers_short_pct": 30.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Bullish", "dmi": "Neutral", "adx": "Trending", "rsi": "Neutral", "bb": "Lower Extreme"}
    },
    "GBPJPY": {
        "name": "GBP/JPY", "asset_class": "FOREX",
        "daily_regime": "Cautious Consolidation", "weekly_regime": "Cautious Consolidation",
        "starting_point": 209.81, "delta": 0.81,
        "res1": 210.62, "sl_res1": 211.02, "res2": 211.43, "sl_res2": 211.84,
        "sup1": 208.99, "sl_sup1": 208.59, "sup2": 208.18, "sl_sup2": 207.77,
        "client_long_pct": 67.0, "client_short_pct": 33.0,
        "indicators": {"ma_short": "Neutral", "ma_long": "Bearish", "dmi": "Neutral", "adx": "Consolidation", "rsi": "Neutral", "bb": "Neutral"}
    },
    "BTCUSD": {
        "name": "Bitcoin (BTC/USD)", "asset_class": "CRYPTO",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Consolidation - Volatile",
        "starting_point": 81287.0, "delta": 1255.0,
        "res1": 82542.0, "sl_res1": 83170.0, "res2": 83797.0, "sl_res2": 84425.0,
        "sup1": 80032.0, "sl_sup1": 79404.0, "sup2": 78777.0, "sl_sup2": 78149.0,
        "client_long_pct": 86.0, "client_short_pct": 14.0,
        "institutional_long_pct": 54.0, "institutional_short_pct": 46.0,
        "leveraged_funds_long_pct": 33.0, "leveraged_funds_short_pct": 67.0,
        "asset_managers_long_pct": 78.0, "asset_managers_short_pct": 22.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Neutral", "dmi": "Neutral", "adx": "Consolidation", "rsi": "Neutral", "bb": "Neutral"}
    },
    "ETHUSD": {
        "name": "Ether (ETH/USD)", "asset_class": "CRYPTO",
        "daily_regime": "Consolidation - Volatile", "weekly_regime": "Consolidation - Volatile",
        "starting_point": 2385.30, "delta": 53.0,
        "res1": 2438.30, "sl_res1": 2464.80, "res2": 2491.20, "sl_res2": 2517.70,
        "sup1": 2332.30, "sl_sup1": 2305.80, "sup2": 2279.30, "sl_sup2": 2252.80,
        "client_long_pct": 89.0, "client_short_pct": 11.0,
        "institutional_long_pct": 53.0, "institutional_short_pct": 47.0,
        "leveraged_funds_long_pct": 24.0, "leveraged_funds_short_pct": 76.0,
        "asset_managers_long_pct": 42.0, "asset_managers_short_pct": 58.0,
        "indicators": {"ma_short": "Bearish", "ma_long": "Neutral", "dmi": "Negative", "adx": "Trending", "rsi": "Neutral", "bb": "Neutral"}
    }
}

# In-Memory Cache for live broker sentiments
_LIVE_SENTIMENT_CACHE: Dict[str, Tuple[float, Dict[str, Any]]] = {}
_SENTIMENT_CACHE_TTL = 300.0  # 5 minutes


class CapitalMarketReportEngine:
    """
    Capital.com Daily Market Report, Contrarian Sentiment & Broker S/R Stop Cluster Engine.
    Invariant 99 Certified Institutional Quantitative Intelligence.
    """

    @classmethod
    def normalize_epic_key(cls, epic: str) -> str:
        """Maps various broker symbols to canonical report registry keys."""
        s = str(epic or "").upper().strip()
        if any(g in s for g in ["GOLD", "XAU"]):
            return "GOLD"
        elif any(slv in s for slv in ["SILVER", "XAG"]):
            return "SILVER"
        elif any(u in s for u in ["US500", "SP500", "S&P"]):
            return "US500"
        elif any(u in s for u in ["US100", "TECH100", "NASDAQ", "NDX"]):
            return "US100"
        elif any(u in s for u in ["US30", "WALLSTREET", "DOW"]):
            return "US30"
        elif any(d in s for d in ["DE40", "GERMANY40", "DAX"]):
            return "DE40"
        elif any(o in s for o in ["OIL_CRUDE", "CRUDE", "WTI", "USOIL"]):
            return "OIL_CRUDE"
        elif any(r in s for r in ["RUSSELL", "US2000"]):
            return "US2000"
        elif any(k in s for k in ["UK100", "FTSE"]):
            return "UK100"
        elif any(a in s for a in ["ASX", "AU200"]):
            return "ASX200"
        elif any(h in s for h in ["HK50", "HSI", "HONGKONG"]):
            return "HK50"
        elif any(j in s for j in ["JP225", "NIKKEI", "JAPAN225"]):
            return "JP225"
        elif any(ng in s for ng in ["NATGAS", "NATURAL_GAS"]):
            return "NATURAL_GAS"
        elif "NVDA" in s or "NVIDIA" in s:
            return "NVDA"
        elif "TSLA" in s or "TESLA" in s:
            return "TSLA"
        elif "AMZN" in s or "AMAZON" in s:
            return "AMZN"
        elif "AAPL" in s or "APPLE" in s:
            return "AAPL"
        elif "MSFT" in s or "MICROSOFT" in s:
            return "MSFT"
        elif "EURUSD" in s:
            return "EURUSD"
        elif "GBPUSD" in s:
            return "GBPUSD"
        elif "EURGBP" in s:
            return "EURGBP"
        elif "USDJPY" in s:
            return "USDJPY"
        elif "AUDUSD" in s:
            return "AUDUSD"
        elif "USDCAD" in s:
            return "USDCAD"
        elif "USDCHF" in s:
            return "USDCHF"
        elif "GBPJPY" in s:
            return "GBPJPY"
        elif any(b in s for b in ["BTCUSD", "BITCOIN"]):
            return "BTCUSD"
        elif any(e in s for e in ["ETHUSD", "ETHER"]):
            return "ETHUSD"
        return s

    @classmethod
    def get_oct23_2026_report_data(cls, epic: str) -> Optional[Dict[str, Any]]:
        """Retrieves exact transcribed report data from Friday, October 23, 2026."""
        key = cls.normalize_epic_key(epic)
        return CAPITAL_OCT23_2026_REPORT_REGISTRY.get(key)

    @classmethod
    def get_all_oct23_2026_reports(cls) -> Dict[str, Dict[str, Any]]:
        """Returns the full 28-asset registry from Friday, October 23, 2026."""
        return dict(CAPITAL_OCT23_2026_REPORT_REGISTRY)

    @classmethod
    def get_market_report_data(
        cls,
        epic: str,
        current_price: float = 0.0,
        daily_atr: float = 0.0
    ) -> Dict[str, Any]:
        """
        Retrieves Monte Safieddine Market Report benchmarks for the given asset.
        If current_price has drifted from the benchmark starting point, it dynamically
        scales S/R and Stop Loss levels using the exact Monte Safieddine volatility formula:
          Res1 = P0 + Delta, SL_Res1 = Res1 + 0.5*Delta
          Res2 = Res1 + Delta, SL_Res2 = Res2 + 0.5*Delta
          Sup1 = P0 - Delta, SL_Sup1 = Sup1 - 0.5*Delta
          Sup2 = Sup1 - Delta, SL_Sup2 = Sup2 - 0.5*Delta
        """
        key = cls.normalize_epic_key(epic)
        report = CAPITAL_DAILY_REPORT_REGISTRY.get(key)
        if not report:
            # Fallback algorithmic generation for assets not in the core 12
            p0 = current_price if current_price > 0 else 100.0
            delta = daily_atr if daily_atr > 0 else max(0.012 * p0, 1.0)
            res1 = round(p0 + delta, 2)
            sl_res1 = round(res1 + 0.5 * delta, 2)
            res2 = round(res1 + delta, 2)
            sl_res2 = round(res2 + 0.5 * delta, 2)
            sup1 = round(p0 - delta, 2)
            sl_sup1 = round(sup1 - 0.5 * delta, 2)
            sup2 = round(sup1 - delta, 2)
            sl_sup2 = round(sup2 - 0.5 * delta, 2)
            return {
                "key": key,
                "is_registered": False,
                "daily_regime": "Consolidation - Volatile",
                "weekly_regime": "Consolidation - Volatile",
                "starting_point": p0,
                "delta": delta,
                "res1": res1, "sl_res1": sl_res1,
                "res2": res2, "sl_res2": sl_res2,
                "sup1": sup1, "sl_sup1": sl_sup1,
                "sup2": sup2, "sl_sup2": sl_sup2,
                "client_long_pct": 50.0, "client_short_pct": 50.0,
                "leveraged_funds_long_pct": 50.0, "leveraged_funds_short_pct": 50.0,
                "asset_managers_long_pct": 50.0, "asset_managers_short_pct": 50.0,
                "conformist_strategy": "Sell 1st Resistance only after significant reversal; Buy 1st Support only after significant reversal",
                "contrarian_strategy": "Buy 1st Resistance upon breakout from below; Sell 1st Support upon breakout from above",
            }

        # If live price is provided and drifted > 3.0%, synthesize fresh dynamic levels
        bench_p0 = float(report["starting_point"])
        delta = float(report["delta"])
        if current_price > 0 and abs(current_price - bench_p0) / bench_p0 > 0.03:
            p0 = current_price
            if daily_atr > 0:
                delta = daily_atr
            else:
                pct_delta = delta / bench_p0
                delta = round(p0 * pct_delta, 2)
            res1 = round(p0 + delta, 2)
            sl_res1 = round(res1 + 0.5 * delta, 2)
            res2 = round(res1 + delta, 2)
            sl_res2 = round(res2 + 0.5 * delta, 2)
            sup1 = round(p0 - delta, 2)
            sl_sup1 = round(sup1 - 0.5 * delta, 2)
            sup2 = round(sup1 - delta, 2)
            sl_sup2 = round(sup2 - 0.5 * delta, 2)
        else:
            p0 = bench_p0
            res1 = float(report["res1"])
            sl_res1 = float(report["sl_res1"])
            res2 = float(report["res2"])
            sl_res2 = float(report["sl_res2"])
            sup1 = float(report["sup1"])
            sl_sup1 = float(report["sl_sup1"])
            sup2 = float(report["sup2"])
            sl_sup2 = float(report["sl_sup2"])

        res = dict(report)
        res.update({
            "key": key,
            "is_registered": True,
            "starting_point": p0,
            "delta": delta,
            "res1": res1, "sl_res1": sl_res1,
            "res2": res2, "sl_res2": sl_res2,
            "sup1": sup1, "sl_sup1": sl_sup1,
            "sup2": sup2, "sl_sup2": sl_sup2,
        })
        return res

    @classmethod
    def fetch_live_client_sentiment(cls, epic: str, engine: Optional[Any] = None) -> Dict[str, Any]:
        """
        Queries Capital.com REST API for live client sentiment:
        Endpoint: GET /api/v1/clients/sentiment or market sentiment details.
        Falls back seamlessly to in-memory institutional report cache.
        """
        now = time.time()
        key = cls.normalize_epic_key(epic)
        if key in _LIVE_SENTIMENT_CACHE:
            ts, data = _LIVE_SENTIMENT_CACHE[key]
            if now - ts < _SENTIMENT_CACHE_TTL:
                return data

        # Attempt to fetch live from Capital.com broker engine
        client_long = None
        client_short = None
        source = "REPORT_BENCHMARK"

        if engine is not None and hasattr(engine, "session"):
            try:
                # Capital.com API endpoint for client sentiment
                url = f"{engine.base_url}/api/v1/clients/sentiment"
                headers = engine._get_headers() if hasattr(engine, "_get_headers") else {}
                resp = engine.session.get(url, headers=headers, timeout=3.5)
                if resp.status_code == 200:
                    payload = resp.json()
                    # Payload format: {"clientSentiments": [{"marketId": "...", "longPositionPercentage": 72.0, "shortPositionPercentage": 28.0}]}
                    sentiments = payload.get("clientSentiments") or payload.get("sentiments", [])
                    resolved_epic = engine.EPIC_MAP.get(epic, epic) if hasattr(engine, "EPIC_MAP") else epic
                    for item in sentiments:
                        m_id = str(item.get("marketId") or item.get("epic") or "").upper()
                        if m_id == resolved_epic.upper() or m_id == key:
                            client_long = float(item.get("longPositionPercentage", 50.0))
                            client_short = float(item.get("shortPositionPercentage", 50.0))
                            source = "LIVE_BROKER_API"
                            break
            except Exception as e:
                logger.debug(f"Capital client sentiment live fetch note: {e}")

        # Fallback to institutional report benchmark
        if client_long is None:
            rep = CAPITAL_DAILY_REPORT_REGISTRY.get(key)
            if rep:
                client_long = float(rep.get("client_long_pct", 50.0))
                client_short = float(rep.get("client_short_pct", 50.0))
            else:
                client_long = 50.0
                client_short = 50.0

        res = {
            "epic": epic,
            "canonical_key": key,
            "client_long_pct": round(client_long, 1),
            "client_short_pct": round(client_short, 1),
            "source": source,
            "timestamp": now,
        }
        _LIVE_SENTIMENT_CACHE[key] = (now, res)
        return res

    @classmethod
    def evaluate_contrarian_sentiment_edge(
        cls,
        epic: str,
        proposed_side: str,
        current_price: float,
        engine: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Pillar 1: Contrarian Sentiment Arbitrage & Retail Liquidity Trap Guard.
        Exploits the mathematical reality that 79.75% of CFD retail accounts lose money.
        - Extreme Retail Long (>= 80%): Vetoes FOMO BUYs at resistance; Boosts Contrarian SELLS.
        - Extreme Retail Short (>= 75%): Vetoes Panic SELLS at support; Boosts Contrarian BUYS.
        """
        side = str(proposed_side or "").upper().strip()
        norm_side = "BUY" if side in ["BUY", "LONG"] else ("SELL" if side in ["SELL", "SHORT"] else "HOLD")
        sent = cls.fetch_live_client_sentiment(epic, engine=engine)
        c_long = sent.get("client_long_pct", 50.0)
        c_short = sent.get("client_short_pct", 50.0)

        rep = cls.get_market_report_data(epic, current_price=current_price)
        lev_funds_short = float(rep.get("leveraged_funds_short_pct", 50.0))
        lev_funds_long = float(rep.get("leveraged_funds_long_pct", 50.0))

        score_boost = 0.0
        is_vetoed = False
        veto_reason = None
        factors = []

        # Case 1: Extreme Retail Crowd Long Trap (e.g. NVDA 94%, AMZN 95%, AAPL 91%, GOLD 79%)
        if c_long >= 80.0:
            if norm_side == "BUY":
                # If price is at or above Resistance 1, retail is buying the top
                if current_price >= rep["res1"] * 0.995:
                    is_vetoed = True
                    veto_reason = f"RETAIL_EXTREME_LONG_TRAP_VETO: Retail crowd is {c_long:.1f}% LONG at broker Resistance 1 (${rep['res1']:,.2f}). High stop-run trap risk."
                    score_boost = -35.0
                    factors.append(f"RETAIL_CROWD_LONG_TRAP ({c_long:.1f}% Long, -35)")
                else:
                    score_boost -= 15.0
                    factors.append(f"RETAIL_LONG_OVERCROWDED ({c_long:.1f}% Long, -15)")
            elif norm_side == "SELL":
                # Smart money distribution / Turtle Soup Short has massive edge
                score_boost += 30.0
                factors.append(f"CONTRARIAN_SMART_MONEY_SHORT (+30, Retail {c_long:.1f}% Trapped Long)")
                if lev_funds_short >= 60.0:
                    score_boost += 10.0
                    factors.append(f"HEDGE_FUND_SHORT_CONFLUENCE (+10, Leveraged Funds {lev_funds_short:.1f}% Short)")

        # Case 2: Extreme Retail Panic Short Trap (Retail >= 70% Short)
        elif c_short >= 70.0:
            if norm_side == "SELL":
                if current_price <= rep["sup1"] * 1.005:
                    is_vetoed = True
                    veto_reason = f"RETAIL_EXTREME_SHORT_TRAP_VETO: Retail crowd is {c_short:.1f}% SHORT at broker Support 1 (${rep['sup1']:,.2f}). High short squeeze trap risk."
                    score_boost = -35.0
                    factors.append(f"RETAIL_CROWD_SHORT_TRAP ({c_short:.1f}% Short, -35)")
                else:
                    score_boost -= 15.0
                    factors.append(f"RETAIL_SHORT_OVERCROWDED ({c_short:.1f}% Short, -15)")
            elif norm_side == "BUY":
                score_boost += 30.0
                factors.append(f"CONTRARIAN_SMART_MONEY_BUY (+30, Retail {c_short:.1f}% Trapped Short)")
                if lev_funds_long >= 60.0:
                    score_boost += 10.0
                    factors.append(f"HEDGE_FUND_LONG_CONFLUENCE (+10, Leveraged Funds {lev_funds_long:.1f}% Long)")

        # Case 3: Moderate Sentiment Edge
        else:
            if norm_side == "BUY" and c_short > 55.0:
                score_boost += 12.0
                factors.append(f"CONTRARIAN_LONG_EDGE (+12, Retail {c_short:.1f}% Short)")
            elif norm_side == "SELL" and c_long > 60.0:
                score_boost += 12.0
                factors.append(f"CONTRARIAN_SHORT_EDGE (+12, Retail {c_long:.1f}% Long)")

        return {
            "epic": epic,
            "proposed_side": norm_side,
            "client_long_pct": c_long,
            "client_short_pct": c_short,
            "leveraged_funds_short_pct": lev_funds_short,
            "score_boost": score_boost,
            "is_vetoed": is_vetoed,
            "veto_reason": veto_reason,
            "factors": factors,
            "broker_levels": rep,
        }

    @classmethod
    def evaluate_broker_stop_cluster_sweep(
        cls,
        epic: str,
        current_price: float,
        high_wick: float,
        low_wick: float,
        spread: float = 0.50
    ) -> Dict[str, Any]:
        """
        Pillar 2: Exact Broker S/R Stop-Loss Cluster Sweep Reversal.
        Detects when price pierced Monte Safieddine's exact SL for 1st/2nd Resistance or Support
        and immediately rejected back inside the dealing range, confirming a textbook
        Turtle Soup Liquidity Hunt at the broker's pre-calculated stop zones.
        """
        rep = cls.get_market_report_data(epic, current_price=current_price)
        res1 = rep["res1"]
        sl_res1 = rep["sl_res1"]
        res2 = rep["res2"]
        sl_res2 = rep["sl_res2"]
        sup1 = rep["sup1"]
        sl_sup1 = rep["sl_sup1"]
        sup2 = rep["sup2"]
        sl_sup2 = rep["sl_sup2"]
        p0 = rep["starting_point"]

        is_bearish_sweep = False
        is_bullish_sweep = False
        swept_level_name = None
        structural_sl = None
        tp1 = None
        tp2 = None
        desc = None

        # Check Bearish Stop Run (Wick pierced SL for Resistance, but closed back below Resistance)
        if high_wick >= sl_res1 and current_price < res1:
            is_bearish_sweep = True
            swept_level_name = "BROKER_SL_RESISTANCE_1"
            structural_sl = round(high_wick + max(2.0 * spread, 0.0010 * current_price), 2)
            tp1 = round(p0, 2)
            tp2 = round(sup1, 2)
            desc = f"Bearish Stop-Run: Pierced Broker SL Res1 (${sl_res1:,.2f}) and rejected below Res1 (${res1:,.2f})"
        elif high_wick >= sl_res2 and current_price < res2:
            is_bearish_sweep = True
            swept_level_name = "BROKER_SL_RESISTANCE_2"
            structural_sl = round(high_wick + max(2.0 * spread, 0.0010 * current_price), 2)
            tp1 = round(res1, 2)
            tp2 = round(p0, 2)
            desc = f"Bearish Mega Stop-Run: Pierced Broker SL Res2 (${sl_res2:,.2f}) and rejected below Res2 (${res2:,.2f})"

        # Check Bullish Stop Run (Wick pierced SL for Support, but closed back above Support)
        elif low_wick <= sl_sup1 and current_price > sup1:
            is_bullish_sweep = True
            swept_level_name = "BROKER_SL_SUPPORT_1"
            structural_sl = round(low_wick - max(2.0 * spread, 0.0010 * current_price), 2)
            tp1 = round(p0, 2)
            tp2 = round(res1, 2)
            desc = f"Bullish Stop-Run: Pierced Broker SL Sup1 (${sl_sup1:,.2f}) and rejected above Sup1 (${sup1:,.2f})"
        elif low_wick <= sl_sup2 and current_price > sup2:
            is_bullish_sweep = True
            swept_level_name = "BROKER_SL_SUPPORT_2"
            structural_sl = round(low_wick - max(2.0 * spread, 0.0010 * current_price), 2)
            tp1 = round(sup1, 2)
            tp2 = round(p0, 2)
            desc = f"Bullish Mega Stop-Run: Pierced Broker SL Sup2 (${sl_sup2:,.2f}) and rejected above Sup2 (${sup2:,.2f})"

        return {
            "has_broker_sweep": (is_bearish_sweep or is_bullish_sweep),
            "sweep_direction": "SELL" if is_bearish_sweep else ("BUY" if is_bullish_sweep else None),
            "swept_level_name": swept_level_name,
            "structural_sl": structural_sl,
            "tp1_target": tp1,
            "tp2_target": tp2,
            "description": desc,
            "broker_levels": rep,
        }

    @classmethod
    def evaluate_market_report_confluence(
        cls,
        epic: str,
        proposed_side: str,
        current_price: float,
        atr_15m: float,
        spread: float,
        high_wick: Optional[float] = None,
        low_wick: Optional[float] = None,
        engine: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Pillar 3: Master Confluence Aggregator for SuperSmartCapitalCitadel.
        Combines Contrarian Sentiment Arbitrage with Exact Broker S/R Stop Sweeps.
        """
        norm_side = "BUY" if str(proposed_side).upper() in ["BUY", "LONG"] else "SELL"
        sent_eval = cls.evaluate_contrarian_sentiment_edge(
            epic=epic,
            proposed_side=norm_side,
            current_price=current_price,
            engine=engine
        )

        h_w = high_wick if high_wick is not None else current_price
        l_w = low_wick if low_wick is not None else current_price

        sweep_eval = cls.evaluate_broker_stop_cluster_sweep(
            epic=epic,
            current_price=current_price,
            high_wick=h_w,
            low_wick=l_w,
            spread=spread
        )

        total_boost = sent_eval["score_boost"]
        factors = list(sent_eval["factors"])
        is_vetoed = sent_eval["is_vetoed"]
        veto_reason = sent_eval["veto_reason"]

        structural_sl = None
        tp1 = None
        tp2 = None

        if sweep_eval["has_broker_sweep"]:
            if sweep_eval["sweep_direction"] == norm_side:
                total_boost += 35.0
                factors.append(f"BROKER_SL_CLUSTER_SWEEP_CONFIRMED (+35, {sweep_eval['swept_level_name']})")
                structural_sl = sweep_eval["structural_sl"]
                tp1 = sweep_eval["tp1_target"]
                tp2 = sweep_eval["tp2_target"]
                # Override minor veto if confirmed broker stop sweep reversal occurred
                if is_vetoed:
                    is_vetoed = False
                    veto_reason = None
            else:
                # Opposite sweep active: trade is counter to broker stop-run momentum
                total_boost -= 25.0
                factors.append(f"COUNTER_BROKER_STOP_RUN (-25, {sweep_eval['swept_level_name']})")

        # Multi-timeframe daily regime bonus
        rep = sent_eval["broker_levels"]
        d_regime = rep.get("daily_regime", "Consolidation - Volatile")
        if "Bull" in d_regime and norm_side == "BUY":
            total_boost += 8.0
            factors.append("DAILY_REGIME_BULL_ALIGNMENT (+8)")
        elif "Bear" in d_regime and norm_side == "SELL":
            total_boost += 8.0
            factors.append("DAILY_REGIME_BEAR_ALIGNMENT (+8)")

        return {
            "epic": epic,
            "proposed_side": norm_side,
            "score_boost": total_boost,
            "is_vetoed": is_vetoed,
            "veto_reason": veto_reason,
            "factors": factors,
            "structural_sl": structural_sl,
            "tp1": tp1,
            "tp2": tp2,
            "sentiment_data": {
                "client_long_pct": sent_eval["client_long_pct"],
                "client_short_pct": sent_eval["client_short_pct"],
                "leveraged_funds_short_pct": sent_eval["leveraged_funds_short_pct"],
            },
            "broker_levels": rep,
            "has_broker_sweep": sweep_eval["has_broker_sweep"],
            "sweep_desc": sweep_eval["description"],
        }
