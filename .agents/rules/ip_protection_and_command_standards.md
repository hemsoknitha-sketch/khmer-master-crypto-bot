# ANGKOR QUANT - DUAL-TIER IP SHIELDING & COMMAND STANDARDS (AQ84 INVARIANT 79 & 81-84)
**Authority:** Absolute Architectural Rule & Permanent Memory Lock Across All Sessions  
**Project:** Angkor Quant (Formerly Khmer Master Crypto)  
**Founder:** HEM SINATH

---

## 1. គោលការណ៍គ្រឹះការពារកម្មសិទ្ធិបញ្ញា (NON-NEGOTIABLE FIDUCIARY IP DIRECTIVE)
> **"សម្រាប់មុខងារ Commands នីមួយៗមិនចាំបាច់រៀបរាប់បច្ចេកទេសនោះទេ ព្រោះនាំឱ្យអ្នកប្រើប្រាស់អាចចម្លងបច្ចេកទេសធ្វើតាមប្រព័ន្ធយើង លើកលែងតែ ADMIN Commands គឺអាចលម្អិតបច្ចេកទេសបាន"**

គ្រប់ AI Agent និងអ្នកអភិវឌ្ឍន៍ទាំងអស់ ត្រូវតែគោរពតាមច្បាប់ដែកថែបនេះជាដាច់ខាត ទោះបីបើក New Conversation ថ្មី ឬប្តូរ Model ក៏ដោយ ហាមដាច់ខាតមិនឱ្យភ្លេច ឬច្រឡំឡើយ។

---

## 2. DUAL-TIER ARCHITECTURE SPECIFICATION

### Tier 1: Public VIP Users (`is_admin=False`)
1. **ការបង្ហាញអត្ថប្រយោជន៍ (User-Centric & Benefits):**
   - ផ្តោតលើភាពងាយស្រួល (Ease of use) ផលប្រយោជន៍ជាក់ស្តែង (Direct benefits) ការការពារដើមទុន (Capital protection) និងគំរូបញ្ជា 1-Tap Copyable Presets។
2. **ចំណុចហាមឃាត់ដាច់ខាត (Strictly Forbidden):**
   - ហាមបង្ហាញរូបមន្តគណិតវិទ្យា (Math formulas, Hawkes jump equations $\lambda(t)$, ATR multipliers, Sharpe ratios)។
   - ហាមបង្ហាញលេខកម្រិតជាក់លាក់ (Exact thresholds, RSI boundaries $\le 38.0$ / $\ge 68.0$, exact breakeven ROI percentages $+3.0\%$, RAM tick latency microseconds $< 0.0003\text{ms}$, Min-Notional shields $\$5.05$)។
   - ហាមបញ្ចេញលេខ Invariant (Invariant 16, 26, 38, 41, etc.) ឬឈ្មោះ Algorithm ផ្ទៃក្នុង (PINN, HMM, MoE, LSTM, PPO)។
   - ហាមបង្ហាញបញ្ជី Pillars បច្ចេកទេស (Technical Pillars lists) ក្នុងសារ Dashboard សាធារណៈ។
3. **Public Commands Limit:**
   - រក្សាត្រឹម ៣០ Commands សំខាន់ៗក្នុង `bot_commands_registry.get_public_bot_commands()` ដោយចាត់ជា ៥ ប្រភេទច្បាស់លាស់។

### Tier 2: Super Admin Exclusive (`is_admin=True` ឬ `chat_id in ADMIN_USER_IDS`)
1. **កម្រិតបច្ចេកទេសពេញលេញ (Full Institutional Depth):**
   - អាចបង្ហាញរូបមន្តគណិតវិទ្យា ស្ថិតិ Telemetry, Invariant logs, Low-level diagnostics, Quorum thresholds និង Fleet Command toggles ពេញលេញ។
   - Admin Commands ទាំងអស់ស្ថិតក្នុង `bot_commands_registry.get_admin_bot_commands()`.

---

## 3. SMART BOT GUIDE & DASHBOARD ARCHITECTURE
- គ្រប់ Views ក្នុង `smart_bot_guide.py` (`_build_spot_view`, `_build_futures_view`, `_build_tradfi_view`, `_build_radars_view`, `_build_guide_view`) ត្រូវតែឆ្លងកាត់ការឆែក `is_admin` ជានិច្ច។
- `/menu` Dashboard ត្រូវតែរៀបចំជា 5-Pillar Visual Dashboard Card ស្រស់ស្អាត ងាយស្រួលចុច និងមាន callback `btn_webapp`។

---

## 4. AUDIT & DEPLOYMENT COVENANT
- មុនពេល Git Commit ត្រូវតែដំណើរការ `python audit_system.py` ជាប់ ១០០% (៦៤/៦៤ Checks Passed, Zero Defects)។
- បន្ទាប់ពី Commit រួច ត្រូវ Push ទៅកាន់ `origin main` ភ្លាមៗដើម្បីឱ្យ GCP VPS ទាញយកតាមរយៈ `auto_update_vps.sh` ស្វ័យប្រវត្តិ។

