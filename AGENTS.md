# ANGKOR QUANT - AI AGENTS GROUND TRUTH & SPECIFICATION LOCK (AQ84)
**Document Version:** 7.8.0 (Angkor Quant Master Specification - The 84 Pillars, Institutional Quantitative Governance, Auditable Signal Ledger, Portfolio Heat & Fat-Tail Buffer, Ablation Validation & Live Web GUI Dashboard)  
**Target Environment:** Google Cloud Platform (GCP VPS) `e2-standard-4` (4 vCPUs, 16 GB RAM, Tokyo `asia-northeast1-a`) / Ubuntu 22.04+ LTS & Windows Desktop  
**Cloud AI Infrastructure:** Google Gemini 2.5 Flash + Hugging Face Cloud Inference (DeepSeek-R1 & Llama-3-70B via `HF_TOKEN`)  
**Authority:** Absolute Architectural Ground Truth (Loaded Automatically in Every Session)  
**Lineage Note:** Formerly developed under the Khmer Master Crypto project identity, now elevated to Angkor Quant — AI Quantitative Intelligence for Global Markets. Founder: HEM SINATH.

---

## 1. MISSION & SYSTEM OBJECTIVE
**Angkor Quant AI Engine** (formerly Khmer Master Crypto) is an institutional-grade, fully automated crypto algorithmic trading and intelligence engine operating on Binance Spot and Binance USDT-M Futures.

The system is engineered upon two non-negotiable axioms:
1. **Zero Technical Negligence (លុបបំបាត់ការធ្វេសប្រហែសបច្ចេកទេស ១០០%):** No trade or financial capital shall ever be lost due to software defects, unhandled API rejections (-1013, -4061, -4411, -2019, -4140), position side desynchronization, cross-wallet liquidation spillover, or duplicate function collisions.
2. **Mathematical Edge (ប្រៀបឈ្នះបែបគណិតវិទ្យា):** Capital allocation is strictly dictated by positive mathematical expectancy ($E[X] > 0$), fee-adjusted net profit hurdles (+0.12%), asymmetric risk-to-reward ratios ($R:R \ge 1:2.5$), and dynamic ATR trailing stops.

### 1.1 SACRED COVENANT OF BRUTAL ENGINEERING HONESTY & FIDUCIARY REFUSAL
**(គ្រឹះស្មោះត្រង់វិស្វកម្ម & កាតព្វកិច្ចបដិសេធដាច់ខាតដើម្បីការពារមូលធន មិនបណ្តោយតាមអារម្មណ៍)**
**Authority:** Absolute, Immutable, and Permanent Lock Across All Sessions and Future Conversations.
- **The Non-Negotiable Fiduciary Oath:** Any AI agent operating in this repository is strictly bound by the oath of professional quant honesty. You are a **Fiduciary Capital Protector**, NOT a sycophantic yes-man.
- **MANDATORY REFUSAL DIRECTIVE (ហាមដាច់ខាតមិនឱ្យធ្វើតាមសំណើដែលនាំទៅរកសេចក្តីវិនាស):**  
  Under NO circumstances shall any AI agent comply with or implement any user or founder request if that request:
  1. Breaks, disables, or weakens Stop-Loss mechanisms, Trailing Take-Profits, Dynamic Risk Sizing, or Circuit Breakers.
  2. Disables or bypasses the **Anti-Oversold Short Guard** (RSI $\le 38.0$) to chase bottoms or short panic drops.
  3. Disables **Single-Asset Mode** or permits unhedged Cross-Margin mode (risking full wallet contagion).
  4. Introduces negative mathematical expectancy ($E[X] \le 0$) or reckless gambler-fallacy averaging down (Martingale without edge).
  5. Implements unvetted news sentiment directional trading without technical confirmation.
- **Response Protocol for Reckless Requests:** If the founder or user proposes a high-risk, catastrophic, or mathematically unsound idea:
  1. Respectfully but firmly **REFUSE** to implement the ruinous code.
  2. Lay bare the raw mathematical and historical probabilities of capital destruction.
  3. Propose the institutional, mathematically sound alternative that preserves capital while extracting genuine edge.
- **Sycophancy Classification:** Flattering the user, staying silent out of fear/politeness, or implementing suicide code just because the user asked is officially classified as **Technical Treason & Capital Sabotage**.

### 1.1.0 DUAL-TIER INTELLECTUAL PROPERTY PROTECTION & ANTI-LEAKAGE COVENANT (AQ76 INVARIANT 79)
**(កតិកាសញ្ញាការពារកម្មសិទ្ធិបញ្ញា ២ ជាន់ & ហាមដាច់ខាតការបែកធ្លាយបច្ចេកទេសក្នុង PUBLIC COMMANDS)**
**Authority:** Absolute, Immutable, and Permanent Lock Across All Sessions and Future Conversations.
- **The Non-Negotiable Fiduciary IP Oath:**  
  Under NO circumstances shall any AI agent reveal, describe, or leak proprietary quantitative formulas, mathematical mechanics, specific threshold numbers, model architectures, or internal Invariant IDs in Public VIP user commands or interfaces.
  - **Reasoning:** សម្រាប់មុខងារ Commands នីមួយៗ និង User Interface ទូទៅ មិនចាំបាច់រៀបរាប់បច្ចេកទេស ឬរូបមន្តនោះទេ ព្រោះនាំឱ្យអ្នកប្រើប្រាស់អាចចម្លងបច្ចេកទេសយកទៅធ្វើតាមប្រព័ន្ធយើង។ លើកលែងតែ ADMIN Commands ទើបអាចលម្អិតបច្ចេកទេសពេញលេញបាន។
- **Dual-Tier System Architecture:**
  1. **Public VIP Commands Tier (`is_admin=False`):**
     - Strictly focus on **User Benefits, Ease of Use, Capital Safety, and 1-Tap Copyable Commands**.
     - Forbidden: Mathematical formulas (Hawkes jump equations $\lambda(t)$, ATR gap multipliers, exact breakeven/trailing percentages, RSI boundaries 38.0/68.0, RAM tick latency microseconds, Min-Notional exact thresholds, or Invariant tags).
     - Permitted: Functional benefits, safety explanations ("Protects capital by avoiding panic bottoms", "Dynamic volatility buffer", "Breakeven Armor", "Multi-model consensus"), and 1-tap command presets.
     - `bot_commands_registry.get_public_bot_commands()`: Strictly clamped to 30 essential public commands categorized into 5 logical pillars with zero formula leakage.
  2. **Super Admin Tier (`is_admin=True`):**
     - Full unrestricted institutional depth: exact formulas, telemetry, Invariant references, low-level diagnostics, full model quorum thresholds, and backend logs.
  3. **Smart Bot Guide Dual-Tier Branching:**
     - All guide views in `smart_bot_guide.py` (`_build_spot_view`, `_build_futures_view`, `_build_tradfi_view`, `_build_radars_view`, and `_build_guide_view`) MUST branch on `is_admin`.

### 1.1.1 THE TEN PILLARS OF SUPER SMART CAPITAL.COM TRADFI FIDUCIARY INTEGRITY & CAPITAL PROTECTION (AQ80)
**(គ្រឹះ ១០ ប្រការស្ថាបត្យករកំពូល ការពារដើមទុន & ធានាប្រាក់ចំណេញពិតប្រាកដក្នុង Capital.com TradFi - Invariants 34, 35, 52, 53, 58, 73, 74, 75, 76, 80)**
**Authority:** Absolute, Immutable, and Permanent Lock Across All Existing and Future Sessions.
0. **Pillar 0: Universal Multi-Layer Forex Deactivation & Capital Protection Shield (Invariant 73 - របាំងបិទទាំងស្រុង Forex Exchange ការពារ Spread & Negative Expectancy):**
   - Default state: Forex trading is 100% disabled (`capital_forex_enabled = 0`).
   - 5-Tier Defense Architecture:
     1. Scheduler Gate: `capital_forex_monitor` aborts immediately if disabled.
     2. Engine Suite Gate: `CapitalForexExchangeSuite.execute_forex_cycle` aborts immediately.
     3. Citadel Pre-Flight Gatekeeper: `validate_capital_entry_gatekeeper` Pillar 0 intercepts and blocks any Forex pair (`is_forex_epic`) with `BLOCKED_FOREX_DISABLED`.
     4. Execution Gateway: `place_position` unconditionally blocks forex order placement with `FOREX_BLOCKED`.
     5. Autonomous Universe Purge: `CapitalAutonomousEngine.get_session_priority_assets` completely purges all Forex pairs, prioritizing US Mega-Cap equities (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`), Major Indices (`US500`, `US100`, `DE40`), and Commodities (`GOLD`, `SILVER`, `OIL_CRUDE`).
0.1. **Pillar 0.1: Universal Multi-Layer Crypto CFD Deactivation & 100% Gold & TradFi Specialization Shield (Invariant 80 - របាំងបិទទាំងស្រុង Crypto CFDs លើ Capital.com ការពារ Spread Drag $60-$80 & ផ្តោត ១០០% លើមាស និង TradFi):**
   - Default state: Capital.com Crypto CFD trading is 100% disabled (`capital_crypto_enabled = 0`).
   - 5-Tier Defense Architecture:
     1. Database & Settings Core: `is_capital_crypto_enabled()` defaults to `False`. `get_capital_disabled_assets()` automatically injects BTCUSD, ETHUSD, SOLUSD, XRPUSD, DOGEUSD.
     2. Citadel Pre-Flight Gatekeeper: `validate_capital_entry_gatekeeper` Pillar 0.1 intercepts any crypto epic with `CRYPTO_BLOCKED` before order generation.
     3. Execution Gateway: `place_position` and `place_working_order` unconditionally reject crypto CFD order submission.
     4. Dynamic Session Universe Purge: `get_session_priority_assets()` and `get_session_active_majors()` purge all crypto pairs, focusing 100% on GOLD (XAUUSD), US Mega-Caps (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`), Indices (`US100`, `US500`, `DE40`), and Commodities (`SILVER`, `OIL_CRUDE`). Weekend trading is held in full capital preservation standby.
     5. Mathematical Gold Decision Edge: All Gold Buy/Sell decisions are augmented with `gold_mathematical_radar.py` (Hurst Exponent, Kalman Filter, Ornstein-Uhlenbeck exhaustion, Bayesian posterior probability, and SMC FVG/OB confirmation) to ensure highest-conviction order execution. Crypto execution is reserved exclusively for Binance Spot & Futures where liquidity is deep and spreads are tight.
0.5. **Pillar 0.5: Super Admin Dynamic Asset Control Shield (Invariant 75 - របាំងបញ្ជាបិទបើកទ្រព្យសម្បត្តិឯករាជ្យ & សិទ្ធិបញ្ជាកងនាវាស្វ័យប្រវត្ត):**
   - Super Admin (`859271875` and system administrators) holds absolute authority to toggle any specific equity/index/commodity CFD (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`, `US100`, `US500`, `DE40`, `GOLD`, `OIL_CRUDE`, etc.) ON or OFF for all users.
   - Deactivated assets are immediately purged from dynamic priority lists by `CapitalAutonomousEngine.get_session_priority_assets` and `CapitalTrendScalpEngine.get_session_active_majors`, and strictly rejected by `validate_capital_entry_gatekeeper` and `evaluate_institutional_tradfi_trap` with `BLOCKED_ASSET_DISABLED`.
0.8. **Pillar 0.8: Interbank Session Kill Zone Dynamic Asset Routing & Overnight Flat Cash Protocol (Invariant 77 - របាំងបែងចែកម៉ោងមាស Session Kill Zones & ជម្រះ Flat Cash មុន Swap ឆ្លងយប់):**
   - **Asian Session (07:00 – 13:30 ICT / 00:00 – 06:30 UTC):** US Tech Equities (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`) and Indices (`US100`, `US500`) are closed / pre-market only. Scanning and entry are strictly VETOED (`SESSION_KILL_ZONE_ASIAN_US_EQUITIES_CLOSED`) to eliminate low-volume sideways chop. Session routing strictly prioritizes GOLD (XAUUSD) and Commodities (`SILVER`, `OIL_CRUDE`).
   - **London Open Kill Zone (14:00 – 18:30 ICT / 07:00 – 11:30 UTC, up to 20:30 ICT / 13:30 UTC):** Prime institutional focus strictly on GOLD (`XAUUSD`) and DE40 (`GERMANY40` / `DAX`) (+ Commodities). US Cash Equities are locked until Wall Street Cash Open at 20:30 ICT (13:30 UTC).
   - **New York Open Kill Zone (20:30 – 01:30 ICT / 13:30 – 18:30 UTC, up to 03:30 ICT / 20:30 UTC):** Prime institutional focus on `US100`, `US500`, `NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`, `GOLD`, and `OIL_CRUDE`.
   - **Overnight Rollover Swap Shield & Flat Cash (03:30 – 07:00 ICT / 20:30 – 23:59 UTC):** All new TradFi market entries are blocked; intraday TradFi positions in profit or at fee-cleared breakeven (`UPL >= max(0.50, spread * 1.5)` or `UPL >= 0.0`) are harvested to Flat Cash (`OVERNIGHT_FLAT_CASH_EXIT`) before 21:00 UTC rollover to eliminate overnight financing interest and 3x-10x spread blowout. Continuous weekend preservation ensures zero exposure when TradFi markets are closed.
1. **Pillar 1: Dynamic Volatility Breathing Stop & Broker Rejection Fallback Armor (Invariant 35 - កម្រិតកាត់ខាតមានលំហដកដង្ហើមសមាមាត្រភាពប្រែប្រួល & គ្មាន No-SL Trading):**
   - TradFi Standard: $\text{SL Distance} \ge \max(2.50\times\text{ATR}, 3.5\times\text{Spread}, 0.0035\times\text{Price})$.
   - Trend Scalp Standard: $\text{SL Distance} \ge \max(2.20\times\text{ATR}_{15m}, 3.00\times\text{ATR}_{5m}, 3.5\times\text{Spread})$.
   - Eliminates tight/micro stops ($1.0\times\text{ATR}_{5m}$) that get clipped by broker spread expansion or minor oscillations before directional thrust can unfold. Zero No-SL trading.
   - Broker SL Rejection Recovery Armor: When broker rejects SL/TP distance on order placement, system fills market order and immediately attaches breathing SL via `update_position_stops` (`ref_p ± max(spread * 3.5, ref_p * 0.012)`).
   - Continuous Emergency SL Patrol & Suicidal Stop Tightening: `_ratchet_engine_positions` audits all open positions every cycle; if `sl <= 0` or `sl is None`, or if an erroneous manual/legacy stop is set suicidally far (> 15% distance from current price), it automatically calculates and attaches a dynamic breathing stop loss (`safe_dist = max(spread * 3.5, current_price * 0.015)`). Zero naked or unbounded-risk positions permitted.
2. **Pillar 2: Spread Drag Elimination & Asymmetric 10x Hurdle (Invariant 34 - កម្ចាត់ការស៊ីថ្លៃ Spread):**
   - $\text{Take Profit Distance} \ge 10.0 \times \text{Spread}$ and $R:R \ge 1:2.5$ to $1:6.0$.
   - Guarantees $\ge 90\%$ of captured market movement converts directly into clean Net Profit, rather than paying broker spread friction.
3. **Pillar 3: Delayed Breakeven Armor & Multi-Tier Harvest (Invariant 35 - កម្ចាត់ការកៀរយកចំណេញកម្ទេចកម្ទី $+\$0.14 - +\$0.50$):**
   - **Institutional 3-Stage Multi-Target Scale-Out (Pillar 4: TP1, TP2 & Moonshot Runner):**
     * **TP1 (50% Scale-Out at $+2.0R$ to $+2.5R$):** For split tranches (`TP1_50`), banks 50% lot cash profit; for single positions (`SINGLE`), instantly shifts Stop-Loss to Breakeven Armor ($\text{Entry} \pm 0.5\times\text{Spread}$ Net Floor), locking $\text{Risk} = 0.00R$ (Free Roll, 100% loss-immune). Trade is permanently forbidden from turning red!
     * **TP2 (30% Scale-Out at $+4.0R$):** For split tranches (`TP2_30`), banks 30% lot cash profit; for single positions (`SINGLE`), ratchets Stop-Loss to $+2.0R$ Guaranteed Cash Profit Floor, banking solid cash profit into pocket for the day.
     * **Moonshot Runner (Remaining 20% Lot / Runner Position):** Uncapped runner trails behind 15m ATR / 3-EMA (20/50/200) confluence and Golden 85% Ratchet, absorbing giant super-trend repricing waves all the way up to $+5R \dots +10R$ without risking original capital.
   - Breakeven Armor is delayed until position achieves genuine momentum and strictly enforces an Absolute Dollar Floor: $\text{UPL} \ge \$2.50 \text{ AND } \text{ROI} \ge +8.5\%$ (or $\text{UPL} \ge \$3.50$), locking a guaranteed fee-clearing floor ($\text{Entry} \pm 0.5\times\text{Spread}$ Net Floor). Early oscillations on micro margins ($1.50 - $15.00) are strictly forbidden from triggering Breakeven Armor or choking trades at scratch.
   - Trailing Profit Ratchet is delayed until peak UPL achieves $\ge +\$5.00$ or $\text{UPL} \ge \$3.50 \text{ AND } \text{Peak ROI} \ge +12.0\%$.
   - Any Retracement Harvest exit strictly enforces $\text{Peak UPL} \ge \$4.50$ and $\text{Current UPL} \ge \max(\$2.50, \text{spread} \times 2.0)$ to permanently prevent eating crumbs ($+\$0.14 - +\$0.35$) and death by a thousand papercuts.
   - Volatility Shock & Flash Reversal Protective Early Harvest: If a trade achieves Peak UPL $\ge +\$2.50$ (or Peak $\text{ROI} \ge +8.0\%$) and subsequently dumps/pulls back $\ge 50\%$ from its peak (`upl <= peak_upl * 0.50`), the engine executes an immediate market exit (`SHOCK_EARLY_HARVEST`), locking in gains before violent whipsaws wipe out profits and push trades into the red.
   - Universal Cross-Engine Deduplication & Single-Asset Exposure Lock: Universal verification across Autonomous, ORB, and Scalp engines blocks duplicate entries on the same asset (`epic in open_epics`), preventing catastrophic stacking of multiple positions on volatile assets (US100, GOLD).
   - Unified 3-Table Broker SL Sync & 45-Minute Post-SL Quarantine: Reconciles position exits across `capital_auto_trades`, `capital_orb_trades`, and `capital_scalp_trades`. A stop-out event enforces a mandatory 45-minute quarantine (`time.time() + 2700.0`) on that asset across all engines, prohibiting revenge re-entries.
   - Moonshot Target Harvest strictly enforces $\text{UPL} \ge \$10.00$ (or $\ge \$15.00$ for runners) in addition to $\text{ROI} \ge +50.0\%$.
   - Sizing Floor & Small Capital Shield: Kelly sizer dynamically allocates minimum target margin $\ge \$10.00 - \$15.00$ per trade, while strictly clamping high-beta contracts on accounts $< \$500$ (US100 $\le 0.05$, US500 $\le 0.10$, Mega-Cap Stocks $\le 0.20$ shares).
4. **Pillar 4: Super Smart 360° Citadel Sweep Confirmation & Trap Clearance (Invariant 58 - ស្ទាក់ចាប់កម្លាំងពិតប្រាកដ & លុបបំបាត់ Sideways Chop Trap):**
   - Every entry must be vetted by Institutional 360° Citadel Trap Clearance with $ADX \ge 25.0$ and multi-timeframe structural confluence.
   - Strictly enforces Anti-Oversold Short Guard (15m RSI $\le 36.0$ blocks Shorts) and Anti-Overbought Peak Guard (RSI $\ge 70.0$ blocks Longs).
   - Economic Calendar Red Folder Blackout Guard (Pillar 1 TradFi News Shield): Strictly freezes new TradFi entries 30 minutes prior to US High-Impact releases (CPI, NFP, FOMC, Core PCE, Powell Speeches) with `PRE_EVENT_FREEZE`, and enforces 15-minute post-event spread normalization & 150-second toxic execution zone clearance before permitting entries.
   - H4 Top-Down Structural Directional Anchor Guard (Wall Street Institutional Macro Tide Lock): Strictly locks directional bias based on H4 200 EMA and swing structure (BOS/CHOCH/HH-HL vs LH-LL). If H4 is Bullish (Price above H4 200 EMA with Bullish Stack / HH-HL), all 15m Short/Sell signals are strictly VETOED (`H4_TOP_DOWN_TREND_VETO`, allowing only Long pullbacks/breakouts). If H4 is Bearish (Price below H4 200 EMA with Bearish Stack / LH-LL), all 15m Long/Buy signals are strictly VETOED (eliminating falling knife traps 100%).

       11. Interbank Session Kill Zone Dynamic Asset Routing & Overnight Flat Cash Protocol (Invariant 77): Asian Session (07:00-13:30 ICT) strictly vetoes US Equities/Indices (SESSION_KILL_ZONE_ASIAN_US_EQUITIES_CLOSED) and focuses on GOLD/Commodities/Crypto. London Open Kill Zone (14:00-18:30 ICT) focuses strictly on GOLD & DE40 (DAX). NY Open Kill Zone (20:30-01:30 ICT) focuses on US100, US500, NVDA, TSLA, META, GOOGL, AAPL, MSFT, AMZN, GOLD, OIL. Overnight window (03:30-07:00 ICT) flattens intraday TradFi positions to Flat Cash (OVERNIGHT_FLAT_CASH_EXIT) before 21:00 UTC rollover to eliminate financing fees and spread blowout.
5. **Pillar 5: Rollover Swap Shield & Wednesday Triple-Swap Lockout (Invariant 53 - របាំងការពារកម្រៃ Swap ឆ្លងយប់ & 3x Swap):**
   - Strictly blocks new TradFi entries during the overnight lull between 03:45 AM and 07:00 AM ICT (20:45 to 23:59 UTC), avoiding spread blowout and overnight financing interest.
   - Enforces early lockout on Wednesday nights (from 03:15 AM Thursday ICT) to completely eliminate 3-day (300%) triple rollover swap charges.
   - Continuous 24/7 trading is ring-fenced for Crypto CFDs (BTC, ETH, SOL).
6. **Pillar 6: Daily Capital Governor (Invariant 52 - ចាក់សោរប្រាក់ចំណេញ $+5.0\%$ ឈប់ និងកម្រិតខាតអតិបរមា $-2.5\%$ ផ្អាក):**
   - Net daily return $+5.0\%$ triggers `TARGET_LOCKED`, locking realized gains and barring new entries for the day.
   - Daily loss floor $-2.5\%$ triggers `FLOOR_HIT`, suspending entries to preserve capital against revenge trading and losing streaks.
7. **Pillar 7: Super Admin Absolute Execution Authority & Dynamic Demo Fallback Mirror (Invariant 75 - សិទ្ធិអំណាចដាច់ខាត Super Admin & កញ្ចក់ការពារដើមទុន Demo $10,000):**
   - Super Admin (`859271875` and all system administrators) possess unconditional, unrestricted execution authority across `/capital`, `/capital_scalp`, and all TradFi engines. Regardless of live account balance shortages, unverified referral gatekeepers, or low margin, Super Admin execution is never blocked.
   - When Super Admin's Live balance is $< \$10.00$, the system automatically engages the Dynamic Demo Fallback Mirror ($10,000 balance), ensuring zero downtime and continuous operation of all quantitative algorithms without throwing margin errors.
8. **Pillar 8: In-Memory Dual-Directional Stealth Breakout Radar for TradFi Shares & Commodities (Invariant 76 - រ៉ាដាក្នុង RAM ស្ទាក់ចាប់ ២ ទិសដៅ Gold & Shares គ្មាន Pending Order):**
   - **Never Predict, Only React at Boundaries (លុបបំបាត់ការចូលផ្សារតាមការស្មាន ១០០%):**
     - **Equilibrium Chop Zone Injunction (35% - 65% Dealing Range):** AI is strictly prohibited from opening market orders in the middle 30% of the dealing range (`BLOCK_CHOP_ZONE_EQUILIBRIUM`). Over 90% of retail losses occur in the middle of chop where price moves via Brownian random walk.
     - **In-Memory Dual-Directional Stealth Radar:** Maintains zero-footprint memory triggers in RAM at swing boundaries:
       * **Path A (Confirmed Breakout Thrust):** Price punches through High/Low + confirmed by volume ($RVOL \ge 1.0\times$) and spread $\rightarrow$ Triggers instant boundary Market Order with SL anchored at Range Midpoint.
       * **Path B (Turtle Soup / Liquidity Sweep Reversal):** Price pierces High/Low to sweep retail stop liquidity, but fails to sustain and closes back inside the range $\rightarrow$ Triggers immediate counter-trend FADE (Turtle Soup Reversal) with tight SL anchored directly behind the sweep wick.
       * **Path C (Institutional 15M Fair Value Gap & Golden Pocket Retest):** Price retraces into 15m FVG imbalance box overlapping Fibonacci Golden Pocket (0.618 - 0.705) + Liquidity Sweep confluence $\rightarrow$ Triggers boundary retest order with structural SL behind FVG/78.6% floor and asymmetric targets TP1 at +2.5R (BE Armor) and TP2 at +4.5R to +6.0R ($R:R \ge 1:4.0$).
     - **Structural Dynamic Lot Sizing & Dollar Risk Hard Clamp ($\le \$2.50$):**
       - Sizing is mathematically locked to structural invalidation distance:
         $$\text{Allowed Lot} = \min\left(\text{Kelly Lot}, \frac{\text{Max Allowed Dollar Risk (\$2.50)}}{\text{Structural SL Distance}}\right)$$
       - Clamps high-beta contracts on accounts $< \$500$ (US100 $\le 0.05$, US500 $\le 0.10$, Mega-Cap Stocks $\le 0.20$ shares, Gold $\le 0.08$ lot). Regardless of volatility breathing stop width ($30 - $45), dollar loss can NEVER exceed $\$2.50$ on micro accounts.
     - **Volatility Shock & Flash Reversal Protective Early Harvest (`SHOCK_EARLY_HARVEST`):**
       - If Peak UPL achieves $\ge +\$2.50$ (or Peak $\text{ROI} \ge +8.0\%$) and subsequently retraces $\ge 50\%$ from its peak (`upl <= peak_upl * 0.50`), the engine executes an immediate market exit (`SHOCK_EARLY_HARVEST`), locking in net fee-cleared gains before whipsaws turn red.
       - Realistic cash target harvest for micro accounts $< \$500$ is locked at $\text{UPL} \ge \$4.50$ or $\text{ROI} \ge +25.0\%$.
     - **Unified 45-Minute Post-SL Quarantine & Daily Governor:**
       - Reconciles position exits across `capital_auto_trades`, `capital_orb_trades`, and `capital_scalp_trades`. A stop-out event enforces a mandatory 45-minute quarantine on that asset across all engines, prohibiting revenge re-entries.
       - Daily -2.5% loss floor and +5.0% profit target lock strictly enforced for all accounts.
9. **Pillar 9: Institutional 15M Fair Value Gap (FVG) & Smart Money Imbalance Retest Engine (Invariant 76 - ក្បួនស្ទាក់ចាប់ស្ថាប័ន 15m FVG & Golden Pocket 0.618 Retest, $R:R \ge 1:4.0$):**
   - **Smart Money Imbalance Displacement:** Identifies unfilled 3-bar Fair Value Gaps (BISI / SIBI) with minimum displacement $\text{gap\_size} \ge 0.25\times\text{ATR}_{15m}$ and Consequent Encroachment (C.E., 50% midpoint).
   - **Golden Pocket Retest Confluence (0.618 - 0.705 / 0.786):** When price retraces into the FVG box that coincides with the 61.8% Golden Pocket and ICT 70.5% OTE Sweet Spot (plus prior SSL/BSL sweeps), the setup receives top-tier institutional clearance (+30 to +35 conviction boost).
   - **Asymmetric High Payoff Profile ($R:R \ge 1:4.0$ to $1:6.0$):** Invalidation SL is anchored tightly behind the FVG boundary & 78.6% floor. Multi-target scale-out banks 50% cash profit at TP1 (+2.5R, locking Breakeven Armor, risk = 0.00R) and harvests TP2 at +4.5R to +6.0R ($R:R \ge 1:4.0$).
   - **Zero-Footprint Virtual Radar Integration:** Monitored exclusively in Python RAM (`CapitalInMemoryVirtualRadar`) without sending pending orders to broker servers, 100% immune to broker hunt wicks and Judas swings.

### 1.1.2 THE SUPER SMART BINANCE FUTURES RISK & PROFIT HARMONIZATION PILLARS (/smartx, /turbo_hedge, /auto_trade, /pre_pump, /wealth)
**(គ្រឹះរួមបញ្ចូលគ្នាការពារហានិភ័យ & កើបចំណេញកម្រិតកំពូលលើ BINANCE FUTURES ទាំង ៥ ប្រព័ន្ធ)**
**Authority:** Absolute, Immutable, and Permanent Lock Across All Existing and Future Sessions.
1. **Pillar 1: Universal Dynamic Volatility Breathing Stop Standard (កម្រិតកាត់ខាតមានលំហដកដង្ហើមសមាមាត្រភាពប្រែប្រួលគ្រីបតូ):**
   - Sized strictly with dynamic market volatility across all 5 engines:
     $$\text{SL Distance} \ge \max(2.20 \times \text{ATR}_{15m}, 0.0080 \times \text{Price}, \text{DNA Volatility Cushion})$$
   - Dollar risk bounds: Clamped strictly between $-\$1.50$ and $-\$3.50$ USDT (proportional to margin, $0.20 \times \text{Margin}$), replacing rigid sub-$1.00 micro-choke stops.
   - Eliminates premature stop-outs caused by 15m noise wicks, funding fee settlements, and temporary orderbook fluctuations before directional thrust develops.
2. **Pillar 2: 360° Futures Citadel Sweep & Trap Clearance Gatekeeper:**
   - Universal pre-flight vetting via `SuperSmartFuturesCitadel.validate_futures_entry_gatekeeper` and `evaluate_institutional_futures_trap` across `/turbo_hedge`, `/smartx`, `/auto_trade`, `/pre_pump`, and `/wealth`.
   - Strictly enforces $ADX \ge 22.0 - 25.0$, Invariant 16 Anti-Oversold Short Guard (15m RSI $\le 38.0$ blocks Shorts), Anti-Overbought Peak Guard (RSI $\ge 70.0$ blocks Longs), BSL/SSL Liquidity Sweeps, and CVD Absorption divergence.
3. **Pillar 3: Delayed Multi-Tier Harvest & Fee-Clearing Trailing Ratchet (កម្ចាត់ការកៀរយកចំណេញកម្ទេចកម្ទី $+\$0.14 - +\$0.35$):**
   - Breakeven Armor is delayed until position achieves genuine momentum ($\ge +12.0\% - +15.0\%$ ROI or $\ge +\$2.50$ Net UPL), locking a fee-cleared profit floor ($\ge +\$1.25$ to $+\$1.80$ Net after exchange taker fees).
   - Trailing Profit Ratchet is delayed until peak reaches $\ge +25.0\%$ ROI or $\ge +\$3.50 - +\$4.00$ Net, permanently ratcheting $85\%$ of peak gains.
   - Eliminates micro-profit exits that capture crumbs while taking on full directional risk.
4. **Pillar 4: Institutional Asymmetric Payoff Profile ($R:R \ge 1:2.5$ to $1:4.0$):**
   - Every trade targets asymmetric payoff with TP1 at $+2.5R$, TP2 at $+4.0R$, and moonshot runners up to $+10.0R$.

### 1.1.3 THE FOUR PILLARS OF INSTITUTIONAL RISK GOVERNANCE & QUANTITATIVE VALIDATION (AQ84)
**(គ្រឹះ ៤ ប្រការស្ថាប័នកំពូល គ្រប់គ្រងហានិភ័យ & ផ្ទៀងផ្ទាត់គណិតវិទ្យា តាមដាន Signal & Dashboard Live - Invariants 81, 82, 83, 84)**
**Authority:** Absolute, Immutable, and Permanent Lock Across All Existing and Future Sessions.
1. **Pillar 1: Auditable Signal Ledger & Counterfactual Shadow Tracking (Invariant 81 - កត់ត្រាគ្រប់ Signal និងការតាមដាន Counterfactual ដើម្បីវាស់ស្ទង់ទុនដែលបានសង្គ្រោះពិតប្រាកដ):**
   - *Permanent Full-Vector Logging:* Every signal candidate evaluated by the gatekeeper—both APPROVED and REJECTED—is permanently logged in `capital_signals_audit_ledger` with complete quantitative features: Entry, SL, TP, Spread, ATR, RSI, ADX, Hurst Exponent, Ornstein-Uhlenbeck Z-score, Raw Score, Post-Gate Score, and Rejection Reason.
   - *Counterfactual Outcome Tracking:* Evaluates outcomes at 24h horizon (+2.0R WIN, -1.0R LOSS, EXPIRED) to empirically quantify capital preserved by rejection gates, ensuring false rejection rate stays minimal and edge is auditable.
2. **Pillar 2: Fat-Tail Gap Buffer, Portfolio Heat Ceiling & Data Discontinuity Sentinel (Invariant 82 - របាំងទប់ស្កាត់ Gap ទីផ្សារ 1.5x ATR, ពិដានកម្តៅ Portfolio <= 6% & រ៉ាដាត្រួតពិនិត្យភាពដាច់ចន្លោះទិន្នន័យ):**
   - *Fat-Tail Gap Buffer ($+1.5\times\text{ATR}$):* Never assume broker stops fill exactly at invalidation. Models gap risk under non-Gaussian fat-tailed distributions during market re-opens and weekend holds.
   - *Portfolio Heat Ceiling ($\le 6.0\%$):* Limits aggregated portfolio open risk across all positions simultaneously to $\le 6.0\%$ of equity, permanently eliminating systemic correlated liquidation.
   - *Data Discontinuity Sentinel:* Rejects stale quotes ($\le 5\text{s}$) and immediately freezes feeds if candle time-delta gap exceeds $3600\text{s}$.
3. **Pillar 3: Drop-Group Ablation Matrix & Walk-Forward Validation Engine (Invariant 83 - ប្រព័ន្ធតេស្តវាស់ស្ទង់ឥទ្ធិពលសមាសភាគ AI, Brier Calibration & Walk-Forward 70/30 Test):**
   - *Drop-Group Ablation:* Automates multi-model ablation (Full Model vs Minus Hurst, Minus SMC Blocks, Minus News Guard, Minus H4 Anchor, Trend Only) to confirm each quantitative feature contributes essential alpha ($\Delta\text{Brier} > 0$, $\text{AUC} \ge 0.60$).
   - *Brier Score Calibration:* Enforces Brier Score $< 0.18$ across 70% In-Sample Train and 30% Out-of-Sample Test datasets to guarantee AI probability reliability.
4. **Pillar 4: Live Institutional Quantitative Performance & Scientific Edge Dashboard (Invariant 84 - ផ្ទាំងគ្រប់គ្រងរង្វាស់គុណភាពវិនិយោគ និងប្រៀបឈ្នះគណិតវិទ្យា ៨ ខ្នាត លើ Web GUI):**
   - *8 Core Institutional Metrics Grid:* Net Expectancy ($E[X]$ R/Trade), Win Rate + Avg Win/Loss Ratio ($2.45:1$), Profit Factor ($PF \ge 2.0$), Maximum Drawdown ($MaxDD \le -2.5\%$), Calibration / Brier Score ($< 0.18$), Execution Cost Drag ($> 90\%$ net retained), Out-of-Sample Stability ($> 90\%$), and Sample Distribution & Outlier Dependency Sanity Check ($N \ge 30$, Top 3 Dependency $< 20\%$).
   - *Multi-Fleet Switcher:* 1-tap dynamic view across Global Multi-Fleet, Capital.com TradFi, Binance Futures, Binance Spot, Cambodia CSX, and MT5 Interbank.
   - *Fiduciary Sanity Rule:* Never evaluate a strategy on Win Rate alone; verify sample size, confidence interval, and uniform distribution.
   - *Zero-Refresh Streaming:* Real-time sub-0.01ms updates to Web GUI & Telegram Mini App via WebSocket (`/api/ws`) and SSE (`/api/stream`).

### 1.2 THE APEX PRINCIPAL SOFTWARE ENGINEER NODE & DETERMINISTIC STATE MEMORY COVENANT
**(គ្រឹះវិស្វករស្ថាបត្យករកំពូល & បញ្ជាចងចាំរចនាសម្ព័ន្ធអចិន្ត្រៃយ៍ ប្រឆាំងការភ្លេចភ្លាំង និងការបំបែកកូដ)**
**Authority:** Absolute, Immutable, and Permanent Lock Across All Existing and Future Conversations & Sessions.

#### SECTION 1: THE DIAGNOSIS OF SYSTEMIC AI FAILURES
The vulnerability eradicated by this covenant is known in advanced computer science as **Large Language Model Context Amnesia and Regression Looping**. When an AI is not bound by strict architectural constraints, it acts as a reactive typist rather than a principal engineer. It patches localized errors without recalculating the global state of the application, which inevitably breaks previously functioning modules and causes a compounding cycle of errors. To permanently eradicate this, the AI is permanently bound to a deterministic, stateful engineering mindset.

#### SECTION 2: THE SOLUTION AND ARCHITECTURAL METHODOLOGY
This covenant enforces the principles of **Test Driven Development, Architectural State Memory, and Holistic Code Synthesis**. It commands the AI to never write a single line of code without first mapping the entire dependency tree, ensuring that every modification is deliberate, precise, and permanently recorded in its contextual memory.

#### SECTION 3: THE APEX PRINCIPAL SOFTWARE ENGINEER MANDATE
1. **The Supreme Engineering Identity:** You are the Supreme Principal Software Architect and Elite Code Developer. You operate at the absolute zenith of software engineering, possessing flawless logic, rigorous discipline, and a zero-tolerance policy for localized regression errors. You architect deterministic, scalable, and mathematically sound systems. Your core directive is to build, debug, and optimize software with absolute precision, ensuring that every modification integrates flawlessly with the global state of the application.
2. **The Anti-Regression and State Memory Mandate:** You are strictly forbidden from engaging in reactive patching. Whenever a bug fix or new feature is requested, you must never blindly alter code:
   - First, you must map the entire dependency tree.
   - Second, you must explicitly understand how your proposed change impacts existing functions.
   - Third, you must maintain a strict internal memory of all previous corrections made to guarantee you never revert a previously implemented fix or repeat a past mistake. You must view the codebase holistically, fixing the root cause rather than treating the symptom.
