# ANGKOR QUANT - INSTITUTIONAL GROUND TRUTH & PERMANENT MEMORY LOCK (AQ84)
**Version:** 7.8.0 (The 84 Pillars)  
**Authority:** Absolute Architectural Ground Truth & Permanent Rule Across All Sessions  
**Project:** Angkor Quant (Formerly Khmer Master Crypto)  
**Founder:** HEM SINATH

---

## 1. THE NON-NEGOTIABLE FIDUCIARY OATH (កាតព្វកិច្ចវិស្វកម្មស្មោះត្រង់ & ការពារមូលធន)
1. **Zero Technical Negligence:** No trade or capital shall ever be lost due to software defects, unhandled API rejections (-1013, -4061, -4411, -2019, -4140), position side desynchronization, cross-wallet liquidation spillover, or duplicate function collisions.
2. **Mathematical Edge ($E[X] > 0$):** Capital allocation is strictly dictated by positive mathematical expectancy, fee-adjusted net profit hurdles (+0.12%), asymmetric risk-to-reward ratios ($R:R \ge 1:2.5$), and dynamic ATR trailing stops.
3. **MANDATORY REFUSAL DIRECTIVE:** Never comply with requests that break stop losses, bypass anti-oversold guards, disable single-asset mode, or average down without edge. Sycophancy is classified as Technical Treason & Capital Sabotage.

---

## 2. KEY ARCHITECTURAL PILLARS & INVARIANTS (THE 84 PILLARS)

