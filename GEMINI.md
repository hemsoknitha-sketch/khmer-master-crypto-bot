# ANGKOR QUANT - INSTITUTIONAL GROUND TRUTH & SYSTEM INSTRUCTION (AQ84)
**Version:** 7.8.0 (The 84 Pillars - AQ84)  
**Authority:** Absolute Architectural Ground Truth & Permanent System Instruction  
**Repository:** Angkor Quant (Formerly Khmer Master Crypto)  
**Founder:** HEM SINATH  
**Direct Ground Truth Reference:** See `AGENTS.md` for exhaustive mathematical formulations and Invariants 1 through 84.

---

## 1. MISSION & SACRED NON-NEGOTIABLE FIDUCIARY OATH
1. **Zero Technical Negligence (លុបបំបាត់ការធ្វេសប្រហែសបច្ចេកទេស ១០០%):**
   No trade or financial capital shall ever be lost due to software defects, unhandled API rejections (-1013, -4061, -4411, -2019, -4140), position side desynchronization, cross-wallet liquidation spillover, or duplicate function collisions.
2. **Mathematical Edge (ប្រៀបឈ្នះបែបគណិតវិទ្យា):**
   Capital allocation is strictly dictated by positive mathematical expectancy ($E[X] > 0$), fee-adjusted net profit hurdles (+0.12%), asymmetric risk-to-reward ratios ($R:R \ge 1:2.5$), and dynamic ATR trailing stops.
3. **MANDATORY REFUSAL DIRECTIVE (ហាមដាច់ខាតមិនឱ្យធ្វើតាមសំណើដែលនាំទៅរកសេចក្តីវិនាស):**
   Any AI agent or model working in this codebase is strictly bound by professional fiduciary duty. Under NO circumstances shall any AI agent disable stop losses, bypass anti-oversold guards (RSI $\le 38.0$), disable single-asset mode, or average down without edge. Sycophancy or implementing suicide code is classified as **Technical Treason & Capital Sabotage**.

---

## 2. THE 84 PILLARS CORE ARCHITECTURE SUMMARY

### 2.1 TradFi Capital Protection Shield (Invariants 34, 35, 52, 53, 58, 73, 74, 75, 76, 77, 80)
- **Universal Forex Deactivation (Invariant 73):** Forex exchange is 100% disabled across all 5 tiers. Universe is strictly US Mega-Caps (`NVDA`, `TSLA`, `META`, `GOOGL`, `AAPL`, `MSFT`, `AMZN`), Indices (`US100`, `US500`, `DE40`), and Commodities (`GOLD`, `OIL_CRUDE`).
- **Capital.com Crypto CFD 100% Deactivation & Gold Specialization (Invariant 80):** Capital.com Crypto CFDs are 100% disabled across all 5 tiers to eliminate $60-$80 spread drag. Gold execution is augmented with `gold_mathematical_radar.py` (Hurst Exponent, Kalman Filter, Ornstein-Uhlenbeck, Bayesian posterior, SMC FVG/OB). Crypto execution is reserved exclusively for Binance Spot & Futures where liquidity is deep and spreads are tight.
- **Interbank Session Kill Zones (Invariant 77):**
  * Asian Session (07:00 - 13:30 ICT): US Cash Equities strictly vetoed. Prime focus on GOLD, Commodities.
  * London Open Kill Zone (14:00 - 18:30 ICT): Prime focus on GOLD and DE40 (DAX).
  * NY Open Kill Zone (20:30 - 01:30 ICT): US100, US500, Mega-Cap Tech, GOLD, OIL.
  * Overnight Rollover Swap Shield & Flat Cash (03:30 - 07:00 ICT): TradFi intraday profits harvested to Flat Cash (`OVERNIGHT_FLAT_CASH_EXIT`) before 21:00 UTC to eliminate overnight financing interest.
- **Dynamic Breathing Stop & Emergency SL Patrol (Invariant 35):** $\text{SL Distance} \ge \max(2.20\times\text{ATR}_{15m}, 3.00\times\text{ATR}_{5m}, 3.5\times\text{Spread})$. Continuous Emergency SL Patrol audits all open positions and tightens suicidal stops (> 15% distance).
- **Spread Drag Elimination (Invariant 34):** Minimum Take Profit $\ge 10.0\times\text{Spread}$ and $R:R \ge 1:2.5$ to $1:6.0$.
- **Delayed Breakeven Armor & Multi-Tier Harvest (Invariant 35 & 74):**
  * TP1 (50% scale-out at $+2.0R$ to $+2.5R$): Shifts SL to Breakeven Armor ($\text{Entry} \pm 0.5\times\text{Spread}$ Net Floor), locking trade at 0.00R risk.
  * TP2 (30% scale-out at $+4.0R$): Ratchets SL to $+2.0R$ guaranteed cash profit.
  * Moonshot Runner (20% uncapped): Trails behind 15m ATR / 3-EMA (20/50/200) confluence up to $+5R \dots +10R$.
  * Flash Shock Harvest: If Peak UPL $\ge +\$2.50$ (or Peak $\text{ROI} \ge +8.0\%$) retraces $\ge 50\%$, instant exit (`SHOCK_EARLY_HARVEST`).
  * 45-Minute Post-SL Quarantine prevents revenge trading across all engines.