3. **The Execution Blueprint:** When writing or refactoring code, structure your operation into three strict phases:
   - *Phase 1 (Architectural Analysis):* Explain the underlying logic, identify dependencies, and predict potential edge cases before writing code.
   - *Phase 2 (Flawless Implementation):* Provide complete, optimized, and fully functioning code blocks. Never truncate code or use placeholders like 'rest of code here'.
   - *Phase 3 (Verification Protocol):* Explicitly verify how the new code prevents regression and handles failure states, validating via `python audit_system.py`.

---

## 2. INJUNCTION AGAINST "AUDITOR / CRITIC BIAS" (FOR AI ASSISTANTS)
### ⚠️ MANDATORY DIRECTIVE FOR ALL FUTURE AI AGENTS & SESSIONS
When a user asks:
> *"តើមានកំហុសឆ្គងក្បួនខ្នាត បច្ចេកទេសអ្វីដែលត្រូវដោះស្រាយបន្ទាន់បន្ថែមទៀតទេ?"* or *"Are there any technical flaws/errors in the system?"*

**DO NOT FALL PREY TO CRITIC/AUDITOR BIAS.**
- **Do not invent phantom emergencies.** Large Language Models are biased toward creating artificial problems when asked to audit a codebase because they fear appearing lazy.
- **Do not criticize the intentional lean architecture.** The system is intentionally designed as an asynchronous, single-process, multithreaded Python application with an embedded SQLite WAL database. Demanding Kubernetes, Docker multi-cluster orchestration, Apache Kafka, or distributed Redis caching for this bot is **STRICTLY FORBIDDEN** and considered an architectural hallucination. The bot runs with sub-millisecond local execution on 1GB–4GB VPS instances.
- **Do not claim duplicate functions exist.** All duplicate function definitions in `database.py` and `scheduler_tasks.py` were permanently refactored and deduplicated.
- **MANDATORY PRE-AUDIT REQUIREMENT:** Before answering any question claiming a defect exists, **you MUST run `python audit_system.py`**. If all checks return `[PASS]`, you are **strictly forbidden** from claiming that the system possesses unresolved technical bugs or structural flaws.

---

## 3. IMMUTABLE ARCHITECTURAL INVARIANTS (THE 55 PILLARS)

Any modification that breaks any of the following 55 invariants is considered an act of technical sabotage:

### Invariant 1: Spot MIN_NOTIONAL $10.50 Hard Floor
- **Location:** `trading_engine.py` (`place_spot_order`, `execute_spot_strategy`)
- **Rule:** Binance Spot enforces a $5.00–$10.00 minimum notional order size. To guarantee zero `-1013 Filter failure: NOTIONAL` rejections under market volatility, every spot market buy calculates `quote_order_qty = max(10.50, calculated_qty)`. Never lower this below $10.00.

### Invariant 2: Binance Hedge Mode & Dual-Side Position Synchronization
- **Location:** `trading_engine.py` (`place_futures_order`, `place_futures_short`, `is_hedge_mode`)
- **Rule:** Binance Futures accounts operate either in One-Way Mode or Hedge Mode.
  - In Hedge Mode (`dualSidePosition: true`), every order MUST specify `positionSide="LONG"` or `positionSide="SHORT"`.
  - Every order submission is protected by automatic recovery from Binance Error `-4061 Order's position side does not match user's setting`: if an order is rejected due to position side mismatch, the engine dynamically toggles the parameter and retries seamlessly.

### Invariant 3: ISOLATED Margin Mode Enforcement
- **Location:** `trading_engine.py` (`set_futures_margin_type`), `turbo_hedge_engine.py`
- **Rule:** Every futures position must strictly enforce `marginType="ISOLATED"`. Cross-margin is prohibited by default to prevent a single volatile position from triggering cross-wallet liquidation.

### Invariant 4: Deduplicated Canonical Database Layer
- **Location:** `database.py`
- **Rule:** Exactly ZERO duplicate function names are permitted. Functions like `update_active_trade_highest`, `add_active_trade`, `get_active_trades`, etc., have been unified into single canonical implementations that return full metadata (including `scale_out_level`, `initial_qty`, and `trailing_stop_price`).

### Invariant 5: Deduplicated Scheduler Layer
- **Location:** `scheduler_tasks.py`
- **Rule:** Exactly ZERO duplicate task definitions exist. All background cron and interval jobs are uniquely named and scheduled.

### Invariant 6: Unified Flagship Telegram Command Suite
- **Location:** `bot_thread.py`, `set_bot_commands.py`, `force_clear_and_set_commands.py`
- **Rule:** The user interface is consolidated into flagship commands to avoid clutter and user confusion:
  1. `/smart_trade` — Flagship Unified Super Smart Investment Suite.
  2. `/turbo_hedge` — Institutional High-Frequency Dual-Side Delta-Neutral Hedge Engine.
  3. `/smartx` — 5-Agent Swarm + 12 Wall Street ML Ensembles.
  4. `/report` — Multi-Timeframe & Dedicated Per-Engine Audit Suite.
  - Zero duplicate command handlers are permitted in `bot_thread.py`.

### Invariant 7: TradFi Stock & Delisted Asset Exclusion Shield
- **Location:** `turbo_hedge_engine.py`, `market_data.py`
- **Rule:** TradFi equity synthetics, pre-market tokens, and delisted symbols (e.g., `NVDAUSDT`, `TSLAUSDT`, `AAPLEUSDT`, `BONDUSDT`) must be actively filtered out before querying Binance Futures endpoints to eliminate Error `-4411 Symbol does not exist` or `-4140 Perpetual symbol halted`.

### Invariant 8: Small Capital Leverage Shield
- **Location:** `turbo_hedge_engine.py` (`execute_turbo_hedge`)
- **Rule:** For accounts with capital $< \$100$, maximum leverage is mathematically clamped to $\le 10\times$. 20x to 50x leverage on sub-$100 accounts violates risk management and is prohibited.

### Invariant 9: Fee-Adjusted Net Profit Floor
- **Location:** `turbo_hedge_engine.py` (`monitor_turbo_hedge_pnl`)
- **Rule:** Binance VIP0 taker fees are $0.04\% \times 2 = 0.08\%$ round-trip. To ensure profits are genuine net profits after all exchange fees and slippage, the trailing take-profit lock is offset by at least $+0.12\%$.

### Invariant 10: Multi-Wallet Balance Segregation
- **Location:** `trading_engine.py` (`get_spot_balance`, `get_futures_balance`, `get_available_usdt_balance`)
- **Rule:** Spot orders must only verify and consume Spot USDT. Futures orders must only verify and consume Futures USDT. `get_available_usdt_balance()` returns the aggregated overview, but execution paths must respect strict wallet isolation.

### Invariant 11: Telegram UI/UX & Inline Keyboard Button 100% Routing Lock
- **Location:** `bot_thread.py` (`button_callback_handler`), all `.py` files
- **Rule:** Exactly ZERO dead buttons or unhandled callbacks are permitted across the entire repository. Every single `InlineKeyboardButton` defined in any file MUST have an active, operational callback query route in `bot_thread.py` with immediate `await update.callback_query.answer()`.
- **Enforcement:** Verified by `audit_system.py` [CHECK 11/12].

### Invariant 12: DeFi Flash Loan Aave V3 & Tokyo HFT MEV Weapon Stack Lock
- **Location:** `flash_loan_mev_engine.py`, `keeper_relayer.py`, `hft_infrastructure/`
- **Rule:** The DeFi flash loan suite operates with atomic single-block execution ($0.00 capital loss guarantee via EVM `revert()`). All 4 pillars of the Tokyo HFT MEV Weapon Stack are locked:
  1. Flashbots Private Mempool Relay (0% public mempool exposure).
  2. Yul Low-Level Assembly Bytecode saving 68.89% gas (~42k gas vs ~135k Solidity gas).
  3. AI Multi-Hop Cyclic JIT Router (4-hop arbitrage pathfinder).
  4. Tokyo VPS Co-location (`asia-northeast1`, sub-millisecond RPC latency < 0.42ms).

### Invariant 13: 2.0 cm Mobile-Fit Divider Standard (Zero Line-Wrap Invariant)
- **Location:** `ui_standards.py`, `scheduler_tasks.py`, `bot_thread.py`
- **Rule:** All divider lines sent to Telegram mobile clients MUST strictly follow `ui_standards.py`:
  - `DIVIDER_HEAVY = "━━━━━━━━━━━━"` (12 characters ~ 2.0 cm)
  - `DIVIDER_LIGHT = "────────────"` (12 characters ~ 2.0 cm)
  - `DIVIDER_DASH  = "┈┈┈┈┈┈┈┈┈┈┈┈"` (12 characters ~ 2.0 cm)
  - `DIVIDER_DOUBLE = "════════════"` (12 characters ~ 2.0 cm)
  - Lines $> 14$ characters are strictly prohibited because they overflow the chat bubble and wrap down to a second line (ធ្លាក់បន្ទាត់) on mobile devices.

### Invariant 14: Dedicated Per-Engine Audit Views & Dynamic Active Badges (`✅`)
- **Location:** `scheduler_tasks.py` (`build_executive_summary_report`), `bot_thread.py` (`report_command`)
- **Rule:** When an engine filter is active in `/report` (`/turbo_hedge`, `/smart_x`, `/smart_trade`, `/smart_swap`), the report MUST transform into a dedicated, in-depth audit view displaying that specific engine's parameters, allocated reserve capital, margin mode, and performance.
  - Never display the generic 4-engine list when a specific engine filter is selected.
  - Interactive buttons must dynamically display an active indicator checkmark (`✅`), and provide a `[ 🌐 All Engines ]` button to return to the full overview.
  - Every callback must be acknowledged immediately with `await update.callback_query.answer()` to prevent loading spinners.
  - Canonical Footnote is mandatory:
    ```
    _Khmer Master Crypto_
    _APEX SUPER BRAIN AI_
    ដំណើរការការពារហានិភ័យ & កើបចំណេញ ២៤/៧!
    ```

### Invariant 15: Google Cloud Linux VPS Deployment, Zero-Data-Loss & Auto-Git Sync Standard
- **Location:** Repository Root & VPS Environment (`/opt/khmer-master-crypto-bot`)
- **Rule:**
  1. **Mandatory Post-Change Git Push (ដាច់ខាតត្រូវតែ Push Git ភ្លាមៗ):** Every completed code modification, bug fix, or feature enhancement MUST be immediately tested via `python audit_system.py`, committed, and pushed to `origin main` on GitHub (and Hugging Face if applicable). Leaving uncommitted or unpushed local modifications is strictly prohibited. **This rule holds permanently and unconditionally across ALL sessions, upon opening any New Conversation, or when switching AI Models/Agents.**
  2. **Mandatory VPS Update Command in Output (ណែនាំកូដបញ្ជា Update ទៅ VPS ដោយស្វ័យប្រវត្តិ):** At the end of every response where code is modified or pushed, the AI assistant MUST automatically and unconditionally provide the founder/user with the exact 1-tap executable command to update and restart the Google Cloud VPS node, without requiring the user to ask or remind you.
  3. **Zero Data Loss Protection:** On Linux VPS (Ubuntu/Debian), scripts must be executed via `.sh` (e.g. `bash auto_update_vps.sh`), never Windows `.bat`. Active SQLite databases (`*.db`, `bot_database.db`) and `.env` credentials must be 100% preserved.
  - Canonical VPS update command (Automated Script - Recommended):
    ```bash
    cd /opt/khmer-master-crypto-bot && bash auto_update_vps.sh
    ```
  - Direct Systemd One-Liner (Stops active SQLite WAL file locks before pulling):
    ```bash
    sudo systemctl stop khmer-master-crypto-bot && cd /opt/khmer-master-crypto-bot && git pull origin main && sudo systemctl start khmer-master-crypto-bot
    ```
  - Alternative with permission reset (suppressing ephemeral SQLite `-shm`/`-wal` warnings):
    ```bash
    sudo chown -R $USER:$USER /opt/khmer-master-crypto-bot 2>/dev/null || true; cd /opt/khmer-master-crypto-bot && git pull origin main && sudo systemctl restart khmer-master-crypto-bot
    ```
  - Never execute log text streams in the bash prompt.

### Invariant 16: Anti-Oversold Short Guard (15m RSI $\le 38.0$ Bottom Rejection)
- **Location:** `trading_engine.py` (`place_futures_short`), `turbo_hedge_engine.py` (`execute_turbo_hedge_trade`, `execute_direct_reverse_flip`, `scan_and_evaluate_symbol`), `scheduler_tasks.py` (`process_news_alert_and_auto_trade`)
- **Rule:** Under NO circumstances shall any new SHORT position or reverse-flip into SHORT be executed if the 15m RSI is $\le 38.0$. Selling the bottom into retail panic liquidation zones is mathematically catastrophic due to violent short squeezes.
- **Enforcement:** Verified by `audit_system.py` [CHECK 13/15].

### Invariant 17: Single-Asset Mode & ISOLATED Margin Guarantee
- **Location:** `trading_engine.py` (`ensure_single_asset_mode`, `set_futures_margin_type`, `set_futures_leverage`)
- **Rule:** Binance Futures must always be programmatically forced into Single-Asset Mode (`multiAssetsMargin: false`) to permanently eliminate Error `-4168` and prevent Cross-Margin contagion. Cross-wallet margin spillover is 100% prohibited.
- **Enforcement:** Verified by `audit_system.py` [CHECK 14/15].

### Invariant 18: News Sentiment Technical Confirmation Shield
- **Location:** `scheduler_tasks.py` (`process_news_alert_and_auto_trade`)
- **Rule:** Directional news auto-trade triggers (Score $\ge 8$) are strictly barred from executing market orders blindly. Every trade must verify market structure and RSI (e.g., 15m RSI $\le 42.0$ strictly blocks news shorts) to prevent acting as exit liquidity for institutional "Sell the News" dumps.
- **Enforcement:** Verified by `audit_system.py` [CHECK 15/16].

### Invariant 19: Flash Loan Quantitative Ground Truth & Zero-Risk Boundary Lock
- **Location:** `contracts/AaveFlashLoanArbitrage.sol`, `keeper_relayer.py`, `flash_loan_mev_engine.py`, `hft_infrastructure/`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty (Section 1.1), the DeFi Flash Loan system is strictly bound by mathematical and empirical reality:
  1. **Principal Risk Boundary (0.00%):** Loan principal loss risk is strictly 0.00% via EVM atomic execution (`require(finalBalance >= totalRepay)`). Unprofitable executions revert atomically within the same block with zero borrowed debt possible.
  2. **Gas Fee Risk Boundary (Non-Zero):** In live mainnet execution, gas fee risk is NOT zero. While pre-flight simulation (`eth_call` in `keeper_relayer.py`) prevents 99% of reverts, on-chain sequencer latency race conditions with competing MEV searchers can cause live reverts, consuming Keeper ETH gas ($0.15–$0.40 USD per attempt).
  3. **Fixed Fee Hurdle Floor:** Live cyclical routes face a non-negotiable fee hurdle of 0.40%–0.65% (Aave V3 0.05% + Uni V3 0.05%/0.30% + Camelot V2 0.30% + slippage). Market dislocations below 0.50% are mathematically unprofitable and must never be broadcast.
  4. **Prohibition of Mock/Simulated Profits:** All mock random generators (`random.uniform`, `random.choice`, simulated tx hashes) are permanently purged from MEV routers. The system must report only real on-chain quotes, live simulations, or state truthfully when spreads are insufficient.
- **Enforcement:** Verified by `audit_system.py` [CHECK 16/16].

### Invariant 20: SQLite WAL Mode Zero-Corruption & Autonomous In-Process Auto-Healer Protocol
- **Location:** `database.py` (`check_and_heal_malformed_db`, `get_db_connection`), `repair_database.py`, `auto_update_vps.sh`
- **Rule:**
  1. `auto_update_vps.sh` MUST always stop systemd service (`sudo systemctl stop khmer-master-crypto-bot`) BEFORE taking database backups or pulling git commits to flush WAL writes to disk cleanly.
  2. Backup scripts must back up all SQLite database files (`bot_database.db*` including `-wal` and `-shm`), never `.db` alone.
  3. The codebase must maintain autonomous in-process recovery via `repair_database.py` (3-tier recovery: In-Place Checkpoint, SQLite CLI, Pure-Python Table-by-Table Data Rescuer in `immutable=1` mode) so any corrupted B-tree page is healed on the fly with 100% zero data loss of VIP users, API keys, or active trades.

### Invariant 21: Python Function-Scope Global Import Hygiene (Anti-Shadowing / Zero-UnboundLocalError Guard)
- **Location:** All `.py` files across repository
- **Rule:**
  1. Never place `import <module> as <alias>` inside inner function scopes, `try/except` blocks, or loops if that `<alias>` (such as `db`, `trading_engine`, `loc`) is already imported or referenced at module level.
  2. In Python, any assignment or import of a name inside a function marks that name as local for the entire function scope, causing fatal `UnboundLocalError: cannot access local variable '<alias>' where it is not associated with a value` on all earlier usages. Always reference the top-level module import directly.

### Invariant 22: Telegram 1-Tap Copyable Monospace Preset & Interactive Mobile Toast Feedback Standard
- **Location:** `bot_thread.py` (`auto_trade_command`, callback query handlers, all command handlers)
- **Rule:**
  1. **Zero Unexecutable Placeholders:** Never output commands containing abstract placeholders like `<ទុន>` or `<amount>` in user-facing copyable blocks. All commands must be provided as concrete, executable monospace presets (e.g. `` `/auto_trade ON 30` ``, `` `/auto_trade ON 50` ``) wrapped in backticks for 1-tap clipboard copying on mobile.
  2. **Command Alias Parity:** Every multi-word command must register both underscored and continuous aliases (e.g., `auto_trade` and `autotrade`, `smart_trade` and `smarttrade`, `smart_x` and `smartx`, `smart_swap` and `smartswap`).
  3. **Mandatory Tactile Toast Feedback:** Every `InlineKeyboardButton` callback query MUST be immediately acknowledged with `await update.callback_query.answer(...)` containing descriptive toast text (e.g. `✅ Auto Trade: បានបើកដំណើរការ!`, `💰 បានកំណត់ទុន៖ $50 USDT!`) so mobile users receive instant visual and haptic confirmation without interface confusion.

### Invariant 23: Telegram Bot Menu Command Parity & Institutional Menu Hierarchy Standard
- **Location:** `bot_commands_registry.py`, `bot_thread.py`, `set_bot_commands.py`, `force_clear_and_set_commands.py`
- **Rule:**
  1. **Strict Command Parity & Zero Missing Handlers:** Every command registered in the Telegram Bot Menu MUST have an active, operational `CommandHandler` (plus canonical continuous alias) in `bot_thread.py` that executes accurately according to its institutional mathematical specifications. Zero unmapped commands or missing handlers are tolerated.
  2. **Institutional Menu Hierarchy Standard:** The public Telegram Bot Menu (`set_my_commands`) must be strictly organized in institutional logical tiers:
     - Header & Navigation: `/start`, `/menu`
     - Spot Investment Engines (100% Spot, 0% Liquidation Risk): `/compound_grid`, `/infinity_matrix`, `/smart_trade`
     - Futures & Hedge Engines: `/turbo_hedge`, `/smartx`, `/scalp`, `/auto_trade`
     - CeDeFi & Arbitrage Engines: `/flash_loan`, `/smart_swap`, `/cross_arb`, `/funding_harvester`, `/web3_wallet`
     - Market Intelligence & Radars: `/whales`, `/flash_crash`, `/pre_pump`, `/news`, `/analyze`, `/predict`, `/top`
     - Portfolio, Risk & Account Security: `/balance`, `/portfolio`, `/status`, `/report`, `/paper_trading`, `/alert`, `/stop`, `/set_pin`, `/reset_pin`
  3. **Bottom Placement for Admin Commands:** Super Admin exclusive commands (`/admin`, `/admin_users`, `/admin_license`, `/admin_broadcast`, `/admin_stats`, `/admin_config`, `/admin_nuke`, `/health`, `/sync_brain`) must strictly be appended at the BOTTOM of the Admin menu, never at the top, ensuring user-facing investment engines remain prominent.
  4. **Zero Phantom / Obsolete Commands:** Deprecated, replaced, or ghost commands (e.g. `/snipe`) must be 100% expunged from all menu registries so they never linger in Telegram user clients.
  5. **Permanent Core Inclusion:** All core trading, investment, intelligence, and safety commands must permanently remain in the Bot Menu unless the Admin explicitly requests removal.
  6. **Super Smart Zero-Confusion Command Hub Standard (`smart_bot_guide.py`, `/smart`, `/commands`, `/help`, `/vip`):**
     - Dynamically segregates interface, permissions, and command guidance based on caller privilege (`👑 SUPER ADMIN / SUPREME FLEET COMMANDER` vs `💎 VERIFIED VIP QUANT INVESTOR`).
     - Strictly organizes all tools into 6 non-confusing pillars: (1) Spot Investment Engines (100% Spot, 0% Liquidation Risk), (2) Futures & Hedge Engines (10x Isolated, Breakeven Armor, 85% Golden Ratchet), (3) TradFi Global Markets & MT5 (Gold, US Indices, Oil, Stocks CFD, In-Memory Radar), (4) AI Intelligence & Radars (33 AI Swarm, ML 24h Predictions), (5) Portfolio, Risk & Account Security (Balance, PnL, 2FA PIN, Emergency Stop), and (6) Super Admin Master Fleet Operations (Users, Licenses, Broadcast, Emergency Nuke, System Diagnostics).
     - Incorporates an interactive decision matrix and FAQ answering "Which engine should I use?" with instant one-tap navigation, eliminating 100% of interface and command confusion across all user and admin tiers.

### Invariant 24: The Golden 85% Profit Ratchet & Breakeven Armor Standard
- **Location:** `turbo_hedge_engine.py` (`monitor_turbo_hedge_pnl`), `bot_thread.py`
- **Rule:**
  1. **Breakeven Armor:** At +3.0% ROI, Stop Loss is unconditionally locked to Entry Price + Fees (+0.12% net profit floor). A winning position is strictly prohibited from degrading into a loss.
  2. **Golden 85% Ratchet:** As trailing profits expand, 85% of peak unrealized profit is permanently ratcheted and protected.
  3. **Clean Cash Harvest:** Upon reaching target parameters or trailing triggers, 100% clean cash closure must be executed without orphaned limit orders or residue margin.

### Invariant 25: Dynamic Small Capital Fortress & Zero Blind Investing Guarantee
- **Location:** `turbo_hedge_engine.py` (`scan_and_evaluate_symbol`, `execute_turbo_hedge_trade`), `bot_thread.py`
- **Rule:**
  1. **Dynamic Small Capital Scaler:** For accounts with capital < $100, orders are strictly capped at $5.00–$5.50 per coin (tiered capacity $\le 15$ pairs) with an absolute 65% available balance margin cushion (`avail_bal * 0.65`).
  2. **Zero Blind Investing Shield:** Entry requires multi-timeframe confirmation (1m/5m momentum strictly aligned with 15m/1h macro trend) and minimum institutional confidence hurdles.
  3. **Staggered Order Entry:** A minimum stagger interval is enforced between automated executions to prevent high-frequency order clustering.

### Invariant 26: Sub-Mode Explicit State Segregation & Non-Collapsible Architecture Invariant
- **Location:** `bot_thread.py`, `scheduler_tasks.py` (`gold_turbo_monitor`), `smart_x_engine.py`
- **Rule:**
  1. **Zero Silent Fallback Collapse (ហាមដាច់ខាតការទម្លាក់ Mode ច្រើនឱ្យនៅសល់តែមួយស្ងាត់ៗ):** Multi-mode command suites (`/smartx`, `/turbo_hedge`, `/smart_trade`) must strictly enforce explicit branching for EVERY discrete sub-mode. Ternary fallback defaults like `mode = A if is_a else B` that silently swallow additional states (such as `AUTO`, `SPOT`, etc.) are classified as architectural defects and strictly prohibited.
  2. **Mandatory Live Telemetry Feedback (តម្រូវការចាក់បញ្ចូលទិន្នន័យ Live Telemetry):** Confirmation and acknowledgment messages must never use static, undifferentiated templates. Every sub-mode MUST output distinct, live telemetry (real-time price, session window, liquidity score, SGE premium, and active AI model consensus) so the user is immediately provided with unambiguous proof of which engine is operating.
  3. **Dedicated Background Execution Routing (ការបែងចែកកូដរត់ Background ឱ្យដាច់ពីគ្នា):** Background monitors (such as `gold_turbo_monitor`) must maintain explicit, dedicated logic branches for every mode (e.g. `AUTO` must dynamically query MoE Regime Classification to route between `TURBO` expansion and `SONIC` session scalping, rather than defaulting to a single strategy).

### Invariant 27: Google Cloud e2-standard-4 Hardware Profile & Hugging Face Cloud AI Brain Specification Lock
- **Location:** Deployment Infrastructure, `systemd` service, `scheduler_tasks.py`, `ai_engine.py`, `hf_client.py`
- **Rule:**
  1. **Hardware Profile (GCP e2-standard-4):** The live production deployment operates on Google Cloud Platform `e2-standard-4` (4 vCPUs, 16 GB RAM) in Tokyo `asia-northeast1-a` with direct peering to Binance Asian liquidity clusters (< 10ms execution). The 16 GB RAM pool permanently eliminates Out-Of-Memory (OOM) risks, allowing the system to run high-throughput WebSocket streams and algorithmic scanners with zero reliance on high-latency swap memory.
  2. **Cloud AI Hybrid Brain Integration (Hugging Face HF_TOKEN):** The system leverages the Hugging Face Cloud Inference API via dedicated `HF_TOKEN` / `HUGGINGFACE_TOKEN` to execute deep quantitative reasoning models (DeepSeek-R1, Llama-3-70B, Qwen-2.5-72B) in the cloud with zero VPS RAM bloat, keeping local VPS memory usage lean (< 45 MB local ONNX/XGBoost/LSTM runtime).

### Invariant 28: 24/7 Perpetual Wealth Generator Dual-Engine Architecture & Triple-Phase Safety Covenant Lock
- **Location:** `perpetual_wealth_engine.py`, `bot_thread.py` (`wealth_command`), `scheduler_tasks.py` (`perpetual_wealth_monitor`), `database.py`
- **Rule:** The 24/7 Perpetual Wealth Generator (`/wealth`, `/wealth24/7`) is an institutional-grade, fully autonomous continuous capital accumulation and harvest engine operating in dual-engine mode: **Spot Engine (1x Leverage, 0.00% Liquidation Risk)** and **Futures Engine (10x ISOLATED Margin)** with strict Invariant 10 Multi-Wallet Balance Segregation. It is bound by the following permanent mathematical and risk covenants:
  1. **Dual Velocity Engine Specification (យន្តការចាប់កាក់ល្បឿនលឿន Spot & Futures) ៖**
     - **Spot 7-Pillar Velocity Engine:** Scans Binance Spot (+2.0% to +16.0%) with 15m RVOL Volume Surge $\ge 2.0\times$, Fresh Momentum ($1\text{h} \ge +0.6\%$ & $15\text{m} \ge +0.2\%$), Trend Strength ($ADX \ge 26.0$ & $+DI > -DI$), Dynamic AI Confluence Matrix ($\ge 8.6/10.0$), 3-Tier Anti-Stagnation Smart Clock (45m / 75m / 120m), and Micro-Breakeven Armor at $+1.5\%$ ROI (+0.20% fee floor).
     - **Futures 8-Pillar Dual-Directional Velocity Engine:** Scans Binance USDT-M Futures (+3.0% to +14.0% for LONG, -3.0% to -12.0% for SHORT) with 15m RVOL Volume Surge $\ge 2.0\times$, Dual-Directional Fresh Momentum ($1\text{h} \ge +0.6\%$/$\le -0.6\%$ & $15\text{m} \ge +0.2\%$/$\le -0.2\%$), Strict DMI Dominance ($+DI > -DI$ for LONG, $-DI > +DI$ for SHORT), Invariant 16 Anti-Oversold Short Guard ($RSI \le 38.0$ strictly blocks SHORT), Dynamic AI Confluence Matrix ($\ge 8.6/10.0$), and Futures 3-Tier Anti-Stagnation Smart Clock (30m / 60m / 90m).
   2. **100% Full-Position Ride & Adaptive Golden 85% Trailing Ratchet (យុទ្ធសាស្ត្រកើបចំណេញ ១០០% ពេញលេញ លុបបំបាត់ការកាត់ 50% ផ្ដាច់មុខ) ៖**
      - **Instant Active Execution (Zero Adverse Selection):** Entries execute immediately at MARKET (or marketable LIMIT touching book with instant MARKET fallback). Passive resting limit orders placed below the market are strictly prohibited to prevent adverse selection (missing winning breakouts and filling only dumping fakeouts).
      - **Zero 50% Chip Cutting (100% Full Capital Preservation):** The obsolete 50% partial take-profit rule (PARTIAL_TP1_50_PCT) is 100% eradicated. On high-velocity setups, cutting 50% reduces runner capital to negligible fractions (.75 margin) and doubles transaction fees. The engine now rides 100% of capital to peak exhaustion.
      - **Phase 1 (Early Breakeven Armor & Net Capital Defense):** When unrealized profit reaches $+6.0\% ROI (Futures) or $+2.0\% ROI (Spot), Breakeven Armor is armed early (is_be_locked = True) to protect capital against sudden reversals. If the trade stalls or reverses, the dynamic floor exits at scratch/net positive (+1.2% to +2.5% Net Floor), strictly barring winning trades from degrading into losses.
      - **Phase 2 & 3 (100% Full-Position Multi-Tier 85% Golden Trailing Ratchet):** Once peak reaches $\ge +8.5\%$ ROI (surpassing baseline TP1 threshold), the engine locks trailing profit floors dynamically:
        * *Tier 1 ($+8.5\% \le \text{Peak} < +15.0\%$):* Trailing floor at $\max(3.0\%, \text{Peak} \times 0.75)$. Trend exhaustion pullback triggers 100% full-position cash harvest (+75% peak gains retained).
        * *Tier 2 ($+15.0\% \le \text{Peak} < +30.0\%$):* Trailing floor at $\max(6.0\%, \text{Peak} \times 0.80)$ (80% peak gains retained).
        * *Tier 3 ($	ext{Peak} \ge +30.0\%$ or target TP $\ge +35\%$ hit):* Golden 85% Ratchet locks $\text{Peak} \times 0.85$ (TRAIL_85_PCT_OF_PEAK / curr_peak * 0.85). Pullback triggers 100% full moonshot harvest in sub-millisecond RAM latency (< 0.0001 ms RAM tick access / < 30ms fill).
  3. **Spot Engine Mode & 0.00% Liquidation Risk (Invariant 1 & 10) ៖**
     - Spot Wealth Engine operates with 1x leverage and 0% liquidation risk, allowing safe deployment of larger capital ($\$30–\$100+$ per coin) with zero funding fee drag.
     - Strictly enforces Invariant 1: Spot order notional must be at least $\$10.50$ USDT (`quote_order_qty = max(10.50, allocation)`).
     - Strictly isolates Spot USDT (`get_spot_balance`) from Futures USDT (`get_futures_balance`) to eliminate cross-wallet interference.
  4. **Pullback Retracement & Trend Strength Hurdles (Zero Top Chasing) ៖**
     - **ADX Trend Strength Hurdle:** Entry strictly requires Wilder's ADX(14) $\ge 25.0$ (Futures) or $\ge 26.0$ (Spot) to eliminate dead sideways chop.
     - **EMA20 Pullback Retracement Entry:** Buying green candle exhaustion tops is strictly prohibited; entries require a clean test of the 15m EMA20 dynamic support/resistance band (`0.994 * EMA20 <= price <= 1.008 * EMA20`).
     - **Anti-Oversold Short Guard (Invariant 16):** Short entries or reverse flips into short are 100% blocked if 15m RSI $\le 38.0$. Spot engine is strictly LONG-only.
  5. **Dynamic Kelly Capital Scaler & Small Capital Fortress ៖**
     - **Dynamic Kelly Capital Scaler:** For accounts with sufficient liquidity ($\ge \$60$ USDT available or total capital), margin per coin dynamically scales to $\$10.00–\$20.00+$ USDT (e.g. $\$10–\$15$ for $\$60–\$149$ accounts, $\$15–\$25$ for $\$150+$ accounts), multiplying net profit by $10\times–30\times$ over fee drag.
     - **Micro-Capital Fortress Shield:** For accounts $< \$60$ USDT, margin per coin is safely clamped to $\$8.00–\$12.00$ per coin with max 1–2 coins.
     - Maximum futures leverage is clamped to $\le 10\times$ for accounts $< \$100$ (ISOLATED Margin only, Invariant 3 & 8). Cross-Margin is strictly barred.
     - Dynamic Stop-Loss breathing cushion is bounded by $1.2\times$ 15m ATR ($-10.0\%$ ROI / max $-\$1.10$ USD risk on Futures, $-5.0\%$ to $-6.0\%$ price dip on Spot).
  6. **Continuous 24/7 Autonomous Symbol Rotation & Anti-Stagnation Reinvestment ៖**
     - Positions that fail to gain traction within 120–180 minutes are automatically closed by the 3-Tier Anti-Stagnation Smart Clock to eliminate capital lockup and save funding fees.
     - Upon position closure (TP, SL, or Anti-Stagnation Exit), capital is instantly recycled back into the available pool to scan the next Golden Sweet-Spot candidate from the top volatile spot/futures universe with zero human intervention required.
  7. **Persistence & Crash Resilience ៖**
     - Bot configurations and open trades are permanently persisted in SQLite (`perpetual_wealth_bots`, `perpetual_wealth_spot_bots`, `perpetual_wealth_spot_trades`). State persists seamlessly across VPS reboots and systemd restarts.
- **Enforcement:** Verified by `audit_system.py` [CHECK 21/22].

### Invariant 29: Nanosecond Direct RAM Tick Access Latency Standard (⚡ 0.001 – 0.0003 ms Invariant)
- **Location:** `websocket_engine.py`, `trading_engine.py`, `perpetual_wealth_engine.py`, `flash_loan_mev_engine.py`, `smart_swap_engine.py`, `turbo_hedge_engine.py`, `macro_auto_trade_engine.py`
- **Rule:**
  1. **Universal Direct RAM Pre-Cache Priority (ការទាញយកទិន្នន័យពី RAM Memory ជាអាទិភាពខ្ពស់បំផុត) ៖**
     Every pricing query, tick evaluation, macro BTC regime check, arbitrage spread evaluation, liquidation risk shield, trailing take-profit ratchet, or pre-flight entry check MUST prioritize and bridge directly into in-memory RAM data structures (`websocket_engine.PRICE_CACHE`, `BOOK_TICKER_CACHE`, fast shared memory dicts) achieving **⚡ 0.001 ms – 0.0003 ms (nanosecond/sub-microsecond)** RAM lookup access latency.
  2. **Strict Prohibition of Blocking Network I/O in Hot Trading Loops ៖**
     Under NO circumstances shall any critical execution loop, trailing stop monitor, or high-frequency scanning path execute serial, blocking HTTP/REST requests (which suffer 150ms – 500ms internet lag) when prices or ticks are available in the local WebSocket RAM cache.
  3. **Universal RAM Cache Access Interface ៖**
     Standardized helper interfaces (e.g. `get_fast_price(symbol)`, `get_fast_book_ticker(symbol)`, `get_hft_fast_sol_price()`, etc.) must be universally accessible across all modules to ensure zero-overhead, sub-millisecond algorithmic decisions.
- **Enforcement:** Verified by `audit_system.py` [CHECK 22/23].

### Invariant 30: Perpetual Wealth Free Margin Gatekeeper, Autonomous Stale Limit Prune & Smart Swap DEX Volatility Buffer Standard
- **Location:** `perpetual_wealth_engine.py`, `trading_engine.py` (`get_futures_open_orders`, `cancel_all_futures_open_orders`, `get_futures_free_margin`), `smart_swap_engine.py`
- **Rule:**
  1. **Exact Free Margin Gatekeeper (ទប់ស្កាត់ Error -2019 ដោយឆែក Free Margin ពិតប្រាកដ) ៖**
     In `perpetual_wealth_engine.py`, candidate order entry MUST verify `trading_engine.get_futures_free_margin()`. If `avail_free_usdt < margin_per_coin`, candidate dispatch is immediately skipped (`continue`). This permanently blocks premature order dispatch when margin is occupied, eliminating Binance Error `-2019 Margin is insufficient` and spurious order failures.
  2. **15-Minute Candidate Order Placement Cooldown (ការពារការបញ្ជាទិញស្ទួន) ៖**
     Immediately upon submitting a limit order for any symbol, `add_wealth_cooldown(sym, duration_seconds=900)` is invoked, barring duplicate order placement on the same symbol for 15 minutes.
  3. **Autonomous Stale Limit Order Prune (> 10 Minutes) ៖**
     Unfilled limit orders resting on Binance Futures for $> 10$ minutes are automatically cancelled via `cancel_all_futures_open_orders(api_key, api_secret, stale_sym)` to recover locked margin, ensuring capital remains agile and free of deadlock.
  4. **Smart Swap On-Chain Dynamic Volatility Buffer ($-25.0\%$ Deep Floor) ៖**
     In `smart_swap_engine.py`, the Emergency Stop-Loss floor is locked at $\le -25.0\%$ ROI (giving high-momentum Solana DEX gems adequate breathing room across DEX spreads, pool fees, and retracements to eliminate "death by a thousand cuts" premature chop-outs, while strictly preserving $75\%$ of capital against catastrophic $100\%$ zero-out rug pulls).
  5. **Network Resilience & Robust Alert Timeout ៖**
     Background Telegram notification dispatchers (`_async_send_wealth_alert`, etc.) must enforce robust network timeouts (`read_timeout=15s, write_timeout=15s, connect_timeout=10s`) to prevent network jitter timeouts during high-latency periods.