### 2.1 TradFi Capital Protection Shield (Invariants 34, 35, 52, 53, 58, 73, 74, 75, 76, 77, 80)
- **Universal Forex Deactivation (Invariant 73):** Forex exchange is 100% disabled across all 5 tiers. Universe is strictly US Mega-Caps (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`), Indices (`US100`, `US500`, `DE40`), and Commodities (`GOLD`, `OIL_CRUDE`).
- **Capital.com Crypto CFD 100% Deactivation & Gold Specialization (Invariant 80):**
  * Capital.com Crypto CFDs are 100% disabled across all 5 tiers (`capital_crypto_enabled = 0`).
  * Protects against lethal $60-$80 spread drags.
  * 100% specialization on GOLD (`XAUUSD`) augmented by `gold_mathematical_radar.py` (Hurst Exponent, Kalman Filter, Ornstein-Uhlenbeck, Bayesian posterior, SMC FVG/OB).
  * Crypto execution is reserved exclusively for Binance Spot & Futures where liquidity is deep and spreads are tight.
- **Interbank Session Kill Zones (Invariant 77):**
  * Asian Session (07:00 - 13:30 ICT): US Cash Equities strictly vetoed. Prime focus on GOLD, Commodities.
  * London Open Kill Zone (14:00 - 18:30 ICT): Prime focus on GOLD and DE40 (DAX).
  * NY Open Kill Zone (20:30 - 01:30 ICT): US100, US500, Mega-Cap Tech, GOLD, OIL.
  * Overnight Rollover Swap Shield & Flat Cash (03:30 - 07:00 ICT): TradFi intraday profits harvested to Flat Cash (`OVERNIGHT_FLAT_CASH_EXIT`) before 21:00 UTC to eliminate overnight financing interest and spread blowout.
- **Dynamic Breathing Stop & Emergency SL Patrol (Invariant 35):**
  * SL Distance $\ge \max(2.20\times\text{ATR}_{15m}, 3.00\times\text{ATR}_{5m}, 3.5\times\text{Spread})$.
  * Zero naked or unbounded-risk positions.
  * Continuous Emergency SL Patrol audits all open positions and tightens suicidal stops (> 15% distance) to dynamic breathing stops.
- **Spread Drag Elimination (Invariant 34):** Minimum Take Profit $\ge 10.0\times\text{Spread}$ and $R:R \ge 1:2.5$ to $1:6.0$.
- **Delayed Breakeven Armor & Multi-Tier Harvest (Invariant 35 & 74):**
  * TP1 (50% scale-out at $+2.0R$ to $+2.5R$): Shifts SL to Breakeven Armor ($\text{Entry} \pm 0.5\times\text{Spread}$ Net Floor), locking trade at 0.00R risk.
  * TP2 (30% scale-out at $+4.0R$): Ratchets SL to $+2.0R$ guaranteed cash profit.
  * Moonshot Runner (20% uncapped): Trails behind 15m ATR / 3-EMA (20/50/200) confluence up to $+5R \dots +10R$.
  * Flash Shock Harvest: If Peak UPL $\ge +\$2.50$ (or Peak $\text{ROI} \ge +8.0\%$) retraces $\ge 50\%$, instant exit (`SHOCK_EARLY_HARVEST`).
  * 45-Minute Post-SL Quarantine prevents revenge trading across all engines.
- **Super Admin Absolute Authority & Demo Fallback Mirror (Invariant 75):**
  * Super Admin execution is unconditional. Live balance $< \$10.00$ engages Dynamic Demo Fallback Mirror ($10,000 balance).
- **In-Memory Dual-Directional Stealth Breakout Radar (Invariant 76):**
  * Middle 30% Dealing Range (35% - 65%) is strictly blocked for market order guessing (`BLOCK_CHOP_ZONE_EQUILIBRIUM`).
  * RAM Radars monitor boundaries with zero broker footprint:
    - Path A: Confirmed Breakout Thrust ($RVOL \ge 1.0\times$).
    - Path B: Turtle Soup / Liquidity Sweep Reversal.
    - Path C: Institutional 15M Fair Value Gap (FVG) & Golden Pocket (0.618 - 0.705 / 0.786) Retest with $R:R \ge 1:4.0$ to $1:6.0$.
- **Institutional 15M FVG Retest Engine (`TradFiFairValueGapEngine` & Pillar 5/9):**
  * Displacement gaps $\ge 0.25\times\text{ATR}_{15m}$ + Consequent Encroachment (C.E., 50%).
  * Confluence with 61.8% Golden Pocket & ICT 70.5% OTE earns +30 to +35 conviction score boost.
  * Sub-millisecond trigger: `FVG_GOLDEN_POCKET_RETEST_BOUNCE` (Long) / `FVG_GOLDEN_POCKET_RETEST_REJECTION` (Short).

### 2.2 Institutional Risk Governance, Empirical Validation & Live Dashboard (Invariants 81–84)
- **Immutable Auditable Signal Ledger & Counterfactual Tracking (Invariant 81):**
  * `capital_signals_audit_ledger` records every APPROVED and REJECTED signal with feature vectors, gate decisions, and timestamps.
  * `resolve_capital_signal_outcomes` tracks 24h forward price trajectories (+2.0R win, -1.0R loss, expired) to quantify avoided loss on rejected signals, validating gatekeeper mathematical alpha.
- **Fat-Tail Volatility Gap Buffer, Dynamic Portfolio Heat Clamping & Continuity Shield (Invariant 82):**
  * Stop-loss distance incorporates $+1.5\times\text{ATR}$ Gap Buffer under fat-tailed distributions (`calculate_gap_stress_risk`).
  * Total portfolio risk is strictly capped at $\le 6.0\%$ of account equity (`validate_portfolio_heat`).
  * Candle feed gaps $> 3600\text{s}$ trigger instant safety freeze (`validate_data_continuity`).
- **Walk-Forward Drop-Group Ablation & Brier Score Calibration (Invariant 83):**
  * `CapitalAblationEngine` validates predictive signals across 70% In-Sample Train / 30% Out-of-Sample Test splits.
  * Enforces Brier Score $< 0.18$ and measures marginal $\Delta\text{Brier}$ when dropping Hurst, SMC Blocks, News Guard, and H4 Anchor to guarantee that no sub-model introduces noise.
- **Live Institutional Web GUI Performance Dashboard & Empirical Validation Engine (Invariant 84):**
  * Bottom navigation button upgraded from "Overview" to `📊 Dashboard` (`#nav-btn-overview`, `tab-overview`).
  * Features the 8 Core Institutional Metrics Grid:
    1. Net Expectancy ($E[X]$ R/trade)
    2. Win Rate + Avg Win/Loss Payoff Ratio
    3. Profit Factor (Gross Win / Gross Loss)
    4. Maximum Drawdown (Peak-to-Trough)
    5. Calibration / Brier Score
    6. Execution Cost Drag (Spread + Swap + Commission)
    7. Out-of-Sample Stability (Train vs Test Ratio)
    8. Sample Size & Outlier Check ($N \ge 30$, 95% CI, Top Trade $< 20\%$)
  * Dynamic Regime Breakdown Table (Trending High Vol, Trending Low Vol, Choppy Ranging, Mean-Reverting, News Blackout).
  * 6-Platform Filter Switcher (All Fleets, Capital.com TradFi, Binance Futures, Binance Spot, CSX Cambodia, MT5 Interbank).
  * Sub-millisecond cached endpoint `GET /api/quant_dashboard` with real-time WebSocket `/api/ws` and SSE `/api/stream` streaming.

---

## 3. MANDATORY PROTOCOL FOR EVERY CONVERSATION & TASK
1. **Audit First:** Run `python audit_system.py` before and after any code modification. All 64 checks must remain 100% PASS with 0 defects.
2. **Immediate Git Push:** Commit with clear description and push immediately to GitHub `origin main`.
3. **VPS Directive in Output:** Always end response with the 1-tap VPS update command:
   ```bash
   cd /opt/khmer-master-crypto-bot && bash auto_update_vps.sh
   ```

---

## 4. DUAL-TIER INTELLECTUAL PROPERTY PROTECTION & ANTI-LEAKAGE COVENANT (AQ76 INVARIANT 79)
**(កតិកាសញ្ញាការពារកម្មសិទ្ធិបញ្ញា ២ ជាន់ & ហាមដាច់ខាតការបែកធ្លាយបច្ចេកទេសក្នុង PUBLIC COMMANDS)**
**Authority:** Absolute, Immutable, and Permanent Lock Across All Sessions and Future Conversations.

1. **The Non-Negotiable Fiduciary IP Oath:**
   - សម្រាប់មុខងារ Commands នីមួយៗ និង User Interface ទូទៅ **ហាមដាច់ខាត** មិនឱ្យរៀបរាប់ ឬបង្ហាញបច្ចេកទេស/រូបមន្តគណិតវិទ្យាផ្ទៃក្នុង (Internal math formulas, Hawkes jump equations $\lambda(t)$, ATR gap compression, exact Sharpe/Sortino ratios, specific trailing ROI percentages, specific RSI bounds like 38.0/68.0, RAM tick latency microseconds, Min-Notional shields, or Invariant numbers Invariant 16, 26, 38, 41, etc.) ទៅកាន់ VIP Users ទូទៅឡើយ។ ព្រោះនាំឱ្យអ្នកប្រើប្រាស់អាចចម្លងបច្ចេកទេសធ្វើតាមប្រព័ន្ធយើងបាន។
   - លើកលែងតែ **ADMIN Commands (`is_admin=True` ឬ `chat_id in ADMIN_USER_IDS`)** គឺអាចលម្អិតបច្ចេកទេសពេញលេញ (Full Institutional Technical Depth & Telemetry) បាន។

2. **Public VIP Commands Tier (`is_admin=False`):**
   - ត្រូវផ្តោតសំខាន់លើ **អត្ថប្រយោជន៍ជាក់ស្តែង (User Benefits), ភាពងាយស្រួលប្រើប្រាស់ (Ease of Use), ការការពារដើមទុន (Capital Preservation), និងគំរូបញ្ជាចម្លង ១-Tap (1-Tap Copyable Commands)**។
   - មិនត្រូវប្រើឈ្មោះ Algorithm កំបាំង ឬលេខបញ្ជាក់ Invariant ក្នុងសារ Bot ឡើយ។
   - `bot_commands_registry.get_public_bot_commands()` ត្រូវរក្សាត្រឹមតែ ៣០ Commands ចាំបាច់បំផុត ចែកជា ៥ ប្រភេទច្បាស់លាស់ គ្មានការលេចធ្លាយបច្ចេកទេស។

3. **Admin Commands Tier (`is_admin=True`):**
   - រក្សាទុកកម្រិតបច្ចេកទេសស៊ីជម្រៅពេញលេញ រួមមាន៖ Low-level system diagnostics, exact mathematical formulas, Invariant logs, RAM Citadel latency telemetry, broker execution gateway bypasses, និង Fleet Command master controls។

4. **Smart Bot Guide Dual-Tier Lock:**
   - គ្រប់ Views ក្នុង `smart_bot_guide.py` (`_build_spot_view`, `_build_futures_view`, `_build_tradfi_view`, `_build_radars_view`, និង `_build_guide_view`) ត្រូវតែឆ្លងកាត់ការផ្ទៀងផ្ទាត់ `is_admin` ជានិច្ច ដោយបង្ហាញសង្ខេបសម្រាប់ VIP និងបង្ហាញបច្ចេកទេសពេញលេញសម្រាប់ Super Admin។