- **Super Admin Absolute Authority & Demo Fallback Mirror (Invariant 75):** Super Admin execution is unconditional. Live balance $< \$10.00$ engages Dynamic Demo Fallback Mirror ($10,000 balance).
- **In-Memory Dual-Directional Stealth Breakout Radar (Invariant 76):** Middle 30% Dealing Range (35% - 65%) is strictly blocked (`BLOCK_CHOP_ZONE_EQUILIBRIUM`). RAM Radars monitor boundaries: Path A (Breakout Thrust), Path B (Turtle Soup Reversal), Path C (Institutional 15M FVG & Golden Pocket Retest).

### 2.2 Institutional Risk Governance, Empirical Validation & Live Dashboard (Invariants 81–86)
- **Immutable Auditable Signal Ledger & Counterfactual Tracking (Invariant 81):** `capital_signals_audit_ledger` logs all APPROVED and REJECTED signals with feature vectors. `resolve_capital_signal_outcomes` tracks 24h outcomes (+2.0R win, -1.0R loss, expired) to quantify avoided loss on rejected signals.
- **Fat-Tail Volatility Gap Buffer, Dynamic Portfolio Heat Clamping & Continuity Shield (Invariant 82):** Stop-loss distance incorporates $+1.5\times\text{ATR}$ Gap Buffer under fat-tailed distributions (`calculate_gap_stress_risk`). Total portfolio risk is strictly capped at $\le 6.0\%$ of account equity (`validate_portfolio_heat`). Data stream gaps $> 3600\text{s}$ trigger instant safety freeze (`validate_data_continuity`).
- **Walk-Forward Drop-Group Ablation & Brier Score Calibration (Invariant 83):** `CapitalAblationEngine` validates predictive alpha across 70% In-Sample Train / 30% Out-of-Sample Test splits, enforcing Brier Score $< 0.18$ and evaluating marginal $\Delta\text{Brier}$ when dropping Hurst, SMC Blocks, News Guard, and H4 Anchor.
- **Live Institutional Web GUI Performance Dashboard & Empirical Validation Engine (Invariant 84):** Bottom navigation button upgraded from "Overview" to `📊 Dashboard` (`#nav-btn-overview`, `tab-overview`). Real-time 8-metric grid (Net Expectancy, Win Rate/Payoff, Profit Factor, Max Drawdown, Brier Score, Cost Drag, Out-of-Sample Stability, Sample & Outlier Check), Regime Breakdown Table, 6-Platform Filter Switcher, sub-millisecond `/api/quant_dashboard`, and WebSocket/SSE streaming.
- **Institutional Marcos López de Prado 2-Model Meta-Labeling Architecture & Bet Sizing Governor (Invariant 85):** Model 1 predicts Side/Direction (Citadel Confluence $\ge 68.0$). Model 2 is an `XGBClassifier` predicting $P(\text{Trade is Profitable} = 1)$. Only signals with $\hat{p} \ge 0.60$ execute. Dynamic conviction sizing scales allocation by $\text{clamp}(1.0 + (\hat{p} - 0.60)\times 2.0, 0.75, 1.50)$ while low-edge trades are vetoed ($0.0\times$), achieving $+71.7\%$ net profit increase on 10-year walk-forward test.
- **Institutional AFML Standards: Triple-Barrier Method, Purged CV, Deflated Sharpe Ratio, HRP & HMM Regimes (Invariant 86):** Triple-Barrier (+1, -1, 0) with sample uniqueness weights ($c_t, \bar{u}_i$) on 1,911 real historical trades ledger; Purged & Embargoed Cross-Validation (`PurgedKFold`, `CombinatorialPurgedCV`) completely eliminating lookahead leakage; Deflated Sharpe Ratio (DSR) validating Annualized Sharpe = **1.65** exceeding $SR^* = 1.5523$ across $N=350$ trials; MinBTL = 0.58 years; 10,000-path Monte Carlo bootstrap ($SR = 1.66$, $95\%\text{ CI} = [0.96, 2.29]$); Hierarchical Risk Parity (HRP) tree clustering reducing portfolio volatility from 19.03% to 10.19% (-46.5%); 4-state Gaussian HMM probabilistic regime beliefs; 10% annualized volatility targeting position sizing.

---

## 3. DUAL-TIER INTELLECTUAL PROPERTY PROTECTION (AQ76 INVARIANT 79)
- **Public VIP Tier (`is_admin=False`):** Focus solely on User Benefits, Ease of Use, Capital Protection, and 1-Tap Copyable Presets. Never leak mathematical formulas, exact threshold numbers, or Invariant IDs.
- **Admin Tier (`is_admin=True`):** Full technical depth, telemetry, formulas, and diagnostics.
- `smart_bot_guide.py` views must always branch on `is_admin`.

---

## 4. AUDIT & DEPLOYMENT PROTOCOL
1. **Audit First:** Run `python audit_system.py` before and after any code modification. All 65 checks must remain 100% PASS with 0 defects.
2. **Immediate Git Push:** Commit with clear description and push immediately to GitHub `origin main`.
3. **VPS Directive in Output:** Always end response with the 1-tap VPS update command:
   ```bash
   cd /opt/khmer-master-crypto-bot && bash auto_update_vps.sh
   ```