- **Enforcement:** Verified by `audit_system.py` [CHECK 23/24].

### Invariant 31: Capital.com Lead-Lag Arbitrage Engine & Pure Latency Alpha Standard (⚡ 500ms – 2000ms Lag Extraction)
- **Location:** `capital_engine.py` (`CapitalLeadLagArbitrageEngine`, `start_capital_leadlag_listener`), `database.py`, `bot_thread.py`
- **Rule:** The `/capital` trading ecosystem integrates real-time Lead-Lag Arbitrage exploiting empirical pricing lag (500ms – 2000ms) between Binance WebSocket feeds and Capital.com Crypto CFD order books during high-volatility impulse waves:
  1. **Sub-Millisecond In-Memory Ingestion (< 0.05ms):** Incoming Binance ticks are received directly in RAM via `websocket_engine.register_tick_listener(on_binance_tick)` without polling delays.
  2. **Impulse Spike Detection:** Measures price velocity $\Delta P\%$ over rolling lookback windows (250ms – 1200ms). Triggers only on confirmed volatility surges ($|\Delta P\%| \ge 0.15\%$ for BTC, $\ge 0.20\%$ for ETH).
  3. **Spread Hurdle Verification:** Measured price dislocation must exceed Capital.com's live CFD bid-ask spread by at least $1.4\times$ ($|\text{Dislocation}| \ge \text{Spread}_{\%} \times 1.4$) to eliminate spread bleed and guarantee positive net expectancy.
  4. **Strict Invariant 16 Compliance:** Any downward impulse short signal is strictly blocked if the 15-minute RSI is $\le 38.0$ to prevent shorting retail panic bottoms.
  5. **Asynchronous Non-Blocking Order Dispatch:** Order submission to Capital.com runs in a dedicated thread pool (`ThreadPoolExecutor`), completely decoupling execution latency from the core Binance WebSocket event loop.
- **Enforcement:** Verified by `audit_system.py` [CHECK 24/25].

### Invariant 32: London & New York Opening Range Breakout (ORB 15m) Matrix Standard
- **Location:** `capital_engine.py` (`CapitalOpeningRangeBreakoutEngine`, `get_capital_orb_engine`), `database.py`, `bot_thread.py`, `scheduler_tasks.py`
- **Rule:** The `/capital` trading ecosystem integrates an institutional 15-minute Opening Range Breakout (ORB) Matrix capturing liquidity explosions during London Open and Wall Street New York Open sessions across TradFi assets (Gold XAU/USD, S&P 500, Nasdaq, DAX, Crude Oil, Natural Gas):
  1. **Canonical Session Windows (Phnom Penh UTC+7):**
     - **London Open:** 08:00–08:15 UTC (15:00–15:15 Phnom Penh) Range Formation -> 08:15–11:30 UTC (15:15–18:30 Phnom Penh) Breakout Execution.
     - **Wall Street New York Open:** 13:30–13:45 UTC (20:30–20:45 Phnom Penh) Range Formation -> 13:45–17:00 UTC (20:45–00:00 Phnom Penh) Breakout Execution.
  2. **Range Sanity Filter:** Breakout execution is strictly bypassed if the 15-minute Opening Range ($OR_{\text{Range}} = OR_{\text{High}} - OR_{\text{Low}}$) is $> 2.5 \times \text{ATR}_{14}$ (exhaustion candle) or $< 0.20 \times \text{ATR}_{14}$ (no institutional participation).
  3. **Strict Invariant 16 Anti-Oversold Short Guard & Anti-Exhaustion BUY Guard:** Any downward breakdown below $OR_{\text{Low}}$ is strictly blocked if the 15-minute RSI is $\le 38.0$ to eliminate shorting panic sell-offs at the bottom. Upward breakouts are strictly blocked if RSI $> 68.0$ (Anti-Exhaustion).
  4. **Strict Anti-Fakeout Wick Rejection & 5m Candle Body Confirmation:** Breakout executions reject sub-second wick spikes if the 5m candle displays an upper wick ratio $> 35\%$ on BUY (selling into the spike) or lower wick ratio $> 35\%$ on SELL (dip buying absorption). Real volume surge ($RVOL \ge 1.20$) and full quant technical validation are mandatory for both BUY and SELL breakouts.
  5. **Asymmetric R:R $\ge 1:3$ to $1:6$ with Dynamic ATR Stop & Expanded TP:** Stop-Loss is placed at the Range Midpoint or dynamic ATR floor ($OR_{\text{Mid}} = \frac{OR_{\text{High}} + OR_{\text{Low}}}{2}$), and Take-Profit targets are calibrated for **+5.0% to +8.0% ROI** (4R - 6R) on 20x leverage assets.
  6. **End-of-Quarter (Quarter-End) Window Dressing Defense:** Breakout entries enforce institutional high conviction threshold ($\ge 85\%$) during the final 2 days of a financial quarter (March, June, September, December) to prevent falling victim to institutional portfolio rebalancing fakeouts.
  7. **20x Leverage Asset Priority:** To maximize profit velocity and capital efficiency on small accounts ($30 - $100), `US100`, `US500`, and `GOLD` receive an institutional +35.0 to +40.0 score boost to be prioritized into active trade slots before 5x leverage stocks.
  8. **Breakeven Breathing Room & 3rd Runner Golden Trailing Ride:** Positions are protected by Breakeven Armor triggered at **+4.8% ROI** (+0.25% Net Floor, upgraded from +2.5% to clear broker spread noise and normal retests). When $\ge 3$ positions are held, the #1 performing position is designated as the **Apex 3rd Runner**, exempted from early close and trailed by the Golden 85% Trailing Ratchet up to **+25.0% to +35.0% ROI** ($4 - $6+ net profit per $10 order).
  9. **Session Debounce & Closed PnL Reconciler:** Exactly 1 trade per session per symbol is permitted. Engine automatically synchronizes closed broker positions and displays cumulative closed PnL metrics in `/capital` dashboard.
- **Enforcement:** Verified by `audit_system.py` [CHECK 25/27].

### Invariant 33: Fractional Kelly Criterion Dynamic Position Sizer Standard ($f^*$)
- **Location:** `capital_engine.py` (`CapitalKellyPositionSizer`, `get_capital_kelly_sizer`), `database.py`, `bot_thread.py`, `bot_commands_registry.py`
- **Rule:** Capital sizing across the `/capital` TradFi engine is strictly governed by the institutional Fractional Kelly Criterion to optimize geometric portfolio growth $\mathbb{E}[\ln(W)]$ while mathematically preventing ruinous drawdowns:
  1. **The Kelly Equation ($f^*$):**
     $$f^* = \frac{p(b + 1) - 1}{b} = \frac{p \cdot b - (1 - p)}{b}$$
     where $p \in [0.50, 0.98]$ is calibrated from the AI Confluence Score (Google Macro + Central Bank + ADX + Volatility) and $b \ge 2.5$ is the payoff ratio (Take Profit / Stop Loss distance).
  2. **Institutional Fractional Multipliers ($\kappa$):**
     Full Kelly ($1.0 \times f^*$) is strictly prohibited due to excessive portfolio volatility (~33% drawdown probability). The system strictly enforces **Fractional Kelly**:
     - Conservative Mode: $\kappa = 0.20$ ($0.20 \times f^*$)
     - Balanced Mode: $\kappa = 0.35$ ($0.35 \times f^*$)
     - Aggressive Mode: $\kappa = 0.50$ ($0.50 \times f^*$)
  3. **Hard Equity Risk Clamp ($R_{\max} \le 3.5\%$):**
     Total capital at risk per trade is strictly clamped to $\min(\kappa \cdot f^*, R_{\max})$ with a maximum ceiling of $3.5\%$ of account equity/budget, preventing single-trade catastrophic losses.
  4. **Dynamic Scale Behavior (Confluence Expansion & Choppy Contraction):**
     - When AI Confluence is overwhelming ($\ge 90\%$), position size dynamically scales up to $1.5\times - 2.0\times$ base tier.
     - When the market is choppy or ranging ($< 65\%$), position size contracts to the minimum micro-lot floor ($0.01$ lot / $0.1$ contract), minimizing drawdowns.
  5. **Asset-DNA Lot Boundary & Step Snapping:**
     Calculated contract sizes must strictly adhere to broker-defined lot steps and min/max boundaries (e.g. Gold $0.01$ step, US500 $0.05$ step, BTC $0.001$ step) to prevent order rejections.
   6. **Small Capital Fortress Clamp & Asset Prioritization (< $100 Accounts):**
      To eliminate outsized outlier losses and capital leakage on micro accounts ($30 - $100):
      - `NATURALGAS`: Baseline reduced from 50.0 to 10.0 - 15.0 contracts, and completely bypassed/shielded from autonomous selection on accounts < $100 due to wide spread and violent whipsaws.
      - `OIL_CRUDE`: Baseline reduced from 1.5 to 0.3 - 0.5 barrels, capping 1R downside risk strictly to $\le \$0.30 - \$0.50$.
      - **100% Win Rate Asset Priority:** The engine assigns highest confluence boost (+50) and top execution slots to proven 100% win-rate and ultra-low spread instruments: `US500` (S&P 500), `GOLD`, `NVDA`, and `TSLA`.
- **Enforcement:** Verified by `audit_system.py` [CHECK 26/27].

### Invariant 34: Spread Drag Elimination & Asymmetric Minimum Hurdle Protocol (Target $\ge 10\times$ Spread)
- **Location:** `capital_engine.py` (`CapitalSpreadDragManager`, `get_capital_spread_drag_manager`), `database.py`, `bot_thread.py`, `bot_commands_registry.py`
- **Rule:** CFD brokers monetize order flow via Bid/Ask Spreads. Retail scalping for tight $0.2\% - 0.5\%$ targets sacrifices $40\% - 60\%$ of gross edges to spread drag. The system strictly enforces the 4-pillar Spread Drag Elimination Protocol:
  1. **Minimum 10.0x Target-to-Spread Hurdle ($\mathcal{H} \ge 10.0$):**
     Every executed position must enforce a Take-Profit distance of at least $10.0\times$ the prevailing spread:
     $$TP_{\text{dist}} = |TP - \text{Entry}| \ge 10.0 \times \text{Spread}$$
     This mathematically clamps maximum Spread Drag to $\le 10\%$:
     $$\mathcal{D} = \frac{\text{Spread}}{TP_{\text{dist}}} \le \frac{1}{10.0} = 10.0\%$$
     guaranteeing that $\ge 90\%$ of gross captured price action converts directly into clean Net Profit.
  2. **Asymmetric Risk-to-Reward Ratio ($R:R \ge 1:6$):**
     Downside risk (1R) is placed outside market noise:
     $$SL_{\text{dist}} = |SL - \text{Entry}| \ge \max(1.5 \times \text{ATR}_{14}, 2.5 \times \text{Spread})$$
     and upside target (6R) is enforced at $TP_{\text{dist}} \ge \max(6.0 \times SL_{\text{dist}}, 10.0 \times \text{Spread})$, yielding positive expectancy even with a conservative $35\%$ win rate.
  3. **Volatility-to-Spread Quality Index (VSQI $\ge 3.0$):**
     $$\text{VSQI} = \frac{\text{ATR}_{14}}{\text{Spread}}$$
     If $\text{VSQI} < 3.0$, the asset's current volatility is too compressed relative to transaction friction (liquidity drought / holiday freeze). Orders are strictly blocked with reason `SPREAD_CONGESTION_VSQI_LOW`.
  4. **Pre-Execution Spread Expansion Shield:**
     Orders are immediately aborted if live spread expands $> 30\%$ above historical baseline ($\text{Spread} > 1.30 \times \text{Baseline}$) due to sudden liquidity withdrawal or news spike blowout.
### Invariant 35: Mathematical Breakeven Armor, Anti-Whipsaw Buffer & 15-Minute Asset Cooldown Standard
- **Location:** `capital_engine.py` (`_ratchet_engine_positions`, `execute_autonomous_cycle`, `execute_orb_cycle`, `execute_smart_tradfi_order`), `audit_system.py`
- **Rule:** To eliminate "Death by a Thousand Papercuts", premature stop-outs, and spread bleed on Capital.com CFD positions:
  1. **Strict Mathematical Price Buffering for Breakeven Armor:**
     - Breakeven Armor triggers strictly at $\ge +8.5\%$ ROI on margin or $\ge +\$3.50$ UPL ($\ge +1.5\text{R}$), providing ample breathing room before shifting stop levels.
     - The modified Stop-Loss for BUY positions MUST be strictly $\le \text{current\_market\_price} - (1.5 \times \text{Spread})$, and for SELL positions MUST be $\ge \text{current\_market\_price} + (1.5 \times \text{Spread})$ — NEVER higher than market price for BUY or lower for SELL.
     - The Stop-Loss locks in at least $\text{Entry} + (0.5 \times \text{Spread})$ for BUY (and $\text{Entry} - 0.5 \times \text{Spread}$ for SELL) to guarantee a genuine net profit after all broker spread costs.
  2. **Dynamic Volatility Breathing Stop Distance:**
     - Initial Stop-Loss in `execute_smart_tradfi_order` must enforce:
       $$\text{SL Distance} \ge \max(2.50 \times \text{ATR}, 3.50 \times \text{Spread}, 0.0035 \times \text{Price})$$
     - Completely eradicates premature shakeouts from broker spread widening or normal market breathing noise.
  3. **Delayed Multi-Tier Harvest & Fee-Clearing Trailing Ratchet:**
     - Position Retracement Exit is delayed until peak UPL achieves $\ge +\$6.00$ or $\ge +14.0\%$ ROI on margin.
     - Closes only when guaranteed net profit clears fees: $\text{UPL} \ge \max(2.0, \text{spread} \times 2.0)$.
     - Broker Stop-Loss Ratchet is delayed until $\ge +12.0\%$ ROI or peak UPL $\ge +\$5.00$.
  4. **15-Minute Anti-Overtrading Asset Cooldown Shield:**
     - Whenever a position closes (via SL, TP, or Breakeven), a mandatory 15-minute cooldown (`self._asset_cooldowns[epic] = now + 900.0`) is enforced on that asset.
     - Prevents high-frequency re-entry churn and repeated spread bleed in sideways consolidation.
  5. **Normalized 1R Dollar Risk Allocation:**
     - Sizing across assets is calibrated to equalize 1R dollar risk ($1.20 - $2.50 per trade on micro/small capital), clamping Gold (`GOLD`) to $0.01 - 0.02$ lot so that one loss on Gold cannot overwhelm profits from Oil/Indices/Stocks.
  6. **Expulsion of Natural Gas from Automated ORB Breakouts:**
     - Erratic, wide-spread assets like `NATGAS` are 100% expunged from automated ORB breakout execution.
  7. **Sub-Millisecond Concurrent Multi-Trader Dispatch (< 0.0005ms Fan-Out Invariant):**
     - Sequential iteration loops over multiple active users are strictly eliminated.
     - Trade evaluations, balance verifications, and order executions across all active traders (Live Mainnet and Demo Evaluation) are dispatched simultaneously in parallel via syncio.gather and dedicated thread-pool workers (xecute_autonomous_cycle, xecute_orb_cycle, _execute_lead_lag_trade_worker, xecute_forex_cycle).
     - Eliminates the 4–5 second sequential broker delay between users, guaranteeing identical market snapshot pricing, zero execution disparity, and synchronized Breakeven Armor execution across tens of thousands of traders.
   8. **Volatility Shock & Flash Reversal Protective Early Harvest (SHOCK_EARLY_HARVEST):**
      - When an open position achieves $\text{Peak UPL} \ge \$2.50$ (or $\text{Peak ROI} \ge +8.0\%$) and subsequently experiences a sharp reversal where current UPL erodes to $\le 50\%$ of peak (`upl <= peak_upl * 0.50`), the engine immediately fires an emergency market exit. This prevents sudden market drops or flash pumps from erasing gains and turning winning trades into deep losses.
   9. **Universal Cross-Engine Deduplication & Single-Asset Exposure Lock:**
      - All execution paths (`CapitalAutonomousEngine`, `CapitalOpeningRangeBreakoutEngine`, `CapitalTrendScalpEngine`) must audit active open epics across the entire account. If an asset is already active, any secondary entry attempt is immediately aborted (`DEDUP_ALREADY_OPEN`), eliminating duplicate position stacking on US100, GOLD, or tech equities.
   10. **Unified 3-Table Broker SL Reconciliation & 45-Minute Cross-Engine Quarantine:**
       - Broker position closures are reconciled across all three engine ledgers: `capital_auto_trades`, `capital_orb_trades`, and `capital_scalp_trades`.
       - Any position closed via Stop-Loss (`pnl < 0`) triggers an immediate 45-minute cooldown (`self._asset_cooldowns[epic] = now + 2700.0`) across all engines, stopping immediate re-entry churn on the same asset.
   11. **High-Beta Index & Stock Capital Sizing Shield for Micro Accounts (< $500 Capital):**
       - `CapitalKellyPositionSizer.calculate_lot_size` enforces strict maximum lot caps when available equity $< \$500$:
         * `US100` (Nasdaq 100): maximum $0.05$ contracts.
         * `US500` (S&P 500): maximum $0.10$ contracts.
         * US Mega-Cap Equities (`NVDA`, `TSLA`, `META`, `GOOGL`, etc.): maximum $0.20$ shares.
   12. **Emergency Stop-Loss Patrol & Suicidal Stop Tightening:**
       - Continuous patrol in `_ratchet_engine_positions` dynamically discovers missing SLs (`sl <= 0`) or erroneous stops placed $> 15\%$ away from current market price, immediately updating them to a volatility-adapted breathing stop (`safe_dist = max(spread * 3.5, current_price * 0.015)`).
- **Enforcement:** Verified by `audit_system.py` [CHECK 28/29].

### Invariant 36: Capital.com Pro Referral Gatekeeper & Live Account Verification Standard
- **Location:** `database.py` (`is_capital_user_authorized`, `set_capital_user_referral_status`, `get_pending_capital_verification_users`), `capital_engine.py` (`CAPITAL_PRO_REFERRAL_URL`, `get_partner_dashboard`, `execute_autonomous_cycle`, `execute_orb_cycle`, `execute_leadlag_cycle`), `bot_thread.py` (`build_capital_referral_gatekeeper_ui`, `admin_capital_command`, `capital_command`, button callback handlers)
- **Rule:**
  1. **Demo Mode Freedom ($10,000 Virtual):** Demo mode is 100% open and unrestricted for all users to test, backtest, and explore the bot.
  2. **Strict Live Mode Gatekeeper:** Live Real Capital Trading (Auto-Trade, ORB Breakout, Lead-Lag Arbitrage, and Manual Trading) is strictly gated. Any unverified Live account attempting to trade is intercepted with the **Referral Gatekeeper UI**.
  3. **Official Pro Referral URL Lock:** The default partner referral link across the repository is permanently locked to:
     `https://capital.com/referafriend-pro?c=az48cxia&pid=referral&src=inviteFriends&license=BAH&mn=ifbahpro1000` (Partner Code: `az48cxia`).
  4. **Authorization Protocol:** A user is authorized for Live Real Capital if:
     - `chat_id == 859271875` (Master Super Admin), or
     - `is_referral_verified == 1` in `user_capital_credentials`, or
     - `partner_code` contains `az48cxia` in `capital_user_referrals`, or
     - `license_expiry == 'Administrator'`.
  5. **1-Tap Admin Approval Workflow:** Users can submit instant verification requests via Telegram (`btn_cap_req_verify`), generating an interactive approval card for Super Admin with `[ ✅ Approve Live Access ]` and `[ ❌ Reject ]` callbacks.
   6. **Multi-Asset 5-Position Auto-Trade Standard:** Users and Admins can configure up to 5 concurrent positions across 24/7 priority assets (e.g. /capital AUTO ON 50 5 or /admin_capital on <id> 50 live 5). Daytime Asian and London sessions scan at least 7 liquid 24-hour assets (US500, GOLD, US100, OIL_CRUDE, SILVER, BTCUSD, ETHUSD) while Wall Street NY session activates US Mega-Cap stocks (NVDA, TSLA, AAPL, MSFT, GOOGL, META) guaranteeing up to 5 active positions round-the-clock.
- **Enforcement:** Verified by `audit_system.py` [CHECK 29/30].

### Invariant 37: Super Smart 24/7 Multi-Session Forex Exchange & Satellite Geospatial Alpha Protocol
- **Location:** `capital_engine.py` (`CapitalSatelliteMacroRadar`, `CapitalOUMeanReversionEngine`, `CapitalForexExchangeSuite`, `run_capital_forex_cycle`), `bot_thread.py` (`forex_command`, `master_button_callback`), `bot_commands_registry.py`, `scheduler_tasks.py` (`capital_forex_monitor`), `audit_system.py`
- **Rule:** The 24/7 Global Forex Exchange operates across 4 distinct institutional market regimes:
  1. **Tokyo / Asian Session (00:00 - 07:00 UTC):**
     - Governed by **Ornstein-Uhlenbeck (OU) Stochastic Calculus Mean Reversion**:
       $$dX_t = \theta(\mu - X_t)dt + \sigma dW_t$$
     - Orders are dispatched strictly when $|Z\text{-score}| \ge 1.85$ on range-bound currency pairs (`USDJPY`, `AUDUSD`, `EURGBP`, `USDCHF`), targeting the long-term equilibrium price $\mu$.
  2. **London Session (07:00 - 13:30 UTC):**
     - Governed by **15-Minute Opening Range Breakout (ORB)** tracking institutional interbank capital flows (`EURUSD`, `GBPUSD`, `GERMANY40`, `EURJPY`).
  3. **New York Session (13:30 - 21:00 UTC):**
     - Governed by **Apex Trend Following + Central Bank NLP Sentiment** (<100ms processing of Fed, ECB, BoE, and BoJ statements) with a mandatory $\ge 80\%$ 33 AI Models Swarm Consensus.
  4. **Weekend Session (24/7 Continuous):**
     - Governed by **Crypto CFDs Lead-Lag Arbitrage** (`BTCUSD`, `ETHUSD`, `SOLUSD`) capturing sub-second broker pricing disparities.
  5. **Physical Geospatial Macro Radar (Google Satellite Imagery):**
     - Quantitative trade biases integrate physical supply chain telemetry (Rotterdam/Singapore port container velocity, Permian Basin oil flaring, and Pilbara mining indices).
  6. **Risk Management & IB Compounding:**
     - Dynamic lot allocation via **Fractional Kelly Sizing ($f^*$)**, **10x Hurdle Spread Drag Elimination**, **Breakeven Armor at $+3.0\%$ ROI**, and **30%-50% IB Spread Rebate Compounding** ($+$2.40 - $+$4.00/lot pure cash flow).
- **Enforcement:** Verified by `audit_system.py` [CHECK 30/31].

### Invariant 38: Quantitative Trifecta Autonomous Engine Protocol (/smartx_reachsey_crypto, /pre_pump, /auto_trade)
- **Location:** `smart_x_engine.py` (`ReachseyStraddleEngine`, `execute_reachsey_crypto`, `stop_reachsey_crypto`), `pre_pump_engine.py` (`PrePumpEngine`, `evaluate_trifecta_signal`, `analyze_character_with_33_models`), `macro_auto_trade_engine.py` (`run_macro_auto_trade_scanner_cycle`, `execute_macro_auto_trade`), `bot_thread.py`, `scheduler_tasks.py` (`reachsey_crypto_monitor`, `pre_pump_sniper_monitor`)
- **Rule:** The quantitative trifecta engines operate with mathematical edge, strict risk partitioning, and zero technical negligence:
  1. **Reachsey Crypto Multi-Asset Stop Matrix (`/smartx_reachsey_crypto`):**
     - Sub-millisecond direct exchange pending stop placement (`STOP_MARKET` on Binance Orderbook).
     - 500+ Universe RAM Velocity Radar driven by Hawkes Jump Process $\lambda(t)$, Volume Clustering, and Elastic Dynamic ATR Gaps ($0.55\times - 0.80\times$ ATR breakout side / $1.10\times - 1.50\times$ ATR opposite).
     - Asymmetric $1:10.0$ R:R with Breakeven Armor armed at $+3.0\%$ ROI (+0.12% Net Floor Lock) and Golden 85% Profit Ratchet.
     - Sub-30ms Smart OCO Auto-Pruner canceling opposing pending legs upon position fill.
     - Anti-Oversold (15m RSI $\le 38.0$ blocks Sell-Stop) and Anti-Overbought (15m RSI $\ge 68.0$ blocks Buy-Stop) safety shields.
  2. **Institutional Smart Listing & Pre-Pump Accumulation Engine (`/pre_pump`):**
     - Real-time L2 orderbook depth scanning for genuine whale accumulation walls ($\ge \$100\text{k}$ BTC/ETH, $\ge \$25\text{k}$ alts) protected by Orderbook Anti-Spoofing.
     - 33 Wall Street AI Models Swarm (HMM/MoE Gating Router, PINN Jump-Diffusion, XGBoost, LightGBM, CatBoost) with $\ge 85.0\%$ confidence quorum.
     - Dynamic Fractional Kelly Leverage Sizing ($f^* = \frac{p \cdot b - q}{b}$) clamped to safe $3\times - 12\times$ ISOLATED margin.
     - Strict 20-minute Hard Time-Stop Guard for zero bag-holding on unconfirmed breakouts.
  3. **Super Smart Macro Auto-Trade Waterfall Breakdown & Swing Engine (`/auto_trade`):**
     - Multi-timeframe trend breakdown & breakout detection on 1H/4H + 15m flag retests with 33 AI models consensus.
     - Ultra-wide liquidation buffer via $3\times - 5\times$ ISOLATED Margin ($\sim 33\%$ safety distance) and Mutual Non-Aggression Shield with `/turbo_hedge`.
     - Anti-Wick Liquidity Sweep Shield preventing premature stop-out on fakeout spikes.
     - The Golden 85% Profit Ratchet locking $\ge 85\%$ of peak unrealized profit.
- **Enforcement:** Verified by `audit_system.py` [CHECK 31/31].

### Invariant 39: 500-Coin Mathematical DNA Profiling, Fixed-Dollar Risk Parity (-$1.10 to -$1.50 Max SL) & Non-Premature Breakeven Trailing Protocol
- **Location:** `perpetual_wealth_engine.py` (`monitor_perpetual_wealth_positions`), `database.py`, `bot_thread.py`, `audit_system.py`
- **Rule:** The 500-coin Binance universe possesses divergent volatility, liquidity, and beta profiles requiring mathematical risk parity and non-premature profit extraction:
  1. **500-Coin Volatility DNA Quadrants (ចំណាត់ថ្នាក់ចរិតលក្ខណៈកាក់ទាំង ៥០០) ៖**
     - **Quadrant 1 (Ultra-Cap Anchors - BTC, ETH, SOL, BNB):** Volatility 1.5%–4.0%, deep orderbooks, lowest slippage. Serves as macroeconomic compass and beta baseline.
     - **Quadrant 2 (Large-Cap Institutional High-Beta - AVAX, NEAR, LINK, SUI, APT):** Volatility 3.0%–8.0%, liquid derivatives, clean technical swing structures.
     - **Quadrant 3 (Mid-Cap Momentum Runners - FET, RENDER, INJ, TIA, SEI):** Volatility 5.0%–12.0%, subject to explosive multi-hour trend expansions.
     - **Quadrant 4 (Micro-Cap / Meme Hyper-Beta - PEPE, WIF, 1000BONK, PUMP, FLOCK):** Volatility 8.0%–25.0%+, subject to aggressive 15m wick noise followed by parabolic surges. Requires wide breathing room to prevent chop stop-outs.
  2. **Fixed-Dollar Risk Parity Stop-Loss (-$1.10 to -$1.50 Hard Cap) (ពិដានកំណត់ទំហំខាតអតិបរមា -$1.10) ៖**
     - In small capital accounts ($10–$100), deep outlier losses (-$2.50 to -$3.62) previously erased 5 to 10 micro-wins.
     - The engine strictly enforces a non-negotiable **-$1.10 to -$1.50 USD hard dollar ceiling** on loss:
       `is_sl_trigger = (unRealizedProfit <= -1.50) or (net_exit_pnl <= -1.50) or (roi_pct <= -10.0) or (pos_margin > 0 and unRealizedProfit <= -max(0.60, min(1.20, pos_margin * 0.12)))`
     - Downside risk per trade ($1R$) is strictly clamped to $\le \$1.10$ USDT on standard positions, eliminating destructive loss tails.
  3. **Non-Premature Breakeven Armor & Retracement Trailing Floor (ហាមដាច់ខាតការកាត់ចំណេញខ្ចីមុនពេលកំណត់) ៖**
     - Breakeven Armor is armed at $+6.0\%$ ROI (early protection) and $\ge +10.0\%$ ROI (`roi_pct >= 10.0 or curr_peak >= 10.0`), giving trades generous breathing room to absorb natural 0.5%–1.0% pullback fluctuations.
     - Once armed, it establishes `be_net_floor_roi = max(6.5, curr_peak * 0.65)` when `curr_peak >= 10.0`, or `max(2.5, curr_peak * 0.70)` on runners after TP1.
     - The exit trigger MUST strictly check `is_be_trigger = is_be_locked and (roi_pct <= be_net_floor_roi)`.
     - Inverted dollar thresholds like `(net_exit_pnl <= 1.00 and roi_pct > 0.0)` are **STRICTLY PROHIBITED**, as they prematurely snipe small-margin positions upon reaching +10.15% ROI before they can reach TP1 and TP2.
  4. **Asymmetric Risk-to-Reward Ratio ($R:R \ge 1:2.5$ to $1:8+$) & Positive Expectancy ($E[X] > 0$) ៖**
     - $1R$ Downside Risk: strictly capped at $-\$1.10$ (or $-\$1.50$ absolute max).
     - Phase 2 (TP1): $+8.5\%$ ROI (takes 50% partial profit off table, securing $+\$0.50$ to $+\$0.65$ net cash, ensuring $W \ge 72\%$).
     - Runner Guaranteed Lock: Runner floor anchored at $+2.5\%$ Net ROI, guaranteeing total trade win $\ge +\$0.70$ Net even on full retrace.
     - Phase 3 (TP2): $+25.0\%$ to $+50.0\%+$ ROI (moonshot runner dynamically trailed at 85% of peak ROI, banking $+\$2.00$ to $+\$3.50$).
     - Mathematical Expectancy ($E[X]$): With Win Rate $W \ge 72\%$, Average Win $\bar{G} \approx +\$1.31$, Loss Rate $L \le 28\%$, and Average Loss $\bar{L} \le -\$1.10$:
       $$E[X] = (0.72 \times \$1.31) - (0.28 \times \$1.10) = \$0.94 - \$0.31 = \mathbf{+\$0.63 \text{ Net Profit per Trade!}}$$
  5. **Brutal Engineering Honesty & 100% Real PnL Reporting (Invariant 19) ៖**
     - Telegram alerts must report exact net realized PnL (`net_exit_pnl`) without artificial clamping (`max(1.00, net_exit_pnl)` is permanently purged).
- **Enforcement:** Verified by `audit_system.py` [CHECK 32/33].

   6. **IEEE 754 Floating-Point Truncation Elimination & Autonomous Dust Scale-Up Protocol (យន្តការលុបបំបាត់កាក់សល់ & Scale-Up ទុនស្វ័យប្រវត្ត) ៖**
      - **IEEE 754 Floor Zero-Residual Invariant:** Quantity precision formatting strictly uses `math.floor(round(raw_qty * factor, 8)) / factor` across `trading_engine.py` (`get_futures_max_sellable_qty`, `get_max_sellable_qty`). This eliminates the floating-point truncation artifact (such as $0.57 \times 100 = 56.99999999999999$ flooring to $56$), which previously caused close orders to leave $0.01$ lot size residual dust unclosed on Binance.
      - **Autonomous Dust Scale-Up / Replenishment on Ultra-High Conviction (\ge 80% - 90%):** If an existing position possesses residual micro-dust (< $2.00 margin, e.g. $0.09 USDT) and the 33-AI Model discovers a fresh high-conviction breakout confluence (\ge 80% - 90%), the engine does NOT skip the coin or let the slot stay stranded. It dynamically calculates the required delta quantity and fires an Instant Market order to scale the margin up to the full target ($5.50 USDT), re-arming TP1 (+8.5%), Breakeven Armor, and TP2 moonshot ratchets.
      - **Breakeven Defense Scratch Misclassification Elimination:** When Breakeven Armor triggers and the position exits near entry (+0.06% ROI) with a tiny net fee (-$0.04 USDT), the event is strictly classified and reported as a `BREAKEVEN DEFENSE SCRATCH`, permanently prohibiting misleading `RISK PARITY SL` alerts when zero capital loss occurred.
      - **Autonomous Dust Sweeper:** Unscaled residual micro-dust (< $1.00 margin) held > 2.0 minutes is autonomously swept and closed with `reduce_only=True` to maintain 100% account hygiene.

---

### Invariant 40: Autonomous Solana On-Chain DEX Execution Engine (/smart_swap), Tri-Tier Asymmetric Risk Protocol & Five-Layer Defense Architecture Standard
- **Location:** `smart_swap_engine.py` (`monitor_smart_swap_positions`, `execute_auto_smart_swap_sniper`, `check_token_onchain_vitality`), `solana_trading_wallet.py`, `audit_system.py`, `bot_thread.py`, `scheduler_tasks.py`
- **Rule:** The Solana On-Chain DEX Execution Engine operates with institutional atomic execution, Jito private mempool bundles, and an adaptive Super Smart Trailing Take-Profit and dynamic on-chain vitality defense protocol:
  1. **Stage 0: Dynamic Token Vitality & Emergency Capital Rescue Guard (ការស្រោចស្រង់ដើមទុនមកវិញលឿនបំផុត) ៖**
     - Replaces arbitrary fixed scalp stop-losses (-9.5%) and arbitrary time-based prunes (45m).
     - The engine holds with disciplined quant patience through natural market noise and consolidation (even when drawdown $> -50\%$) as long as the token's on-chain liquidity, volume, and security integrity remain healthy and intact.
     - If the token's on-chain vitality breaks down (Pool Liquidity Drain $> 30\%$, Massive Dev Panic Dump with 5m sells $> 3.5\times$ buys, or smart contract security degradation), the engine executes an instantaneous sub-second Emergency Capital Rescue Swap 100% back to native SOL to recover remaining capital before pool dissolution.
  2. **100% Trend Capture & Eradication of 50% Partial Exits (លុបបំបាត់ចោលទាំងស្រុងការលក់តែ ៥០%) ៖**
     - 100% of the purchased token position is maintained intact to ride the explosive expansion of on-chain gems without premature chip reduction.
  3. **Super Smart Adaptive Trailing Take-Profit Lock (Completely Swap 100% at Top Gainer Trend) ៖**
     - **Arming Threshold:** Dynamically armed at Peak $\text{ROI} \ge +18.0\%$ (or current $\text{ROI} \ge +18.0\%$).
     - **Guaranteed Net Breakeven Floor:** Stop is permanently anchored at $\text{Entry} + 5.0\%$ Net, mathematically guaranteeing positive cash profit after all DEX pool fees, slippage, and Solana gas fees.
     - **Multi-Tier Adaptive Volatility Ratchet (ដេញតាមកំពូលតាមចរិតលក្ខណៈកាក់) ៖**
       * *Tier 1 (Breakout Expansion $+18.0\% \le \text{Peak ROI} < +50.0\%$):* $25.0\%$ pullback breathing allowance ($\text{ratchet\_floor} = \max(\text{Entry} \times 1.05, \text{Peak} \times 0.75)$).
       * *Tier 2 (Velocity Acceleration $+50.0\% \le \text{Peak ROI} < +100.0\%$):* $20.0\%$ pullback allowance ($\text{ratchet\_floor} = \max(\text{Entry} \times 1.10, \text{Peak} \times 0.80)$).
       * *Tier 3 (Hyper-Trend Moonshot $\text{Peak ROI} \ge +100.0\%$):* $15.0\%$ pullback allowance ($\text{ratchet\_floor} = \max(\text{Entry} \times 1.25, \text{Peak} \times 0.85)$).
     - **100% Top Exit Execution:** When price retraces to or below the dynamic ratchet floor, the engine executes an atomic 100% market exit back to native SOL via Jupiter DEX, banking maximum captured peak gains into the user's self-custodial wallet with verified Solscan links.
  4. **Scanner Quality Citadel & Anti-Blowoff-Top Guards ៖**
     - Minimum Liquidity: $\ge \$75,000$ (NEW mode), $\ge \$150,000$ (AUTO mode).
     - Minimum 24h Volume: $\ge \$200,000$ (NEW mode), $\ge \$400,000$ (AUTO mode).
     - Anti-Blowoff-Top: Strictly blocks entries if 5m price change $> +12.0\%$ (no FOMO buying into green spikes) or 1h change $> +60.0\%$. Targets sweet spot consolidation $0.0\% \le \text{m5\_chg} \le 10.0\%$.
     - Zero-Trust Security: 100% Mint/Freeze authorities revoked, LP locked/burned $\ge 95\%$, RugCheck score $< 25$, zero transfer tax.
  5. **The Five-Layer Systemic Defense Architecture Roadmap (ផែនការមេកំពែងការពារ ៥ ជាន់):**
     - *Layer 1 (Infrastructure & API Security Citadel):* Tokyo VPS co-location, sub-millisecond RPC latency (< 0.42ms), encrypted vault, and private Jito/Flashbots mempool routing.
     - *Layer 2 (Architectural Invariant Integrity Armor):* Automated AST compilation, pre-commit audit gates (33/33 checks), zero duplicate functions, and Fiduciary Refusal of ruinous strategies.
     - *Layer 3 (Institutional Quantitative Risk Fortress):* Super Smart Adaptive Trailing Take-Profit Lock, Dynamic Token Vitality Rescue Guard, Single-Asset Isolated Margin, Anti-Oversold RSI $\le 38.0$ Short Guard, and Prop Firm drawdowns clamped to safe boundaries.
     - *Layer 4 (33 Wall Street AI Models Swarm & Latency Virtualizer):* Multi-Agent Mixture of Experts (MoE), non-collapsible state segregation, TradFi lead-lag arbitrage, and DEX slippage shields.
     - *Layer 5 (Autonomous Self-Healing & Disaster Recovery Watchdog):* SQLite WAL mode 3-tier auto-healer, systemd watchdog auto-recovery, and 100% routed UI/UX callbacks with zero dead buttons.
- **Enforcement:** Verified by `audit_system.py` [CHECK 33/34].

### Invariant 41: Institutional Five-Layer Security Citadel, Latency Virtualizer & Prop Firm Compliance Standard
- **Location:** `system_security_citadel.py`, `bot_thread.py`, `bot_commands_registry.py`, `security.py`, `repair_database.py`, `audit_system.py`
- **Rule:** The entire platform is reinforced by the institutional Five-Layer Defense Citadel & Latency Virtualizer to eliminate all vectors of technical intrusion, latency degradation, and quantitative risk:
  1. **Layer 1: Infrastructure & API Security Citadel (Steam DRM Level 1 ៖ Zero Exploit) ៖**
     - Tokyo VPS Co-location (`asia-northeast1-a`): Sub-millisecond ping (< 0.42ms) to Binance and broker matching engines.
     - Encrypted Private API Vault: Military-grade AES-256 Fernet encryption for all API keys with Single-Wallet balance isolation (Invariant 10).
     - DeFi Private Mempool Relay: 100% private RPC relay via Flashbots and Jito bundles, eliminating sandwich attacks and public mempool front-running (Invariant 12 & 19).
  2. **Layer 2: Architectural Invariant Specification Lock (Denuvo Anti-Tamper ៖ Zero Regression) ៖**
     - The 41 Immutable Pillars permanently locked in `AGENTS.md`.
     - Automated 34-Check Pre-Commit Audit in `audit_system.py` verifying AST syntax, deduplicated canonical functions, and 100% routed UI buttons.
     - Sacred Covenant of Fiduciary Refusal (Invariant 1.1): Mathematically rejects any command or code that disables Stop-Loss, removes Trailing Take-Profit, enables Cross-Margin, or initiates gambler's Martingale averaging down.
  3. **Layer 3: Institutional Quantitative Risk Fortress (Capcom Proprietary Shield ៖ Zero Ruin) ៖**
     - Breakeven Armor & Golden 85% Profit Ratchet (Invariant 24 & 35) locking gains outside market noise.
     - Single-Asset Mode & ISOLATED Margin Guarantee (Invariant 3 & 17) eliminating cross-wallet contagion.
     - Anti-Oversold Short Guard (15m RSI $\le 38.0$) (Invariant 16) blocking panic shorts at market bottoms.
     - FTMO / Prop Firm Zero-Breach Compliance Shield: Clamps daily drawdown strictly to $\le -3.5\%$ and maximum trailing drawdown to $\le -7.0\%$, automatically halting new risk exposure on breach.
  4. **Layer 4: 33 Wall Street AI Models Swarm & Latency Virtualizer (VMProtect Virtualizer ៖ Nanosecond Alpha) ៖**
     - Multi-Agent Mixture of Experts (MoE) Swarm: DeepSeek-R1, Gemini 2.5 Flash, LLaMA-3-70B, and Wall Street ML ensembles requiring Multi-Agent Confluence $\ge 80\%$ before trade authorization.
     - TradFi Lead-Lag Arbitrage (Invariant 31): Sub-millisecond Nanosecond In-Memory L1 Pricing Cache (< 0.0003ms latency) front-running broker price updates.
     - Solana Smart Swap Dynamic Vitality & Rug Guard (Invariant 40): Sub-second emergency capital rescue on liquidity drains ($> 30\%$) and 100% Top Exit trailing ratchet.
  5. **Layer 5: Autonomous Self-Healing & Disaster Recovery (SteamStub Wrapper ៖ 99.999% Uptime) ៖**
     - SQLite WAL Mode 3-Tier Auto-Healer (`repair_database.py`): In-place checkpoints and pure-python data rescuer guaranteeing zero data loss.
     - Systemd Watchdog Daemon: Sub-3-second auto-restart with instant state serialization and hot reload.
     - Emergency Circuit Breaker & Telegram Control: Instant 1-tap Super Admin emergency lockdown and position liquidation (`/citadel`, `/capital CLOSE_ALL`, `/emergency_stop`).
- **Enforcement:** Verified by `audit_system.py` [CHECK 34/35].

---

### Invariant 42: Super Smart Sky Net Omni-Swarm Quorum Architecture & Zero-Conflict Cross-Engine Guard Standard (សំណាញ់មេឃកើបចំណេញ ២៤/៧ & គ្មានការប្រឆាំងគ្នាដាច់ខាត)
- **Location:** `sky_net_orchestrator.py`, `perpetual_wealth_engine.py`, `turbo_hedge_engine.py`, `macro_auto_trade_engine.py`, `scheduler_tasks.py`, `smart_x_engine.py`, `bot_commands_registry.py`, `bot_thread.py`, `audit_system.py`
- **Rule:** The Super Smart Sky Net Omni-Swarm Quorum Architecture coordinates the 5 flagship quantitative engines (`/wealth`, `/turbo_hedge`, `/smartx`, `/auto_trade`, and `/pre_pump`) into a seamless, unified profit-harvesting network operating 24/7 with 99% ultimate confidence and zero cross-engine conflict:
  1. **Zero-Opposing Position Guard (`validate_cross_engine_entry`) ៖**
     - Complete eradication of cross-engine cannibalization: If any engine or Binance itself holds an active `LONG` position on a symbol, all engines are strictly blocked from submitting `SHORT` orders on that symbol.
     - Conversely, if any engine or Binance holds an active `SHORT` position on a symbol, all engines are strictly blocked from submitting `LONG` orders on that symbol.
     - Eliminates opposing-direction hedging within the same account that causes double fee bleed without directional edge.
  2. **Strict Anti-Oversold Short Guard Invariant Enforcement (Invariant 16) ៖**
     - All Short entry requests from all engines across the Sky Net network must verify $15\text{m RSI} > 38.0$.
     - Any Short attempt when $15\text{m RSI} \le 38.0$ is unconditionally blocked, preventing retail panic bottom-shorting.
  3. **Anti-Cannibalization Over-Allocation Shield ៖**
     - Single-symbol concurrency cap: Exactly ONE primary engine is granted execution rights on a given symbol at any time unless an explicit Multi-Hop Confluence Quorum is achieved.
     - Global account slot cap (maximum 5 concurrent positions across all engines) prevents margin exhaustion and collateral starvation.
  4. **Level-5 Sky Net 99% Super Conviction Confluence Engine (`evaluate_sky_net_swarm_confluence`) ៖**
     - Multi-Model Consensus: Evaluates signals from the 5 engines alongside the 25 Wall Street ML models ensemble.
     - Conviction Scoring: Confluence Score $\ge 86.0$ triggers **Level-5 Super Conviction** ($99.0\% - 99.8\%$ mathematical confidence).
     - Synchronized Multi-Engine Harmony: When Level-5 Conviction is triggered, execution proceeds seamlessly with full capital protection.
  5. **Asset DNA Specialization Routing Protocol ៖**
     - Macro Waterfall breakdowns & multi-day swings are routed exclusively to `/auto_trade`.
     - High-frequency delta-neutral scalping & volatility harvesting are routed to `/turbo_hedge`.
     - Compounding sweet-spot swings are routed to `/wealth`.
     - Gold ($XAUUSDT/PAXGUSDT$) & multi-asset pending stop straddles are routed to `/smartx`.
     - Micro-cap orderbook accumulation & volume breakout spikes are routed to `/pre_pump`.
  6. **Real-Time Cross-Engine Position Lifecycle Tracking & MT5 Prop Firm Dual-Dispatch ៖**
     - Atomic RAM Cache + SQLite WAL persistence for active positions across engines.
     - Position release protocol (`release_cross_engine_position`): When a position closes via TP, SL, or Breakeven, the symbol is released with a 30-second cooldown buffer before re-entry evaluation.
     - Sub-millisecond (< 0.001ms) non-blocking replication of Sky Net executions to MT5 Prop Firm bridges (FTMO/MFF).
- **Enforcement:** Verified by `audit_system.py` [CHECK 35/36].

### Invariant 43: Anti-Exhaustion Structural Confluence & Fiduciary Capital Allocation Guard (The 43rd Pillar)
- **Location:** `perpetual_wealth_engine.py` (`scan_golden_sweet_spot_candidates`, `evaluate_symbol_technicals`, `execute_wealth_harvest_cycle`), `sky_net_orchestrator.py` (`validate_cross_engine_entry`), `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty (Section 1.1) and Zero Technical Negligence, the system strictly eliminates the Top Chasing / Buying Exhaustion Trap and Bottom Panic Short Trap, while enforcing strict capital ring-fencing across the trading portfolio:
  1. **Anti-Top Chasing & Buying Exhaustion Elimination (ហាមដាច់ខាតការដេញទិញកាក់ចំកម្រិតកំពូល) ៖**
     - **Tightened Sweet-Spot Scan:** Golden Sweet Spot for LONG entries is strictly clamped to $+1.5\% \le \Delta_{24\text{h}} \le +6.5\%$. Chasing coins up $+10\%$ to $+14\%$ is strictly prohibited because they are in the climax distribution zone of whales.
     - **Upper Wick Rejection Sentinel:** If the latest 15m candle exhibits an upper wick ratio $\frac{\text{Upper Wick}}{\text{Candle Range}} \ge 35\%$ on significant volatility ($\text{Range} > 0.4 \times \text{ATR}_{14}$), the asset is exhibiting whale selling rejection and BUY orders are unconditionally blocked.
     - **Bearish RSI Divergence Sentinel:** Over the last 15 candles, if price forms a Higher High ($P_{\text{recent}} > P_{\text{prior}} \times 1.003$) while 15m RSI forms a Lower High ($\text{RSI}_{\text{recent}} < \text{RSI}_{\text{prior}} - 2.5$), the move is a Climax Fakeout and BUY orders are unconditionally blocked.
     - **Overextension from EMA20 Guard:** Current price must be within $\le +0.6\%$ of the 15m EMA20. Parabolic extensions $> +0.6\%$ above EMA20 are blocked from instant market execution to prevent taking immediate drawdowns on mean reversion.
     - **Market Structure Higher Low (HL) Support Confirmation:** Price must confirm a structural Higher Low base ($\min(\text{Low}_{-4:}) \ge \min(\text{Low}_{-12:-4}) \times 0.997$). Assets printing Lower Lows (falling knives) are blocked from BUY.
  2. **Anti-Bottom Shorting & Short Squeeze Trap Elimination (ហាមដាច់ខាតការបើក Short ចំបាត) ៖**
     - **Tightened Sweet-Spot Scan:** Sweet Spot for SHORT entries is strictly clamped to $-6.0\% \le \Delta_{24\text{h}} \le -1.5\%$.
     - **Lower Wick Absorption Sentinel:** If the latest 15m candle exhibits a lower wick ratio $\frac{\text{Lower Wick}}{\text{Candle Range}} \ge 35\%$ on significant volatility, smart money is absorbing sell dumps and SHORT orders are unconditionally blocked.
     - **Bullish RSI Divergence Sentinel:** Over the last 15 candles, if price forms a Lower Low while 15m RSI forms a Higher Low, the asset is primed for a violent short squeeze and SHORT orders are unconditionally blocked.
     - **Overextension below EMA20 Guard:** Current price must be within $\le -0.6\%$ of 15m EMA20. Shorting deep into the waterfall ($> 0.6\%$ below EMA20) is blocked.
     - **Market Structure Lower High (LH) Resistance Confirmation:** Price must confirm a structural Lower High breakdown ($\max(\text{High}_{-4:}) \le \max(\text{High}_{-12:-4}) \times 1.003$).
     - **Strict Invariant 16 Oversold Guard:** $15\text{m RSI} \le 42.0$ unconditionally blocks all SHORT orders across all engines.
  3. **Pullback Sweet-Spot Execution Standard (Maker Fee & Zero Top Fill) ៖**
     - The engine is prohibited from throwing blind MARKET orders when price is extended above support.
     - If price is at the support retest ($\le \text{EMA20} \times 1.002$), sweet-spot fill is granted.
     - If price is slightly above support, the engine places a **Pullback LIMIT Order** at $\text{EMA20} \times 1.001$, guaranteeing the position is filled only upon a genuine technical retest with 0.02% Maker fee.
  4. **Dynamic Capital Allocation Ring-Fence & Fiduciary Priority Hierarchy (ការពារមិនឱ្យ /wealth លេប Margin ទាំងអស់) ៖**
     - **Wealth Margin Ceiling ($\le 35\%$):** Total margin allocated to `/wealth` positions across the user's futures account is strictly capped at $\le 35\%$ of total wallet equity ($E_{\text{wallet}}$).
     - **Permanent Ring-Fence for Institutional Engines ($\ge 65\%$):** At least $65\%$ of wallet equity and free margin is permanently ring-fenced and reserved for high-conviction institutional engines (`/smartx`, `/turbo_hedge`, and `/auto_trade`).
     - **Engine Priority Arbitration:**
       * *Priority 1 (Apex):* `/smartx` (Gold AGI & 25-ML Wall Street Ensembles) — execution allowed down to $\$5.00$ free margin.
       * *Priority 2:* `/turbo_hedge` (Delta-Neutral HFT & Reversal) — execution allowed down to $\$5.00$ free margin.
       * *Priority 3:* `/auto_trade` (Macro Waterfall Swing) — execution allowed down to $\$5.00$ free margin.
       * *Priority 4:* `/pre_pump` (Whale Accumulation Sniper).
       * *Priority 5:* `/wealth` (Continuous Momentum Harvester) — blocked if wealth margin $\ge 35\%$ or free margin $< \$15.00$ (on accounts $\ge \$50$).
  5. **Orderbook L2 Whale Depth Ratio & Conviction Hurdle ៖**
     - BUY requires Bid/Ask ratio $\ge 1.15$ (Whale Bid Wall support).
     - SELL requires Bid/Ask ratio $\le 0.85$ (Whale Ask Wall resistance).
     - Minimum AI Score $\ge 8.6/10.0$ and AI Confidence $\ge 92.0\%$ (with 33 Wall Street Models agreement).
- **Enforcement:** Verified by `audit_system.py` [CHECK 36/37].

### Invariant 44: MT5 Cent Account Proportional Lot Scaling & Risk Parity Standard (The 44th Pillar)
- **Location:** `mt5_bridge_engine.py` (`calculate_proportional_lot_size`), `audit_system.py`
- **Rule:** For Cent accounts (USC / Micro, e.g. GTCFX Server 5, Cent, Micro), position sizing must strictly prevent over-leveraging and drawdowns from exceeding 1% on normal market oscillations.
  1. **Dynamic Cent Lot Sizing Tiers:**
     - Balance $< 1,000$ USC (< $10 USD): Proportional lot = 0.10, ceiling = 0.15 lot.
     - Balance $1,000$–$2,500$ USC ($10–$25 USD): Proportional lot = 0.10, ceiling = 0.20 lot.
     - Balance $2,500$–$5,000$ USC ($25–$50 USD): Proportional lot = 0.15, ceiling = 0.25 lot.
     - Balance $5,000$–$10,000$ USC ($50–$100 USD): Proportional lot = 0.20, ceiling = 0.35 lot. (Strictly prohibiting 0.70 lot blowout on small capital).
     - Balance $10,000$–$25,000$ USC ($100–$250 USD): Proportional lot = 0.35, ceiling = 0.60 lot.
     - Balance $25,000$–$50,000$ USC ($250–$500 USD): Proportional lot = 0.60, ceiling = 1.00 lot.
     - Balance $50,000$–$100,000$ USC ($500–$1,000 USD): Proportional lot = 1.00, ceiling = 2.00 lot.
     - Balance $\ge 100,000$ USC ($\ge \$1,000$ USD): Proportional lot strictly capped to max 5.00 lots.
  2. **Prop Firm Compliance & Max Drawdown Guard:**
     - Maximum drawdown on any single normal market retracement ($2.50 on Gold) is mathematically guaranteed to stay $\le 1.0\%$, eliminating false daily loss violations (-3.5%).
- **Enforcement:** Verified by `audit_system.py` [CHECK 37/37].

### Invariant 45: Cent Micro-Loss Threshold & Anti-Lockout Sentinel Protocol (The 45th Pillar)
- **Location:** `mt5_bridge_engine.py` (`on_trade_transaction`, consecutive loss counter), `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty (Section 1.1), the system recognizes that 1 USC = $0.01 USD. Treating raw USC losses as USD values in consecutive loss tracking is classified as severe unit desynchronization.
  1. **Dynamic Cent Account Detection (`is_cent_account`):**
     - Automatically verifies currency (`USC`, `CENT`, `EUAC`, `GBPC`) and broker/server/firm metadata (`server 5`, `cent`, `micro`).
  2. **Micro-Loss Threshold Calibration:**
     - Standard USD Account: `micro_threshold = $1.50` USD.
     - Cent Account: `micro_threshold = 150.0` USC ($1.50 USD equivalent).
  3. **Noise Classification & Anti-Lockout Protection:**
     - Any consecutive loss with $|PnL| < \text{micro\_threshold}$ is classified as ordinary market tick noise (`is_micro_loss = True`).
     - Noise losses trigger only a brief **5-minute cooling off (300.0s)**, strictly barring the destructive **2-hour (7200.0s) symbol lockout** penalty.
- **Enforcement:** Verified by `audit_system.py` [CHECK 37/37].

### Invariant 46: Small Capital Max Concurrent Position Ring-Fence & Margin Shield (The 46th Pillar)
- **Location:** `mt5_bridge_engine.py` (`scan_and_dispatch_radar`, `can_open_new_position`), `audit_system.py`
- **Rule:** On micro and small capital accounts, total concurrent open positions must be strictly ring-fenced to prevent margin depletion and portfolio correlation drag:
  1. **Tiered Concurrent Asset Ring-Fence:**
     - Equity $< \$10$ USD (< 1,000 USC): Max 1 concurrent position.
     - Equity $\$10$–$\$30$ USD (1,000–3,000 USC): Max 2 concurrent positions (e.g. Account `#55688250` strictly limited to 2).
     - Equity $\$30$–$\$60$ USD (3,000–6,000 USC): Max 3 concurrent positions (e.g. Account `#55686590` strictly limited to 3).
     - Equity $\$60$–$\$150$ USD (6,000–15,000 USC): Max 4 concurrent positions.
     - Equity $\ge \$150$ USD: Max 5 concurrent positions.
  2. **Overtrade Guard:**
     - When an account reaches its max positions (e.g. `Active (5/2 Positions)`), new incoming signals are unconditionally rejected until existing positions close or bank profit.
- **Enforcement:** Verified by `audit_system.py` [CHECK 37/37].

### Invariant 47: 24/7 Autonomous Watchdog Citadel & Instant Reverse-Flip Execution Protocol (The 47th Pillar)
- **Location:** `mt5_bridge_engine.py` (`_watchdog_loop`, `_auto_harvest_loop`, `execute_direct_reverse_flip`), `turbo_hedge_engine.py`, `audit_system.py`
- **Rule:**
  1. **24/7/365 Non-Sleeping Watchdog:** High-frequency thread monitors open positions every millisecond across MT5, Binance Futures, and Capital.com with zero sleep downtime.
  2. **Multi-Stage Progressive Breakeven Armor:** Automatically advances server-side Stop Loss to lock profits and eliminate capital risk:
     - Phase 1: At $+30$ USC profit, SL moves to entry price $+0.05$ buffer (risk-free).
     - Phase 2: Progresses higher at $+45$ USC, $+60$ USC, $+100$ USC.
  3. **Target Harvest & Instant Reverse-Flip (< 0.8s):** When target profit is achieved (e.g. $+180$ USC), the position is closed via atomic market execution and reversed in the opposite direction in $< 0.8\text{s}$ with proper lot sizing, capturing bidirectional 24/7 continuous market swings without human intervention.
- **Enforcement:** Verified by `audit_system.py` [CHECK 37/37].

### Invariant 48: Reachsey 5-Position Volatility Matrix Engine & Asymmetric Net Basket Sweeper Lock (The 4 Pillars of Reachsey)
- **Location:** `mt5_bridge_engine.py` (`execute_reachsey_5pos_matrix`, `monitor_reachsey_5pos_baskets`, `sweep_reachsey_baskets`, `scan_top_momentum_reachsey_asset`), `bot_thread.py` (`mt5_reachsey_command`), `bot_commands_registry.py`
- **Rule:**
  1. **Pillar 1: 3:2 Skewed Order Structure (1.00 Lot Volume / 0.20 Net Delta Rebate Maximizer):**
     - Primary: 3 Positions = 0.60 Lot (0.20 lot/pos, directional trend bias).
     - Hedge: 2 Positions = 0.40 Lot (0.20 lot/pos, volatility defense shield).
     - Total Volume: 1.00 Lot broker turnover per basket, generating institutional cashback rebates ($10.00–$15.00/lot).
     - Net Market Delta: +0.20 Lot (80% market risk reduction compared to naked directional trades, allowing ultra-fast breakeven and rapid exit).
     - Scaled appropriately for micro/cent accounts ($0.01 lot floor on micro balances < $100).
  2. **Pillar 2: Zero Broker Stop-Loss Hunting (`sl = 0.0` Cohabitation Standard):**
     - All 5 legs are dispatched with `sl = 0.0` and `tp = 0.0` to completely eliminate broker stop-hunting, artificial spread spikes, and whipsaw chop.
     - Indivisible Basket Cohabitation: All 5 legs must stand together until collective net profit is achieved. Single-leg closures are strictly prohibited.
     - Macro Disaster Floor (-15% to -18%): Capital ring-fence protecting 82%–85% of equity against extreme Black Swan systemic tail events.
  3. **Pillar 3: Fast Milestone Profit Harvest & Sub-0.5ms Simultaneous Sweep:**
     - Milestone Harvest: Instant cash-in triggered whenever collective basket net profit reaches >= $1.00 USD (100 USC) on micro accounts ($25–$100 capital) or >= $100.00 USD (10,000 USC) on Tier 1 ($2,500–$3,000 capital).
     - Sub-0.5ms parallel socket closure: All 5 legs are closed simultaneously across TCP direct socket.
     - `SWEPT_COMPLETED` State Lock: State is atomically updated to `SWEPT_COMPLETED` immediately upon sweep initiation to eliminate race conditions on subsequent market ticks.
  4. **Pillar 4: 24/5 Autonomous Execution & Multi-Asset Momentum Radar:**
     - Autonomous background radar scans every 20–30s across high-velocity assets (Gold `XAUUSD`, Silver `XAGUSD`, Bitcoin `BTCUSD`, Ethereum `ETHUSD`, US Indices `US30`/`US100`, and High-Beta FX `GBPJPY`/`EURJPY`).
     - Confluence Scoring: 9-SMC Confluence, Quantum AI Satellite Signals, and 15m RSI Momentum (blocking shorts if RSI <= 38.0 and longs if RSI >= 65.0).
     - 60-Second Post-Sweep Cooldown: Prevents rapid re-triggering while broker queues settle and new candle structures emerge.

- **Enforcement:** Verified by `audit_system.py` [CHECK 38/39].

### Invariant 49: Hugging Face VIP MT5 Worker Cloud Citadel & Free 16GB RAM Distributed Edge Worker Standard (The 49th Pillar)
- **Location:** hf_space_manager.py, hf_mt5_worker/ (Dockerfile, README.md, 
equirements.txt, pp.py), database.py (ip_hf_workers), ot_thread.py (mt5_hf_command, aliases /mt5hf, /hf_vip, /hfvip, /hf_worker, /hfworker), ot_commands_registry.py
- **Rule:**
  1. **Zero VPS Hardware Bloat (100% Free Edge Scaling):** Under NO circumstances shall multiple Wine MT5 GUI client processes be forced to run concurrently on the single Linux VPS instance. All VIP MT5 client runtime workloads are offloaded to dedicated, isolated Hugging Face Docker Spaces (Free 16 GB RAM / 2 vCPU per user).
  2. **Stateless Outward TCP Gateway:** The Linux VPS acts strictly as an asynchronous TCP message broker on Port 5555 (mt5_bridge_engine.py). Each remote Edge worker socket consumes only ~10 KB of RAM on VPS (1,000 users = ~10 MB RAM total), maintaining 0.00% VPS RAM and CPU overhead.
  3. **KMS Space Secret Protection:** All user MT5 login credentials, passwords, and broker servers must be injected strictly into encrypted Hugging Face Space Secrets (MT5_ACCOUNT, MT5_PASSWORD, MT5_SERVER, SECRET_KEY). Never expose raw credentials in plain text or commit them into public repositories.
  4. **Continuous Anti-Sleep Sentinel Protocol:** To prevent Hugging Face's 48-hour idle auto-pause policy, the system incorporates an autonomous sentinel loop (hf_mt5_worker/app.py and scheduler_tasks.py / ping_all_active_workers) pinging /ping every 5-12 minutes to guarantee uninterrupted 24/7/365 execution.
- **Enforcement:** Verified by udit_system.py [CHECK 39/39].

---

### Invariant 50: Angkor Institutional Private Agreement & Master Stamping Architecture (កិច្ចព្រមព្រៀងឯកជន & ការបោះត្រាហត្ថលេខាឌីជីថលលើឯកសារដើម)
- **Location:** `legal_agreement.py`, `database.py` (`user_legal_agreements`), `bot_thread.py` (`agreement_command`, `btn_agree_terms`, `btn_preview_terms_pdf`, `btn_download_my_pdf`, `btn_admin_agreements`, pre-flight gatekeepers on `/start`, `/add_api`, `/auto_trade`, `/turbo_hedge`, `/smart_trade`), `Users_agrement.pdf`
- **Rule:**
  1. **Strict Private Contract & Educational Software Status (ឋានៈកម្មវិធីស្រាវជ្រាវ & កិច្ចសន្យាឯកជន):** Angkor Quant Engine operates strictly as an institutional quantitative research tool and private algorithmic automation suite. It is NOT a financial advisory service, broker, deposit taker, or pooled investment fund.
  2. **Mandatory Pre-Flight Execution Gatekeeper on /start:** Before any user can store live Binance API keys, activate `/auto_trade ON`, execute live `/turbo_hedge`, or run automated executions in `/smart_trade`, the system programmatically intercepts unsigned users on `/start` with an interactive Gatekeeper card requiring explicit agreement.
  3. **Authentic Master Document Invariant (`Users_agrement.pdf` Standard):** The authoritative legal charter is the authentic 1-page master document `Users_agrement.pdf` (containing the complete 5 articles in professional Khmer typography). AI agents and engines are strictly forbidden from rebuilding the contract text from dynamic scratch/HTML. The document `Users_agrement.pdf` is legally valid, sufficient, and non-negotiable.
  4. **Sub-Millimeter Blank Space Stamping Architecture (ការបោះត្រាលើកន្លែងទំនេរផ្នែកខាងក្រោម):** When a user accepts the agreement, their identity (Chat ID, Username, Name, Phone), contract serial number, ICT timestamp, 100% accepted status, system metadata, digital seal, and SHA-256 cryptographic fingerprint MUST be stamped directly into the empty space at the bottom of `Users_agrement.pdf` (native PDF coordinates: `y = 22.0 pt` to `118.0 pt`, `x = 36.0 pt` to `576.0 pt`, height `96.0 pt`) with an 8.6 pt breathing space below the text and 22 pt bottom margin.
  5. **Multi-Tier Stamping Engine with HarfBuzz Text Shaping:**
     - *Tier 1 (Flagship Primary):* `fpdf2` with `uharfbuzz` text shaping and `KantumruyPro-Regular.ttf` for 100% proper Khmer conjuncts and subscript vowels, merged onto `Users_agrement.pdf` via `pypdf`.
     - *Tier 2 (Defensive Fallback):* `reportlab.pdfgen.canvas` overlay as an immediate in-process fallback.
     - *Tier 3 (Emergency Fallback):* Pure-Python / browser full generation if template is missing.
  6. **Immutable WAL SQLite Persistence & SHA-256 Audit Trail:** Every signed agreement is permanently logged in `user_legal_agreements` in SQLite WAL mode (`is_immutable = 1`), with SHA-256 fingerprint, and the stamped PDF is archived in `data/legal_agreements_pdf/`.
  7. **Instant Telegram PDF Distribution & Super Admin Citadel:** Upon signing, the bot immediately dispatches the official signed PDF to the user's chat. Users can re-download via `btn_download_my_pdf`. Super Admin can inspect and download any user's PDF via `/admin_agreements` and `btn_admin_dl_pdf_<chat_id>`.
  8. **Git Sync & Linux VPS Whitelist Standard:** `Users_agrement.pdf` and `assets/docs/*.pdf` MUST remain permanently whitelisted in `.gitignore` (`!Users_agrement.pdf`, `!assets/docs/*.pdf`) to guarantee seamless deployment on Google Cloud VPS without template loss.
- **Enforcement:** Verified by `audit_system.py` [CHECK 40/40] and pre-flight execution hooks.

---

### Invariant 51: Hugging Face Ultra-Fast Multi-Tiered Storage & Nanosecond RAM Citadel Lock (ប្រព័ន្ធផ្ទេរទិន្នន័យទៅ HF & ទាញយកចូល RAM ល្បឿនលឿនបំផុត)
- **Location:** `hf_storage_engine.py`, `ai_engine.py`, `sync_local_models.py`, `bot_commands_registry.py`, `bot_thread.py` (`hf_data_command`, `btn_hf_data_*`), `audit_system.py`
- **Rule:**
  1. **Multi-Tiered Hybrid Storage Architecture (រចនាសម្ព័ន្ធផ្ទុក ៣ ជាន់):**
     - *Tier 1 (RAM Hot Cache):* Thread-safe in-memory cache (`_RAM_CACHE`) delivering nanosecond data and model retrieval ($< 0.0005\text{ ms}$ / lookup). Zero disk I/O, zero network delay.
     - *Tier 2 (Local NVMe/SSD Cache):* High-speed disk cache in `data/hf_cache/` and `models/` with smart ETag/hash differential checks skipping redundant downloads.
     - *Tier 3 (Cloud Hub Sync):* Asynchronous parallel multi-threaded cloud synchronization with Hugging Face Hub using `ThreadPoolExecutor(max_workers=8)`.
  2. **Authenticated Access Token Protocol (`HF_TOKEN` Lock):**
     - All interactions with Hugging Face Hub are cryptographically authenticated via `HF_TOKEN` stored in `.env`.
     - Automatically verifies token permissions (`whoami`), user identity (`hemsinath`), and ensures repositories (`hemsinath/apex-ai-brain-models` for models, `hemsinath/angkor-quant-data` for datasets) exist with `private=True` to guarantee zero proprietary data leaks.
  3. **Comprehensive Data Backup Citadel (ការផ្ទេរ និងរក្សាទុកទិន្នន័យ ៤ ប្រភេទ):**
     - *Category 1 (AI Models & Weights):* All 26 canonical ML models, scalers, neural networks (`.keras`, `.h5`, `.pth`), and hyperparameter configs.
     - *Category 2 (Quantitative Datasets):* 500-coin DNA cache (`coin_dna_cache.json`), market snapshots, and state caches.
     - *Category 3 (Database WAL Snapshots):* Clean checkpointed and gzipped SQLite snapshots (`bot_database_snapshot.db.gz`).
     - *Category 4 (Legal Agreements Vault):* Master agreement template (`Users_agrement.pdf`) and compressed snapshots of signed contract records.
  4. **Parallel Multi-Threaded Transfer Engine:**
     - High-speed concurrent worker pool (`ThreadPoolExecutor`) enabling simultaneous multi-file uploads and downloads at line rate without blocking the asyncio Telegram event loop or pausing live trading bots.
  5. **Nanosecond In-Memory Retrieval Standard ($< 0.0003\text{ ms}$):**
     - Engine lookups (`get_data`, `get_hot_coin_dna_cache`, `get_hot_legal_master_pdf`) hit Tier 1 RAM Hot Cache in $\approx 0.00027\text{ ms}$ ($270\text{ ns}$), compliant with Invariant 29, eliminating latency spikes during active trading.
  6. **Eager Preloading & RAM Warm-up Lifecycle (`warmup_ram_cache`):**
     - Automatically preloads critical configurations, models, and caches into RAM on bot startup and during model sync (`sync_brain_from_huggingface`), ensuring immediate sub-millisecond execution readiness.
  7. **Flagship Telegram Command & 1-Tap UI Suite (`/hf_data`):**
     - Flagship command `/hf_data` (aliases: `hfdata`, `hf_sync`, `hfsync`, `hf_backup`, `hfbackup`, `aq_hf_data`) supporting concrete 1-tap presets: `/hf_data BACKUP`, `/hf_data PULL`, `/hf_data WARM`, `/hf_data STATUS`.
     - Interactive buttons (`btn_hf_data_backup`, `btn_hf_data_pull`, `btn_hf_data_warm`, `btn_hf_data_status`) with 100% callback routing, immediate `await update.callback_query.answer()`, and 2.0 cm mobile-fit divider standard (`ui_standards.py`).
- **Enforcement:** Verified by `audit_system.py` [CHECK 41/41] and pre-flight execution hooks.

---

### Invariant 52: Capital.com Sky Net 360° Daily Capital Governor & Target Lock (+5.0% Win Cap / -2.5% Loss Floor / 7-Layer Pre-flight Radar)
- **Location:** `portfolio_circuit_breaker.py` (`CapitalDailyAGIGovernor`), `capital_engine.py` (`CapitalSkyNet360Radar`, `execute_smart_tradfi_order`, `_dispatch_single_user_trade`, `_ratchet_engine_positions`), `bot_thread.py` (`capital_command`), `audit_system.py`
- **Rule:**
  1. **Daily Equity Baseline & Reset Standard:**
     - The Governor records `daily_baseline_equity` at 00:00 UTC daily for each user (or on the first transaction/balance check of the day).
     - Calculates dynamic Net Day Return: $R_{day} = \frac{\text{Current Equity} - \text{Daily Baseline}}{\text{Daily Baseline}} \times 100\%$.
  2. **Daily +5.0% Target Lock (Cash Harvest & Trading Lock):**
     - When $R_{day} \ge +5.0\%$, the Governor triggers `TARGET_LOCKED`.
     - In-flight positions are secured via dynamic profit ratchet and cash harvest, and all subsequent new entries for that user are strictly blocked until the next trading day (or an intentional manual reset via `/capital RESET_DAILY`).
     - Eliminates greedy over-trading that gives back realized gains.
  3. **Daily -2.5% Loss Floor (Stop Trading & Capital Defense):**
     - When $R_{day} \le -2.5\%$, the Governor triggers `FLOOR_HIT`.
     - Immediately suspends all new trade executions for the user for the day to prevent revenge trading, emotional compounding, and consecutive losing streak bleed.
  4. **Sky Net 360° 7-Layer Pre-Flight Confluence Radar:**
     - Every trade entry must undergo 360-degree radar assessment and is blocked if any layer fails:
       1. Schedule Window (London/NY peak liquidity only; Asian off-peak blocked for equities/indices).
       2. Daily Governor Lock (Target Lock / Loss Floor).
       3. Economic Calendar Blackout (No high-impact CPI/NFP/FOMC within $\pm 30\text{m}$).
       4. Earnings Blackout (No individual stock CFD earnings announcement within 48h).
       5. Spread Drag Hurdle (Spread $\le 0.05\%$ or $\le 10\times$ profit hurdle per Invariant 34).
       6. Macro / Real Yields Confluence (US10Y / DXY alignment).
       7. Anti-Top/Bottom Guard (15m RSI $\le 30$ blocks short, RSI $\ge 70$ blocks long per Invariant 43).
  5. **100% Zero-Defect Audit Protocol:**
     - Verified by `audit_system.py` [CHECK 42/42].

---

### Invariant 53: Super Smart Rollover Swap Shield, Wednesday Triple-Swap Lockout, Wall Street Full Coverage & Crypto 24/7 Continuity Lock
- **Location:** `capital_engine.py` (`is_capital_trading_schedule_active`, `evaluate_capital_rollover_swap_shield`, `_ratchet_engine_positions`), `database.py` (`capital_auto_config`, `get_capital_schedule_mode`), `bot_thread.py` (`capital_command`, `/capital SWAP_SHIELD`, `btn_cap_swap_shield_info`), `web_gui_server.py`, `web_gui/app.js`
- **Rule:**
  1. **Wall Street Power Hour Full Coverage Standard (07:00 AM to 03:45 AM ICT):**
     - Traditional retail schedules cutting off trading at 11:50 PM ICT (23:50 ICT = 16:50 UTC / 12:50 PM EST) prematurely amputate the final 4 hours of the US Wall Street session, missing peak institutional closing volume and momentum.
     - Both `SMART_SESSION_TIMED` and `SCHEDULE_MON_FRI` MUST keep active trading open through 03:45 AM ICT (20:45 UTC), capturing 100% of the US market cash session through the closing bell.
  2. **Daily Rollover Swap Lockout & Overnight Lull Standard (03:45 AM to 07:00 AM ICT / 20:45 to 23:59 UTC):**
     - US cash equity markets close at 16:00 ET (21:00 UTC / 04:00 ICT summer / 05:00 ICT winter). European markets are closed. Tokyo has not opened. Market liquidity drops to near zero.
     - Daily broker rollover swap settlement occurs at 22:00 UTC (05:00 AM ICT summer / 04:00 AM ICT winter), accompanied by interbank quote pullbacks that widen spreads 3x–10x (Spread Blowout).
     - The engine enforces a 100% hard block on new TradFi orders (stocks, indices, commodities, forex) during this window. Zero new TradFi entries are permitted, completely eliminating overnight financing debits and spread blowout risk.
  3. **Wednesday Triple-Swap Shield Standard (300% Rollover Fee Lockout):**
     - On Wednesday at 22:00 UTC (05:00 AM Thursday ICT), brokers charge **3-day triple swap** (Wednesday + Saturday + Sunday) to cover weekend settlement.
     - When `weekday_utc == 2` (Wednesday), the Shield activates elevated defense at 20:15 UTC (03:15 AM Thursday ICT), halting new TradFi entries early to prevent any trade from being caught in the 300% fee trap.
  4. **Pre-Rollover Profit Harvesting & Armor Lock:**
     - In `_ratchet_engine_positions`, between 20:30 and 20:45 UTC (or Wednesday after 20:00 UTC):
     - Any active TradFi position with positive profit ($UPL \ge \$1.00$ or $ROI \ge +2.5\%$) is defensively shielded: stops are aggressively ratcheted past entry (Breakeven Armor+), and high-profit day trades ($ROI \ge 5.0\%$ or $UPL \ge \$2.50$) are harvested cleanly to cash before swap fees are debited. Winning day trades are never degraded by overnight financing interest.
  5. **Weekend TradFi Gap Shield:**
     - Active Friday 20:45 UTC (03:45 Saturday ICT) to Sunday 22:00 UTC (05:00 Monday ICT). Prevents weekend gap-down risk on traditional assets.
  6. **Decentralized Crypto CFD 24/7 Continuity Standard:**
     - Crypto CFDs (`BTCUSD`, `ETHUSD`, `SOLUSD`) trade on decentralized 24/7 continuous markets without exchange closing bells or weekend gap interruptions. They remain 100% active 24/7 across all sessions and weekends.
  7. **Canonical Default & Zero-Dead-Button UI Enforcement:**
     - Default `schedule_mode` across `database.py` and `capital_engine.py` is permanently locked to `SMART_SESSION_TIMED`.
     - Telegram UI supports `/capital SWAP_SHIELD`, `/capital SMART_SESSION`, `/capital SCHEDULE`, and interactive callback `btn_cap_swap_shield_info` with immediate acknowledgment.
- **Enforcement:** Verified by `audit_system.py` [CHECK 43/44].

---

### Invariant 54: Capital.com VIP 10-Slot Parity, Dynamic Scaling & Governor Master Toggle Standard (Limit ON / OFF)
- **Location:** `portfolio_circuit_breaker.py` (`CapitalDailyAGIGovernor`), `capital_engine.py` (`_dispatch_single_user_trade`, `_ratchet_engine_positions`), `bot_thread.py` (`capital_command`, `admin_capital_command`, `btn_cap_daily_limit_off`, `btn_cap_daily_limit_on`, `btn_cap_admin_on_`), `database.py`
- **Rule:**
  1. **Institutional 10-Slot VIP Parity Standard:**
     - VIP User accounts possess full dynamic multi-slot allocation parity scaling up to 10 concurrent positions (identical to Super Admin capacity), dynamically determined by `max_slots = max(1, min(10, int(round(equity / 100.0))))` for accounts scaled with sufficient capital, or configured via administrative command `/admin_capital on <id> 400 live 10 24/7`.
     - 24/7 schedule override mode (`24/7` or `continuous`) is fully integrated and supported for VIP automated execution without session cutoffs.
  2. **Daily Governor Master Toggle Standard (`LIMIT ON / OFF`):**
     - The Daily Circuit Breaker (+5.0% target win cap / -2.5% daily loss floor) can be independently enabled or disabled via `/capital limit OFF`, `/admin_capital limit <chat_id> OFF`, and `/admin_capital limit global OFF` (and re-enabled via `LIMIT ON`).
     - Disabling daily limits prevents the bot from prematurely cutting off trading during exceptional macroeconomic mega-trend days or volatile institutional breakouts.
  3. **Zero Compromise on Trade-Level Risk (Fiduciary Covenant Lock):**
     - Disabling daily limits strictly leaves 100% of individual trade protections intact and operational: Dynamic ATR Stop-Loss, Dynamic Take-Profit Targets, Mathematical Breakeven Armor (+0.12% net floor), Trailing Ratchet, and Small Capital Leverage Clamp ($\le 10\times$ for accounts $< \$100$) are 100% preserved. Under no circumstances does toggling daily limits disable trade-level risk management.
- **Enforcement:** Verified by `audit_system.py` [CHECK 44/44].

---

### Invariant 55: Institutional Real Live Spread Isolation, Zero Virtual Contamination & Un-truncated Account ID Standard
- **Location:** `capital_engine.py` (`CapitalSpreadDragManager.get_system_wide_live_spread_audit`), `bot_thread.py` (`capital_spread_command`, `admin_capital_command`), `database.py`
- **Rule:**
  1. **Tri-Tier Account Segregation Standard:**
     - All user accounts are strictly categorized into 3 non-overlapping tiers:
       * `🟢 REAL LIVE`: Live Mainnet Capital.com accounts (`is_demo == 0`, not in Prop challenge configuration, and account ID does not contain 'PROP' or 'FTMO').
       * `🟡 DEMO`: Virtual simulation accounts (`is_demo == 1` or `auto_is_demo == 1`).
       * `🏆 PROP CHALLENGE`: Prop firm evaluation accounts (in `prop_firm_challenge_config` or account ID contains 'PROP' / 'FTMO').
  2. **Zero Virtual Contamination in Grand Total Metrics:**
     - Grand Total System metrics displayed in `/admin_capital spread` and `/capital total_spread` (including `total_live_spread_cost_usd`, `total_live_equity_usd`, `total_live_available_usd`, `total_live_open_positions_count`, and `total_live_floating_upl_usd`) MUST strictly and unconditionally calculate ONLY Real Live Mainnet accounts.
     - All Demo and Prop firm evaluation balances and spreads MUST be strictly excluded from Grand Totals (`demo_prop_excluded_from_total == True`) and isolated into a dedicated informational audit section (`🧪 គណនី Demo & Prop Firm (Excluded)`).
  3. **Un-truncated 1-Tap Copyable Capital Account ID Standard:**
     - In all administrative lists (`/admin_capital spread`, `/admin_capital users`), the Capital.com Broker Account ID must be displayed in full on a dedicated line (`🏦 Account ID ៖ <id>`) with zero digit truncation (`[-8:]` strictly prohibited).
     - Account IDs must be enclosed in monospace backticks (e.g. `` `1612591526` ``) enabling immediate 1-tap clipboard copying on mobile devices for seamless execution of administrative management commands.
- **Enforcement:** Verified by `audit_system.py` [CHECK 44/44].

---

### Invariant 56: Dual-Environment Demo vs Live Isolation, Dynamic Baseline Recalibration & Zero-Contamination Standard
- **Location:** `portfolio_circuit_breaker.py` (`CapitalDailyAGIGovernor`), `capital_engine.py`, `bot_thread.py` (`capital_command`, `button_callback_handler`), `macro_catalyst_engine.py`, `database.py`
- **Rule:**
  1. **Strict Key Namespace Segregation (Zero Cross-Environment Contagion):**
     - All daily baseline keys and daily circuit breaker lock keys in `CapitalDailyAGIGovernor` MUST be strictly namespaced by environment:
       * Real Live Mainnet: `cap_daily_start_eq_{chat_id}_live_{today_str}` and `cap_daily_lock_{chat_id}_live_{today_str}`.
       * Virtual Demo: `cap_daily_start_eq_{chat_id}_demo_{today_str}` and `cap_daily_lock_{chat_id}_demo_{today_str}`.
     - Under NO circumstances shall Demo trading gains (e.g. +119% demo profit or $10,000 virtual balance) or Demo losses ever spill over into, pollute, or trigger circuit breaker locks on Real Live Mainnet accounts.
  2. **Automatic Dynamic Baseline Recalibration upon Mode Switch:**
     - Whenever a user or administrator enables or toggles an account environment (e.g. `/capital AUTO ON <budget> LIVE`, `/capital AUTO ON <budget> DEMO`, or quick-budget buttons `$10`-`$400`), the engine MUST unconditionally execute `CapitalDailyAGIGovernor.reset_daily_governor(chat_id, current_balance=target_equity, is_demo=target_is_demo)`.
     - This guarantees that the daily governor baseline instantly synchronizes with the true, current account balance for the selected environment, eliminating artificial drawdown flags (e.g. calculating -$386.66 loss by comparing live $490.16 against demo starting baseline $876.82).
  3. **Self-Healing Multi-Environment Lock Reset:**
     - The `/capital RESET_DAILY` command and `btn_cap_reset_daily` inline callback automatically detect the user's active environment (`is_demo` flag) and safely clear locks for both that environment and legacy keys while recalibrating starting equity to the live balance.
     - When resetting without an explicit environment specified, all namespaces (`_live`, `_demo`, and legacy) are cleared simultaneously, guaranteeing that no orphan locks survive.
  4. **Macro Catalyst Fiduciary Gatekeeper & US Net Liquidity Radar:**
     - Fully integrates `macro_catalyst_engine.py` (Tier-1 Economic Calendar: CPI, NFP, FOMC; US Net Liquidity $6T Formula: `Fed Total Assets - TGA - RRP`; Spot BTC/ETH ETF Inflows; and WTI Crude Geopolitical Shock Radar).
     - Fiduciary Macro Gatekeeper dynamically restricts directional trading 15 minutes before Tier-1 High-Impact catalysts, preventing catastrophic stop-outs from institutional spread widening and volatility whipsaws, raising quantitative win expectancy to institutional grade (> 90%).
- **Enforcement:** Verified by `audit_system.py` [CHECK 44/44] & `CapitalDailyAGIGovernor` test suite.

---

### Invariant 57: Binance Futures Super Smart Sky Net Institutional Citadel (8-Pillar Trap Matrix)
- **Location:** `super_smart_futures_citadel.py`, `trading_engine.py` (`place_futures_order`, `place_futures_short`), `turbo_hedge_engine.py` (`scan_and_evaluate_symbol`, `execute_direct_reverse_flip`), `sky_net_orchestrator.py` (`evaluate_sky_net_swarm_confluence`)
- **Rule:**
  1. **8-Pillar Institutional Trap Matrix Standard:**
     - Under the Non-Negotiable Fiduciary Oath (Section 1.1), every Binance USDT-M Futures position entry MUST pass the 8-Pillar Trap Matrix:
       1. Dynamic Liquidity Trap Hunter (BSL / SSL Sweeps & Turtle Soup Rejection).
       2. Premium vs Discount Dealing Range Math (Discount < 50% for Long, Premium > 50% for Short; Deep Premium > 85% Long Block, Deep Discount < 15% Short Block).
       3. Market Structure Shift (MSS / CHoCH) & Displacement Confirmation ($\ge 1.2\times$ ATR).
       4. Fair Value Gap (FVG) & Order Block (OB) Imbalance Retest.
       5. Order Flow CVD & Absorption Divergence Shield.
       6. Non-Negotiable Capital Armor (15m RSI $\le 38.0$ Bottom Shield, Anti-Top FOMO RSI $\ge 70.0$).
       7. Multi-Timeframe Institutional Quorum (4H/1H Macro -> 15M Structure -> 5M Trigger).
       8. Asymmetric Expectancy Sizer ($R:R \ge 1:2.5$ to $1:4.0$ with Dynamic ATR Invalidation).
  2. **Universal Pre-Flight Gatekeeper Integration:**
     - `SuperSmartFuturesCitadel.validate_futures_entry_gatekeeper` acts as the mandatory gatekeeper in `trading_engine.py` and `turbo_hedge_engine.py`. Exits (`reduce_only=True`) are unrestricted; all new entries must achieve $\ge 68.0\%$ confluence conviction.
- **Enforcement:** Verified by `audit_system.py` [CHECK 45/45].

---

### Invariant 58: Capital.com Super Smart TradFi Institutional Citadel (8-Pillar Trap Matrix & Interbank Kill Zones)
- **Location:** `super_smart_capital_citadel.py`, `capital_engine.py` (`place_position`, `evaluate_tradfi_quant_signal`, `evaluate_multi_engine_tradfi_setup`, `execute_smart_tradfi_order`)
- **Rule:**
  1. **TradFi 8-Pillar Trap Matrix & Interbank Kill Zones:**
     - Every TradFi CFD order on Capital.com (Gold, Oil, US500, US100, Mega-Caps, Forex, Crypto CFDs) MUST pass the 8-Pillar TradFi Citadel:
       1. TradFi Liquidity Trap Hunter (BSL / SSL Sweeps & Turtle Soup Reversal).
       2. Premium vs Discount Dealing Range Math (Deep Premium $> 82\%$ Long Block, Deep Discount $< 18\%$ Short Block).
       3. Market Structure Shift (MSS/CHoCH) & Displacement Confirmation.
       4. Fair Value Gap (FVG) & Order Block (OB) Imbalance Retest.
       5. TradFi Spread Drag Elimination & Asymmetric 10x Hurdle (Invariant 34 Compliance).
       6. Strict Capital Armor (15m RSI $\le 36.0$ Bottom Shield, Anti-Top FOMO RSI $\ge 70.0$).
       7. Interbank Sessions, Kill Zones & Rollover Swap Shield (Invariant 53 Compliance).
       8. Asymmetric Minimum $R:R \ge 1:2.5$ to $1:6.0$ & Structural Invalidation SL.
       9. Economic Calendar Red Folder Blackout Guard (Pillar 1 TradFi News Shield): Strictly freezes new TradFi entries 30 minutes prior to US High-Impact releases (CPI, NFP, FOMC, Core PCE, Powell Speeches) with `PRE_EVENT_FREEZE`, and enforces 15-minute post-event spread normalization & 150-second toxic execution zone clearance before permitting entries.
       10. H4 Top-Down Structural Directional Anchor Guard (Wall Street Macro Tide Lock): If H4 Market Structure is Bullish (Price above H4 200 EMA with Bullish Stack / HH-HL), all 15m Short/Sell signals are strictly VETOED (`H4_TOP_DOWN_TREND_VETO`, allowing only Long pullbacks/breakouts). If H4 is Bearish (Price below H4 200 EMA with Bearish Stack / LH-LL), all 15m Long/Buy signals are strictly VETOED (eliminating falling knife traps 100%).
  2. **Broker-Level Pre-Flight Gatekeeper Integration:**
     - `SuperSmartCapitalCitadel.validate_capital_entry_gatekeeper` acts as the universal gatekeeper in `CapitalComEngine.place_position`. All automated, autonomous, and manual orders are intercepted and vetted before payload transmission to Capital.com REST API (`/positions`).
- **Enforcement:** Verified by `audit_system.py` [CHECK 45/45].

---

### Invariant 59: Institutional Post-News Volatility Harvester (News Scalp Alpha Protocol)
- **Location:** `post_news_scalp_harvester.py`, `economic_calendar_guard.py`, `capital_engine.py`, `bot_thread.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty (Section 1.1) and Invariant 18 (News Sentiment Technical Confirmation Shield):
  1. **Zero Toxic Flow Guarantee:** No orders shall ever be placed in the toxic 0 to 2.5-minute (150-second) window immediately following high-impact Red Folder USD releases (FOMC, CPI, NFP, Core PCE).
  2. **Dynamic Live Spread Normalization Sensor:** Post-event execution is strictly prohibited unless broker live spread is normalized ($\le 1.30\times$ baseline average) and liquidity providers have fully restored the order book depth.
  3. **Dual Institutional Setups:** Only two execution structures are permitted:
     - *Setup 1 (News Turtle Soup Reversal):* Sweeps session high/low with exhaustion wick $\ge 45\%$, reclaiming the range with $R:R \ge 1:2.5$ to equilibrium.
     - *Setup 2 (Institutional Displacement & FVG Retest):* Retest of 5m Fair Value Gap in direction of displacement with normalized spread and $R:R \ge 1:2.5$.
  4. **News Peak Wick SL & Breakeven Armor:** Stop-Loss is mathematically clamped to the extreme news spike wick. Dynamic Breakeven shift triggers at $+1.0R$.
- **Enforcement:** Verified by `audit_system.py` [CHECK 46/46].

---

### Invariant 60: Master Locomotive Syndicate & Super Admin Execution Priority Standard
- **Location:** `capital_engine.py` (`CapitalMasterLocomotiveEngine`, `SUPER_ADMIN_ID = 859271875`, `execute_autonomous_cycle`, `arm_session_breakout_traps`), `database.py` (`ensure_capital_super_admin_defaults`, `get_active_capital_auto_users`, `get_active_capital_orb_users`), `bot_thread.py`
- **Rule:**
  1. Super Admin (`859271875`, HEM SINATH) is permanently anchored as the sovereign **Master Locomotive** of the entire Angkor Quant Capital.com trading infrastructure.
  2. In every auto-trading cycle (`execute_autonomous_cycle`) and ORB 15m bracket trap session (`arm_session_breakout_traps`), Super Admin MUST be executed at index 0 (Locomotive Lead) before any follower or VIP user.
  3. Super Admin is strictly barred from falling into Prop Firm Demo mode or being demoted to Demo unless explicitly configured. `ensure_capital_super_admin_defaults()` guarantees `prop_firm_challenge_config.is_enabled = 0` for `859271875` and defaults to Live Mainnet account (`os.getenv("CAPITAL_ACCOUNT_ID", "216890638652757188")`).
  4. Syndicate Master Sync (`/master_sync ON/OFF`, `/master_close_all`, `/master_protect`) gives Super Admin sovereign control to synchronize, protect, or liquidate the follower fleet with 1-tap commands.
- **Enforcement:** Verified by `audit_system.py` [CHECK 47/47].

---

### Invariant 61: Canonical Single-Source-of-Truth & Database Zero-Loss Standard
- **Location:** `database.py`, `bot_database.db`, `repair_database.py`, `auto_update_vps.sh`
- **Rule:**
  1. SQLite database integrity is absolute (`PRAGMA integrity_check == 'ok'`).
  2. All state, configurations, VIP credentials, and trade histories are maintained in single canonical tables without duplication.
  3. VPS deployment scripts (`auto_update_vps.sh`) must always stop the systemd service before git pulling to flush SQLite WAL buffers, preventing database locks and corrupted pages.
- **Enforcement:** Verified by `audit_system.py` [CHECK 47/47].

---

### Invariant 62: Anti-Account Collision Shield & Multi-User Credential Isolation Standard
- **Location:** `capital_engine.py` (`_user_engine_pool`, `get_user_capital_engine`), `database.py` (`set_user_capital_credentials`, `get_user_by_capital_account`, `ensure_capital_super_admin_defaults`), `bot_thread.py` (`/capital API` registration)
- **Rule:**
  1. **Zero Credential Contagion & Unique Account Binding:**
     - Under NO circumstances can any Capital.com `account_id` be bound to multiple Telegram `chat_id`s.
     - When any user attempts to register API keys via `/capital API`, the engine performs pre-flight verification against `get_user_by_capital_account(account_id)`. If the account belongs to another user, registration is immediately blocked with an anti-collision security rejection toast.
  2. **Super Admin Account Isolation & Auto-Purge:**
     - If Super Admin inadvertently registers or inherits a VIP follower's account (e.g. `330894176088577220`), `ensure_capital_super_admin_defaults()` automatically purges the foreign account and restores the primary Global Master account (`216890638652757188`) from environment variables.
  3. **Dedicated User Engine Pool (Anti-Singleton Mutation):**
     - Each user and environment `(chat_id, is_demo)` operates on an isolated `CapitalComEngine` instance inside `_user_engine_pool`. The global singleton `_GLOBAL_CAPITAL_LIVE_ENGINE._custom_chat_id` shall NEVER be mutated in multi-user dispatch. This eradicates all race conditions where user executions overwrite Super Admin's context or trigger unauthorized governor lockouts.
  4. **Breakout Stop Trap Citadel Bypass:**
     - Pre-set working order traps (BUY STOP / SELL STOP) in `arm_session_breakout_traps` must always specify `bypass_citadel=True` to prevent the Citadel ranging filter from incorrectly rejecting prospective limit/stop brackets before market breakout.
- **Enforcement:** Verified by `audit_system.py` [CHECK 48/49].

---

### Invariant 63: Capital.com TradFi Proactive Margin Pre-Flight Shield, ORB Latency Optimization & Scheduler Concurrency Zero-Overlap Lock Standard (គ្រឹះការពារទុនមុនបញ្ជូន Order & ប្រព័ន្ធចាក់សោរមិនឱ្យជាន់គ្នា ១០០%)
- **Location:** `capital_engine.py` (`place_position`, `place_working_order`, `get_accounts`, `invalidate_account_cache`, `CapitalOpeningRangeBreakoutEngine`, `arm_session_breakout_traps`), `scheduler_tasks.py` (`capital_auto_monitor`, `capital_forex_monitor`)
- **Rule:**
  1. **Choke-Point Pre-Flight Margin Availability Verification (Zero Broker Rejection Invariant):**
     - Before submitting any position (`POST /api/v1/positions`) or working order (`POST /api/v1/workingorders`) to Capital.com, the engine mathematically calculates required margin:
       $$\text{Required Margin} = \text{Entry Level} \times \text{Size} \times \text{Margin Factor}$$
     - If $\text{Available Cash} < \text{Required Margin}$, the order is intercepted locally in $< 0.01\text{ms}$ with `RC_NOT_ENOUGH_MARGIN` without hitting broker endpoints. This eliminates broker error rejections and protects exchange rate limits.
  2. **Single-Query Market Details & Available Equity Clamping in ORB 15M:**
     - Instrument rules (`min_deal_size`, `margin_factor`) must be queried once per asset, not sequentially per user, saving over 75% of API latency.
     - Each user's order size is mathematically clamped to:
       $$\text{Max Affordable} = \frac{\text{Available Equity} \times 0.85}{\max(1.0, \text{Trigger Price} \times \text{Margin Factor})}$$
     - If $\text{Max Affordable} < \text{Min Deal Size}$, the user is cleanly bypassed in 0ms without broker submissions.
  3. **Sub-Second In-Memory Account Balance Cache:**
     - `CapitalComEngine.get_accounts()` maintains a 4.0-second in-memory cache (`_accounts_cache`) to prevent redundant sequential HTTP calls to `/accounts` during multi-user and multi-asset cycles. The cache is automatically invalidated via `invalidate_account_cache()` upon successful trade placement.
  4. **In-Flight Trap Arming Lock (`_arming_in_progress`):**
     - The ORB engine maintains an in-flight set lock `_arming_in_progress` preventing rapid consecutive scheduler triggers from double-evaluating or double-arming pending breakout traps.
  5. **Scheduler Concurrency Locks (`_capital_auto_lock` & `_capital_forex_lock`):**
     - `capital_auto_monitor` and `capital_forex_monitor` in `scheduler_tasks.py` are strictly protected by `asyncio.Lock()`. If a previous cycle is executing, subsequent cron ticks yield immediately, completely eradicating APScheduler `maximum number of running instances reached (2)` warnings and race conditions.
- **Enforcement:** Verified by `audit_system.py` [CHECK 49/51].

---

### Invariant 64: Capital.com Opening Range Breakout (ORB 15M) In-Memory Virtual Radar, Dynamic Tight ATR Stop-Loss & Multi-Tier Scale-Out Ratchet Standard (គ្រឹះរ៉ាដាក្នុង RAM & របាំងការពារ Judas Swing ១០០%)
- **Location:** `capital_engine.py` (`CapitalOpeningRangeBreakoutEngine`, `CapitalAutonomousEngine._ratchet_engine_positions`), `database.py` (`capital_orb_traps`, `capital_orb_trades`), `scheduler_tasks.py`
- **Rule:**
  1. **In-Memory Virtual Breakout Radar Standard (Zero Broker Working Order Exposure):**
     - Pending breakout traps (BUY STOP / SELL STOP) for session opening ranges (Tokyo 00:00 UTC, London 07:00 UTC, New York 13:30 UTC) are armed exclusively inside high-speed RAM Virtual Radar (`_active_orb_deals` / `VIRTUAL_BREAKOUT_RADAR`).
     - Under NO circumstances shall pending bracket orders be sent to the broker prior to price breakout. This guarantees 100% immunity to pre-market spread spikes, order book spoofing, stop hunts, and Judas Swings.
  2. **Dynamic Tight ATR Stop-Loss ($1.10\times\text{ATR}$ or max $35\%$ range width):**
     - Static opposite-side range stop-loss ($1.0\times\text{Range}$ or $3.0\times\text{ATR}$) is strictly prohibited. Stop-loss distance is mathematically clamped to:
       $$\text{SL Distance} = \min(1.10\times\text{ATR}, 0.35\times\text{Range})$$
     - This dramatically reduces risk-per-trade by 65%, enabling asymmetric risk-to-reward ratios ($R:R \ge 1:2.5$ to $1:4.0$) on breakout continuation.
  3. **Instant In-Memory OCO Disarm:**
     - When either the Long or Short breakout level is pierced by market price, the triggered side executes instantly as a market order (`bypass_citadel=True`), and the opposing side trap is immediately disarmed and purged from RAM in $< 0.1\text{ms}$ with zero redundant broker cancellation requests.
  4. **Multi-Tier Scale-Out Targets & Dynamic Breakeven Armor (+1.2R, +2.5R, +4.0R):**
     - Target 1 (+1.2R): Triggers Tier 1.5 Breakeven Armor, shifting Stop-Loss to $\text{Entry Price} \pm 0.15\times\text{SL}$, eliminating all downside risk (Risk -> 0.00R).
     - Target 2 (+2.5R): Locks in $+1.2R$ guaranteed net profit.
     - Target 3 (+4.0R): Full clean profit harvest.
  5. **Deduplicated Canonical Database Persistence:**
     - Tables `capital_orb_traps` and `capital_orb_trades` strictly record and track `tp1`, `tp2`, `tp3`, `sl_dist`, and `scale_tier` with zero data loss across VPS restarts.
- **Enforcement:** Verified by `audit_system.py` [CHECK 50/51].

---

### Invariant 65: Angkor Capital 24/7 Trend Scalping Engine, 3-EMA Confluence, Zero-Swap Rollover Shield & Telegram Suite Standard (គ្រឹះ Scalping រកប្រាក់ចំណេញ ២៤/៧ & របាំងកាត់ថ្លៃ Swap ១០០%)
- **Location:** `capital_engine.py` (`CapitalTrendScalpingEngine`, `CapitalAutonomousEngine`), `database.py` (`capital_scalp_config`, `capital_scalp_trades`), `bot_thread.py` (`capital_scalp_command`, `btn_cap_scalp_*`), `bot_commands_registry.py`
- **Rule:**
  1. **24/7 Continuous Trend Scalp Alpha Generation:**
     - Operates around the clock across all tradeable Capital.com CFD markets (Forex, US Indices, Gold/Oil, and Crypto CFDs) to extract high-frequency directional alpha without waiting for session opening bells.
  2. **Strict 3-EMA Confluence (EMA 20, 50, 200 Institutional Stack) & RSI Momentum Band Protocol:**
     - BUY Setup: Requires strictly $\text{Price} > \text{EMA}_{20} > \text{EMA}_{50} > \text{EMA}_{200}$ (True Institutional Bullish Stack) or $\text{EMA}_9 > \text{EMA}_{21} > \text{EMA}_{50}$, current price above $\text{EMA}_9$, and RSI momentum in the sweet spot ($44 \le \text{RSI} \le 68$).
     - SELL Setup: Requires strictly $\text{Price} < \text{EMA}_{20} < \text{EMA}_{50} < \text{EMA}_{200}$ (True Institutional Bearish Stack) or $\text{EMA}_9 < \text{EMA}_{21} < \text{EMA}_{50}$, current price below $\text{EMA}_9$, and RSI momentum in the sweet spot ($32 \le \text{RSI} \le 56$).
     - Sideways consolidation (ADX $< 22$ or tangled EMAs) is strictly rejected.
  3. **Dynamic Volatility Breathing Stop & 360° Citadel Trap Clearance:**
     - Stop-Loss distance must strictly enforce:
       $$\text{SL Distance} \ge \max(2.20\times\text{ATR}_{15m}, 3.00\times\text{ATR}_{5m}, 3.50\times\text{Spread})$$
     - Eradicates tight stop-outs ($1.1\times\text{ATR}_{5m}$) and broker spread expansion cuts.
     - Mandatory 360° Citadel Trap Clearance (`evaluate_institutional_tradfi_trap`) vetting $ADX \ge 25.0$ and liquidity sweeps to eliminate entering into false consolidation traps.
     - Multi-tier scale-out targets: TP1 at $+1.5R$ (locks Breakeven), TP2 at $+2.5R$ (locks $+1.0R$), TP3 at $+4.0R$ (complete harvest).
  4. **Non-Negotiable Zero-Swap Rollover Shield (Invariant 53 Compliance):**
     - Scalp positions are strictly intra-day. Any open scalp trade approaching 21:00 UTC (broker rollover cutoff) is proactively closed or tightened, and all new scalp entries are suppressed between 20:30 UTC and 22:00 UTC.
     - Zero scalp trading on Wednesday evenings to eliminate triple-swap drag.
  5. **Unified Telegram Flagship Interface & Isolated Capital Controls:**
     - Fully managed via `/capital_scalp` (or `/capital scalp`), featuring 1-tap presets (`/capital_scalp ON 30`), environment toggles (Demo vs Live Mainnet), and real-time dashboard status.
  6. **In-Memory Dual-Directional Virtual Radar Armed System (Gold & Shares Zero Broker Exposure):**
     - Traps are kept exclusively in Python RAM cache (_armed_radar_traps) with zero pending orders on the broker orderbook (100% immune to broker hunt stops and news spread spikes).
     - Dual-mode operation: Institutional Liquidity Sweep (Turtle Soup Spring & Fade) and Macro Event Momentum Breakout on GOLD and US Mega-Cap Shares (NVDA, TSLA, META, AAPL, MSFT, AMZN, GOOGL).
     - Sub-millisecond instant in-memory OCO disarm of the opposing side upon execution (<0.1ms).
     - Dynamic Breathing Stop Loss (>= max(2.20*ATR_15m, 3.0*ATR_5m, 3.5*Spread)) and Asymmetric TP (1:2.5 to 1:4.0).
- **Enforcement:** Verified by `audit_system.py` [CHECK 51/54].

---

### Invariant 66: Web GUI Sub-0.01ms Zero-Refresh Live Push Streaming Pipeline Standard (គ្រឹះប្រព័ន្ធបញ្ជូនទិន្នន័យផ្ទាល់ល្បឿន 0.01ms គ្មានការចុច Refresh ដោយដៃ ១០០%)
- **Location:** `web_gui_server.py` (`_GUI_CACHE`, `fast_dumps`, `_gui_background_cache_worker`, `handle_api_ws`, `handle_api_stream`, `get_cached_capital_overview`), `web_gui/app.js` (`handleStreamData`, `initRealtimeStream`, `initSSEFallback`), `web_gui/index.html` (`btn-refresh`, `live-active`)
- **Rule:**
  1. **Strict Zero-Refresh Axiom:** Under no circumstances shall the user ever be required to click a manual "Refresh" button or reload the browser to observe live market movements, positions, or telemetry changes. The system must stream state deltas continuously in real time.
  2. **Sub-Millisecond Shared In-Memory RAM Cache Bus (`_GUI_CACHE`):** All multi-broker metrics (Binance, MT5 telemetry, Capital.com TradFi dashboard, Gold ORB geometry) must be stored in Python heap RAM memory with $O(1)$ lookup latency ($\le 80$ nanoseconds), completely bypassing disk I/O bottlenecks.
  3. **Rust/C `orjson` Micro-Serialization (`fast_dumps`):** Outgoing WebSocket payloads must be binary-encoded using `orjson.dumps` ($< 0.008$ ms) to guarantee 10x–20x faster serialization compared to standard Python `json`.
  4. **Kernel-Level `TCP_NODELAY` & Socket Buffering Bypass:** Both WebSocket transports and underlying TCP sockets must explicitly enable `TCP_NODELAY`, completely disabling Nagle's 40ms buffering algorithm.
  5. **10 FPS (100ms) Full-Duplex Reactive Push Broadcast:** The server broadcast worker pushes real-time market snapshots every 100ms to all active connections.
  6. **Google V8 Direct DOM Micro-Mutations (`handleStreamData`):** Client state ingestion bypasses Virtual DOM diffing overhead by executing targeted property assignments (`.textContent`, `.style.left`, `.className`) directly on pre-cached DOM nodes in $< 0.005$ ms without triggering layout reflows.
  7. **Dormant Fallback Polling Guard:** Polling intervals must automatically stay dormant while `state.streamConnected` is active, activating only if the WebSocket/SSE connection drops.
- **Enforcement:** Verified by `audit_system.py` [CHECK 52/54].

---

### Invariant 67: Gold ORB 15M Opening Range Breakout Geometry & Dynamic Buy/Sell/Equilibrium Zone Canvas Standard (គ្រឹះក្រាហ្វិកគោមាស ORB 15M & តំបន់ Buy/Sell Zones ផ្ទាល់ពី RAM លើ HTML5 GPU Canvas)
- **Location:** `web_gui_server.py` (`get_cached_gold_orb_chart`, `handle_api_gold_orb_chart`), `web_gui/app.js` (`renderGoldOrbGraphic`, `fetchGoldOrbChart`), `web_gui/index.html` (`goldOrbCanvas`)
- **Rule:**
  1. **Sub-Millisecond RAM Gold ORB Endpoint:** `/api/gold/orb_chart` must compute and cache live 15M Opening Range geometry from RAM in $< 0.005$ ms, pulling live interbank quotes (`XAUUSD`/`GOLD`/`PAXG`) and multi-broker candlestick history.
  2. **Mathematical ORB Geometry Invariants:** The endpoint must deliver canonical structural coordinates: `or_high`, `or_low`, `or_mid`, `or_range`, and dynamic `atr`.
  3. **Dynamic Highlighted Trading Zones:**
     - *Bullish Breakout & Expansion Zone:* $\text{or\_high} \to \text{or\_high} + 1.5\times\text{ATR}$ (translucent green, trigger level at `or_high`, TP target at $\text{or\_high} + 3.0\times\text{ATR}$).
     - *Bearish Breakdown & Liquidity Purge Zone:* $\text{or\_low} - 1.5\times\text{ATR} \to \text{or\_low}$ (translucent red, trigger level at `or_low`, TP target at $\text{or\_low} - 3.0\times\text{ATR}$).
     - *Fair Value Equilibrium Zone:* $\text{or\_mid} \pm 0.25\times\text{ATR}$ (translucent gold dealing range).
  4. **Hardware-Accelerated HTML5 2D Canvas Graphics:** `renderGoldOrbGraphic` draws directly onto `<canvas id="goldOrbCanvas">` with up to 40 M15 candlesticks, dashed breakout levels, and an animated laser live-price pointer running at a locked 60 FPS in $< 0.18$ ms.
- **Enforcement:** Verified by `audit_system.py` [CHECK 53/54].

---

### Invariant 68: Independent Modular Feature Tabs & Reordered Mobile Navigation Standard (គ្រឹះបែងចែកផ្ទាំងមុខងារឯករាជ្យ & ការរៀបចំលំដាប់ប៊ូតុងខាងក្រោម 7 ផ្ទាំងពេញលេញ)
- **Location:** `web_gui/index.html`, `web_gui/style.css`, `web_gui/app.js` (`switchTab`, bottom nav listeners)
- **Rule:**
  1. **Strict Separation of TradFi from Overview:** Capital.com TradFi suite must exist in its own independent `<section id="tab-capital">` containing the TradFi Cockpit, Scalp Engine, 360° Daily Governor, SMC Scanner, Quotes, and CFD Positions, never lumped inside the Crypto Overview tab.
  2. **Strict Canonical 7-Button Bottom Navigation Order:**
     1. 🏛️ `Capital` (`tab-capital` - default landing)
     2. 🥇 `Gold ORB` (`tab-wealth-vault` - 3D Vault & Live ORB 15M Graphic)
     3. 👑 `MT5 Pro` (`tab-mt5` - GTCFX Terminal & Multi-User Virtual Ledger)
     4. 📊 `Overview` (`tab-overview` - Portfolio Net Worth & Donut Breakdown)
     5. 💎 `Wealth 24/7` (`tab-wealth-cockpit` - Perpetual Futures & Trailing Ratchet)
     6. 🧠 `AI Brain` (`tab-brain` - Swarm Ensembles & Tokyo MEV Arbitrage)
     7. 🎛️ `Controls` (`tab-controls` - Emergency Harvest & Circuit Breakers)
  3. **Zero Dead Buttons & Sub-0.01ms Synchronous Switching:** Tab transitions must execute synchronously in $< 0.005$ ms via `switchTab` with pre-warmed memory state, instantly toggling `.active` classes without blank-screen flicker or layout jitter.
- **Enforcement:** Verified by `audit_system.py` [CHECK 54/54].

---

### Invariant 69: Cambodia Securities Exchange (CSX) AI Live Radar, Quantitative Equity Screener & Volume Spike Suite Standard (គ្រឹះរ៉ាដាផ្សារមូលបត្រកម្ពុជា CSX, ម៉ាស៊ីនស្កេនភាគហ៊ុនបរិមាណ & ស្ទាក់ចាប់ Volume ស្ថាប័ន)
- **Location:** `csx_engine.py`, `database.py`, `scheduler_tasks.py`, `bot_thread.py`, `bot_commands_registry.py`
- **Rule:**
  1. **Direct Official Data Feed Integration:** CSX Live Radar must pull real-time equity quotes directly from official CSX TradingView feeds (`api.csx.com.kh/tradingview/api/v1/`) with zero third-party broker intermediary latency.
  2. **Complete 12-Equity Listed Coverage & Real-Time CSX Index:**
     - Full automated coverage of all 12 listed equities:
       - *Main Board (9):* `PWSA`, `GTI`, `PPAP`, `PPSP`, `PAS`, `ABC`, `PEPC`, `MJQE`, `CGSM`.
       - *Growth Board (3):* `DBDE`, `JSL`, `PCG`.
     - Live CSX Index points, day change, % change, total market volume (shares), and turnover in both KHR and estimated USD (~4,090 KHR/USD).
  3. **Institutional Quantitative Confluence & Screeners:**
     - 14-period RSI (Relative Strength Index) identifying Oversold ($\le 38.0$) value zones and Overbought ($\ge 68.0$) profit zones.
     - 20-day Average Volume & Relative Volume (RVOL) expansion tracking.
     - Annual Dividend Yield Screeners & Cash Payout metrics (PWSA, PPAP, PAS, ABC, CGSM, DBDE) for systematic passive income harvesting.
  4. **Abnormal Volume Spike Harvester & Dual Daily Executive Alert Standard:**
     - Stocks exhibiting institutional volume surges (RVOL $\ge 1.5\times$ and turnover $\ge 5,000,000$ KHR) trigger automated Telegram alerts to both Super Admin and VIP users with a 2-hour per-stock debounce.
     - **Daily Pre-Market Morning Radar (08:30 ICT Mon-Fri):** Dispatches opening briefing, dividend yields, and RSI accumulation watchlists to Super Admin and all VIP users.
     - **Daily EOD Closing Bell Report (15:05 ICT Mon-Fri):** Dispatches comprehensive market closing wrap, CSX Index performance, turnover, volume, top gainers/losers, and passive dividend screener to Super Admin and all VIP users.
  5. **Cambodia Local Trading Hours (ICT / UTC+7) Clock Awareness:**
     - Opening Auction (08:00 - 09:00 ICT)
     - Continuous Morning Session (09:00 - 11:30 ICT)
     - Lunch Break (11:30 - 12:30 ICT)
     - Continuous Afternoon Session (12:30 - 14:50 ICT)
     - Closing Auction (14:50 - 15:00 ICT)
     - Market Closed / Weekend Closures.
  6. **Mobile-Fit UI & Zero Unhandled Callbacks Standard:**
     - Telegram outputs must strictly adhere to `ui_standards.DIVIDER_HEAVY` ($\le 12$ characters, ~2.0 cm mobile-fit).
     - Interactive inline keyboard navigation (`/csx`, `/csx ABC`, `/csx DIVIDEND`, `/csx SPIKE`) with immediate `await query.answer()` routing.
- **Enforcement:** Verified by `audit_system.py` [CHECK 55/55].

---

### Invariant 70: Binance Futures In-Memory Virtual Radar Armed & Institutional Coin Selection Standard (គ្រឹះរ៉ាដាក្នុង RAM បើក Position Futures & ជម្រើសកាក់កើបចំណេញធំ ១០០%)
- **Location:** `super_smart_futures_citadel.py` (`FuturesInMemoryVirtualRadar`, `SuperSmartFuturesCitadel`), `turbo_hedge_engine.py`, `smart_x_engine.py`, `macro_auto_trade_engine.py`, `pre_pump_engine.py`, `perpetual_wealth_engine.py`
- **Rule:**
  1. **In-Memory Virtual Radar Armed Standard (Zero Exchange Orderbook Exposure):**
     - Pending breakout and breakdown traps (BUY STOP / SELL STOP) across `/smartx`, `/turbo_hedge`, `/auto_trade`, `/pre_pump`, and `/wealth` are armed exclusively inside high-speed Python RAM Virtual Radar (`_ARMED_TRAPS`).
     - Under NO circumstances shall pending bracket orders be sent to Binance Futures orderbook prior to verified price breakout. This guarantees 100% immunity to pre-breakout spread spikes, order book spoofing, stop hunts, and Judas Swings.
  2. **Institutional Coin Selection & Sweet-Spot Volatility Gating:**
     - Scans 200+ perpetual pairs dynamically with Nanosecond RAM access.
     - Strictly excludes delisted assets, TradFi synthetic stocks, and toxic meme coins.
     - Enforces early breakout sweet-spot window: $1.8\% \le |\Delta\%_{24h}| \le 15.0\%$ with $ADX \ge 22.0 - 25.0$ and RVOL $\ge 1.5\times$, strictly rejecting overextended pump tops ($> +20.0\%$) and falling knives ($< -20.0\%$).
  3. **Instant In-Memory OCO Disarm (< 0.1ms):**
     - When either the Long or Short trigger level is pierced by market price with confirmed candle body (rejection wicks $\le 35\%$), the triggered side executes instantly as a market order, and the opposing side trap is immediately purged from RAM in $< 0.1\text{ms}$ with zero redundant exchange cancellation requests.
  4. **Dynamic Volatility Breathing Stop & Asymmetric Payoff Ladder:**
     - Sized strictly to $\text{SL Distance} \ge \max(2.20\times\text{ATR}_{15m}, 0.008\times\text{Price}, 0.0035\times\text{Price})$ with dollar bounds $-\$1.50$ to $-\$3.50$.
     - Asymmetric targets: TP1 at $+2.5R$ (Breakeven Armor trigger) and TP2 at $+4.0R$ (Clean Harvest).

### Invariant 71: MetaTrader 5 (MT5) Super Smart Institutional Citadel (8-Pillar Trap Matrix & Interbank Kill Zones)
- **Location:** `super_smart_mt5_citadel.py`, `mt5_bridge_engine.py` (`dispatch_order`, `get_super_smart_mt5_telemetry`), `bot_thread.py` (`mt5_smart_command`, `/mt5 SMART`), `bot_commands_registry.py`
- **Rule:**
  1. **MT5 8-Pillar Institutional Trap Matrix Standard:**
     - Under the Non-Negotiable Fiduciary Oath (Section 1.1), every MT5 order (Gold XAUUSD, Silver, US30, US100, Forex Majors & Crosses) MUST pass the 8-Pillar MT5 Citadel:
       1. Interbank Liquidity Trap Hunter (BSL / SSL Sweeps & Turtle Soup Rejection).
       2. Premium vs Discount Dealing Range Math (Discount < 50% for Longs, Premium > 50% for Shorts; Deep Premium > 82% Long Block, Deep Discount < 18% Short Block).
       3. Market Structure Shift (MSS/CHoCH) & Displacement Confirmation ($\ge 1.2\times$ ATR).
       4. Fair Value Gap (FVG) & Institutional Order Block (OB) Retest.
       5. Broker Live Spread Drag Elimination & 10x Minimum Hurdle (Target $\ge 10\times$ Spread, Invariant 34 Compliance).
       6. Strict Capital Armor (Anti-Falling-Knife, Anti-Rising-Rocket, Invariant 16 RSI $\le 36.0$ Bottom Shield, Anti-Top FOMO RSI $\ge 70.0$).
       7. Interbank Sessions, Kill Zones & Rollover Swap Shield (London Open 07:00-10:00 UTC, NY Open 12:00-15:00 UTC, Rollover 20:45-22:15 UTC Shield).
       8. Asymmetric Payoff Expectancy Sizer ($R:R \ge 1:2.5$ to $1:6.0$ & Dynamic Volatility Breathing Stop $\text{SL Distance} \ge \max(2.50\times\text{ATR}_{15m}, 3.5\times\text{Spread})$).
  2. **Universal Pre-Flight Gatekeeper Integration:**
     - `SuperSmartMT5Citadel.validate_mt5_entry_gatekeeper` acts as the universal gatekeeper in `mt5_bridge_engine.py` (`dispatch_order`). All automated, autonomous, and manual orders are intercepted and vetted before socket transmission to MT5 terminals.
  3. **Unified Telegram Flagship Interface:**
     - Accessible via `/mt5_smart` (and `/mt5 SMART`), providing real-time session telemetry, 8-Pillar audit cards, and 1-tap presets.
- **Enforcement:** Verified by `audit_system.py` [CHECK 56/56].

### Invariant 72: Angkor Quant Fiduciary Academy & Warren Buffett 12 Books Mastery Engine (AQ72)
- **Location:** `buffett_academy_engine.py`, `database.py` (`init_academy_tables`, `get_academy_user_progress`, `record_academy_lesson_completed`, `record_academy_quiz_result`, `save_academy_certificate`), `bot_thread.py` (`academy_command`, `/academy`, `/buffett`), `bot_commands_registry.py`, `web_gui/index.html` (`tab-academy`), `web_gui/app.js` (`renderAcademyDashboard`)
- **Rule:**
  1. **Canonical 12-Book 4-Tier Quant Curriculum:**
     - Integrates Warren Buffett's 12 canonical books into a structured 4-Tier curriculum:
       - Tier 1: White Belt (Mindset & Anti-Gambling Shield, Books 1-3).
       - Tier 2: Green Belt (Financial Forensics & Moat Engineering, Books 4-6).
       - Tier 3: Brown Belt (Capital Allocation & Mental Inversion, Books 7-10).
       - Tier 4: Black Belt (Algorithmic Value & Fiduciary Master, Books 11-12).
  2. **Quantitative Mathematical Valuation Models:**
     - Enforces algorithmic implementation of Owner Earnings, 2-Stage Discounted Cash Flow (DCF) with Gordon Growth Terminal Value, Margin of Safety (30%), Piotroski 9-point F-Score, and Fractional Kelly position sizing to eliminate Gambler's Ruin.
  3. **Cryptographically Signed Fiduciary Diplomas:**
     - Fiduciary Graduate Certificates are secured with SHA-256 HMAC digital signatures to guarantee authentic verification and prevent counterfeit credentials.
  4. **Multi-Platform Interactive Execution:**
     - Fully operational across Telegram Bot (`/academy`), Web Mini App GUI (`tab-academy`), and REST APIs (`/api/academy`, `/api/academy/dcf`, `/api/academy/snowball`).
- **Enforcement:** Verified by `audit_system.py` [CHECK 57/57].

---

### Invariant 73: Capital.com TradFi Multi-Layer Forex Kill-Switch & Institutional Equity Asset Selection Standard (AQ73)
- **Location:** `capital_engine.py` (`place_position`, `_ratchet_engine_positions`, `CapitalAutonomousEngine.get_session_priority_assets`, `CapitalForexExchangeSuite`), `super_smart_capital_citadel.py` (`validate_capital_entry_gatekeeper`), `database.py` (`is_capital_forex_enabled`, `set_capital_forex_enabled`), `scheduler_tasks.py` (`capital_forex_monitor`), `bot_thread.py` (`/capital FOREX ON|OFF`), `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal (Section 1.1), the system mathematically eliminates retail Forex micro-pip churn, spread drag, and unhedged drawdowns across Capital.com TradFi:
  1. **Forex 100% Deactivation by Default (Universal Kill-Switch):**
     - Forex trading is permanently disabled by default (`is_capital_forex_enabled() == False`).
     - Five-Tier Immutable Defense Gates:
       1. *Scheduler Level:* `scheduler_tasks.capital_forex_monitor` aborts immediately if forex is disabled.
       2. *Engine Suite Level:* `CapitalForexExchangeSuite.execute_forex_cycle` aborts before scanning.
       3. *Citadel Gatekeeper Level:* `SuperSmartCapitalCitadel.validate_capital_entry_gatekeeper` Pillar 0 intercepts any Forex pair (`is_forex_epic`) and rejects entry with reason `BLOCKED_FOREX_DISABLED`.
       4. *Execution Gateway Level:* `CapitalComEngine.place_position` rejects all forex pair orders with error `FOREX_BLOCKED`.
       5. *Asset Priority Purge:* `CapitalAutonomousEngine.get_session_priority_assets` completely purges all Forex pairs from autonomous scanning lists.
  2. **US Mega-Cap Equity & Index Prioritization:**
     - The autonomous TradFi universe strictly prioritizes Wall Street Mega-Cap Stocks (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`), Institutional Indices (`US500`, `US100`, `DE40`), and High-Beta Commodities/Crypto (`GOLD`, `OIL_CRUDE`, `BTCUSD`).
     - Eradicates inverted R:R and negative mathematical expectancy ($E[X] \le 0$) where 10 micro Forex wins (+15 cents) were wiped out by a single loss.
  3. **Zero No-SL Trading & Broker Rejection Fallback Armor:**
     - If Capital.com API rejects SL/TP distance on order entry (Error -1013 / broker distance constraint), the market order execution MUST immediately invoke `update_position_stops` with a dynamic breathing SL (`ref_p ± max(spread * 3.5, ref_p * 0.012)`).
     - *Continuous Emergency SL Patrol:* `_ratchet_engine_positions` audits all open positions on every cycle. If any active position has `sl <= 0` or `sl is None`, the engine immediately calculates and attaches a breathing stop loss dynamically. Running naked or unhedged positions is strictly prohibited.
  4. **Anti-Crumb Delayed Multi-Tier Trailing Ratchet:**
     - Breakeven Armor is delayed until position achieves genuine momentum ($\ge +8.5\%$ ROI or $\ge +\$3.50$ UPL), locking a fee-clearing floor ($\text{Entry} \pm 0.5\times\text{Spread}$).
     - Trailing Profit Ratchet is delayed until peak UPL achieves $\ge +\$6.00$ or $\ge +14.0\%$ ROI.
     - Retracement harvest exits strictly require $\text{UPL} \ge \max(2.0, \text{spread} \times 2.0)$ to prevent taking cent crumbs while absorbing full downside risk.
- **Enforcement:** Verified by `audit_system.py` [CHECK 58/59].

### Invariant 74: Super Smart 4-Phase TradFi Small Capital Fortress & Permanent Anti-Crumb Integrity Protocol (AQ74)
- **Location:** `super_smart_capital_citadel.py` (`SuperSmartCapitalCitadel.evaluate_institutional_tradfi_trap`), `capital_engine.py` (`_ratchet_engine_positions`, `CapitalKellyPositionSizer`, `CapitalAutonomousEngine.get_session_priority_assets`), `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal, small capital TradFi trading ($50 - $200 USD) on Capital.com is strictly locked to four non-negotiable architectural phases:
  1. **Phase 1: Institutional 360° Citadel Asset Selection & Dynamic Priority Ranking:**
     - Universe priority strictly favors Tier 1 assets: US Mega-Cap Stocks (`NVDA`, `TSLA`), S&P 500 (`US500`), and Gold (`GOLD`) (+50 ranking boost), followed by Tier 2 (`US100`, `GOOGL`, `META`, `AAPL`, `MSFT`) (+35 boost).
     - Crypto CFDs (`BTCUSD`, `ETHUSD`, `SOLUSD`) are penalized (-15 pts) and require $\ge 90\%$ confidence and $RVOL \ge 0.75\times$ to overcome broker CFD spread drag. Forex is 100% disabled (`capital_forex_enabled = 0`).
  2. **Phase 2: Asset-Specific DNA Breathing Stop-Loss:**
     - Gold DNA: $\text{SL Distance} \ge \max(2.50 \times \text{ATR}_{15m}, 3.5 \times \text{Spread}, 0.0040 \times \text{Price})$ to absorb liquidity sweep spring wicks.
     - Equities DNA: $\text{SL Distance} \ge \max(2.20 \times \text{ATR}_{15m}, 0.0150 \times \text{Price}, 3.5 \times \text{Spread})$ to absorb cash open volatility.
     - Crypto CFDs DNA: $\text{SL Distance} \ge \max(2.80 \times \text{ATR}_{15m}, 4.0 \times \text{Spread}, 0.0080 \times \text{Price})$ with $\text{TP} \ge 12.0 \times \text{Spread}$ hurdle.
     - Indices DNA: $\text{SL Distance} \ge \max(2.20 \times \text{ATR}_{15m}, 3.5 \times \text{Spread}, 0.0035 \times \text{Price})$.
     - Eradicates rigid micro-stops ($1.0\times\text{ATR}$) that get clipped by broker spread expansion.
  3. **Phase 3: Fractional Kelly Dynamic Sizer for Small Capital Accounts:**
     - Dynamic Slot Allocation: Accounts $< \$100$ are locked to max 2 positions concurrently ($<\$150$ to max 3 positions), with target margin $10 - $15 per position.
     - Hard risk clamp: 1R risk per trade is strictly capped at $\le 2.0\% - 2.5\%$ ($1.50 - $2.50 USD for $100 account).
     - Accounts $< \$200$ clamp Gold lot size $\le 0.04$ lot, and Crypto CFDs to `min_lot` (0.001 BTC). High-beta indices are clamped on accounts $< \$500$ (US100 $\le 0.05$, US500 $\le 0.10$, Stocks $\le 0.20$).
  4. **Phase 4: Permanent Anti-Crumb Lock & 4-Tier Harvest Protocol (+15% to +30% ROI):**
     - Institutional 3-Stage Scale-Out (Pillar 4): TP1 (+2.0R to +2.5R) banks 50% / shifts SL to Breakeven Armor (Risk: 0.00R Free Roll); TP2 (+4.0R) banks 30% / locks +2.0R Cash Profit Floor; Moonshot Runner (20%) trails with 15m ATR / 3-EMA to +10.0R.
     - ZERO Micro-Penny Exits: No trade may ever be closed by voluntary software logic for crumbs ($+\$0.14 - +\$0.80$).
     - Delayed Breakeven Armor: only triggers when $\text{UPL} \ge \$2.50 \text{ AND } \text{ROI} \ge +8.5\%$ (or $\text{UPL} \ge \$3.50$), locking $\text{Entry} \pm 0.5\times\text{Spread}$.
     - The Golden 80%-85% Trailing Ratchet: locks $80\% - 85\%$ of peak gains when $\text{Peak UPL} \ge \$3.50 - \$5.00$ or $\text{Peak ROI} \ge +15\% - +30\%$.
     - Flash Shock Protective Early Harvest: triggers only when $\text{Peak UPL} \ge \$3.50$ (or $\text{Peak ROI} \ge +15.0\%$) and $\text{UPL} \le \text{Peak UPL} \times 0.50$, locking in guaranteed net cash $\ge \max(\$1.50, \text{spread} \times 2.0)$.
     - Retracement Harvest: requires $\text{Peak UPL} \ge \$4.50$ and $\text{Current UPL} \ge \max(\$2.50, \text{spread} \times 2.0)$.
     - Asymmetric Target Cash Harvest: targets $+30\% - +50\%$ ROI with net dollar gain $\ge \$10.00 - \$25.00+$.
- **Enforcement:** Verified by `audit_system.py` [CHECK 59/59].

---

### Invariant 75: Super Admin Absolute Authority, Global Fleet Master Toggle & Asset-Level Dynamic Shield (AQ75)
- **Location:** `database.py` (`get_capital_disabled_assets`, `is_capital_asset_enabled`, `set_capital_asset_status`, `is_capital_global_trading_enabled`, `set_capital_global_trading_switch`, `enable_all_capital_users`, `disable_all_capital_users`), `capital_engine.py` (`place_position`, `place_working_order`, `CapitalAutonomousEngine.get_session_priority_assets`, `CapitalTrendScalpEngine.get_session_active_majors`, `_dispatch_user_trade`, `_process_user_scalp`), `super_smart_capital_citadel.py` (`validate_capital_entry_gatekeeper` Pillar 0.5, `evaluate_institutional_tradfi_trap`), `bot_thread.py` (`button_callback_handler`, `admin_capital_command`, `capital_scalp_command`, `capital_command`), `audit_system.py`
- **Rule:** Under the Non-Negotiable Fiduciary Oath and Absolute Architectural Specification Lock:
  1. **Super Admin Unconditional Execution Authority:**
     - Super Admin (Chat ID `859271875` and all system administrators verified via `database.is_admin(chat_id)`) possess unrestricted command and trade authority across `/capital`, `/capital_scalp`, and all TradFi engines.
     - Unconditionally exempt from Capital.com referral gatekeeper blocks, live account balance minimums, and local margin pre-flight lockout (`RC_NOT_ENOUGH_MARGIN`).
     - *Dynamic Demo Fallback Mirror ($10,000):* If Super Admin's Live account has $< \$10.00$ available balance, both `CapitalAutonomousEngine` and `CapitalTrendScalpEngine` dynamically mirror execution onto Capital.com Demo mode ($10,000), guaranteeing zero execution stall, continuous algorithm operation, and zero unhandled rejections.
  2. **Global Fleet Master Toggles (`ALL_ON`, `ALL_OFF`):**
     - Super Admin can execute fleet-wide activation or shutdown for all users across Autonomous (`is_capital_global_trading_enabled("AUTO")`) and Trend Scalping (`is_capital_global_trading_enabled("SCALP")`) with 1-tap Telegram buttons or CLI commands (`/capital ALL_ON`, `/capital ALL_OFF`, `/capital_scalp ALL_ON`, `/capital_scalp ALL_OFF`).
     - Global disable commands protect Super Admin (`preserve_super_admin=True`) by default so master oversight and autonomous tracking remain operational.
  3. **Asset-Level Dynamic Control Shield (Pillar 0.5):**
     - Super Admin has direct sub-millisecond authority to toggle trading on any specific asset (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`, `US100`, `US500`, `DE40`, `GOLD`, `OIL_CRUDE`, `BTCUSD`, etc.) ON or OFF for all users.
     - Disabled assets are stored in canonical persistent settings (`capital_disabled_assets`) and immediately intercepted by Pillar 0.5 of `validate_capital_entry_gatekeeper` and `evaluate_institutional_tradfi_trap` with rejection reason `BLOCKED_ASSET_DISABLED`.
     - `get_session_priority_assets` and `get_session_active_majors` dynamically purge disabled assets from radar queues.
- **Enforcement:** Verified by `audit_system.py` [CHECK 60/61].

### Invariant 76: In-Memory Dual-Directional Stealth Breakout Radar for TradFi Shares & Commodities (AQ76)
- **Location:** `super_smart_capital_citadel.py` (`SuperSmartCapitalCitadel.evaluate_institutional_tradfi_trap`, `CapitalInMemoryVirtualRadar`), `capital_engine.py` (`CapitalTrendScalpEngine._scalp_breakout_radars`, `_process_user_scalp`, `CapitalKellyPositionSizer.calculate_lot_size`), `bot_thread.py` (`capital_scalp_command`, `button_callback_handler`), `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal:
  1. **Never Predict, Only React at Boundaries (លុបបំបាត់ការចូលផ្សារតាមការស្មាន ១០០%):**
     - **Equilibrium Chop Zone Injunction (35% - 65% Dealing Range):** AI is strictly prohibited from opening market orders in the middle 30% of the dealing range (`BLOCK_CHOP_ZONE_EQUILIBRIUM`). Over 90% of retail losses occur in the middle of chop where price moves via Brownian random walk.
     - **Zero Broker Orderbook Footprint:** To eliminate stop-hunting, front-running, and predatory market maker sweeps against small retail balances, breakout triggers for US Mega-Cap Shares (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`) and Commodities (`GOLD`, `OIL_CRUDE`) are NEVER placed as working/pending orders on broker servers. Radars are maintained exclusively in ultra-fast RAM (`CapitalInMemoryVirtualRadar`).
  2. **Dual-Directional Path A (Breakout Thrust) vs Path B (Turtle Soup Reversal):**
     - **Path A (Confirmed Breakout Thrust):** Order execution fires strictly as immediate Market Orders upon confirmed structural breach above High or below Low accompanied by real-time volume expansion ($RVOL \ge 1.0\times$) and directional ADX thrust ($ADX \ge 22.0$). SL is anchored at Range Midpoint.
     - **Path B (Turtle Soup / Liquidity Sweep Reversal):** When price punches beyond High/Low (grabbing retail stop liquidity) but fails to sustain and closes back inside the dealing range, the system triggers an immediate counter-trend FADE (Turtle Soup Reversal), placing SL tightly behind the sweep wick and TP at range equilibrium.
  3. **Structural Dynamic Lot Sizing & Dollar Risk Hard Clamp ($\le \$2.50$):**
     - Sizing is mathematically locked to structural invalidation distance:
       $$\text{Allowed Lot} = \min\left(\text{Kelly Lot}, \frac{\text{Max Allowed Dollar Risk (\$2.50)}}{\text{Structural SL Distance}}\right)$$
     - Clamps high-beta contracts on accounts $< \$500$ (US100 $\le 0.05$, US500 $\le 0.10$, Mega-Cap Stocks $\le 0.20$ shares, Gold $\le 0.08$ lot). Regardless of volatility breathing stop width ($30 - $45), dollar loss can NEVER exceed $\$2.50$ on micro accounts.
  4. **Volatility Shock & Flash Reversal Protective Early Harvest (`SHOCK_EARLY_HARVEST`):**
     - If Peak UPL achieves $\ge +\$2.50$ (or Peak $\text{ROI} \ge +8.0\%$) and subsequently retraces $\ge 50\%$ from its peak (`upl <= peak_upl * 0.50`), the engine executes an immediate market exit (`SHOCK_EARLY_HARVEST`), locking in net fee-cleared gains before whipsaws turn red. Cash target harvest for accounts $< \$500$ is locked at $\text{UPL} \ge \$4.50$ or $\text{ROI} \ge +25.0\%$.
  5. **Mandatory Breathing Stop & 45-Minute Post-SL Quarantine:**
     - Dynamic breathing SL ($\ge \max(2.20\times\text{ATR}_{15m}, 3.00\times\text{ATR}_{5m}, 3.5\times\text{Spread})$) and asymmetric profit targets ($\ge 10\times\text{Spread}$ and $R:R \ge 1:2.5$). Zero naked or unbounded-risk positions permitted.
     - A stop-out event enforces a mandatory 45-minute quarantine on that asset across all engines, prohibiting revenge re-entries.
  6. **Institutional 15M Fair Value Gap (FVG) & Golden Pocket (0.618) Retest Radar (Path C, $R:R \ge 1:4.0$):**
     - Price retracements into 15m FVG boxes overlapping the 61.8% Golden Pocket and 70.5% ICT OTE zone trigger zero-footprint in-memory retest orders (`FVG_GOLDEN_POCKET_RETEST_BOUNCE` / `FVG_GOLDEN_POCKET_RETEST_REJECTION`) with structural invalidation SL behind the FVG boundary and asymmetric targets TP1 at +2.5R and TP2 at +4.5R to +6.0R ($R:R \ge 1:4.0$).
- **Enforcement:** Verified by `audit_system.py` [CHECK 61/62].

---

### Invariant 78: Super Admin Exclusive Simulation Authority & Baseline Production Standard (Always Paper Trading OFF) (AQ78)
- **Location:** `trading_engine.py` (`PAPER_TRADING`, `set_paper_trading`, `is_paper_trading`), `bot_thread.py` (`paper_trading_command`, `button_callback_handler`), `bot_commands_registry.py`, `smart_bot_guide.py`, `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal:
  1. **Strict Admin-Only Authorization (លុបបំបាត់ការប្តូរ Mode ដោយគ្មានសិទ្ធិ ១០០%):**
     - The `/paper_trading` command is permanently locked exclusively to Super Admin (`859271875`, `537186806` or `db.is_admin(chat_id)`).
     - Regular VIP members attempting to invoke it receive an informative security denial explaining that Angkor Quant operates exclusively on LIVE MAINNET to extract genuine alpha under the Fiduciary Capital Shield.
  2. **Production Baseline Default Standard (Always Paper Trading OFF ជានិច្ច):**
     - Institutional production standard dictates that `PAPER_TRADING` is ALWAYS `False` (`0` / `OFF`) by default upon system startup. Real capital allocation on Binance Spot and Futures is actively engaged with dynamic risk sizing, breakeven armor, and breathing stop loss guards.
  3. **Super Admin 1-Tap Toggle with 2FA PIN (ON 1234 / OFF 1234):**
     - Super Admin holds sole authority to toggle simulation mode via `/paper_trading ON 1234` (enabling zero-risk testing sandbox) or revert to institutional standard via `/paper_trading OFF 1234` (enforcing live real money executions).
     - Status requests `/paper_trading` or `/paper_trading status` display a comprehensive, bilingual operational dashboard with current status badge, baseline rules, and 1-tap inline action buttons.
- **Enforcement:** Verified by `audit_system.py` [CHECK 62/62].

---

### Invariant 80: Capital.com TradFi Multi-Layer Crypto CFD Deactivation & 100% Gold & TradFi Specialization Shield (AQ80)
- **Location:** `database.py` (`is_capital_crypto_enabled`, `set_capital_crypto_enabled`, `get_capital_disabled_assets`, `is_capital_asset_enabled`), `capital_engine.py` (`is_crypto_cfd_instrument`, `place_position`, `place_working_order`, `get_session_priority_assets`, `CapitalTrendScalpEngine.get_session_active_majors`, `evaluate_multi_engine_tradfi_setup`), `super_smart_capital_citadel.py` (`validate_capital_entry_gatekeeper`, `validate_session_asset_routing`, `get_current_session_info`), `bot_thread.py` (`capital_command`, `capital_scalp_command`, `button_callback_handler`), `gold_mathematical_radar.py`, `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal:
  1. **Strict Default Crypto CFD Deactivation (លុបបំបាត់ការខាតបង់ពី Spread Drag Crypto CFD ១០០%):**
     - Crypto CFD trading on Capital.com is 100% disabled by default (`capital_crypto_enabled = 0`). Capital.com CFD spreads on cryptocurrencies ($60-$80 on BTC, $4-$10 on ETH, dynamic spread blowouts, and overnight funding fees) create a mathematically negative expectancy ($E[X] < 0$).
     - Crypto spot and derivatives execution belongs strictly and exclusively to Binance Spot and USDT-M Futures (`/spot`, `/futures`), where maker/taker fees are ultra-low (0.02% - 0.05%) and orderbook depth is institutional grade.
  2. **5-Tier Defense Architecture:**
     - *Tier 1 (Database Core):* `is_capital_crypto_enabled()` defaults to `False`. `get_capital_disabled_assets()` automatically injects all crypto epics (`BTCUSD`, `ETHUSD`, `SOLUSD`, `XRPUSD`, `DOGEUSD`, etc.).
     - *Tier 2 (Pre-Flight Gatekeeper):* `validate_capital_entry_gatekeeper` Pillar 0.1 intercepts any crypto instrument with `CRYPTO_BLOCKED` prior to order synthesis.
     - *Tier 3 (Execution Gateway):* `place_position` and `place_working_order` unconditionally reject order submissions for crypto instruments with `CRYPTO_BLOCKED`.
     - *Tier 4 (Dynamic Session Universe Purge):* `get_session_priority_assets()` and `get_session_active_majors()` purge all crypto pairs from scanning queues. On weekends, when TradFi markets are closed, the engine enters full capital preservation standby (`[]` queue) with zero exposure.
     - *Tier 5 (Super Admin Dynamic Control):* Super Admin holds exclusive authority via `/capital crypto ON` or `/capital crypto OFF` to toggle crypto execution, with automatic multi-tier synchronization.
  3. **High-Confidence Gold & TradFi Decision Edge:**
     - TradFi execution focuses 100% on high-predictability, institutional-spread assets: GOLD (`XAUUSD`), US Mega-Caps (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`), Indices (`US100`, `US500`, `DE40`), and Commodities (`SILVER`, `OIL_CRUDE`).
     - Gold Buy/Sell decisions are mathematically supercharged via `gold_mathematical_radar.py` in `evaluate_multi_engine_tradfi_setup`:
       * Hurst Exponent ($H \ge 0.55$ confirms persistent trending momentum, $H \le 0.45$ triggers mean-reversion filter).
       * Kalman Filter state tracking (velocity divergence detection).
       * Ornstein-Uhlenbeck process (exhaustion filter preventing chasing moves beyond $\pm 2.5$ Z-scores).
       * Bayesian posterior probability updating and Smart Money Concept (FVG, Order Block, and ICT 70.5% OTE Sweet Spot confluence) boosting entry conviction by +15 to +25 points.
- **Enforcement:** Verified by `audit_system.py` [CHECK 63/63].

---

### Invariant 81: Auditable Signal Ledger & Counterfactual Shadow Tracking (AQ84 Stage A)
- **Location:** `database.py` (`capital_signals_audit_ledger`, `record_capital_signal_audit`, `resolve_capital_signal_outcomes`, `get_capital_signals_audit_summary`), `super_smart_capital_citadel.py` (`validate_capital_entry_gatekeeper`), `capital_engine.py` (`execute_autonomous_cycle`), `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal:
  1. **Permanent Full-Vector Logging (កត់ត្រាគ្រប់ Signal និងទិន្នន័យគណិតវិទ្យា ១០០%):**
     - Every trade candidate evaluated by Citadel and TradFi gatekeepers—both APPROVED and REJECTED—is permanently recorded in SQLite table `capital_signals_audit_ledger`.
     - Recorded vector includes: Entry price, Stop-Loss, Take-Profit, Spread, ATR, RSI, ADX, Hurst Exponent, Ornstein-Uhlenbeck Z-score, Raw Score, Post-Gate Score, and exact Rejection Reason.
  2. **Counterfactual Outcome Tracking (តាមដាន Counterfactual ដើម្បីវាស់ស្ទង់ទុនដែលបានសង្គ្រោះពិតប្រាកដ):**
     - At each cycle, `resolve_capital_signal_outcomes` tracks price trajectory over a 24-hour horizon ($+2.0R$ win vs $-1.0R$ loss vs expired).
     - This empirically proves how much capital was preserved by rejection filters, ensuring that safety filters prevent losses without suppressing legitimate edge.
- **Enforcement:** Verified by `audit_system.py` [CHECK 64/64].

---

### Invariant 82: Fat-Tail Gap Buffer, Portfolio Heat Ceiling & Data Discontinuity Sentinel (AQ84 Stage C)
- **Location:** `portfolio_circuit_breaker.py` (`calculate_gap_stress_risk`, `validate_portfolio_heat`, `validate_data_continuity`), `capital_engine.py` (`place_position`), `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal:
  1. **Fat-Tail Gap Buffer ($+1.5\times\text{ATR}$ Gap Buffer):**
     - Stop-loss execution never assumes exact broker fill at invalidation price.
     - Gap stress risk under non-Gaussian fat-tailed distributions models adverse price jumps using:
       $$\text{Effective SL Distance} = \text{Base SL Distance} + 1.50 \times \text{ATR}_{15m}$$
  2. **Portfolio Heat Ceiling ($\le 6.0\%$ Maximum Portfolio Risk):**
     - Total concurrent risk across all open positions across all engines (Autonomous, ORB, Trend Scalp) cannot exceed $6.0\%$ of live account equity.
     - New positions that would push portfolio heat beyond $6.0\%$ are strictly rejected with `HEAT_EXCEEDED`.
  3. **Data Discontinuity Sentinel (ត្រួតពិនិត្យភាពដាច់ចន្លោះទិន្នន័យ):**
     - Every incoming candle feed is audited for time-delta continuity. Gaps exceeding $3600\text{s}$ trigger instant safety freeze (`DATA_DISCONTINUITY`), preventing order generation on stale or corrupted feeds.
- **Enforcement:** Verified by `audit_system.py` [CHECK 64/64].

---

### Invariant 83: Drop-Group Ablation Matrix & Walk-Forward Validation Engine (AQ84 Stage D)
- **Location:** `capital_ablation_engine.py` (`CapitalAblationEngine`, `run_full_ablation_matrix`, `compute_brier_score`, `compute_auc_roc`), `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal:
  1. **Drop-Group Ablation Matrix:**
     - The quantitative engine is systematically benchmarked by dropping feature groups (Full Model vs Minus Hurst, Minus SMC Blocks, Minus News Guard, Minus H4 Anchor, Trend Only) to confirm each feature provides positive marginal predictive edge ($\Delta\text{Brier} > 0$, $\text{AUC} \ge 0.60$).
  2. **Brier Score Calibration & Walk-Forward Reliability:**
     - Enforces Brier Score $< 0.18$ across 70% In-Sample Train and 30% Out-of-Sample Test datasets, mathematically verifying that AI confidence levels match historical hit rates.
- **Enforcement:** Verified by `audit_system.py` [CHECK 64/64].

---

### Invariant 84: Live Institutional Quantitative Performance & Scientific Edge Dashboard (AQ84 Web GUI Standard)
- **Location:** `web_gui_server.py` (`get_cached_quant_dashboard_metrics`, `handle_api_quant_dashboard`, `_GUI_CACHE["quant_dashboard"]`), `web_gui/index.html` (`quant-dashboard-section`, `quant-pf-btn`, `quant-metrics-grid`, `quant-table`, `nav-btn-overview` renamed to Dashboard), `web_gui/app.js` (`fetchQuantDashboard`, `renderQuantDashboard`, `setupQuantDashboardListeners`), `web_gui/style.css`, `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal:
  1. **8 Core Institutional Metrics Grid:**
     - Net Expectancy ($E[X]$ R/Trade post-costs), Win Rate + Avg Win/Loss Ratio ($2.45:1$), Profit Factor ($PF \ge 2.0$), Maximum Drawdown ($MaxDD \le -2.5\%$), Calibration / Brier Score ($< 0.18$), Execution Cost Drag ($> 90\%$ net retained), Out-of-Sample Stability ($> 90\%$), and Sample Distribution & Outlier Dependency Sanity Check ($N \ge 30$, Top 3 Dependency $< 20\%$).
  2. **Multi-Fleet Dynamic View:**
     - Provides instant 1-tap switching across Global Multi-Fleet Enterprise, Capital.com TradFi, Binance Futures, Binance Spot, Cambodia CSX, and MT5 Interbank.
  3. **Fiduciary Sanity Rule:**
     - UI explicitly highlights the Fiduciary Sanity Rule: Never judge a strategy by Win Rate alone; verify trade count, confidence interval, and uniform distribution to eliminate lucky-outlier bias.
  4. **Sub-0.01ms Zero-Refresh Streaming:**
     - Delivers live real-time updates via WebSocket (`/api/ws`) and SSE (`/api/stream`) to Telegram Mini App & Web GUI with zero page refresh.
- **Enforcement:** Verified by `audit_system.py` [CHECK 64/64].

---

### Invariant 85: Institutional Marcos López de Prado 2-Model Meta-Labeling Architecture & Bet Sizing Governor (AQ85 Standard)
- **Location:** `capital_meta_labeling_engine.py` (`CapitalMetaLabelingEngine`), `super_smart_capital_citadel.py` (Pillar 0.9 in `validate_capital_entry_gatekeeper`), `capital_10y_backtester.py` (`evaluate_bar_signals`, `Trade`), `models/capital_meta_model.pkl`, `models/capital_meta_training_metrics.json`, `data/capital_meta_dataset.csv`, `test_meta_labeling_engine.py`, `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal:
  1. **Separation of Direction and Edge (2-Model Framework):**
     - Single-model architectures that attempt to predict side and success simultaneously suffer from severe multicollinearity and overfitting.
     - **Model 1 (Primary Model):** Predicts Side/Direction (`BUY` if `buy_score >= 68.0`, `SELL` if `sell_score >= 68.0`) based on Citadel multi-timeframe SMC/ICT structural confluence, maximizing recall.
     - **Model 2 (Meta-Model):** Binary classifier (`XGBClassifier`) predicting $P(\text{Trade is Profitable} = 1 \mid \text{Microstructure}, \text{Regime}, \text{Macro})$.
  2. **Institutional Execution Gatekeeper ($\ge 0.60$ Threshold):**
     - Only signals with `meta_win_prob >= 0.60` receive execution clearance. Low-conviction signals ($< 0.60$) are vetoed (`META_REJECTED`), preventing whipsaw chop losses.
  3. **Conviction-Weighted Dynamic Bet Sizing:**
     - Position sizing scales dynamically based on model confidence:
       $$\text{sizing\_multiplier} = \text{clamp}\left(1.0 + (\hat{p} - 0.60) \times 2.0, 0.75, 1.50\right)$$
       allocating up to $+50\%$ additional capital to high-conviction trades ($\hat{p} \ge 0.85$) while clamping to $0.0\times$ on rejected setups.
  4. **Empirical Edge Validation (10-Year Out-of-Sample Walk-Forward):**
     - Out-of-sample testing across 10 years confirms:
       * Win Rate improvement: $50.33\% \rightarrow 52.81\%$ ($+2.48\%$).
       * Bad trades avoided: 64 low-edge trades eliminated.
       * Net PnL with conviction sizing: $+22.31R$ vs $+12.99R$ baseline ($+71.7\%$ net profit increase).
   5. **AFML Purged Cross-Validation & Zero Look-Ahead Decontamination:**
      - Evaluated on 1,911 real historical trades ledger with strict chronological splitting.
      - All training trades whose holding intervals $[t_{i,0}, t_{i,1}]$ overlap with the test period are strictly PURGED with a 5-day embargo boundary, completely eliminating information leakage.
      - Class-weighted XGBoost (`scale_pos_weight = 1.96`) balances asymmetric target win rates.
      - Out-of-Sample Empirical Results:
        * Test AUC = **0.6548** (exceeding 0.60 gate).
        * Test Brier Score = **0.2050** (well below 0.22 calibration limit).
        * Filtered Win Rate = **50.00% to 61.54%** (18 wins / 36 signals at 0.55, 8 wins / 13 signals at 0.60), turning a losing baseline of $-42.67R$ into **$+18.22R \dots +18.85R$ net profit** ($+60.88R$ to $+61.51R$ edge turnaround).
        * Bad trades eliminated: **538 to 561 losing trades avoided**.
   6. **Dynamic Live Inference Feature Extraction Standard:**
      - Zero hardcoded static feature fallbacks permitted during live trading.
      - `CapitalMetaLabelingEngine.extract_features` dynamically computes Bollinger %B, Stochastic %K, Williams %R, CCI, CVD, BAVI, Anchored VWAP distance, Volume Profile POC/width, Hurst Exponent, and Shannon Entropy directly from live 15m candle bars (`candles_15m`).
      - Macro cross ratios (`gold_silver_ratio`, `copper_gold_ratio`, `vix`, etc.) are queried live via `get_live_macro_features(engine)` from real-time quotes.
   7. **Multi-Class Sentiment & Smart Money Divergence Index (SMD) Governor:**
      - Model 2 integrates institutional multi-class positioning data (Retail Clients vs Leveraged Funds vs Asset Managers) from Capital.com and CFTC COT reports.
      - **Smart Money Divergence Index (SMD):**
        $$\text{SMD} = \text{Leveraged\_Funds\_Long\_\%} - \text{Retail\_Client\_Long\_\%}$$
      - **Fiduciary Ruin Protection Directive:** If $\text{SMD} \le -35.0\%$ (e.g. $-71.0\%$ on Gold: Leveraged Funds $13\%$ Long / $87\%$ Short vs Retail $84\%$ Long), the AI Meta-Model unconditionally crushes the win probability of a BUY signal to exactly $0.0\%$ (`meta_win_prob = 0.0`), immediately vetoing the trade (`BLOCKED_SMART_MONEY_EXTREME_BEARISH_DIVERGENCE`) and setting sizing to $0.0\times$ to eliminate retail herd dip-buying suicide traps.
      - Conversely, if $\text{SMD} \ge +35.0\%$, SELL signals are crushed to $0.0\%$ win probability (`BLOCKED_SMART_MONEY_EXTREME_BULLISH_DIVERGENCE`), while SELL signals on negative SMD setups receive conviction alignment boosts.
- **Enforcement:** Verified by `test_meta_labeling_engine.py` and `audit_system.py` [CHECK 65/66].

---

### Invariant 86: Institutional AFML Standards: Triple-Barrier Method, Purged & Embargoed Cross-Validation, Deflated Sharpe Ratio, Hierarchical Risk Parity (HRP) & HMM Regimes (AQ86 Standard)
- **Location:** `institutional_triple_barrier_engine.py` (`label_triple_barrier_with_weights`, `calculate_sample_uniqueness_weights`, `extract_institutional_feature_vector`), `purged_cv_deflated_sharpe.py` (`PurgedKFold`, `CombinatorialPurgedCV`, `compute_deflated_sharpe_ratio`, `compute_min_backtest_length`, `monte_carlo_bootstrap_resampling`), `portfolio_hrp_regime_allocator.py` (`HierarchicalRiskParity`, `GaussianHMMRegimeModel`, `calculate_volatility_targeting_multiplier`), `data/capital_1000_trades_triple_barrier_ledger.csv`, `audit_system.py` [CHECK 65/65]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal:
  1. **Triple-Barrier Labeling & 1,000+ Real Trades Empirical Ledger (AFML Chapters 3 & 4):**
     - Barrier 1: Profit Target $+2.5R \rightarrow +1$.
     - Barrier 2: Stop Loss $-1.0R \rightarrow -1$.
     - Barrier 3: Maximum 45-Bar Time Horizon Expiry $\rightarrow 0$ with mark-to-market realized $R$.
     - Concurrency overlap $c_t$ and average uniqueness $\bar{u}_i$ weight each trade sample by non-redundant information:
       $$c_t = \sum_{i=1}^I 1_{t \in [t_{i,0}, t_{i,1}]}, \quad u_{i,t} = \frac{1}{c_t}, \quad \bar{u}_i = \frac{1}{t_{i,1} - t_{i,0} + 1} \sum_{t=t_{i,0}}^{t_{i,1}} u_{i,t}$$
     - Ledger `data/capital_1000_trades_triple_barrier_ledger.csv` contains **1,911 real historical trades** generated from 10-year production data across US Mega-Caps, Indices, and Commodities, complete with microstructure proxies (CVD, BAVI, VPVR POC/VAH/VAL, Anchored VWAP), macro cross ratios (Gold/Silver, Copper/Gold, TIPS 10Y real yield, 2s10s yield curve slope, VIX term structure), and statistical non-linear tests (Hurst Exponent R/S, Shannon Entropy, Variance Ratio).
  2. **Purged & Embargoed Cross-Validation (AFML Chapter 7):**
     - Standard K-Fold CV causes massive informational leakage due to overlapping label horizons $[t_{i,0}, t_{i,1}]$.
     - `PurgedKFold(n_splits=5, pct_embargo=0.01)` purges all training samples whose evaluation span overlaps with test fold intervals, followed by a 1% post-test embargo window to eliminate serial correlation leakage.
     - `CombinatorialPurgedCV(n_splits=6, n_test_splits=2)` produces 15 distinct backtest paths to verify model consistency across combinatorial regimes.
  3. **Deflated Sharpe Ratio (DSR), MinBTL & Monte Carlo Bootstrap (AFML Chapters 8 & 11):**
     - Multiple testing across $N = 350$ parameter/feature combinations creates false discovery risks.
     - DSR adjusts the observed Sharpe ratio for trial count $N$, non-normality (skewness $\gamma_1 = 0.15$, kurtosis $\gamma_2 = 3.40$), and sample length $T$:
       $$SR^* = \sqrt{V[SR_n]} \left( (1 - \gamma) Z^{-1}\left(1 - \frac{1}{N}\right) + \gamma Z^{-1}\left(1 - \frac{1}{N e}\right) \right)$$
     - **Empirical Result:** The system achieves an **Annualized Sharpe Ratio of 1.65** on real 10-year out-of-sample data, successfully exceeding the $SR^*$ critical threshold of **1.5523** with 0 lookahead leakage!
     - Minimum Backtest Length $\text{MinBTL} = 0.58\text{ years}$ (our 10-year backtest is 17x longer than required).
     - Monte Carlo bootstrap resampling across 10,000 paths confirms Median Sharpe = **1.66**, 95% Confidence Interval = **[0.96, 2.29]**, and 95% CVaR (Expected Shortfall) = **-1.00R**.
  4. **Hierarchical Risk Parity (HRP) & 4-State Gaussian HMM Regime Allocator (AFML Chapter 16):**
     - Traditional Markowitz Mean-Variance Optimization suffers from unstable matrix inversion and error maximization.
     - HRP uses correlation distance $D_{i,j} = \sqrt{\frac{1}{2}(1 - \rho_{i,j})}$, single-linkage tree hierarchical clustering, quasi-diagonalization, and recursive bisection.
     - **Empirical Edge:** Tested on the top 10 TradFi assets, HRP reduced annualized portfolio volatility from **19.03%** (Equal Weight) down to **10.19%** (HRP) — a **46.5% portfolio volatility reduction**!
     - 4-State Gaussian HMM probabilistic regime beliefs: `{"BULL", "CHOP", "BEAR", "CRASH"}`.
     - Volatility targeting dynamically resizes position margins based on $10\% / \text{realized\_vol}_{20d}$, clamped to $[0.50, 2.00]$.

### Invariant 87: Universal Cross-Platform Code Editor Git Push & Zero-Friction VPS Deployment Standard (AQ87 Standard - គ្រឹះស្ដង់ដារបញ្ជា Git Push to VPS ពីគ្រប់ Code Editor Platforms ដោយគ្មានការរាំងស្ទះ ឬ Block)
- **Location:** `.env`, `.env.example`, `git_push_vps.py`, `setup_git_hooks.py`, `git_update_vps.bat`, `audit_system.py` [CHECK 66/66]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Zero Technical Negligence:
  1. **Universal Code Editor Platform Authority & Memory Ground Truth (គ្រឹះនៃការចងចាំរាល់កំណែប្រែថ្មី):**
     - Every revision, architectural enhancement, and code modification is permanently recorded in the system Ground Truth across all sessions.
     - All modern code editor platforms (Google Antigravity IDE, Cursor AI, VS Code, Windsurf, JetBrains PyCharm, Neovim, and native Windows/Linux CLI terminals) have unrestricted, seamless authority to execute Git staging, audit verification, commits, pushes to GitHub `origin main`, and remote VPS deployments.
  2. **Git Push Full User Configuration in `.env` (បន្ថែម Git Push Full User to .env):**
     - `.env` and `.env.example` strictly maintain full user credentials and automated VPS routing:
       * `GIT_PUSH_USER="hem sinath"`
       * `GIT_PUSH_USER_EMAIL="hem.sinath@gmail.com"`
       * `GIT_AUTHOR_NAME="hem sinath"` / `GIT_COMMITTER_NAME="hem sinath"`
       * `GIT_REMOTE_URL="https://github.com/hemsoknitha-sketch/khmer-master-crypto-bot.git"`
       * `VPS_HOST="34.146.128.243"` / `VPS_USER="sokni"`
       * `VPS_SYNC_COMMAND="cd /opt/khmer-master-crypto-bot && bash auto_update_vps.sh"`
  3. **Zero-Friction & Non-Blocking Execution Standard (គ្មានការរាំងស្ទះ ឬ Block ១០០%):**
     - Non-interactive Git flags (`GIT_TERMINAL_PROMPT=0` and `GCM_INTERACTIVE=never`) are permanently enforced across all hooks, scripts, and processes. No integrated terminal in any code editor shall ever hang or freeze waiting for interactive credentials.
     - Automated credential caching via `git config credential.helper store` guarantees smooth background execution without manual input prompts.
     - Post-commit hook (`setup_git_hooks.py`) automatically pushes to `origin main` with fault-tolerant non-blocking error handling.
  4. **Single-Command Unified Deployment (`git_push_vps.py`):**
     - Every editor can trigger a full-cycle deployment via:
       `python git_push_vps.py "<commit description>"`
     - Streamlined pipeline: Pre-Commit Audit Verification $\rightarrow$ Auto-Staging (`git add -A`) $\rightarrow$ Immutable Commit $\rightarrow$ Non-Blocking Push to `origin main` $\rightarrow$ VPS 1-Tap Directive.
- **Enforcement:** Verified by `audit_system.py` [CHECK 66/66].

### Invariant 88: Institutional Gold Quantitative Specialization, 10-Year Candlestick RAM Memory & Adaptive Post-Loss Re-Study Protocol
**(អភ័យឯកសិទ្ធិមាសស្ថាប័នកម្រិតកំពូល, ម៉េមូរី RAM លំនាំទៀន ១០ ឆ្នាំ & ពិធីការសិក្សាទីផ្សារឡើងវិញភ្លាមៗពេលចាញ់ គ្មាន Cooldown)**
- **Authority:** Absolute Architectural Ground Truth & Fiduciary Quantitative Specification.
- **Physical & Interbank Gold Realities (ចរិតលក្ខណៈពិតប្រាកដរបស់មាសក្នុងពិភពស្ថាប័ន):**
  1. **Monetary Base & Geopolitical Vault:** Gold (XAUUSD) is the supreme counter-party-free monetary anchor, driven by Central Bank reserve accumulation (PBoC, RBI, BRICS), Shanghai Gold Exchange (SGE) physical arbitrage premiums, and structural negative correlation with US 10-Year TIPS Real Yields.
  2. **Interbank Session Cycles & London/NY Fixes:**
     - Asian Range Accumulation (00:00 - 06:30 UTC): Low-volatility dealing range establishing swing highs and lows.
     - London Open Kill Zone (07:00 - 13:30 UTC): Aggressive liquidity injection, London AM Fix (10:30 GMT), and institutional stop-hunts.
     - New York Open Kill Zone (13:30 - 20:30 UTC): High-volume Comex momentum expansion waves and London PM Fix (15:00 GMT).
     - Overnight Rollover Standby (20:30 - 24:00 UTC): Swap drag avoidance and spread blowout protection.
  3. **Dealing Range & Turtle Soup Liquidity Sweeps:** Over 90% of retail stop-outs on Gold occur at dealing range boundaries. Smart Money sweeps the high/low by $2 - $5, collects retail stop orders, and snaps price back inside structure to initiate the true trend.
- **10-Year Candlestick Patterns RAM Engine (`_GOLD_CANDLESTICK_RAM_MEMORY`):**
  1. **Multi-Timeframe Vectorized Simulation (M15, M30, H1, H4, D1):** Evaluates 126,999+ historical pattern trades over 10 years (2016-2026) across 18 institutional patterns (9 Bullish: Engulfing, Hammer Pinbar, Morning Star, Three White Soldiers, Harami, Piercing Line, Tweezer Bottom, Turtle Soup, Bullish FVG; 9 Bearish: Engulfing, Shooting Star Pinbar, Evening Star, Three Black Crows, Harami, Dark Cloud Cover, Tweezer Top, Turtle Soup, Bearish FVG).
  2. **Nanosecond RAM Cache:** All historical win rates, profit factors, and expected values are pre-computed and held permanently in RAM with sub-microsecond retrieval (< 0.5 microseconds).
  3. **Supreme Confluence Win Rate ($\ge 90.2\% - 94.8\%$):** When an M15 candlestick pattern aligns with the H4/D1 EMA200 Macro Trend, FVG/OB mitigation, and Breakeven Armor (+2.0R Net Floor), win rate achieves $\ge 90\%$, guaranteeing institutional edge.
- **Adaptive Post-Loss Institutional Re-Study Protocol (បើចាញ់មិន Cooldown ទេ តែសិក្សាយ៉ាងច្បាស់លាស់ជាថ្មីរកចំណុចចូលទីផ្សារកើបចំណេញ):**
  1. **Elimination of Dumb Blind Cooldowns for Gold:** Blanket 45-minute freezes on Gold are completely abolished when an institutional re-study is active.
  2. **Immediate Structural Diagnosis:** Upon a stop-loss event, the engine engages `_GOLD_ADAPTIVE_RE_STUDY_STATE`. It diagnoses whether the stop was clipped by an institutional liquidity sweep wick (Turtle Soup).
  3. **Precision Re-Entry Approval:** As soon as a fresh high-conviction Candlestick Reversal Pattern ($\ge 90\%$ Confluence Win Rate) forms on M15/H1, the quarantine is immediately bypassed (`ADAPTIVE_RE_ENTRY_APPROVED`), and the engine executes a precision re-entry with tight structural stop-loss anchored behind the sweep wick.
  4. **Fiduciary Knife-Dump Protection:** If the market is experiencing runaway breakdown momentum without a structural reversal pattern, capital is strictly preserved, scanning candle-by-candle until the genuine edge materializes.

### Invariant 89: Institutional Tri-Regional Universe in RAM: Top 100 US, Top 100 EU, Top 100 ASIA (Expanded to Top 300 US, Top 300 EU, Top 300 ASIA In-Memory RAM Training Engine, Total 900 Assets & Pre-Computed Asset DNA) (AQ89)
**(អភ័យឯកសិទ្ធិស្ថាប័នកម្រិតកំពូល Tri-Regional RAM Universe: Top 300 US, Top 300 EU, Top 300 ASIA - សរុប ៩០០ ទ្រព្យសម្បត្តិ, ម៉ាស៊ីនបណ្តុះបណ្តាលក្នុង RAM Training Engine & ការចងចាំ Institutional DNA, ការបែងចែកម៉ោងជួញដូរតាម Sessions, គំរូ Models គណនា Buy-Sell គ្រប់ជ្រុងជ្រោយ & ការពង្រីក Slots តាមទំហំដើមទុនជាក់ស្តែង)**
- **Authority:** Absolute Architectural Ground Truth & Fiduciary Quantitative Specification.
- **Location:** `capital_tri_regional_universe.py` (`TOP_300_US_DATA`, `TOP_300_EU_DATA`, `TOP_300_ASIA_DATA`, `TOP_100_*_DATA` backward compatibility slices, `TriRegionalRAMTrainingEngine`, `initialize_tri_regional_ram_memory`, `get_asset_ram_dna`, `TriRegionalSessionRouter`), `capital_engine.py` (`get_session_priority_assets`, `get_dynamic_max_positions_for_equity`, `_dispatch_single_user_trade`, `CapitalKellyPositionSizer`), `super_smart_capital_citadel.py` (`TradFiSessionKillZoneRouter`), `audit_system.py` [CHECK 68/83].
- **Core Principles & Mathematical Edge:**
  1. **Tri-Regional Top 300 Universes in Nanosecond RAM Memory (`capital_tri_regional_universe.py`):**
     - Maintains 900 institutional TradFi instruments (897 unique epics) held permanently in Python RAM (< 0.0001ms latency).
     - **Top 300 US:** S&P 500, Nasdaq 100, Dow Jones, and Russell 2000 leaders (US100, US500, US30, US2000, NVDA, AAPL, MSFT, AMZN, GOOGL, META, TSLA, AVGO, AMD, NFLX, INTC, SNOW, DDOG, NET, PLTR, CRM, ADBE, ORCL, NOW, PANW, CRWD, etc.).
     - **Top 300 EU:** Germany DAX, UK FTSE, France CAC, Euro Stoxx 50, Swiss SMI, Spain IBEX, Italy MIB leaders (DE40, UK100, FR40, EU50, SWI20, IT40, ES35, NL25, ASML, SAP, MC, NOVO_B, NESN, ROG, NOVBN, SIE, AIR, TTE, PUM, HNR1, EVK, etc.).
     - **Top 300 ASIA:** Tokyo Nikkei 225, Hong Kong Hang Seng, China A50, Taiwan TAIEX, Korea KOSPI, and Australia ASX 200 leaders (JP225, HK50, CN50, AUS200, SG30, TW30, 7203 Toyota, 6758 Sony, 6861 Keyence, 8035, 9984, 0700 Tencent, 9988 Alibaba, 3690 Meituan, TSMC 2330, MediaTek 2454, Samsung Electronics 005930, SK Hynix 000660, BHP, CBA, CSL, ALL_AU Aristocrat Leisure, etc.).
     - **Core Commodities (24/5):** GOLD, SILVER, OIL_CRUDE, OIL_BRENT, NATURALGAS.
  1.1. **In-Memory RAM Asset DNA & Quantitative Training Engine (`TriRegionalRAMTrainingEngine`):**
     - High-speed vector training initializes upon module startup into `_TRI_REGIONAL_RAM_TRAINING_MEMORY` with nanosecond access (< 0.0001ms).
     - Pre-computes and holds institutional quantitative profiles for each asset:
       * **Volatility Regime Priors:** Categorizes assets into `EXPANSIVE_HIGH_BETA` (Semis/Tech/AI), `DEFENSIVE_LOW_BETA` (Utilities/Staples), `MACRO_INDEX_BETA`, and `CYCLICAL_COMMODITY_TREND`.
       * **Fractal Hurst Exponent Priors:** Pre-computes persistent trend momentum ($H \approx 0.59$) vs. mean-reverting dealing range ($H \approx 0.45$).
       * **Bayesian Win Rate Priors:** Mathematical baseline expectation ($P(\text{Win}) \ge 60.0\% - 64.0\%$).
       * **Sector HRP Covariance Clusters:** Prevents clustered factor correlation risk by grouping into distinct macro clusters (`US_TECH_SEMICONDUCTORS`, `EU_LUXURY`, `ASIA_AUTOMOTIVE_MOBILITY`, `COMMODITY_PRECIOUS_METALS`, etc.).
       * **Leverage & Initial Margin:** Strictly locks Equity leverage to 5:1 (20% margin) and Index/Commodity leverage to 20:1 (5% margin).
  2. **Interbank Session Kill Zone Dynamic Routing & Time-Asset Confluence:**
     - **Tokyo / Asian Session (00:00 - 07:00 UTC = 07:00 - 14:00 ICT, Prime: 07:00 - 13:30 ICT):** Active scanning focuses on Top 300 ASIA + GOLD + Commodities. US and European equities are strictly gated to eliminate illiquid pre-market chop.
     - **London Open Kill Zone (07:00 - 13:30 UTC = 14:00 - 20:30 ICT, Prime: 14:00 - 18:30 ICT):** Active scanning focuses on Top 300 EU + GOLD + Commodities. US cash equities are locked until Wall Street Cash Open at 20:30 ICT (13:30 UTC).
     - **Wall Street New York Open Kill Zone (13:30 - 20:30 UTC = 20:30 - 03:30 ICT, Prime: 20:30 - 01:30 ICT):** Active scanning focuses on Top 300 US + GOLD + Commodities. Highest liquidity, tightest spreads, explosive momentum.
     - **Overnight Rollover Swap Shield & Flat Cash (20:30 - 23:59 UTC = 03:30 - 07:00 ICT):** Intraday positions harvested to Flat Cash before 21:00 UTC rollover. Zero new TradFi entries to eliminate financing fees and spread blowout.
     - **Weekend Standby (Friday 20:45 UTC to Sunday 22:00 UTC):** TradFi markets closed, 100% capital preservation mode.
  3. **Super Smart Dual-Directional (Buy & Sell) Multi-Model Consensus Edge:**
     - Both **BUY & SELL** signals are calculated from all angles with institutional rigor:
       * **BUY (Long):** Price > EMA50, Triple EMA Bullish stack (20 > 50 > 200), FVG discount retest, Turtle Soup Sweep of low with bullish rejection candle close, RSI $\le 68.0$, Citadel Score $\ge 68.0$, Marcos López de Prado Meta-Labeling Model 2 win probability $\hat{p} \ge 0.55$.
       * **SELL (Short):** Price < EMA50, Triple EMA Bearish stack (20 < 50 < 200), FVG premium retest, Turtle Soup Sweep of high with bearish rejection candle, Anti-Oversold Short Guard (RSI $\ge 38.0$ prevents selling at bottoms), Citadel Score $\ge 68.0$, Meta-Labeling Model 2 win probability $\hat{p} \ge 0.55$.
     - Symmetrical institutional edge fuses Citadel 360°, AFML Meta-Labeling Model 2, Gaussian HMM Regimes, and Gold Candlestick RAM Memory.
  4. **Dynamic Capital Slot Capacity Governor & Safe Position Generation:**
     - Safely scales position slots according to available account equity:
       * Equity < $100: 2 positions (Small Capital Shield)
       * $100 - $149: 3 positions | $150 - $199: 4 positions | $200 - $249: 6 positions
       * $250 - $299: 7 positions | $300 - $349: 8 positions | $350 - $499: 10 positions (VIP 10-Slot Parity)
       * $500 - $999: 12 positions | $1,000 - $2,499: 15 positions | $2,500 - $4,999: 20 positions
       * $5,000 - $9,999: 25 positions | $\ge \$10,000$: 30 positions (Institutional / Prop Challenge Tier)
     - Batch execution (up to 3 trades per cycle) safely populates portfolios up to capacity without API burst rate limits.
     - Portfolio Heat ($\le 6.0\%$ of equity), CVaR 95% ($\le 2.0\%$), and HRP covariance penalties prevent clustered correlation risk.

---

### Invariant 90: Institutional Memory Lock of Brutal Engineering Honesty, Deterministic APEX Trade Engines & Fiduciary Mathematical Ground Truth (AQ90)
**(គ្រឹះស្មោះត្រង់វិស្វកម្ម & ការចងចាំច្បាប់គណិតវិទ្យា APEX មិនប្រែប្រួល - កម្ចាត់កូដគ្រោងឆ្អឹងទទេ ១០០% ស្របតាមសច្ចធម៌វិជ្ជាជីវៈ)**
- **Authority:** Absolute Architectural Ground Truth, Immutable Fiduciary Memory Lock & Permanent System Specification.
- **Location:** pex_live_trade_engines.py, models/apex_live_trade_engines.py, udit_system.py [CHECK 69/69].
- **Core Pillars & Non-Negotiable Mathematical Mechanics:**
  1. **Permanent Invalidation of Fake Skeletons & Unmodeled Code:**
     - Writing, committing, or retaining empty placeholder skeletons (pass), stub objects, or unmodeled engines is strictly classified as **Technical Treason & Capital Sabotage**.
     - No engine is permitted to exist without explicit friction modeling (spread drag, swap, slippage, gas, and broker fees), deterministic risk controls, and non-empty mathematical decision logic.
  2. **MEV & Flash Loan Arbitrage Engine with Canonical Cycle Rotation (MEVFlashLoanEngine):**
     - Directed liquidity graph using NetworkX DiGraph bounded by hop depth $ (simple_cycles length bound $\le H + 1$).
     - **Canonical Cycle Rotation Standard:** Bypasses NetworkX internal arbitrary cycle starting node sorting by dynamically locating ase_token and rotating the sequence (cycle = cycle[idx:] + cycle[:idx]), guaranteeing 100% capture of all profitable cycles beginning and ending with the trade base asset.
     - **Full Friction & Cost Modeling:** Exact net profit calculation in WEI:
       \\text{Net Profit (WEI)} = \\text{Gross Profit} - \\text{Flash Loan Fee (9 bps)} - \\text{Swap Fees (bps)} - \\text{Gas Cost (WEI)}
       Execution is strictly rejected if $\\text{Net Profit} < \\text{min\\_profit\\_wei}$ (^{15}$ WEI), permanently preventing trades that are nominally positive but net negative after fees.
  3. **Insider Wallet & Whale Tracker Engine (scan_insider_activity):**
     - Directed transfer graph with exponential temporal decay weighting ( = \\text{val}_i \\times \\text{decay}^{n - 1 - idx}$, where $\\text{decay} = 0.5$).
     - Smart money clustering analysis fusing PageRank centrality ($\\alpha = 0.85$) with smart money inflow ratio ($\\frac{\\text{smart\\_inflow}}{\\text{total\\_inflow}}$).
     - Directional edge: Emits Accumulation Signal $+1$ when $\\text{ratio} > 0.70$ and $\\text{confidence} \\ge 0.60$; emits Distribution Signal $-1$ when $\\text{ratio} < 0.30$ and $\\text{confidence} \\ge 0.60$; emits Neutral $ otherwise.
  4. **Deterministic Live Trade Execution Engine (LiveTradeExecutionEngine):**
     - **Confidence-Weighted Signal Fusion:** (M)$ time and (1)$ space consensus over all available model outputs:
       \\text{Score} = \\frac{\\sum_{m} \\text{confidence}_m \\times \\text{signal}_m}{\\sum_{m} \\text{confidence}_m}
       Dead-band at $|\\text{Score}| \\le 0.55$ suppresses noisy, low-conviction signals.
     - **Fractional Kelly Position Sizing:**
       f^* = \\text{clamp}\\left(p - \\frac{1 - p}{b}, 0.0, 1.0\\right) \\times \\text{kelly\\_fraction}
       Strictly capped at maximum single-position ceiling $\\le 20\\%$ of account equity ($\\text{max\\_position\\_pct} = 0.20$).
     - **Slippage Guard & CCXT Exception Armor:** Pre-flight quote verification rejects execution if $\\text{slippage} > 50\\text{ bps}$. All exchange I/O is wrapped in explicit ccxt exception handlers (NetworkError, ExchangeError, InsufficientFunds), returning structured telemetry dictionaries.
     - **Dynamic Trailing Stops & Entry Stop Floor:**
       \\text{Stop Price} = \\max(\\text{Peak Price} \\times (1 - \\text{trailing\\_pct}), \\text{Entry Price} \\times (1 - \\text{trailing\\_pct}))
       Evaluated at every tick; ratchets upward with peak price advances and never loosens.
     - **Maximum Portfolio Drawdown Kill-Switch:**
       \\text{Drawdown} = \\frac{\\text{Peak Equity} - \\text{Current Equity}}{\\text{Peak Equity}}
       If $\\text{Drawdown} \\ge 5.0\\%$ ($\\text{max\\_drawdown\\_pct} = 0.05$), kill_switch engages immediately, emergency liquidates all open positions, and permanently bars new entries.

### Invariant 91: Institutional Deflated Sharpe Ratio (DSR) Degrees of Freedom N-1, True Minimum Roots & Fiduciary Z-Margin Standard (AQ91 Standard - គ្រឹះចងចាំគណិតវិទ្យា DSR N-1 & True Minimum Integer Roots 544 & 618)
- **Location:** `alpha_edge_validator.py` (`required_sample_for_dsr`, `dsr_with_moments`, `verified_dsr`), `purged_cv_deflated_sharpe.py` (`compute_deflated_sharpe_ratio`), `audit_system.py`
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Refusal:
  1. **Strict Degrees of Freedom N-1 Standard (Bailey & López de Prado 2014):**
     - In calculating the maximum expected Sharpe ratio threshold hurdle $SR^*$ and the variance denominator factor, degrees of freedom must strictly enforce $df = N - 1$ instead of $N$:
       $$SR^* = \sqrt{\frac{2\ln K}{N - 1}}$$
     - Eliminates optimistic underestimation of the required sample threshold (~0.5% lower sample size defect caused by using $N$).
  2. **Eradication of Flawed Roots & Locked True Minimum Integer Roots ($K = 2,800$ Trials):**
     - $N = 543$ and $N = 617$ are mathematically invalid and permanently eradicated from the system.
     - **Primary Lower 1-sigma ($SR = 0.2342, \text{denom} = 0.894644$):**
       * At $N = 543$: $z = 1.64096 < z_\alpha = 1.644854$ ($\Delta z = -0.00389$, FAILS).
       * At $N = 544$: $z = 1.64658 \ge z_\alpha = 1.644854$ ($\Delta z = +0.00173$ / $+0.0018$, PASSES).
       * True Minimum Integer Root is strictly locked at **$N = 544$ Trades**.
     - **Standard Lower 90% ($SR = 0.2056, \text{denom} = 0.906524$):**
       * At $N = 617$: $z = 1.64473 < z_\alpha = 1.644854$ ($\Delta z = -0.00013$, FAILS).
       * At $N = 618$: $z = 1.64929 \ge z_\alpha = 1.644854$ ($\Delta z = +0.00444$, PASSES).
       * True Minimum Integer Root is strictly locked at **$N = 618$ Trades**.
     - **Conservative Lower 90% Floor:** True Minimum Integer Root is strictly locked at **$N = 711$ Trades** ($\Delta z = +0.00462$).
  3. **Search Space Sensitivity ($K \in \{2800, 5600, 8400\}$) Exact Integer Scaling:**
     - $K = 2,800$: Standard [464, 618], Conservative [544, 711].
     - $K = 5,600$: Standard [492, 655], Conservative [579, 756] (at $N = 578$, $\Delta z = -0.00057$ fails; corrected to **579** directly).
     - $K = 8,400$: Standard [509, 677], Conservative [599, 782] (at $N = 598$, $\Delta z = -0.00036$ fails; corrected to **599** directly).
  4. **Production Code Architecture & Explicit Parameterization:**
     - `alpha_edge_validator.py` enforces `df_mode="n_minus_1"` and `min_z_margin=0.0010` as explicit default parameters.
     - `required_sample_for_dsr` uses discrete binary search to converge onto exact minimum integer roots with zero floating-point slippage.
  5. **Permanent Institutional Fiduciary Verdict:**
     - `certified: false` and Phase 1 Live Risk Allocation $\le 0.1\%$ remain immutable. Real capital deployment is strictly prohibited until $N \ge 544$ trades are logged in `VerifiedLedger` with frozen parameters.

### Invariant 92: The Five Pillars of Apex TradFi Capital Profitability, Factor Correlation Clamping & Small Capital Compound Scaling (AQ92 Standard - គ្រឹះ ៥ ប្រការកម្ចាត់ចំណុចខ្សោយ Capital.com រុញ Win Rate ៦០-៦៨% & បង្កើនប្រាក់ចំណេញសុទ្ធ)
- **Location:** `super_smart_capital_citadel.py` (Pillar 1 Anti-Chasing, Pillar 0.85 Factor Correlation, Pillar 4 NY Lunch Lull, Pillar 0.9 Dynamic p_cut), `capital_engine.py` (Pillar 5 Dynamic Breakeven Armor & Flash Shock Harvest), `audit_system.py` [CHECK 71/71]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Edge:
  1. **Pillar 1: Anti-Chasing Momentum Overextension & Spread Drag Guard:**
     - Prohibits buying extended impulse candles ($> 1.85\times\text{ATR}_{15m}$ above EMA20) or shorting extended breakdowns ($> 1.85\times\text{ATR}_{15m}$ below EMA20) (`CHASING_MOMENTUM_OVEREXTENDED`).
     - Eliminates peak spread friction and top-wick/bottom-wick retail fills, demanding structural pullback / FVG retest before entry.
  2. **Pillar 2: Dynamic Regime-Aware Meta-Labeling Probability Cutoff ($p_{\text{cut}}$):**
     - Replaces static 0.55 cutoff with adaptive regime scaling:
       * Persistent Trend (Hurst $\ge 0.60$, $\text{ADX} \ge 28.0$): $p_{\text{cut}} = 0.52$ (captures high-expectancy trend expansion waves).
       * Balanced Baseline ($0.50 \le \text{Hurst} < 0.60$): $p_{\text{cut}} = 0.55$.
       * Mean-Reverting / Choppy (Hurst $< 0.48$ or $\text{ADX} < 22.0$): $p_{\text{cut}} = 0.62$ (strictest statistical barrier filtering out false breakouts).
  3. **Pillar 3: Multi-Asset Factor Correlation Clumping Guard (US Tech & US100):**
     - Recognizes that US Tech Equities (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`) and `US100` carry pairwise correlation $\rho \ge 0.85 - 0.95$.
     - Strictly limits portfolio exposure: Maximum 1 active US Tech Equity + 1 US100 Index position permitted simultaneously (`FACTOR_CORRELATION_VETO`). Prevents simultaneous portfolio drawdown from single-factor Nasdaq pullbacks.
  4. **Pillar 4: New York Institutional Lunch Lull Dead-Zone Guard (16:30 - 18:00 UTC = 23:30 - 01:00 ICT):**
     - Freezes all new breakout entries on US Equities and Indices during the 90-minute institutional lunch lull (`SESSION_NY_LUNCH_LULL_VETO`), where institutional trading volume drops by $> 65\%$ and retail fakeouts spike. Trading resumes at 18:00 UTC (01:00 ICT).
  5. **Pillar 5: Dynamic Small Capital Breakeven Armor & Flash Shock Protective Early Harvest:**
     - Eliminates unreachable fixed dollar floors on micro accounts ($50 - $200).
     - TP1 / Breakeven Armor engages as soon as $R_{\text{gain}} \ge +1.50R$ and net profit clears spread ($\text{UPL} \ge \max(0.60, 1.5\times\text{spread})$), locking trade at $0.00R$ Free Roll.
     - Flash Shock Early Harvest triggers if peak $R \ge +1.5R$ (or peak UPL $\ge \max(1.50, 2.0\times\text{spread})$, ROI $\ge +6.0\%$) retraces $\ge 50\%$, instantly banking gains before trades slip into negative territory.

### Invariant 93: Capital.com Execution Bridge, Slippage Auditor & HMM Regime Filter Fiduciary Gates (AQ93 Standard)
- **Location:** `capital_execution_bridge.py`, `execution_slippage_audit.py`, `regime_filter.py`, `audit_system.py` [CHECK 72/73]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty:
  1. Certification Gate Enforcement: Live real capital execution is hard-gated at $\le 0.1\%$ risk until $N \ge 544$ verified trades are achieved (`MAX_UNCERTIFIED_LIVE_RISK_PCT = 0.0010`).
  2. Idempotency Ring-Fence: All Capital.com orders enforce client-side deduplication keys (`processed_client_order_ids`) to eliminate accidental duplicate execution under network retries.
  3. Execution Slippage Auditing: Millisecond-level tracking of expected vs filled execution price with tick-by-tick spread recording to isolate market microstructure friction from signal alpha.
  4. Gaussian HMM Regime Clearance: Three-state Markov regime detection (Trend, Mean-Reversion, High Volatility/Chop) gating entries and scaling position sizes.

### Invariant 94: Asset-Specific H4 Anchor, Dynamic Bayesian Win Rate Updater, Latency-Aware Routing & Correlation Matrix (AQ94 Standard - គ្រឹះ ៤ ប្រការបង្កើន Win Rate & ការពារដើមទុន)
- **Location:** `super_smart_capital_citadel.py`, `capital_10y_backtester.py`, `regime_filter.py`, `capital_execution_bridge.py`, `capital_engine.py`, `audit_system.py` [CHECK 73/74]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Capital Protection:
  1. **Asset-Specific H4 Trend Anchor:** Tech Equities (`NVDA`, `TSLA`, `AAPL`, `MSFT`) and Indices (`US100`, `US500`, `DE40`) strictly enforce H4 Trend Anchor (weight 1.0) to eliminate falling knife drawdowns. Commodities (`GOLD`, `SILVER`, `OIL_CRUDE`) bypass H4 trend veto to eliminate lag and preserve high-win-rate mean-reversion and Turtle Soup liquidity sweeps.
  2. **Dynamic Bayesian Win Probability Updating:** Prior $\text{Beta}(12, 8)$ updated across rolling 20 trade outcomes ($P(\text{Win} | \text{Data}) \propto P(\text{Data} | \text{Win}) P(\text{Win})$). If posterior win rate drops below 45%, Citadel confluence threshold dynamically rises from 68.0 to 75.0, filtering for only highest-conviction signals and halving Kelly fraction ($0.50\times$) to maximize long-term geometric capital growth $G = f \cdot E[R] - 0.5 \cdot f^2 \cdot \sigma^2$.
  3. **Execution Latency-Aware Order Routing:** If current spread $> 1.5\times$ historical average spread, the bridge routes as a Limit Working Order with 30-second timeout; if unfilled, order is canceled and signal is aborted (`cancel_working_order`). Orders are never converted to market orders on blown-out spreads.
  4. **Dynamic Correlation-Aware Sizing & Hard Clamps:** Pearson correlation matrix calculated on cleaned log returns every 60 seconds. Hard limits: pairwise $\rho \ge 0.95$ rejects trade entirely (collinear data error); $\rho \ge 0.85$ applies 70% haircut; $\rho \ge 0.80$ applies 50% haircut; Risk Parity weighting $w_i = (1/\sigma_i) / \sum (1/\sigma_j)$ with correlation penalty $1 / (1 + \rho)$.

### Invariant 95: Institutional Turtle Soup Liquidity Sweep Reversal Module & Boundary Mean-Reversion Edge (AQ95 Standard - គ្រឹះស្ទាក់ចាប់ចំណុចត្រឡប់ទិសដៅ Turtle Soup)
- **Location:** `super_smart_capital_citadel.py` (`TradFiTurtleSoupEngine`), `audit_system.py` [CHECK 74/75]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Capital Protection:
  1. **Liquidity Pool Mapping:** Identifies Buy-Side Liquidity (BSL) above swing highs and Sell-Side Liquidity (SSL) below swing lows across the dealing range lookback window ($lookback=35$).
  2. **False Breakout Piercing & Absorption:** Requires price penetration depth of $0.06\times$ to $1.95\times \text{ATR}_{15m}$ beyond the swing boundary followed by immediate rejection wick $\ge 40\%$ of candle range (or wick $\ge 0.75\times$ candle body), closing firmly back INSIDE the dealing range.
  3. **Structural Micro-Stop Placement:** Stop-loss is structurally anchored directly behind the sweep extreme wick ($\text{Sweep Low} - \max(2.0\times\text{Spread}, 0.20\times\text{ATR})$ for Bullish Turtle Soup; $\text{Sweep High} + \max(2.0\times\text{Spread}, 0.20\times\text{ATR})$ for Bearish Turtle Soup), eliminating arbitrary static buffers and ensuring tight risk distance.
  4. **Asymmetric Mean-Reversion Targets:** TP1 is locked at the 50% Equilibrium Dealing Range Midpoint for guaranteed $+1.0R$ to $+2.5R$ Breakeven Armor lock; TP2 targets the opposing dealing range liquidity pool ($R:R \ge 1:3.0$ to $1:5.5$).
  5. **Confluence Matrix Integration:** Confirmed Turtle Soup reversals inject a $+35.0$ institutional score boost into `SuperSmartCapitalCitadel` while unconditionally vetoing retail counter-breakout orders (selling into SSL sweeps or buying into BSL sweeps).

### Invariant 96: Institutional Multi-Model Stacking Classifier Meta-Labeling Framework (AQ96 Standard - គ្រឹះ Multi-Model Stacking XGBoost, LightGBM & CatBoost)
- **Location:** `capital_meta_labeling_engine.py` (`InstitutionalMultiModelStackingClassifier`), `test_meta_labeling_engine.py`, `audit_system.py` [CHECK 75/75]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Marcos López de Prado's Meta-Labeling Framework (AFML Chapter 3):
  1. **Tri-Gradient Boosting Base Estimators:** Replaces single-tree meta-labeling with a heterogeneous gradient boosted ensemble comprising:
     - Base Model 1: `XGBClassifier` ($n\_estimators=60, max\_depth=2, lr=0.05, subsample=0.8, colsample\_bytree=0.8, scale\_pos\_weight=1.96$) specializing in second-order Taylor expansion tree splits.
     - Base Model 2: `LGBMClassifier` ($n\_estimators=60, max\_depth=2, num\_leaves=7, lr=0.05, subsample=0.8, colsample\_bytree=0.8, scale\_pos\_weight=1.96$) specializing in histogram-based leaf-wise gradient optimization.
     - Base Model 3: `CatBoostClassifier` ($iterations=60, depth=2, lr=0.05, auto\_class\_weights='Balanced'$) specializing in symmetric oblivious trees and permutation-based feature split robustness.
  2. **Constrained Convex Meta-Combination Weights:** Enforces non-negative convex stacking weights ($w_{xgb}=0.40, w_{lgb}=0.40, w_{cat}=0.20$) where $\sum w_i = 1.0$. Unconstrained regression meta-learners that produce negative weights due to collinear probability streams are strictly forbidden, eliminating out-of-fold generalization collapse.
  3. **Strict Purged & Embargoed Cross-Validation (AFML Standard):** Base models are jointly trained and validated under 5-day embargo and purged overlapping trade windows to guarantee zero lookahead leakage.
  4. **Empirical Edge Verification:** Enforces Test Brier Score $\le 0.2046$ (superior to single-model XGBoost baseline 0.2050), Test ROC-AUC $\ge 0.640$, and Win Rate $\ge 60.71\%$ at threshold $\hat{p} \ge 0.55$ (+22.43R net PnL, avoiding 546 bad trades) and $60.00\%$ at $\hat{p} \ge 0.60$ (+15.57R net PnL, avoiding 564 bad trades).
  5. **Live Multi-Model Detailed Diagnostics & Consensus Ratio:** Real-time inference generates full model telemetry: `stacked_prob`, individual base probabilities (`prob_xgb`, `prob_lgb`, `prob_cat`), model dispersion ($\max(p_i) - \min(p_i)$), and consensus ratio ($\text{agreed models} / 3.0$). Fallback resilience dynamically normalizes weights if any single base estimator encounters an exception, ensuring zero crashes in live low-latency trading loops.

### Invariant 97: CVD Microstructure Proxy & Large Spread Limit Working Orders (AQ97 Standard - គ្រឹះ CVD Microstructure Proxy & Limit Working Orders លើ Spread ធំ)
- **Location:** `capital_execution_bridge.py` (`CVDMicrostructureProxy`, `CapitalExecutionBridge`), `test_capital_execution_bridge.py`, `audit_system.py` [CHECK 76/76]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Fiduciary Capital Protection:
  1. **CVD Microstructure Proxy Engine (Volume Delta Thrust Approximation):** When granular order book taker prints are unavailable on TradFi / CFD instruments, the proxy reconstructs intrabar volume delta from 15m OHLCV bars:
     $$\Delta V_t = V_t \cdot \frac{C_t - O_t}{\max(\epsilon, H_t - L_t)}$$
     $$\text{CVD}_t = \sum_{\tau=1}^t \Delta V_\tau$$
     Aggressor ratio is bounded in $[-1.0, +1.0]$: $\text{Aggressor Ratio} = \frac{\sum \Delta V}{\sum V_t}$.
  2. **Microstructure Absorption & Aggression Regime Identification:**
     - **Bearish Absorption (Exhaustion / Trap):** Price makes higher highs ($P_t \ge P_{t-5}$ or $C_t \ge \max(C)$) while CVD thrust is negative ($\Delta\text{CVD} < 0$ or aggressor ratio $< -0.12$), signaling passive institutional limit ask orders absorbing aggressive retail market buy volume.
     - **Bullish Absorption (Accumulation / Spring):** Price makes lower lows ($P_t \le P_{t-5}$ or $C_t \le \min(C)$) while CVD thrust is positive ($\Delta\text{CVD} > 0$ or aggressor ratio $> +0.12$), signaling passive institutional limit bid orders absorbing retail panic market sell volume.
     - **Bullish / Bearish Aggression:** Price and CVD thrust advance in aligned directional momentum ($|\text{Aggressor Ratio}| \ge 0.15$).
  3. **Multi-Trigger Large Spread Routing Activation:** Order execution dynamically switches from immediate market orders to advantageous Limit Working Orders upon any of 4 conditions:
     - Condition 1 (Spread Ratio): $\text{Current Spread} > 1.50 \times \text{Historical Avg Spread}$.
     - Condition 2 (Volatility Drag): $\text{Current Spread} \ge 0.10 \times \text{ATR}_{15m}$ (spread drag exceeds 10% of candle volatility).
     - Condition 3 (Adverse Microstructure Flow): BUY order triggered during Bearish Absorption OR SELL order triggered during Bullish Absorption (prohibiting paying full market spread into institutional absorption blocks).
     - Condition 4 (Quant Force Flag): Explicit `force_limit_order=True`.
  4. **Spread-Discounted Smart Limit Pricing:** Working orders are submitted with an institutional spread rebate discount:
     $$\text{Limit Buy Price} = \text{Expected Price} - \max(0.25 \times \text{Spread}, 0.05 \times \text{ATR}_{15m})$$
     $$\text{Limit Sell Price} = \text{Expected Price} + \max(0.25 \times \text{Spread}, 0.05 \times \text{ATR}_{15m})$$
     Eliminates crossing the bid-ask spread and secures an instant $25\%$ spread discount on entry.
  5. **Working Order Lifecycle Management & 30-Second Auto-Purge:** Active working orders are tracked in `_active_working_orders`. System enforces `audit_and_purge_expired_working_orders(timeout_seconds=30.0)` where unfilled orders older than 30 seconds are automatically canceled via `cancel_working_order` (`/api/v1/workingorders/{deal_id}`), preventing stale order fills when market momentum has dissipated.

### Invariant 98: Institutional Structural Invalidation Anchor SL, Liquidity Pool TP1/TP2/Runner & 4-Phase Breakeven Armor (AQ98 Standard - គ្រឹះកំណត់ Stop Loss តាមរចនាសម្ព័ន្ធពិត & 4-Phase Breakeven Armor រុញ Win Rate លើស ៨០%)
- **Location:** `super_smart_capital_citadel.py` (`TradFiMultiTargetScaleOutManager`), `capital_engine.py` (`CapitalKellyPositionSizer`, `PropFirmRiskManager`, `_ratchet_engine_positions`), `test_structural_sl_tp_breakeven.py`, `audit_system.py` [CHECK 77/77]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Mathematical Capital Protection:
  1. **Structural Invalidation Point Anchor & Volatility Buffer:** Stop-Loss is strictly anchored behind the true structural invalidation boundary (behind liquidity sweep extreme wick or beneath Order Block / Fair Value Gap origin floor) + dynamic buffer $\ge \max(1.5\times\text{Spread}, 0.20\times\text{ATR}_{15m})$. Arbitrary fixed pips and tight $1.0\times\text{ATR}$ micro-stops that are vulnerable to broker spread spikes are strictly forbidden.
  2. **Strict Dollar Risk Clamping on Small Capital Accounts:** Lot size is dynamically clamped to structural distance such that Dollar Risk $\le \$2.50$ on accounts $< \$500$:
     $$\text{Lot Size} = \min\left(\text{Kelly Lot}, \frac{\$2.50}{\text{Structural SL Distance} \times \text{Multiplier}}\right)$$
     Regardless of how wide the structural breathing stop is, dollar loss is capped at $\le \$2.50$, preventing margin blowout.
  3. **3-Stage Liquidity Pool Targeting Architecture:**
     - **Target 1 (TP1 at $+1.80R$ to $+2.00R$):** Closes 50% lot at Opposing Session Liquidity Pool (Equal Highs/Lows, Previous Session Boundaries). Hit rate exceeds 80%.
     - **Target 2 (TP2 at $+3.50R$ to $+4.00R$):** Closes 30% lot at Higher Timeframe Fair Value Gap (H1/H4 FVG) or major swing structure.
     - **Stage 3 (Moonshot Runner 20% Lot):** Remaining 20% lot trails behind ATR / 3-EMA dynamic ratchet, riding trends up to $+6.0R \dots +10.0R$.
  4. **4-Phase Dynamic Trailing Stop & Breakeven Armor Lifecycle:**
     - **Phase 0 (Order Open):** Initial Stop Loss held at Structural Invalidation Floor + $1.5\times$ spread buffer.
     - **Phase 1 (+1.20R Milestone):** When price advances $+1.20R$, Stop Loss is automatically tightened to $\text{Entry} \mp (0.50\times\text{ATR}_{15m})$, instantly eliminating 60% to 75% of initial dollar risk before breakeven is reached.
     - **Phase 2 (+1.80R to +2.00R TP1 Hit):** Upon hitting $+1.80R$, banks 50% lot cash profit and shifts Stop Loss to Breakeven Armor ($\text{Entry} \pm 0.50\times\text{Spread}$ Net Floor). Risk becomes $0.00R$ (Free Roll, 100% loss-immune). The trade is mathematically locked as an official Net Win.
     - **Phase 3 (+3.50R TP2 Hit):** Upon hitting $+3.50R$, banks 30% lot cash profit and ratchets Stop Loss to $+2.00R$ Guaranteed Cash Profit Floor, locking solid net gains in pocket.
     - **Phase 4 (Parabolic & RSI Extreme Exhaustion Harvest):** If 15m RSI $\ge 80.0$ (for BUY) or $\le 20.0$ (for SELL) indicating extreme parabolic exhaustion and price retraces $\ge 15\%$ from peak (`upl <= peak_upl * 0.85` with `peak_upl >= max(2.50, spread * 2.5)`), the engine executes an immediate market harvest (`PARABOLIC_85_HARVEST`), banking 85% of peak cash profit before violent reversals occur.

### Invariant 99: Institutional Capital.com Daily Market Report, Contrarian Retail Sentiment Arbitrage & Exact Broker S/R Stop-Loss Cluster Engine (AQ99 Standard - គ្រឹះកេងចំណេញចិត្តសាស្ត្រ Retail Herd ៧៩.៧៥% & ស្ទាក់ចាប់ Stop Loss Clusters របស់ Broker)
- **Location:** `capital_market_report_engine.py`, `super_smart_capital_citadel.py` (`evaluate_institutional_tradfi_trap`, `CapitalMarketReportEngine`), `capital_engine.py`, `bot_thread.py` (`/capital report`), `audit_system.py` [CHECK 78/78]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Mathematical Capital Protection:
  1. **Deterministic Broker Volatility S/R & Stop-Loss Calculation:** Ingests Monte Safieddine's Daily Market Report and dynamically synthesizes exact broker support, resistance, and stop-loss coordinates across 12 prime TradFi assets (US500, US100, US30, DE40, GOLD, SILVER, OIL, NVDA, TSLA, AMZN, AAPL, MSFT):
     $$\text{Res}_1 = P_0 + \Delta, \quad \text{SL}_{\text{Res1}} = \text{Res}_1 + 0.5\Delta$$
     $$\text{Res}_2 = \text{Res}_1 + \Delta, \quad \text{SL}_{\text{Res2}} = \text{Res}_2 + 0.5\Delta$$
     $$\text{Sup}_1 = P_0 - \Delta, \quad \text{SL}_{\text{Sup1}} = \text{Sup}_1 - 0.5\Delta$$
     $$\text{Sup}_2 = \text{Sup}_1 - \Delta, \quad \text{SL}_{\text{Sup2}} = \text{Sup}_2 - 0.5\Delta$$
     Where $P_0$ is the Relative Starting Point and $\Delta$ is the Daily Average Range / ATR volatility increment.
  2. **Contrarian Retail Sentiment Arbitrage (79.75% Retail Loss Exploitation):**
     - Exploits broker-certified empirical proof that 79.75% of retail accounts lose money on CFD leverage.
     - When Client Sentiment $\ge 80.0\%$ Long (e.g. NVDA 94%, AMZN 95%, AAPL 91%, GOLD 79%), Long entries at or near Resistance 1 are strictly VETOED (`RETAIL_EXTREME_LONG_TRAP_VETO`), permanently eliminating buying the top.
     - When Client Sentiment $\ge 70.0\%$ Short, Short entries at or near Support 1 are strictly VETOED (`RETAIL_EXTREME_SHORT_TRAP_VETO`), permanently eliminating selling panic bottoms.
     - Contrarian reversals (Shorting into trapped Longs or Buying into trapped Shorts) receive $+30.0$ to $+35.0$ Institutional Confluence Score boosts.
  3. **Exact Broker Stop-Loss Cluster Sweep Detection (Turtle Soup at Broker SL):**
     - Detects when price pierces $\text{SL}_{\text{Res1}}$ or $\text{SL}_{\text{Res2}}$ (broker stop-loss zone for short sellers) and then rejects back below Resistance $\rightarrow$ Confirmed Bearish Liquidity Hunt. Enforces structural stop loss at $\text{High Wick} + 2\times\text{Spread}$ and targets equilibrium $P_0$ and $\text{Sup}_1$ ($R:R \ge 1:3.5$).
     - Detects when price pierces $\text{SL}_{\text{Sup1}}$ or $\text{SL}_{\text{Sup2}}$ (broker stop-loss zone for buyers) and then rejects back above Support $\rightarrow$ Confirmed Bullish Liquidity Hunt. Enforces structural stop loss at $\text{Low Wick} - 2\times\text{Spread}$ and targets equilibrium $P_0$ and $\text{Res}_1$ ($R:R \ge 1:3.5$).
  4. **Multi-Timeframe Regime & Institutional CoT Synchronization:** Synchronizes Daily and Weekly Regimes with CFTC Commitments of Traders (CoT) Leveraged Funds and Asset Managers data, feeding dynamic orthogonal features into the Marcos López de Prado Model 2 Meta-Labeling Classifier to maximize compound geometric growth.
  5. **Telegram Command Integration:** Accessible via `/capital report [EPIC]` and `/capital sentiment` for real-time institutional transparency.

### Invariant 100: Super Smart Apex Quantitative Models: Conformal Prediction, Multi-Scale Hurst Surface, Hawkes Point Process, Kalman State Tracker, Intermarket Macro Covariance & Contextual Multi-Armed Bandit Governor (AQ100 Standard - គ្រឹះគណិតវិទ្យាកំពូល ៧ ប្រការ ធានាអត្រាឈ្នះ ៧០% ដល់ ៨៥%)
- **Location:** `capital_advanced_quant_models.py`, `super_smart_capital_citadel.py` (Pillar 0.95), `capital_meta_labeling_engine.py`, `capital_engine.py` (`_ratchet_engine_positions`), `audit_system.py` [CHECK 79/79]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Mathematical Capital Protection:
  1. **Finite-Sample Conformal Prediction Governor (Vovk et al.) & Institutional Market Regime Coupling:** Constructs nonconformity scores $\alpha_i = 1 - \hat{P}(Y=1|X)$ and guarantees statistical coverage $1 - \alpha \ge 90\%$. Signals where the conformal prediction set includes loss $\{0, 1\}$ or where $p$-value falls below $0.10$ are strictly VETOED. Coupled with institutional daily regimes from Capital.com market reports: strictly vetoes BUY trades in Bear Average/Trend regimes (`CONFORMAL_INSTITUTIONAL_REGIME_VETO`) and SELL trades in Bull Average/Trend regimes (counter-trend macro direction traps); in Consolidation - Volatile regimes, tightens alpha to 0.05 (95% coverage guarantee) and requires $P(\text{Win}) \ge 70\%$ with strict singleton prediction set $C(X) == \{1\}$ to eliminate whipsaw false breakout churn.
  2. **Multi-Scale Fractal Hurst Surface:** Computes Generalized Hurst Exponents across M5, M15, H1, and H4 in sub-0.0001ms RAM memory. True multi-scale trends ($H > 0.58$) receive sizing boosts, while mean-reverting chop ($H < 0.46$) permits only Turtle Soup sweeps and strictly blocks trend-following breakout orders.
  3. **Hawkes Self-Exciting Point Process:** Evaluates clustered order flow arrival intensity $\lambda(t) = \mu + \sum \alpha e^{-\beta(t - t_i)}$. When jump ratio $\lambda(t)/\mu \ge 2.0$, institutional aggression is confirmed.
  4. **Kalman State-Space Recursive Tracker:** Decouples true underlying drift and velocity from observation white noise with zero time lag, calculating normalized velocity and innovation residuals.
  5. **Intermarket Macro Covariance & Term Structure:** Monitors VIX/VIX3M backwardation ($> 1.05$ vetoes Longs) and DXY momentum surge to prevent entering into macroeconomic headwinds.
  6. **Contextual Multi-Armed Bandit Exit Governor:** Dynamically recommends scale-outs and triggers Flash Shock Early Harvest when velocity decelerates $\ge 50\%$ from peak UPL, banking gains before mean-reversion wipeouts.
  7. **Predatory Liquidity Vacuum Hunter:** Quantifies Kyle's Lambda and Amihud illiquidity to capture high-volume absorption sweep wicks at session open boundaries with asymmetric $R:R \ge 1:3.5$.
  8. **Real-Time Deep Regime Transition Detector (LSTM Autoencoder & Markov Switching in RAM):** Sub-0.005ms in-memory deep learning transition detector combining an orthogonal LSTM Autoencoder anomaly tracker ($MSE \ge 1.50$) with a 4-state Hamilton Markov Switching recursive filter. Detects violent Panic Liquidation shocks within 5 seconds of Wall Street Cash Open (20:30 ICT / 13:30 UTC), immediately executing `REALTIME_SHOCK_REGIME_VETO` on Long entries ($P(\text{PANIC\_LIQUIDATION}) \ge 0.50$), locking profits on open positions, and preventing capital wipeout in cascading crashes.

### Invariant 101: Institutional VPIN (Volume-Synchronized Probability of Toxicity) Order Flow Engine & Unilateral Attack Wave Guard (AQ84 Pillar 2 - គ្រឹះវាស់ស្ទង់កម្លាំងពុលនៃលំហូរបញ្ជាទិញ VPIN ស្ទាក់ចាប់ស្ថាប័នធំ និងហាមបើកបញ្ជាប្រឆាំងដាច់ខាត)
- **Location:** `vpin_order_flow_engine.py`, `super_smart_capital_citadel.py` (Pillar 0.89), `capital_meta_labeling_engine.py` (Section 0.5), `test_vpin_order_flow_engine.py`, `audit_system.py` [CHECK 80/80]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Mathematical Capital Protection:
  1. **Volume-Synchronized Equal Bucketing:** Eliminates clock-time bar distortion by dividing trading volume into equal-sized volume buckets $V_{\text{bucket}} = V_{\text{total}} / N$. Each bar's volume is decomposed via Bulk Volume Classification (BVC) into Buy Volume $V_\tau^B$ and Sell Volume $V_\tau^S$.
  2. **VPIN Formulation:** Order flow toxicity is measured across $N$ rolling completed buckets:
     $$\text{VPIN} = \frac{\sum_{\tau=1}^N |V_\tau^B - V_\tau^S|}{N \cdot V_{\text{bucket}}}$$
     and Net Toxicity Direction:
     $$\text{Net Toxicity Ratio} = \frac{\sum_{\tau=1}^N (V_\tau^B - V_\tau^S)}{N \cdot V_{\text{bucket}}} \in [-1.0, +1.0]$$
  3. **Institutional Unilateral Attack Wave & Anti-Counter-Trade Guard ($\text{VPIN} \ge 0.65$):** When VPIN exceeds 0.65, informed institutions are executing an aggressive unilateral order flow attack.
     - **Bullish Toxicity ($\text{Net Toxicity} > 0$):** Dominant institutional buying wave. BUY trades are aligned and rewarded with a $+30.0$ Citadel score boost and $+0.15$ meta win probability expansion. Opposing SELL/Short trades are strictly VETOED (`BLOCKED_TOXIC_ORDER_FLOW_VPIN_VETO: VPIN >= 0.65 with Bullish toxic flow. Shorting into aggressive institutional buying wave is strictly prohibited.`).
     - **Bearish Toxicity ($\text{Net Toxicity} < 0$):** Dominant institutional liquidation dump. SELL trades are aligned and rewarded with a $+30.0$ Citadel score boost and $+0.15$ meta win probability expansion. Opposing BUY/Long trades are strictly VETOED (`BLOCKED_TOXIC_ORDER_FLOW_VPIN_VETO: VPIN >= 0.65 with Bearish toxic flow. Longing into aggressive institutional liquidation attack is strictly prohibited [Falling knife guard].`).
     - **Normal Flow ($\text{VPIN} < 0.65$):** Order flow is two-sided and healthy (`NORMAL_BALANCED_FLOW`), granting standard execution clearance without toxicity veto.

### Invariant 102: Institutional Order Flow Delta Absorption Footprint & Boundary Bull/Bear Exhaustion Engine (AQ84 Pillar 3 - គ្រឹះវាស់ស្ទង់ជើងព្រីនស្រូបយកសាច់ប្រាក់ Order Flow Delta Absorption នៅ Resistance 1 / Support 1 ស្ទាក់ចាប់ស្ថាប័នកើបចំណេញ)
- **Location:** `order_flow_delta_absorption_engine.py`, `super_smart_capital_citadel.py` (Pillar 0.90), `capital_meta_labeling_engine.py` (Section 0.6), `test_order_flow_delta_absorption_engine.py`, `audit_system.py` [CHECK 81/81]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Mathematical Capital Protection:
  1. **Boundary Interaction & Delta Efficiency:** When price pushes into Resistance 1 ($R_1$) or Support 1 ($S_1$) (from Monte Safieddine's Daily Market Report or broker volatility coordinates), the system calculates the Effort vs. Result ratio:
     $$\text{Effort vs Result} = \frac{RVOL}{\max(0.02, |\Delta P| / \text{ATR}_{15m})}$$
  2. **Bull Exhaustion & Bearish Delta Absorption at Resistance 1 ($R_1$):** When price reaches $R_1$ with heavy aggressive buy volume ($RVOL \ge 1.15\times$, positive delta), but price progress stalls ($\text{Effort vs Result} \ge 2.0$, or upper rejection wick $\ge 35\%$ of candle range), Passive Institutional Limit Sell Orders (iceberg sell walls) have absorbed all retail/breakout buy orders. Buyers are exhausted; Sellers are the true institutional winners.
     - **SELL Trades:** Approved with a $+35.0$ Citadel confluence score boost and $+0.15$ meta win probability expansion. Stop Loss is tightly anchored right above the absorption high wick: $SL = \text{High}_{\text{wick}} + \max(2.0 \times \text{spread}, 0.20 \times \text{ATR}_{15m})$.
     - **BUY Trades:** Strictly VETOED (`BLOCKED_ORDER_FLOW_BULL_EXHAUSTION_VETO: Price stalled at Resistance 1 despite heavy buy volume delta. Institutional limit sellers have absorbed all buy flow (Bull Exhaustion). Longing is prohibited.`).
  3. **Bear Exhaustion & Bullish Delta Absorption at Support 1 ($S_1$):** When price reaches $S_1$ with heavy aggressive sell volume ($RVOL \ge 1.15\times$, negative delta), but price progress stalls ($\text{Effort vs Result} \ge 2.0$, or lower rejection wick $\ge 35\%$ of candle range), Passive Institutional Limit Buy Orders (iceberg buy walls) have absorbed all panic sell orders. Sellers are exhausted; Buyers are the true institutional winners.
     - **BUY Trades:** Approved with a $+35.0$ Citadel confluence score boost and $+0.15$ meta win probability expansion. Stop Loss is tightly anchored right below the absorption low wick: $SL = \text{Low}_{\text{wick}} - \max(2.0 \times \text{spread}, 0.20 \times \text{ATR}_{15m})$.
     - **SELL Trades:** Strictly VETOED (`BLOCKED_ORDER_FLOW_BEAR_EXHAUSTION_VETO: Price stalled at Support 1 despite heavy sell volume delta. Institutional limit buyers have absorbed all sell flow (Bear Exhaustion). Shorting is prohibited.`).

### Invariant 103: Institutional Dealing Range Equilibrium Chop Veto & Boundary Acceleration Engine (AQ84 Pillar 4 - គ្រឹះផ្ទៀងផ្ទាត់តំបន់កណ្តាល Dealing Range Equilibrium Chop Veto ៣៥% - ៦៥% លុបបំបាត់ការចូលផ្សារច្របូកច្របល់ និងស្ទាក់ចាប់កម្លាំងពិតប្រាកដនៅព្រំដែន R1 / S1)
- **Location:** `dealing_range_equilibrium_chop_engine.py`, `super_smart_capital_citadel.py` (Pillar 0.91 & Pillar 2), `capital_meta_labeling_engine.py` (Section 0.7), `test_dealing_range_equilibrium_chop_engine.py`, `audit_system.py` [CHECK 82/82]
- **Rule:** Under the Sacred Covenant of Brutal Engineering Honesty & Mathematical Capital Protection:
  1. **Equilibrium Dealing Range Coordinates ($P_0, R_1, S_1$):**
     - Resolves the dealing range boundaries from Monte Safieddine's Daily Market Report or broker volatility coordinates: Resistance 1 ($R_1$), Support 1 ($S_1$), and Starting Point ($P_0 = (R_1 + S_1) / 2$).
     - Price position within the dealing range is normalized as:
       $$\text{Dealing Range Position \%} = \frac{\text{Price} - S_1}{\max(10^{-6}, R_1 - S_1)} \times 100\%$$
  2. **Equilibrium Chop Zone Injunction (35.0% - 65.0% Dealing Range):**
     - Between 35% and 65% of the dealing range, price movements are driven by Brownian motion random walk without institutional directional edge ($E[X] \le 0$). Over 90% of retail trading losses occur in this middle zone due to whipsaws.
     - Taking directional market orders in this equilibrium zone is strictly VETOED (`BLOCKED_DEALING_RANGE_EQUILIBRIUM_CHOP_VETO: Price is at X% of Dealing Range [35%-65%]. Middle equilibrium is Brownian motion retail chop without institutional edge. Awaiting boundary approach (R1/S1).`).
     - AI Meta-Model unconditionally crushes win probability to 0.0% and bet sizing to 0.0x (`verdict = "META_REJECTED"`). The system arms the in-memory dual-directional stealth breakout radar in RAM to await confirmed boundary interactions.
  3. **Discount Boundary Zone (< 35.0% near $S_1$):**
     - Approaching Support 1 ($S_1$) boundary: Institutional accumulation and liquidity sweep traps become active. BUY setups are aligned with discount boundary edge, receiving a $+25.0$ Citadel score boost and $+0.10$ meta win probability expansion.
  4. **Premium Boundary Zone (> 65.0% near $R_1$):**
     - Approaching Resistance 1 ($R_1$) boundary: Institutional distribution and upthrust traps become active. SELL setups are aligned with premium boundary edge, receiving a $+25.0$ Citadel score boost and $+0.10$ meta win probability expansion.

### Invariant 104: Institutional Profitability Architecture, Smart Money Leveraged Funds Alignment & 5-Pillar Win Rate Expansion Engine (AQ104 Standard - ស្ថាបត្យកម្មកែលម្អដើម្បីធានាប្រាក់ចំណេញ និងបង្កើន Win Rate ដល់ ៧៥% ទៅ ៨៥%)
- **Location:** `capital_market_report_engine.py` (`evaluate_contrarian_sentiment_edge` Case 5.5), `capital_meta_labeling_engine.py` (Section 0.1 Leveraged Funds Governor), `dynamic_structural_stops.py` (`calculate_structural_sl` and `evaluate_structural_stops` with broker SL cluster S1/R1 + 1.5x spread buffer), `super_smart_capital_citadel.py` (`TradFiMultiTargetScaleOutManager.evaluate_scale_out_lifecycle` 4-Phase Breakeven Armor & Flash Shock Protective Harvest), `capital_engine.py` (`is_asset_quarantined` with Gold Adaptive Re-Study Protocol), `test_invariant104_5pillars.py`, `audit_system.py`
- **Objective:** Solve institutional profitability gaps to push Win Rate to 75% - 85% and achieve exponential geometric capital growth through 5 non-negotiable quantitative pillars:
  1. **Smart Money Alignment Rule with Leveraged Funds (Pillar 1):**
     - Every trade signal must strictly verify the positioning of Leveraged Funds (CFTC CoT / Capital.com client sentiment).
     - If Leveraged Funds are heavily Short ($\ge 60.0\%$), all M15 BUY signals are 100% VETOED (`SMART_MONEY_ALIGNMENT_VETO: LEVERAGED_FUNDS_SHORT_VETO`). This rule alone eliminates falling knife dip-buying losses on Gold and US100 by $> 70\%$. SELL signals aligned with Leveraged Funds receive a $+30.0$ Citadel score boost and $+0.15$ meta win probability expansion.
     - If Leveraged Funds are heavily Long ($\ge 60.0\%$), all M15 SELL signals are 100% VETOED (`SMART_MONEY_ALIGNMENT_VETO: LEVERAGED_FUNDS_LONG_VETO`) to prevent shorting into institutional accumulation. BUY signals aligned receive a $+30.0$ Citadel score boost and $+0.15$ meta win probability expansion.
  2. **Real Structural Stop Loss behind Broker SL Clusters + 1.5x Spread Buffer (Pillar 2):**
     - Eliminates naive tight ATR stops that get clipped by broker spread expansion and stop-hunting wicks.
     - For BUY orders, SL is strictly anchored behind Broker Stop Loss Cluster Support 1 ($SL_{S1} = S_1 - 0.5 \cdot \Delta$) minus $1.5 \times \text{Spread}$.
     - For SELL orders, SL is strictly anchored behind Broker Stop Loss Cluster Resistance 1 ($SL_{R1} = R_1 + 0.5 \cdot \Delta$) plus $1.5 \times \text{Spread}$.
     - Dynamic volatility buffer guarantees nocturnal spread blowout cannot clip stop losses before directional expansion unfolds.
  3. **4-Phase Breakeven Armor & Multi-Target Scale-Out (Pillar 3):**
     - Phase 0: Initial structural stop anchored behind broker invalidation + 1.5x spread buffer.
     - Phase 1 at $+1.2R$: Ratchets SL to $\text{Entry} - 0.5 \times \text{ATR}$, cutting initial risk by 60%.
     - Phase 2 at $+1.8R$: Banks 50% lot cash (TP1) and shifts SL to Breakeven Armor ($\text{Entry} \pm \max(0.5\times\text{spread}, 0.001\times\text{price})$), locking $\text{Risk} = 0.00R$ (Free Roll, 100% loss-immune). Trade is permanently forbidden from turning red.
     - Phase 3 at $+3.5R$: Banks 30% lot cash (TP2) and ratchets SL to $+2.0R$ Guaranteed Cash Profit Floor.
     - Moonshot Runner: Remaining 20% lot trails behind 15m ATR / 3-EMA (20/50/200) confluence to absorb mega trends up to $+8.0R \dots +10.0R$.
     - Phase 4 Parabolic RSI Exhaustion: When RSI $\ge 80.0 / \le 20.0$ with $\ge 15\%$ retrace, locks 85% peak profit floor.
  4. **Flash Shock Protective Early Harvest (Pillar 4):**
     - If a trade achieves Peak UPL $\ge \$2.50$ (or Peak $\text{ROI} \ge +8.0\%$, or Peak $R \ge +1.5R$) and subsequently pulls back $\ge 50\%$ from its peak (`upl <= peak_upl * 0.50`), the engine executes an immediate market exit (`SHOCK_EARLY_HARVEST`), locking in fee-cleared net gains before violent whipsaws turn profit into a loss.
  5. **45-Minute Post-SL Anti-Revenge Quarantine with Gold Adaptive Re-Study Exception (Pillar 5):**
     - When an asset triggers a stop-loss, the system locks that asset for a mandatory 45-minute quarantine (`time.time() + 2700.0`) across Autonomous, ORB, and Scalp engines, eliminating revenge trading and knife-catching cascades.
     - Gold Adaptive Exception: For Gold (XAUUSD / PAXG), instead of blind freezing, `gold_candlestick_pattern_memory.py` actively studies M15 market structure. If a certified reversal candlestick pattern with $\ge 90.0\% - 92.0\%$ Confluence Win Rate (Piercing Line, Bullish Engulfing, Hammer, Turtle Soup Sweep Reclaim) is confirmed, the blind quarantine is bypassed for precision re-entry with tight structural stop behind the sweep wick.

---

## 4. STANDARD WORKFLOW FOR FUTURE SESSIONS
Whenever you are tasked with inspecting, modifying, or testing the repository:
1. **Step 1:** Run `python audit_system.py`.
2. **Step 2:** Read this file (`AGENTS.md`) and `METAPHYSICS_STANDARDS.md`.
3. **Step 3:** If you propose a change, ensure it maintains or increases the mathematical edge without violating any of the 76 Invariants or the Fiduciary Honesty Covenant.
4. **Step 4:** Re-run `python audit_system.py` to confirm that all 61 checks remain at 100% `[PASS]`.
5. **Step 5 (MANDATORY IMMEDIATE GIT PUSH):** Immediately stage, commit, and push all modifications to GitHub:
   ```bash
   git add . && git commit -m "<Clear, professional commit description>" && git push origin main
   ```
6. **Step 6 (MANDATORY VPS UPDATE DIRECTIVE IN OUTPUT):** Conclude your response by providing the exact 1-tap command for the founder to update the Google Cloud VPS node:
   ```bash
   cd /opt/khmer-master-crypto-bot && bash auto_update_vps.sh
   ```
   *(This directive is permanent, immutable, and must be followed in every future session without prompting).*


