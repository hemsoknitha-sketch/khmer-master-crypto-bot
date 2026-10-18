# -*- coding: utf-8 -*-
"""
ANGKOR QUANT - SUPER SMART BOT COMMAND & INTERACTIVE NAVIGATOR (AQ76)
Document Version: 7.6.0
Authority: Invariants 22, 23 & 75 (AGENTS.md)

Dedicated Zero-Confusion Command Navigator & Interactive Hub for:
- Super Admin (Fleet Command & Control)
- Verified VIP Quant Investors (Spot, Futures, TradFi, Radars, Security)

Eliminates 100% of interface and command confusion across all user tiers.
"""

from typing import Tuple, Optional, Dict, Any
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
import database as db

SUPER_ADMIN_ID = 859271875


def is_user_admin(chat_id: int) -> bool:
    """Checks whether the user has Super Admin authority."""
    if chat_id in [SUPER_ADMIN_ID, 537186806]:
        return True
    try:
        return bool(db.is_admin(chat_id))
    except Exception:
        return False


def get_user_lang(chat_id: int) -> str:
    """Resolves user language preference to km, en, or zh."""
    try:
        raw_lang = db.get_user_language(chat_id)
        lang = str(raw_lang or 'km').lower().strip()
        if lang in ['km', 'khmer', '0', '1', 'auto'] or lang.isdigit():
            return 'km'
        elif lang in ['en', 'english']:
            return 'en'
        elif lang in ['zh', 'chinese']:
            return 'zh'
        return 'km'
    except Exception:
        return 'km'


def build_smart_bot_payload(chat_id: int, user_lang: Optional[str] = None, category: str = "home") -> Tuple[str, InlineKeyboardMarkup]:
    """
    Builds the rich, institutional Super Smart Bot text and interactive keyboard
    tailored specifically for Admin vs VIP User to guarantee zero confusion.
    """
    if not user_lang:
        user_lang = get_user_lang(chat_id)
    is_admin = is_user_admin(chat_id)

    # Dynamic status badges
    try:
        import trading_engine
        is_paper = getattr(trading_engine, "PAPER_TRADING", False)
        mode_badge = "🧪 PAPER TRADING" if is_paper else "🚀 REAL LIVE TRADING"
    except Exception:
        mode_badge = "🚀 REAL LIVE TRADING"

    category = (category or "home").lower().strip()

    # Route to appropriate category builder
    if category == "spot":
        return _build_spot_view(is_admin, user_lang, mode_badge)
    elif category == "futures":
        return _build_futures_view(is_admin, user_lang, mode_badge)
    elif category == "tradfi":
        return _build_tradfi_view(is_admin, user_lang, mode_badge)
    elif category == "radars":
        return _build_radars_view(is_admin, user_lang, mode_badge)
    elif category == "security":
        return _build_security_view(is_admin, user_lang, mode_badge)
    elif category == "admin":
        return _build_admin_view(is_admin, user_lang, mode_badge)
    elif category == "guide":
        return _build_guide_view(is_admin, user_lang, mode_badge)
    else:
        return _build_home_view(is_admin, user_lang, mode_badge)


# ==============================================================================
# 1. MASTER HOME VIEW (Zero Confusion Executive Hub)
# ==============================================================================
def _build_home_view(is_admin: bool, lang: str, mode_badge: str) -> Tuple[str, InlineKeyboardMarkup]:
    if is_admin:
        role_badge = "👑 SUPER ADMIN / SUPREME FLEET COMMANDER"
    else:
        role_badge = "💎 VERIFIED VIP QUANT INVESTOR"

    if lang == "en":
        text = (
            f"🧠 **ANGKOR QUANT | SUPER SMART BOT DIRECTORY** 🧠\n"
            f"══════════════════════════════\n"
            f"👤 **YOUR ROLE**: `{role_badge}`\n"
            f"⚡ **SYSTEM STATUS**: `🟢 24/7 ONLINE` | `Latency: <15ms`\n"
            f"🛡️ **TRADING ENGINE**: `{mode_badge}` | `ISOLATED MARGIN`\n"
            f"══════════════════════════════\n\n"
            f"💡 **NO-CONFUSION QUICK GUIDE (Which Engine Should You Use?):**\n"
            f"• 🟢 **Want 0% liquidation risk & safe growth?** ➔ **Spot Engines** (`/compound_grid`, `/infinity_matrix`)\n"
            f"• 🟡 **Want 24/7 automated high yield & hedge?** ➔ **Futures Engines** (`/wealth`, `/turbo_hedge`, `/smartx`)\n"
            f"• 🔵 **Want Gold (XAUUSD), US Tech & S&P 500?** ➔ **TradFi & MT5** (`/capital`, `/mt5`)\n"
            f"• 🟣 **Want AI analysis, forecasts & whales?** ➔ **Radars & AI** (`/analyze`, `/predict`, `/whales`)\n"
            f"• 🔴 **Need balance, PnL or emergency stop?** ➔ **Security & Risk** (`/portfolio`, `/balance`, `/stop ALL`)\n"
        )
        if is_admin:
            text += (
                f"• 👑 **Admin Fleet Control & User Licensing?** ➔ **Fleet Command** (`/admin`, `/admin_users`, `/admin_license`)\n"
            )
        text += (
            f"\n👇 **Tap any interactive category below for full syntax, examples & instant launch:**"
        )
    elif lang == "zh":
        text = (
            f"🧠 **ANGKOR QUANT | 超级智能指令主控中心** 🧠\n"
            f"══════════════════════════════\n"
            f"👤 **当前身份**: `{role_badge}`\n"
            f"⚡ **系统状态**: `🟢 24/7 在线` | `延迟: <15ms`\n"
            f"🛡️ **交易引擎**: `{mode_badge}` | `隔离保证金`\n"
            f"══════════════════════════════\n\n"
            f"💡 **防混淆快速指引（我该选择哪个引擎？）：**\n"
            f"• 🟢 **追求 0% 爆仓风险与稳健复利？** ➔ **现货引擎** (`/compound_grid`, `/infinity_matrix`)\n"
            f"• 🟡 **追求 24/7 全自动高频收益与对冲？** ➔ **合约引擎** (`/wealth`, `/turbo_hedge`, `/smartx`)\n"
            f"• 🔵 **交易黄金 (XAUUSD)、美股龙头与标普？** ➔ **TradFi 全球市场** (`/capital`, `/mt5`)\n"
            f"• 🟣 **需要 AI 深度技术分析与链上巨鲸？** ➔ **AI 智能雷达** (`/analyze`, `/predict`, `/whales`)\n"
            f"• 🔴 **查询余额、盈亏或一键紧急平仓？** ➔ **资金与风控** (`/portfolio`, `/balance`, `/stop ALL`)\n"
        )
        if is_admin:
            text += (
                f"• 👑 **管理员舰队管理、授权与系统监控？** ➔ **超级管理员舰队** (`/admin`, `/admin_users`, `/admin_license`)\n"
            )
        text += (
            f"\n👇 **点击下方分类按钮，查看各模块详细指令、语法示例与一键启动：**"
        )
    else:  # Khmer (Default)
        text = (
            f"🧠 **ANGKOR QUANT | SUPER SMART BOT COMMAND HUB** 🧠\n"
            f"══════════════════════════════\n"
            f"👤 **តួនាទីរបស់អ្នក ៖** `{role_badge}`\n"
            f"⚡ **ស្ថានភាពប្រព័ន្ធ ៖** `🟢 24/7 ONLINE` | `Latency: <15ms`\n"
            f"🛡️ **យន្តការជួញដូរ ៖** `{mode_badge}` | `ISOLATED MARGIN`\n"
            f"══════════════════════════════\n\n"
            f"💡 **មគ្គុទ្ទេសក៍ជ្រើសរើសច្បាស់លាស់ (កុំឱ្យភ័ន្តច្រឡំក្នុងការប្រើប្រាស់) ៖**\n"
            f"• 🟢 **ចង់បានសុវត្ថិភាព ១០០% គ្មានហានិភ័យ Liquidation?** ➔ **Spot Engines** (`/compound_grid`, `/infinity_matrix`)\n"
            f"• 🟡 **ចង់បានផលចំណេញខ្ពស់ 24/7 មាន Breakeven Armor?** ➔ **Futures Engines** (`/wealth`, `/turbo_hedge`, `/smartx`)\n"
            f"• 🔵 **ចង់ជួញដូរមាស Gold, ប្រេង, ភាគហ៊ុនអាមេរិក (NVDA, TSLA)?** ➔ **TradFi & MT5** (`/capital`, `/mt5`)\n"
            f"• 🟣 **ចង់បាន AI វិភាគបច្ចេកទេស និងតាមដានត្រីបាឡែន?** ➔ **AI Radars** (`/analyze`, `/predict`, `/whales`)\n"
            f"• 🔴 **ចង់ឆែកសមតុល្យលុយ ឬបិទ Bot អាសន្ន?** ➔ **Portfolio & Risk** (`/portfolio`, `/balance`, `/stop ALL`)\n"
        )
        if is_admin:
            text += (
                f"• 👑 **គ្រប់គ្រងសមាជិក VIP, បញ្ជាកងនាវា & អាសន្នប្រព័ន្ធ?** ➔ **Admin Fleet** (`/admin`, `/admin_users`, `/admin_license`)\n"
            )
        text += (
            f"\n👇 **សូមចុចលើប៊ូតុងផ្នែកនីមួយៗខាងក្រោម ដើម្បីមើលពាក្យបញ្ជាលម្អិត និងរបៀបប្រើប្រាស់ ៖**"
        )

    # Build Buttons
    keyboard = [
        [
            InlineKeyboardButton("🟢 1. Spot Engines (0% Risk)", callback_data="smart_cat_spot"),
            InlineKeyboardButton("🟡 2. Futures & Hedge", callback_data="smart_cat_futures")
        ],
        [
            InlineKeyboardButton("🔵 3. TradFi & MT5 Suite", callback_data="smart_cat_tradfi"),
            InlineKeyboardButton("🟣 4. AI Radars & Intelligence", callback_data="smart_cat_radars")
        ],
        [
            InlineKeyboardButton("🔴 5. Portfolio & Security", callback_data="smart_cat_security"),
            InlineKeyboardButton("💡 6. Selection Guide (FAQ)", callback_data="smart_cat_guide")
        ]
    ]

    if is_admin:
        keyboard.append([
            InlineKeyboardButton("👑 7. Super Admin Fleet Command", callback_data="smart_cat_admin"),
            InlineKeyboardButton("📊 System Stats & PnL", callback_data="btn_admin_stats_refresh")
        ])

    keyboard.append([
        InlineKeyboardButton("🎛️ Master Control Panel", callback_data="btn_menu_refresh"),
        InlineKeyboardButton("🔄 Refresh Smart Hub", callback_data="smart_hub_refresh")
    ])

    return text, InlineKeyboardMarkup(keyboard)


# ==============================================================================
# 2. SPOT ENGINES VIEW (100% Spot, 0% Liquidation Risk)
# ==============================================================================
def _build_spot_view(is_admin: bool, lang: str, mode_badge: str) -> Tuple[str, InlineKeyboardMarkup]:
    if is_admin:
        # Super Admin View (Institutional Mathematical & Algorithmic Depth)
        if lang == "en":
            text = (
                "🟢 **CATEGORY 1: SPOT INVESTMENT ENGINES (100% SPOT, 0% LEVERAGE) [ADMIN VIEW]** 🟢\n"
                "══════════════════════════════\n"
                "🛡️ **Institutional Capital Standard:** 0% Leverage, zero liquidation risk ($0.00). Powered by dynamic volatility bands and geometric Fibonacci grids.\n"
                "══════════════════════════════\n\n"
                "📈 **1. Dynamic Volatility Compound Grid:**\n"
                "• `/compound_grid <PAIR> <INVEST_USDT> <PIN>`\n"
                "  _Example:_ `/compound_grid BTC 100 1234`\n"
                "  Buys dips and sells rips within dynamic ATR channels, reinvesting net profits into base asset.\n\n"
                "♾️ **2. Fibonacci Geometric Infinity Matrix:**\n"
                "• `/infinity_matrix <PAIR> <INVEST_USDT> <PIN>`\n"
                "  _Example:_ `/infinity_matrix ETH 100 1234`\n"
                "  Infinite upper/lower geometric grid based on Fibonacci golden ratios, never bounded during massive bull runs.\n\n"
                "💎 **3. Spot Accumulator & Institutional DCA:**\n"
                "• `/smart_trade <PAIR> <AMOUNT>`\n"
                "  _Example:_ `/smart_trade SOL 50`\n"
                "  Accumulates spot assets at institutional orderbook cluster support levels.\n\n"
                "🏦 **4. Spot Profit Harvester Vault:**\n"
                "• `/spot_harvest`\n"
                "  Sweeps and locks all accumulated spot trading profits into USDT cold vault.\n"
            )
        elif lang == "zh":
            text = (
                "🟢 **模块 1：现货投资引擎 (100% 现货，0% 爆仓风险) [管理员深度模式]** 🟢\n"
                "══════════════════════════════\n"
                "🛡️ **资金安全基准：** 无杠杆、无借贷、绝对零爆仓风险 ($0.00)。依托动态 ATR 通道与斐波那契几何网格。\n"
                "══════════════════════════════\n\n"
                "📈 **1. 动态波动率复利网格 (Compound Grid):**\n"
                "• `/compound_grid <币种> <投资USDT> <安全PIN>`\n"
                "  _示例:_ `/compound_grid BTC 100 1234`\n"
                "  在动态 ATR 波动区间内自动逢低吸筹、逢高套利，收益全自动复利再投资。\n\n"
                "♾️ **2. 斐波那契几何无限矩阵 (Infinity Matrix):**\n"
                "• `/infinity_matrix <币种> <投资USDT> <安全PIN>`\n"
                "  _示例:_ `/infinity_matrix ETH 100 1234`\n"
                "  基于斐波那契黄金分割比率的无上限几何级数网格，单边大牛市永不出界。\n\n"
                "💎 **3. 机构订单簿深度定投 (Smart Trade DCA):**\n"
                "• `/smart_trade <币种> <金额>`\n"
                "  _示例:_ `/smart_trade SOL 50`\n"
                "  在订单簿集群与机构支撑位精准吸筹，消除追高杀跌。\n\n"
                "🏦 **4. 现货收益金库收割机 (Spot Harvest):**\n"
                "• `/spot_harvest`\n"
                "  一键将所有现货套利利润归集锁定至 USDT 安全金库。\n"
            )
        else:
            text = (
                "🟢 **ផ្នែកទី ១ ៖ SPOT INVESTMENT ENGINES (100% SPOT, 0% ហានិភ័យ) [ADMIN VIEW]** 🟢\n"
                "══════════════════════════════\n"
                "🛡️ **ស្តង់ដារការពារដើមទុន ៖** គ្មានខ្ចីលុយ (0% Leverage), គ្មានហានិភ័យ Liquidation 100% ($0.00)។ ដំណើរការដោយ dynamic ATR channels & Fibonacci geometric grid។\n"
                "══════════════════════════════\n\n"
                "📈 **១. Dynamic Volatility Compound Grid ៖**\n"
                "• `/compound_grid <COIN> <INVEST_USDT> <PIN>`\n"
                "  _ឧទាហរណ៍ ៖_ `/compound_grid BTC 100 1234`\n"
                "  ទិញតាម ATR dip និងលក់ពេលឡើងថ្លៃដោយស្វ័យប្រវត្ត ហើយយកប្រាក់ចំណេញមក Reinvest បង្កើនទុនបន្តបន្ទាប់។\n\n"
                "♾️ **២. Fibonacci Geometric Infinity Matrix ៖**\n"
                "• `/infinity_matrix <COIN> <INVEST_USDT> <PIN>`\n"
                "  _ឧទាហរណ៍ ៖_ `/infinity_matrix ETH 100 1234`\n"
                "  សំណាញ់គណិតវិទ្យា Fibonacci Geometric Grid រត់តាមតម្លៃទីផ្សាររហូត មិនចេះជាប់គាំងក្នុង Bull Market។\n\n"
                "💎 **៣. Institutional Orderbook DCA ៖**\n"
                "• `/smart_trade <COIN> <AMOUNT>`\n"
                "  _ឧទាហរណ៍ ៖_ `/smart_trade SOL 50`\n"
                "  ទិញសន្សំកាក់ល្អៗនៅចំណុច Support Orderbook Clusters របស់ស្ថាប័នធំៗ។\n\n"
                "🏦 **៤. Spot Harvest Vault (ទូដកប្រាក់ចំណេញ Spot) ៖**\n"
                "• `/spot_harvest`\n"
                "  ប្រមូលប្រាក់ចំណេញពីការជួញដូរ Spot ទាំងអស់ចូលទៅក្នុងកាបូបសុវត្ថិភាព USDT។\n"
            )
    else:
        # Public VIP User View (Zero Technical Leakage - User Benefits & Safe Simplicity)
        if lang == "en":
            text = (
                "🟢 **CATEGORY 1: SPOT INVESTMENT ENGINES (100% SPOT, 0% LEVERAGE)** 🟢\n"
                "══════════════════════════════\n"
                "🛡️ **Capital Safety Standard:** Zero borrowing, zero liquidation risk ($0.00). Ideal for capital preservation and long-term compounding growth.\n"
                "══════════════════════════════\n\n"
                "📈 **1. Dynamic Compound Grid:**\n"
                "• `/compound_grid <PAIR> <INVEST_USDT> <PIN>`\n"
                "  _Example:_ `/compound_grid BTC 100 1234`\n"
                "  Automatically buys dips and sells rips within dynamic price channels, compounding profits into your balance.\n\n"
                "♾️ **2. Continuous Infinity Grid:**\n"
                "• `/infinity_matrix <PAIR> <INVEST_USDT> <PIN>`\n"
                "  _Example:_ `/infinity_matrix ETH 100 1234`\n"
                "  Continuous long-term spot accumulator designed to capture sustained market uptrends without hitting upper limits.\n\n"
                "💎 **3. Spot Accumulator & DCA:**\n"
                "• `/smart_trade <PAIR> <AMOUNT>`\n"
                "  _Example:_ `/smart_trade SOL 50`\n"
                "  Smart spot accumulation at optimal entry levels to avoid emotional timing mistakes.\n\n"
                "🏦 **4. Spot Profit Harvester Vault:**\n"
                "• `/spot_harvest`\n"
                "  Sweeps and locks all accumulated spot trading profits into your USDT balance.\n"
            )
        elif lang == "zh":
            text = (
                "🟢 **模块 1：现货投资引擎 (100% 现货，0% 爆仓风险)** 🟢\n"
                "══════════════════════════════\n"
                "🛡️ **资金安全基准：** 无杠杆、无借贷、绝对零爆仓风险 ($0.00)。专为大资金保本与长期复利设计。\n"
                "══════════════════════════════\n\n"
                "📈 **1. 动态复利网格 (Compound Grid):**\n"
                "• `/compound_grid <币种> <投资USDT> <安全PIN>`\n"
                "  _示例:_ `/compound_grid BTC 100 1234`\n"
                "  在波动区间内自动逢低买入、逢高套利，收益复利滚存。\n\n"
                "♾️ **2. 无界现货网格 (Infinity Matrix):**\n"
                "• `/infinity_matrix <币种> <投资USDT> <安全PIN>`\n"
                "  _示例:_ `/infinity_matrix ETH 100 1234`\n"
                "  长期连续现货定投吸筹，伴随牛市行情持续捕获收益，无需担心触顶出界。\n\n"
                "💎 **3. 智能现货定投 (Smart Trade DCA):**\n"
                "• `/smart_trade <币种> <金额>`\n"
                "  _示例:_ `/smart_trade SOL 50`\n"
                "  自动在合理价位分批建仓吸筹，避免情绪化追高。\n\n"
                "🏦 **4. 现货金库收益收割 (Spot Harvest):**\n"
                "• `/spot_harvest`\n"
                "  一键将现货套利利润归集锁定至 USDT 安全账户。\n"
            )
        else:
            text = (
                "🟢 **ផ្នែកទី ១ ៖ SPOT INVESTMENT ENGINES (100% SPOT, 0% ហានិភ័យ)** 🟢\n"
                "══════════════════════════════\n"
                "🛡️ **ស្តង់ដារការពារដើមទុន ៖** គ្មានខ្ចីលុយ (0% Leverage), គ្មានហានិភ័យ Liquidation 100% ($0.00)។ ស័ក្តិសមបំផុតសម្រាប់អ្នកចង់សន្សំទុន និងបង្កើនប្រាក់ចំណេញរយៈពេលវែង។\n"
                "══════════════════════════════\n\n"
                "📈 **១. Dynamic Compound Grid (ម៉ាស៊ីនបាញ់សំណាញ់កើនទុន) ៖**\n"
                "• `/compound_grid <COIN> <INVEST_USDT> <PIN>`\n"
                "  _ឧទាហរណ៍ ៖_ `/compound_grid BTC 100 1234`\n"
                "  ទិញពេលធ្លាក់ និងលក់ពេលឡើងដោយស្វ័យប្រវត្ត ហើយយកប្រាក់ចំណេញមកបង្កើនទុនបន្តបន្ទាប់។\n\n"
                "♾️ **២. Continuous Infinity Grid (ម៉ាស៊ីនសន្សំទុនរយៈពេលវែង) ៖**\n"
                "• `/infinity_matrix <COIN> <INVEST_USDT> <PIN>`\n"
                "  _ឧទាហរណ៍ ៖_ `/infinity_matrix ETH 100 1234`\n"
                "  ប្រព័ន្ធសន្សំកាក់រយៈពេលវែងដែលរត់តាមទីផ្សារឡើងថ្លៃជាប់ជានិច្ច ដោយមិនបារម្ភពីរឿងផុតដែនកំណត់។\n\n"
                "💎 **៣. Smart Trade & DCA (ម៉ាស៊ីនទិញសន្សំកាក់ឆ្លាតវៃ) ៖**\n"
                "• `/smart_trade <COIN> <AMOUNT>`\n"
                "  _ឧទាហរណ៍ ៖_ `/smart_trade SOL 50`\n"
                "  ទិញសន្សំកាក់ល្អៗនៅកម្រិតតម្លៃសមរម្យដោយស្វ័យប្រវត្ត ជៀសវាងការទិញតាមអារម្មណ៍។\n\n"
                "🏦 **៤. Spot Harvest Vault (ទូដកប្រាក់ចំណេញ Spot) ៖**\n"
                "• `/spot_harvest`\n"
                "  ប្រមូលប្រាក់ចំណេញពីការជួញដូរ Spot ទាំងអស់ចូលទៅក្នុងកាបូបសុវត្ថិភាព USDT។\n"
            )

    keyboard = [
        [
            InlineKeyboardButton("🚀 Launch Infinity Matrix", callback_data="btn_infinity_grid_launch"),
            InlineKeyboardButton("💎 Smart Trade", callback_data="btn_smart_swap_menu")
        ],
        [
            InlineKeyboardButton("🔙 Back to Smart Hub", callback_data="smart_hub_home"),
            InlineKeyboardButton("🎛️ Master Control Panel", callback_data="btn_menu_refresh")
        ]
    ]
    return text, InlineKeyboardMarkup(keyboard)


# ==============================================================================
# 3. FUTURES & HEDGE VIEW (High-Yield Delta-Neutral & Directional)
# ==============================================================================
def _build_futures_view(is_admin: bool, lang: str, mode_badge: str) -> Tuple[str, InlineKeyboardMarkup]:
    if is_admin:
        # Super Admin View (Institutional Technical Ground Truths & Exact Formulas)
        if lang == "en":
            text = (
                "🟡 **CATEGORY 2: FUTURES & HEDGE ENGINES [ADMIN VIEW - FULL TECHNICAL DEPTH]** 🟡\n"
                "══════════════════════════════\n"
                "🛡️ **Institutional Protection Standards (AQ76 Master Invariants):**\n"
                "• `ISOLATED MARGIN (10x)` - Strict wallet partition, zero cross-margin spillover risk\n"
                "• `Breakeven Armor` - Stop-loss ratchets to Entry + 0.12% fee floor when UPL >= +3.0% ROI\n"
                "• `Golden 85% Ratchet` - Permanently preserves 85% of peak unrealized high-water mark\n"
                "• `Anti-Oversold Short Guard` - RSI <= 38.0 strictly blocks short entries to eliminate dump chasing\n"
                "══════════════════════════════\n\n"
                "💎 **1. 24/7 Perpetual Wealth Generator:**\n"
                "• `/wealth [SPOT/FUTURES] [ON/OFF] [USDT]`\n"
                "  _Example:_ `/wealth FUTURES ON 100` | `/wealth STATUS`\n"
                "  Flagship engine. 100% full-position ride to peak exhaustion without premature 50% profit cuts.\n\n"
                "🚀 **2. Turbo Hedge HFT Multi-Coin Engine:**\n"
                "• `/turbo_hedge [TOP/COIN] [MARGIN] [LEVERAGE] [MODE] [PROFIT] [PIN]`\n"
                "  _Example:_ `/turbo_hedge TOP 20 10 AUTO 2.50 1234`\n"
                "  High-frequency dual-directional scanner with dynamic volatility breathing stops (>=2.20x ATR15m).\n\n"
                "👑 **3. Angkor Intelligence X (33 AI Model Swarm):**\n"
                "• `/smartx [COIN] [AUTO/TURBO/SONIC]`\n"
                "  _Example:_ `/smartx BTC AUTO`\n"
                "  Matrix intelligence analyzing real-time order flow, CVD absorption divergence, and macro regimes.\n\n"
                "🏓 **4. Micro-Volatility Scalper:**\n"
                "• `/scalp [PAIR] [USDT]`\n"
                "  _Example:_ `/scalp ETH 50`\n"
                "  Sub-minute liquidity scalp exploiting temporary orderbook imbalances.\n\n"
                "🦅 **5. Omni-Swarm Fleet Commander:**\n"
                "• `/command` or `/skynet`\n"
                "  Master autonomous orchestrator coordinating multi-strategy capital allocation.\n"
            )
        elif lang == "zh":
            text = (
                "🟡 **模块 2：合约与对冲引擎 [管理员深度模式 - 完整底层技术]** 🟡\n"
                "══════════════════════════════\n"
                "🛡️ **机构级风控标准 (AQ76 核心不变量)：**\n"
                "• `逐仓保证金 (10x)` - 严禁全仓，彻底杜绝账户资金连带清算风险\n"
                "• `保本装甲 (Breakeven Armor)` - 浮盈达到 +3% ROI 时，无条件上移止损至开仓价 + 0.12% 手续费\n"
                "• `黄金 85% 动态追踪` - 永久锁定最高峰值利润的 85%\n"
                "• `超卖防做空禁令` - RSI <= 38.0 时严禁盲目追空恐慌插针\n"
                "══════════════════════════════\n\n"
                "💎 **1. 24/7 永续财富引擎 (Perpetual Wealth):**\n"
                "• `/wealth [SPOT/FUTURES] [ON/OFF] [USDT]`\n"
                "  _示例:_ `/wealth FUTURES ON 100` | `/wealth STATUS`\n"
                "  核心旗舰引擎，100% 仓位全程护航至行情动能耗尽，拒绝过早减仓。\n\n"
                "🚀 **2. Turbo Hedge HFT 高频对冲引擎:**\n"
                "• `/turbo_hedge [TOP/币种] [保证金] [杠杆] [模式] [目标] [PIN]`\n"
                "  _示例:_ `/turbo_hedge TOP 20 10 AUTO 2.50 1234`\n"
                "  多币种 24/7 全自动高频双向对冲扫描器，自带波动率呼吸止损 (>=2.20x ATR15m)。\n\n"
                "👑 **3. SmartX 33 大 AI 模型集群:**\n"
                "• `/smartx [币种] [AUTO/TURBO/SONIC]`\n"
                "  _示例:_ `/smartx BTC AUTO`\n"
                "  实时分析订单簿深度、CVD 累积成交吸收背离与宏观市场政权。\n\n"
                "🏓 **4. 超精准微波动剥头皮 (Scalp):**\n"
                "• `/scalp [币种] [USDT]`\n"
                "  _示例:_ `/scalp ETH 50`\n"
                "  毫秒级捕捉订单簿瞬时失衡与微观流动性。\n\n"
                "🦅 **5. 全智能自主指挥官 (SkyNet):**\n"
                "• `/command` 或 `/skynet`\n"
                "  宏观自主协同编队，智能分配多策略资金权重。\n"
            )
        else:
            text = (
                "🟡 **ផ្នែកទី ២ ៖ FUTURES & HEDGE ENGINES [ADMIN VIEW - FULL TECHNICAL DEPTH]** 🟡\n"
                "══════════════════════════════\n"
                "🛡️ **ប្រព័ន្ធការពារដើមទុនកម្រិតស្ថាប័ន (AQ76 Master Invariants) ៖**\n"
                "• `ISOLATED MARGIN (10x)` - កាត់ផ្តាច់ហានិភ័យកាបូប មិនឱ្យឆ្លងចូលដើមទុនផ្សេង\n"
                "• `Breakeven Armor` - ចំណេញដល់ +3% ROI រុញ SL មកចំណុចដើម + 0.12% ថ្លៃសេវា ធានាថាមិនចាញ់\n"
                "• `Golden 85% Ratchet` - ចាក់សោរប្រាក់ចំណេញ 85% នៃកម្រិតខ្ពស់បំផុតមិនឱ្យបាត់បង់\n"
                "• `Anti-Oversold Short Guard` - RSI <= 38.0 ហាមដាច់ខាតមិនឱ្យ Short តាមគេកុំឱ្យជាប់អន្ទាក់\n"
                "══════════════════════════════\n\n"
                "💎 **១. 24/7 Perpetual Wealth Engine (ម៉ាស៊ីនទាញទ្រព្យស្វ័យប្រវត្ត) ៖**\n"
                "• `/wealth [SPOT/FUTURES] [ON/OFF] [USDT]`\n"
                "  _ឧទាហរណ៍ ៖_ `/wealth FUTURES ON 100` | `/wealth STATUS`\n"
                "  ម៉ាស៊ីនជើងឯក រត់ទាញយកប្រាក់ចំណេញ ១០០% ពេញលេញ រហូតដល់ចុងរលក ដោយគ្មានការកាត់ 50% ផ្ដាច់មុខ។\n\n"
                "🚀 **២. Turbo Hedge HFT (ម៉ាស៊ីនស្កេន និងការពារហានិភ័យល្បឿនលឿន) ៖**\n"
                "• `/turbo_hedge [TOP/COIN] [MARGIN] [LEVERAGE] [MODE] [PROFIT] [PIN]`\n"
                "  _ឧទាហរណ៍ ៖_ `/turbo_hedge TOP 20 10 AUTO 2.50 1234`\n"
                "  ស្កេនកាក់កំពូលៗក្នុងទីផ្សារ 24/7 បើក Position និងតាមការពារដើមទុន (>=2.20x ATR15m)។\n\n"
                "👑 **៣. Angkor Intelligence X (SmartX - 33 AI Swarm) ៖**\n"
                "• `/smartx [COIN] [AUTO/TURBO/SONIC]`\n"
                "  _ឧទាហរណ៍ ៖_ `/smartx BTC AUTO`\n"
                "  ប្រើប្រាស់ម៉ូឌែល AI ចំនួន ៣៣ វិភាគរួមគ្នាលើ Order Book, CVD Absorption Divergence និង Volume។\n\n"
                "🏓 **៤. Precision Micro Scalper ៖**\n"
                "• `/scalp [COIN] [USDT]`\n"
                "  _ឧទាហរណ៍ ៖_ `/scalp ETH 50`\n"
                "  ចាប់យករលកខ្លីៗល្បឿនលឿន ក្នុងរយៈពេលប៉ុន្មាននាទី។\n\n"
                "🦅 **៥. Omni-Swarm Master Commander ៖**\n"
                "• `/command` ឬ `/skynet`\n"
                "  បញ្ជាប្រព័ន្ធរ៉ាន់ស្វ័យប្រវត្តទាំងអស់ឱ្យដំណើរការរួមគ្នាប្រកបដោយសាមគ្គីភាព។\n"
            )
    else:
        # Public VIP User View (Zero Technical Formula Leakage - User Benefits & Safety)
        if lang == "en":
            text = (
                "🟡 **CATEGORY 2: FUTURES & HEDGE ENGINES (HIGH YIELD & RISK DEFENSE)** 🟡\n"
                "══════════════════════════════\n"
                "🛡️ **Institutional Protection Standards:**\n"
                "• `ISOLATED MARGIN` - Ring-fences trade margin, zero risk of spillover to other wallet funds\n"
                "• `Breakeven Armor` - Automatically moves stop-loss to entry once in profit, eliminating loss risk\n"
                "• `Dynamic Profit Lock` - Trails market highs to securely lock in captured gains\n"
                "• `Anti-Trap Guard` - Proprietary protection preventing emotional panic entries and sudden reversal traps\n"
                "══════════════════════════════\n\n"
                "💎 **1. 24/7 Perpetual Wealth Generator:**\n"
                "• `/wealth [SPOT/FUTURES] [ON/OFF] [USDT]`\n"
                "  _Example:_ `/wealth FUTURES ON 100` | `/wealth STATUS`\n"
                "  Core flagship engine capturing sustained market momentum while maintaining continuous capital armor.\n\n"
                "🚀 **2. Turbo Hedge Autonomous Engine:**\n"
                "• `/turbo_hedge [TOP/COIN] [MARGIN] [LEVERAGE] [MODE] [PROFIT] [PIN]`\n"
                "  _Example:_ `/turbo_hedge TOP 20 10 AUTO 2.50 1234`\n"
                "  High-speed dual-directional scanner monitoring top market opportunities 24/7.\n\n"
                "👑 **3. Angkor Intelligence X (SmartX Master Suite):**\n"
                "• `/smartx [COIN] [AUTO/TURBO/SONIC]`\n"
                "  _Example:_ `/smartx BTC AUTO`\n"
                "  Comprehensive market intelligence evaluating real-time momentum, trend strength, and execution clarity.\n\n"
                "🏓 **4. Precision Micro Scalper:**\n"
                "• `/scalp [PAIR] [USDT]`\n"
                "  _Example:_ `/scalp ETH 50`\n"
                "  Fast-turnaround scalping engine capturing intraday micro-swings.\n\n"
                "🦅 **5. Omni-Fleet Commander:**\n"
                "• `/command` or `/skynet`\n"
                "  Unified autonomous control coordinator balancing multiple strategy allocations.\n"
            )
        elif lang == "zh":
            text = (
                "🟡 **模块 2：合约与对冲引擎 (高频对冲与资金护盾)** 🟡\n"
                "══════════════════════════════\n"
                "🛡️ **机构级风控标准：**\n"
                "• `逐仓保证金模式` - 严格隔离交易本金，彻底杜绝钱包资金连带风险\n"
                "• `保本装甲护盾` - 盈利后自动上移止损锁定保本，消除亏损风险\n"
                "• `动态利润锁存` - 顺势跟随行情新高，智能锁定已捕获收益\n"
                "• `防诱导陷阱卫士` - 智能过滤恐慌杀跌与假突破诱多，杜绝追高杀跌\n"
                "══════════════════════════════\n\n"
                "💎 **1. 24/7 永续财富引擎 (Perpetual Wealth):**\n"
                "• `/wealth [SPOT/FUTURES] [ON/OFF] [USDT]`\n"
                "  _示例:_ `/wealth FUTURES ON 100` | `/wealth STATUS`\n"
                "  核心旗舰引擎，全程智能护航捕捉趋势红利，自带动态风控装甲。\n\n"
                "🚀 **2. Turbo Hedge 自动对冲引擎:**\n"
                "• `/turbo_hedge [TOP/币种] [保证金] [杠杆] [模式] [目标] [PIN]`\n"
                "  _示例:_ `/turbo_hedge TOP 20 10 AUTO 2.50 1234`\n"
                "  全天候自动扫描市场优质标的，智能执行对冲与风控。\n\n"
                "👑 **3. SmartX 核心智能旗舰套件:**\n"
                "• `/smartx [币种] [AUTO/TURBO/SONIC]`\n"
                "  _示例:_ `/smartx BTC AUTO`\n"
                "  综合多维度深度研判市场强弱与动能方向，保障决策确定性。\n\n"
                "🏓 **4. 极速微波动交易 (Scalp):**\n"
                "• `/scalp [币种] [USDT]`\n"
                "  _示例:_ `/scalp ETH 50`\n"
                "  敏锐捕捉日内短线波动机会，快进快出锁定收益。\n\n"
                "🦅 **5. 全自动编队指挥中心 (SkyNet):**\n"
                "• `/command` 或 `/skynet`\n"
                "  统一调度全套量化策略，科学平衡各模块资金权重。\n"
            )
        else:
            text = (
                "🟡 **ផ្នែកទី ២ ៖ FUTURES & HEDGE ENGINES (ម៉ាស៊ីនជួញដូរផលចំណេញខ្ពស់)** 🟡\n"
                "══════════════════════════════\n"
                "🛡️ **ប្រព័ន្ធការពារដើមទុនកម្រិតស្ថាប័ន ៖**\n"
                "• `ISOLATED MARGIN` - កាត់ផ្តាច់ហានិភ័យកាបូប មិនឱ្យឆ្លងចូលដើមទុនផ្សេង\n"
                "• `Breakeven Armor` - យន្តការរុញ Stop-Loss ការពារដើមទុនដោយស្វ័យប្រវត្ត ធានាថាមិនចាញ់\n"
                "• `Trailing Profit Lock` - ចាក់សោរប្រាក់ចំណេញតាមកំពូលទីផ្សារជាប់ជានិច្ច មិនឱ្យបាត់បង់មកវិញ\n"
                "• `Anti-Trap Guard` - ប្រព័ន្ធឆ្លាតវៃទប់ស្កាត់ការលក់តាមគេពេលទីផ្សារធ្លាក់គំហុក កុំឱ្យជាប់អន្ទាក់\n"
                "══════════════════════════════\n\n"
                "💎 **១. 24/7 Perpetual Wealth Engine (ម៉ាស៊ីនទាញទ្រព្យស្វ័យប្រវត្ត) ៖**\n"
                "• `/wealth [SPOT/FUTURES] [ON/OFF] [USDT]`\n"
                "  _ឧទាហរណ៍ ៖_ `/wealth FUTURES ON 100` | `/wealth STATUS`\n"
                "  ម៉ាស៊ីនជើងឯក ជួយទាញយកប្រាក់ចំណេញពេញលេញ និងតាមការពារដើមទុនជាប់ជានិច្ច។\n\n"
                "🚀 **២. Turbo Hedge HFT (ម៉ាស៊ីនស្កេន និងការពារហានិភ័យស្វ័យប្រវត្ត) ៖**\n"
                "• `/turbo_hedge [TOP/COIN] [MARGIN] [LEVERAGE] [MODE] [PROFIT] [PIN]`\n"
                "  _ឧទាហរណ៍ ៖_ `/turbo_hedge TOP 20 10 AUTO 2.50 1234`\n"
                "  ស្កេនកាក់កំពូលៗក្នុងទីផ្សារ 24/7 បើក Position និងតាមការពារដើមទុនដោយស្វ័យប្រវត្ត។\n\n"
                "👑 **៣. Angkor Intelligence X (SmartX Master Suite) ៖**\n"
                "• `/smartx [COIN] [AUTO/TURBO/SONIC]`\n"
                "  _ឧទាហរណ៍ ៖_ `/smartx BTC AUTO`\n"
                "  យន្តការវិភាគកម្លាំងទីផ្សារ និងទិសដៅច្បាស់លាស់ មុនពេលបញ្ជាជួញដូរ។\n\n"
                "🏓 **៤. Precision Micro Scalper ៖**\n"
                "• `/scalp [COIN] [USDT]`\n"
                "  _ឧទាហរណ៍ ៖_ `/scalp ETH 50`\n"
                "  ចាប់យករលកខ្លីៗល្បឿនលឿនក្នុងទីផ្សារ។\n\n"
                "🦅 **៥. Master Fleet Commander ៖**\n"
                "• `/command` ឬ `/skynet`\n"
                "  បញ្ជាប្រព័ន្ធរ៉ាន់ស្វ័យប្រវត្តទាំងអស់ឱ្យដំណើរការរួមគ្នាប្រកបដោយប្រសិទ្ធភាពខ្ពស់។\n"
            )

    keyboard = [
        [
            InlineKeyboardButton("💎 Launch Wealth 24/7", callback_data="btn_wealth"),
            InlineKeyboardButton("🚀 Launch Turbo Hedge", callback_data="btn_turbo_hedge")
        ],
        [
            InlineKeyboardButton("👑 Launch SmartX AI", callback_data="btn_smart_x_metrics"),
            InlineKeyboardButton("🦅 SkyNet Orchestrator", callback_data="btn_skynet")
        ],
        [
            InlineKeyboardButton("🔙 Back to Smart Hub", callback_data="smart_hub_home"),
            InlineKeyboardButton("🎛️ Master Control Panel", callback_data="btn_menu_refresh")
        ]
    ]
    return text, InlineKeyboardMarkup(keyboard)


# ==============================================================================
# 4. TRADFI & MT5 VIEW (Capital.com, Gold, Indices & Commodities)
# ==============================================================================
def _build_tradfi_view(is_admin: bool, lang: str, mode_badge: str) -> Tuple[str, InlineKeyboardMarkup]:
    if is_admin:
        # Super Admin View (Institutional TradFi Ground Truths - The Nine Pillars)
        if lang == "en":
            text = (
                "🔵 **CATEGORY 3: TRADFI GLOBAL MARKETS & MT5 SUITE [ADMIN VIEW - 9 PILLARS]** 🔵\n"
                "══════════════════════════════\n"
                "🛡️ **Institutional TradFi Ground Truths (AQ76 Nine Pillars):**\n"
                "• `In-Memory Stealth Breakout Radar` - Zero resting orders on broker, 100% immune to stop-hunt wicks\n"
                "• `Spread Drag Elimination` - Take-Profit distance >= 10x Spread, converting >=90% movement into clean cash\n"
                "• `Delayed Breakeven Armor` - Delayed until UPL >= $2.50 & ROI >= +8.5%, eliminating crumb choking\n"
                "• `Overnight Swap Shield` - Strict lockout before 21:00 UTC rollover; Wednesday 3x swap completely blocked\n"
                "• `Universal Forex Kill-Switch` - Forex exchange 100% disabled; capital locked to Gold, Indices & US Equities\n"
                "══════════════════════════════\n\n"
                "🏛️ **1. Capital.com Institutional TradFi Engine:**\n"
                "• `/capital` - Master Capital.com Dashboard & Autonomous Scanner\n"
                "  _Assets:_ GOLD (XAUUSD), US100 (Nasdaq), US500 (S&P), Crude Oil, Mega-Cap Stocks (NVDA, TSLA, AAPL, MSFT)\n\n"
                "⚡ **2. Tokyo GTCFX MT5 Institutional Bridge:**\n"
                "• `/mt5` - MT5 Bridge Dashboard & Sub-15ms Master Liquidity Pool\n"
                "• `/mt5_smart` - Super Smart MT5 8-Pillar Trap Matrix & Interbank Kill Zones\n"
                "• `/mt5_reachsey` - Reachsey 5-Position Matrix Basket Sweeper\n\n"
                "📈 **3. 24/7 Trend Scalping Engine:**\n"
                "• `/capital_scalp [ON/OFF] [USDT]`\n"
                "  3-EMA confluence trend scalper riding momentum on US Tech & Gold.\n\n"
                "🎯 **4. London & NY 15m Opening Range Breakout (ORB):**\n"
                "• `/capital_orb`\n"
                "  Captures explosive opening volatility at London Cash Open (14:00 ICT) and NY Wall Street Open (20:30 ICT).\n\n"
                "🤝 **5. Institutional IB Rebates & Partner Commission:**\n"
                "• `/capital_ib`\n"
                "  30% - 50% spread rebate tracking directly back to VIP accounts.\n"
            )
        elif lang == "zh":
            text = (
                "🔵 **模块 3：全球 TradFi 传统金融与 MT5 机构套件 [管理员深度模式 - 九大支柱]** 🔵\n"
                "══════════════════════════════\n"
                "🛡️ **TradFi 机构级核心风控 (AQ76 九大支柱)：**\n"
                "• `内存隐形突破雷达` - 券商端零挂单，100% 免疫机构插针诱空与扫损洗盘\n"
                "• `点差磨损消除机制` - 止盈距离 >= 10倍点差，确保 90% 以上行情净转化落袋\n"
                "• `延迟保本装甲` - 浮盈达到 $2.50 且 ROI >= +8.5% 才锁定，彻底杜绝几毛钱的碎屑出局\n"
                "• `隔夜利息防护与周三 3 倍利息锁死` - 21:00 UTC 滚动前平仓，杜绝高额隔夜利息\n"
                "• `多层外汇拦截盾` - 外汇全线禁用，资金锁定于黄金、美股科技巨头与股指\n"
                "══════════════════════════════\n\n"
                "🏛️ **1. Capital.com 全球机构交易引擎:**\n"
                "• `/capital` - 核心 TradFi 控制面板与全自动扫描\n"
                "  _标的:_ 现货黄金 (XAUUSD), 纳斯达克 100, 标普 500, 原油, 美股巨头 (NVDA, TSLA, AAPL, MSFT)\n\n"
                "⚡ **2. 东京 GTCFX MT5 机构网桥:**\n"
                "• `/mt5` - MT5 机构主控台与低延迟流动性池\n"
                "• `/mt5_smart` - 8 大机构陷阱矩阵与银行间 Kill Zone 监控\n"
                "• `/mt5_reachsey` - Reachsey 5 仓位矩阵一键式自动清道夫\n\n"
                "📈 **3. 24/7 趋势剥头皮引擎:**\n"
                "• `/capital_scalp [ON/OFF] [USDT]`\n"
                "  3-EMA 多周期趋势顺势交易，专攻黄金与美股科技股。\n\n"
                "🎯 **4. 伦敦与纽约 15 分钟首根 K 线突破 (ORB):**\n"
                "• `/capital_orb`\n"
                "  捕捉伦敦开盘 (14:00 ICT) 与纽约华尔街开盘 (20:30 ICT) 的瞬时爆发动能。\n\n"
                "🤝 **5. 机构 IB 点差返佣 (30%-50%):**\n"
                "• `/capital_ib`\n"
                "  直连券商机构返佣结算系统，自动返现至 VIP 账户。\n"
            )
        else:
            text = (
                "🔵 **ផ្នែកទី ៣ ៖ TRADFI GLOBAL MARKETS & MT5 [ADMIN VIEW - THE NINE PILLARS]** 🔵\n"
                "══════════════════════════════\n"
                "🛡️ **គ្រឹះ ៩ ប្រការស្ថាបត្យករ TradFi (AQ76 Ground Truths) ៖**\n"
                "• `In-Memory Stealth Breakout Radar` - ចាប់ទិសដៅក្នុង RAM មិនផ្ញើ Pending Order ទៅ Broker ការពារការបរបាញ់ SL ១០០%\n"
                "• `Spread Drag Elimination` - ចម្ងាយ TP ធំជាង Spread ១០ ដង ធានាថាប្រាក់ចំណេញ ៩០% ចូលហោប៉ៅពិតប្រាកដ\n"
                "• `Delayed Breakeven Armor` - ពន្យាពេលដាក់ BE រហូតដល់ UPL >= $2.50 & ROI >= +8.5% ការពារការកាត់ចំណេញកម្ទេចកម្ទី\n"
                "• `Overnight Swap Shield` - បិទទីផ្សារមុនម៉ោង 21:00 UTC Rollover និងបិទយប់ថ្ងៃពុធ ជម្រះថ្លៃ Swap ឆ្លងយប់ ៣០០%\n"
                "• `Universal Forex Kill-Switch` - បិទ Forex ១០០% ផ្ដោតតែលើ មាស (Gold), ប្រេងឆៅ, សន្ទស្សន៍ US100/US500 និងហ៊ុនបច្ចេកវិទ្យា\n"
                "══════════════════════════════\n\n"
                "🏛️ **១. Capital.com Institutional TradFi Engine ៖**\n"
                "• `/capital` - ផ្ទាំងបញ្ជា Capital.com & ម៉ាស៊ីនស្កេនស្វ័យប្រវត្ត\n"
                "  _ទ្រព្យសម្បត្តិ ៖_ មាស GOLD (XAUUSD), US100 (Nasdaq), US500 (S&P), ប្រេងឆៅ Oil, ហ៊ុនយក្ស (NVDA, TSLA, AAPL, MSFT)\n\n"
                "⚡ **២. MetaTrader 5 (MT5 Tokyo Bridge) ៖**\n"
                "• `/mt5` - MT5 Bridge Master Pool (Latency <15ms)\n"
                "• `/mt5_smart` - Super Smart MT5 8-Pillar Trap Matrix & Interbank Kill Zones\n"
                "• `/mt5_reachsey` - Reachsey 5-Position Matrix Basket Sweeper\n\n"
                "📈 **៣. 24/7 Trend Scalping Engine ៖**\n"
                "• `/capital_scalp [ON/OFF] [USDT]`\n"
                "  ម៉ាស៊ីនចាប់ Trend តាម 3-EMA Confluence លើមាស និងបច្ចេកវិទ្យាអាមេរិក។\n\n"
                "🎯 **៤. London & NY 15m Opening Range Breakout (ORB) ៖**\n"
                "• `/capital_orb`\n"
                "  ស្ទាក់ចាប់កម្លាំងផ្ទុះពេលទីផ្សារ London បើក (14:00 ICT) និង Wall Street បើក (20:30 ICT)។\n\n"
                "🤝 **៥. Institutional IB Rebates (កម្រៃជើងសារ 30%-50%) ៖**\n"
                "• `/capital_ib`\n"
                "  តាមដាន និងបើកប្រាក់ Rebate ពី Broker ត្រឡប់មកក្នុងកាបូប VIP វិញដោយស្វ័យប្រវត្ត។\n"
            )
    else:
        # Public VIP User View (Zero Technical Secrets - User Benefits & Safe Guidance)
        if lang == "en":
            text = (
                "🔵 **CATEGORY 3: TRADFI GLOBAL MARKETS & MT5 SUITE** 🔵\n"
                "══════════════════════════════\n"
                "🛡️ **Institutional TradFi Protection Standards:**\n"
                "• `Broker Slippage Shield` - Advanced spread optimization ensuring maximum captured movement converts to net profit\n"
                "• `Capital Growth Armor` - Dynamic breakeven protection securing realized gains as trades advance\n"
                "• `Overnight Fee Protection` - Automated protection against costly overnight financing charges\n"
                "• `Institutional Asset Focus` - Focused strictly on global power assets: Gold (XAUUSD), US Indices, and Tech Leaders\n"
                "══════════════════════════════\n\n"
                "🏛️ **1. Capital.com Global Markets Engine:**\n"
                "• `/capital` - Master Global Markets Dashboard & Scanner\n"
                "  _Assets:_ GOLD (XAUUSD), US100 (Nasdaq), US500 (S&P), Crude Oil, Mega-Cap Stocks (NVDA, TSLA, AAPL, MSFT)\n\n"
                "⚡ **2. MetaTrader 5 (MT5 Tokyo Suite):**\n"
                "• `/mt5` - MT5 Gateway & High-Speed Liquidity Access\n"
                "• `/mt5_smart` - Smart Institutional Execution & Risk Controls\n"
                "• `/mt5_reachsey` - Multi-Position Basket Portfolio Manager\n\n"
                "📈 **3. 24/7 Global Trend Scalper:**\n"
                "• `/capital_scalp [ON/OFF] [USDT]`\n"
                "  Trend scalping engine capturing directional momentum on Gold and US Tech.\n\n"
                "🎯 **4. Market Opening Momentum Engine (ORB):**\n"
                "• `/capital_orb`\n"
                "  Captures prime momentum during major international market opening sessions.\n\n"
                "🤝 **5. Partner Commission & Rebates:**\n"
                "• `/capital_ib`\n"
                "  Tracks broker rebates credited back to your account.\n"
            )
        elif lang == "zh":
            text = (
                "🔵 **模块 3：全球 TradFi 传统金融与 MT5 机构套件** 🔵\n"
                "══════════════════════════════\n"
                "🛡️ **TradFi 全球市场风控标准：**\n"
                "• `点差滑点优化盾` - 精准优化交易成本，确保行情收益最大化转化为账户净利\n"
                "• `收益安全装甲` - 顺势自动上移保本，锁定已实现成果\n"
                "• `隔夜利息防护` - 智能规避高昂隔夜持仓利息，守护本金安全\n"
                "• `核心资产聚焦` - 严选全球优质标的：现货黄金 (XAUUSD)、美股指数与科技巨头\n"
                "══════════════════════════════\n\n"
                "🏛️ **1. Capital.com 全球市场引擎:**\n"
                "• `/capital` - 全球资产控制面板与自动扫描\n"
                "  _标的:_ 现货黄金 (XAUUSD), 纳斯达克 100, 标普 500, 原油, 美股巨头 (NVDA, TSLA, AAPL, MSFT)\n\n"
                "⚡ **2. 东京 MT5 机构交易套件:**\n"
                "• `/mt5` - MT5 交易主网关与高速流动性通道\n"
                "• `/mt5_smart` - 智能机构风控与策略执行中心\n"
                "• `/mt5_reachsey` - 多仓位篮子组合资产管理器\n\n"
                "📈 **3. 24/7 趋势追踪交易 (Trend Scalp):**\n"
                "• `/capital_scalp [ON/OFF] [USDT]`\n"
                "  顺势交易引擎，专注捕获黄金与美股科技股主升行情。\n\n"
                "🎯 **4. 核心开盘爆发动能引擎 (ORB):**\n"
                "• `/capital_orb`\n"
                "  精准捕捉全球主要金融中心开盘时段的爆发性动能红利。\n\n"
                "🤝 **5. 机构返佣管理 (IB Rebates):**\n"
                "• `/capital_ib`\n"
                "  实时跟踪与结算券商返还至 VIP 账户的点差返佣。\n"
            )
        else:
            text = (
                "🔵 **ផ្នែកទី ៣ ៖ TRADFI GLOBAL MARKETS & MT5 (មាស, ប្រេង, ហ៊ុនអាមេរិក)** 🔵\n"
                "══════════════════════════════\n"
                "🛡️ **ស្តង់ដារការពារដើមទុន TradFi Global Markets ៖**\n"
                "• `Broker Slippage Shield` - យន្តការការពារថ្លៃសេវា Spread ធានាឱ្យការជួញដូរទទួលបានប្រាក់ចំណេញសុទ្ធខ្ពស់\n"
                "• `Capital Growth Armor` - ប្រព័ន្ធចាក់សោរប្រាក់ចំណេញសុវត្ថិភាព មិនឱ្យប្រាក់ចំណេញក្លាយជាខាត\n"
                "• `Overnight Fee Protection` - ប្រព័ន្ធការពារហានិភ័យ និងកម្រៃសេវាឆ្លងយប់ដោយស្វ័យប្រវត្ត\n"
                "• `Institutional Asset Focus` - ផ្ដោតលើទ្រព្យសម្បត្តិលំដាប់ពិភពលោក (មាស Gold, ប្រេង, សន្ទស្សន៍អាមេរិក និងភាគហ៊ុនបច្ចេកវិទ្យា)\n"
                "══════════════════════════════\n\n"
                "🏛️ **១. Capital.com Global Markets Engine ៖**\n"
                "• `/capital` - ផ្ទាំងបញ្ជាជួញដូរទីផ្សារសកលលោក Capital.com\n"
                "  _ទ្រព្យសម្បត្តិ ៖_ មាស GOLD (XAUUSD), US100 (Nasdaq), US500 (S&P), ប្រេងឆៅ Oil, ហ៊ុនយក្ស (NVDA, TSLA, AAPL, MSFT)\n\n"
                "⚡ **២. MetaTrader 5 (MT5 Tokyo Suite) ៖**\n"
                "• `/mt5` - MT5 Gateway Master Pool (ល្បឿនលឿន Latency <15ms)\n"
                "• `/mt5_smart` - Smart MT5 Institutional Execution & Risk Controls\n"
                "• `/mt5_reachsey` - Reachsey Multi-Position Basket Manager\n\n"
                "📈 **៣. 24/7 Global Trend Scalper ៖**\n"
                "• `/capital_scalp [ON/OFF] [USDT]`\n"
                "  ម៉ាស៊ីនចាប់ឱកាស Trend លើមាស និងភាគហ៊ុនបច្ចេកវិទ្យាអាមេរិក។\n\n"
                "🎯 **៤. Market Opening Momentum Engine (ORB) ៖**\n"
                "• `/capital_orb`\n"
                "  ចាប់ឱកាសប្រាក់ចំណេញពេលទីផ្សារអន្តរជាតិធំៗបើកដំណើរការជួញដូរ។\n\n"
                "🤝 **៥. Institutional IB Rebates (កម្រៃជើងសារត្រឡប់មកវិញ) ៖**\n"
                "• `/capital_ib`\n"
                "  តាមដាន និងបើកប្រាក់ Rebate ពី Broker ត្រឡប់មកក្នុងកាបូប VIP វិញដោយស្វ័យប្រវត្ត។\n"
            )

    keyboard = [
        [
            InlineKeyboardButton("🏛️ Capital.com TradFi", callback_data="btn_capital_menu"),
            InlineKeyboardButton("⚡ MT5 Tokyo Bridge", callback_data="btn_mt5_menu")
        ],
        [
            InlineKeyboardButton("📈 Capital Scalp", callback_data="btn_cap_scalp_refresh"),
            InlineKeyboardButton("🤝 IB Rebates", callback_data="btn_capital_ib")
        ],
        [
            InlineKeyboardButton("🔙 Back to Smart Hub", callback_data="smart_hub_home"),
            InlineKeyboardButton("🎛️ Master Control Panel", callback_data="btn_menu_refresh")
        ]
    ]
    return text, InlineKeyboardMarkup(keyboard)


# ==============================================================================
# 5. AI RADARS & INTELLIGENCE VIEW
# ==============================================================================
def _build_radars_view(is_admin: bool, lang: str, mode_badge: str) -> Tuple[str, InlineKeyboardMarkup]:
    if is_admin:
        # Super Admin View (Institutional Deep Architecture & Model Telemetry)
        if lang == "en":
            text = (
                "🟣 **CATEGORY 4: AI INTELLIGENCE, RADARS & FORECASTING [ADMIN VIEW]** 🟣\n"
                "══════════════════════════════\n"
                "🧠 **AI Brain**: Google Gemini 2.5 Flash + Hugging Face Cloud Inference (DeepSeek-R1 & Llama-3-70B)\n"
                "⚡ **Inference Standard**: Real-Time CVD Absorption, Liquidity Sweep & 16-Model ML K-Line Prediction\n"
                "══════════════════════════════\n\n"
                "🧠 **1. 360° Multi-Agent Technical Analysis:**\n"
                "• `/analyze <COIN>`\n"
                "  _Example:_ `/analyze BTC` | `/analyze ETH`\n"
                "  Full institutional evaluation across RSI, MACD, Orderflow, CVD Absorption, Liquidity Sweep, and Trap Matrix.\n\n"
                "📈 **2. Wall Street 16-Model ML Price & Trend Forecast:**\n"
                "• `/predict <COIN>`\n"
                "  _Example:_ `/predict SOL` | `/predict NVDA`\n"
                "  24-Hour K-Line probability forecast with directional win-rate confidence score.\n\n"
                "📰 **3. Journalistic AI Crypto News & Impact:**\n"
                "• `/news`\n"
                "  Instant 3-paragraph news breakdown with financial sentiment and macroeconomic impact assessment.\n\n"
                "🐋 **4. Whale Orderflow & Dark Pool Radar:**\n"
                "• `/whales`\n"
                "  Real-time tracking of massive on-chain and exchange whale transactions (> $1,000,000).\n\n"
                "🎯 **5. Flash Crash & Liquidation Cascade Hunter:**\n"
                "• `/flash_crash`\n"
                "  Identifies deep wick cascading liquidation events for instant mean-reversion snipes.\n\n"
                "🔥 **6. Pre-Pump Accumulation Radar:**\n"
                "• `/pre_pump`\n"
                "  Detects stealth institutional wallet accumulation prior to major market breakouts.\n\n"
                "🏛️ **7. Cambodia Stock Exchange (CSX) AI Radar:**\n"
                "• `/csx`\n"
                "  Live CSX equity telemetry, volume spikes, dividend yields, and closing reports.\n"
            )
        elif lang == "zh":
            text = (
                "🟣 **模块 4：AI 智能情报、市场雷达与行情预测 [管理员深度模式]** 🟣\n"
                "══════════════════════════════\n"
                "🧠 **核心算力**: Google Gemini 2.5 Flash + Hugging Face 深度推理集群 (DeepSeek-R1 / Llama-3-70B)\n"
                "⚡ **量化标准**: 实时 CVD 累积吸收、流动性掠夺与 16 机器学习模型 24H K 线预测\n"
                "══════════════════════════════\n\n"
                "🧠 **1. 360° 多智能体全景技术分析:**\n"
                "• `/analyze <币种>`\n"
                "  _示例:_ `/analyze BTC` | `/analyze ETH`\n"
                "  综合分析 RSI、MACD、订单流、CVD 成交吸收、流动性掠夺与陷阱清除。\n\n"
                "📈 **2. 华尔街 16 机器学习模型 24 小时 K 线预测:**\n"
                "• `/predict <币种>`\n"
                "  _示例:_ `/predict SOL` | `/predict NVDA`\n"
                "  预测未来 24 小时价格走势、支撑阻力位与方向胜率概率。\n\n"
                "📰 **3. 3段式 AI 权威快讯与影响评级:**\n"
                "• `/news`\n"
                "  提炼全球最新宏观与加密重大资讯，提供量化情绪评级。\n\n"
                "🐋 **4. 链上巨鲸与暗盘雷达:**\n"
                "• `/whales`\n"
                "  实时追踪百万美元级以上巨鲸大单流动与交易所转账。\n\n"
                "🎯 **5. 闪崩瀑布与深度插针捕手:**\n"
                "• `/flash_crash`\n"
                "  精准捕捉多头/空头连环踩踏爆仓插针，执行均值回归狙击。\n\n"
                "🔥 **6. 暴涨前蓄势吸筹雷达:**\n"
                "• `/pre_pump`\n"
                "  在代币主升浪启动前，敏锐识别主力和做市商的静默建仓。\n\n"
                "🏛️ **7. 柬埔寨证券交易所 (CSX) 量化雷达:**\n"
                "• `/csx`\n"
                "  实时 CSX 股市看板、高分红股票排行与成交量异动监测。\n"
            )
        else:
            text = (
                "🟣 **ផ្នែកទី ៤ ៖ AI RADARS, ព័ត៌មាន & ការទស្សន៍ទាយទីផ្សារ [ADMIN VIEW]** 🟣\n"
                "══════════════════════════════\n"
                "🧠 **AI Brain**: Google Gemini 2.5 Flash + Hugging Face DeepSeek-R1 & Llama-3-70B\n"
                "⚡ **Inference Standard**: CVD Absorption, Liquidity Sweep & 16-Model ML K-Line Prediction\n"
                "══════════════════════════════\n\n"
                "🧠 **១. 360° Multi-Agent Technical Analysis ៖**\n"
                "• `/analyze <COIN>`\n"
                "  _ឧទាហរណ៍ ៖_ `/analyze BTC` | `/analyze ETH`\n"
                "  AI វិភាគបច្ចេកទេសគ្រប់ជ្រុងជ្រោយ (RSI, MACD, Volume, Order Flow, CVD & Trap Clearance)។\n\n"
                "📈 **២. ML 24h K-Line Trend & Win-Rate Forecast ៖**\n"
                "• `/predict <COIN>`\n"
                "  _ឧទាហរណ៍ ៖_ `/predict SOL` | `/predict NVDA`\n"
                "  ទស្សន៍ទាយទិសដៅតម្លៃទីផ្សាររយៈពេល ២៤ ម៉ោងខាងមុខ ជាមួយភាគរយ Win Rate នៃកាក់នីមួយៗ។\n\n"
                "📰 **៣. AI Financial News & Macro Sentiment ៖**\n"
                "• `/news`\n"
                "  ព័ត៌មានហិរញ្ញវត្ថុ និង Crypto សង្ខេប ៣ កថាខណ្ឌខ្លីៗ វិភាគផលប៉ះពាល់លើទីផ្សារ Real-Time។\n\n"
                "🐋 **៤. Whale & Dark Pool Radar ៖**\n"
                "• `/whales`\n"
                "  តាមដានចលនា Wallet របស់ត្រីបាឡែនធំៗ (> $1,000,000) ដែលកំពុងរុញទីផ្សារ។\n\n"
                "🎯 **៥. Flash Crash Wick Hunter ៖**\n"
                "• `/flash_crash`\n"
                "  ស្ទាក់ចាប់កាក់ដែលធ្លាក់គំហុកដោយសារ Liquidation Cascade ដើម្បីចូលទិញនៅចំណុចបាតបំផុត។\n\n"
                "🔥 **៦. Pre-Pump Accumulation Radar ៖**\n"
                "• `/pre_pump`\n"
                "  រ៉ាដាចាប់សញ្ញាកាក់ដែលកំពុងមានស្ថាប័នធំៗលួចទិញប្រមូលទុក មុនពេលតម្លៃហោះឡើងខ្លាំង។\n\n"
                "🏛️ **៧. Cambodia Stock Exchange (CSX) AI Radar ៖**\n"
                "• `/csx`\n"
                "  រ៉ាដាផ្សារភាគហ៊ុនកម្ពុជា មើលទិន្នន័យ Volume, ភាគលាភខ្ពស់ និងរបាយការណ៍បិទផ្សារប្រចាំថ្ងៃ។\n"
            )
    else:
        # Public VIP User View (Zero Technical Secrets - User Benefits & Strategic Clarity)
        if lang == "en":
            text = (
                "🟣 **CATEGORY 4: AI INTELLIGENCE, RADARS & FORECASTING** 🟣\n"
                "══════════════════════════════\n"
                "🧠 Powered by Angkor Quant Proprietary Quantitative Intelligence Engine\n"
                "══════════════════════════════\n\n"
                "🧠 **1. 360° Multi-Angle Market Analysis:**\n"
                "• `/analyze <COIN>`\n"
                "  _Example:_ `/analyze BTC` | `/analyze ETH`\n"
                "  Comprehensive institutional evaluation of market structure, volume profile, momentum, and risk balance.\n\n"
                "📈 **2. 24-Hour Trend & Probability Forecast:**\n"
                "• `/predict <COIN>`\n"
                "  _Example:_ `/predict SOL` | `/predict NVDA`\n"
                "  24-Hour market directional outlook and confidence probability scoring.\n\n"
                "📰 **3. Financial News & Market Impact Assessment:**\n"
                "• `/news`\n"
                "  Curated 3-paragraph executive summary of global financial news and market sentiment.\n\n"
                "🐋 **4. Whale Capital & Flow Radar:**\n"
                "• `/whales`\n"
                "  Real-time tracking of major institutional capital flows and high-volume transactions.\n\n"
                "🎯 **5. Flash Crash Liquidation Reversal Hunter:**\n"
                "• `/flash_crash`\n"
                "  Identifies extreme sudden market overextension for high-probability rebound entries.\n\n"
                "🔥 **6. Pre-Breakout Accumulation Radar:**\n"
                "• `/pre_pump`\n"
                "  Detects stealth institutional accumulation prior to major directional expansions.\n\n"
                "🏛️ **7. Cambodia Securities Exchange (CSX) Radar:**\n"
                "• `/csx`\n"
                "  Live CSX market telemetry, top dividend stocks, and daily trading session summaries.\n"
            )
        elif lang == "zh":
            text = (
                "🟣 **模块 4：AI 智能情报、市场雷达与行情研判** 🟣\n"
                "══════════════════════════════\n"
                "🧠 由 Angkor Quant 机构级量化智能引擎驱动\n"
                "══════════════════════════════\n\n"
                "🧠 **1. 360° 多维度全景技术分析:**\n"
                "• `/analyze <币种>`\n"
                "  _示例:_ `/analyze BTC` | `/analyze ETH`\n"
                "  全景评估标的趋势结构、成交量分布、多空动能与风控安全边界。\n\n"
                "📈 **2. 24 小时趋势与胜率概率预测:**\n"
                "• `/predict <币种>`\n"
                "  _示例:_ `/predict SOL` | `/predict NVDA`\n"
                "  研判未来 24 小时走势方向、关键支撑阻力位与胜率信心评分。\n\n"
                "📰 **3. 精炼财经快讯与量化情绪评估:**\n"
                "• `/news`\n"
                "  提炼全球最新宏观与行业重大资讯，量化评估对行情的真实影响。\n\n"
                "🐋 **4. 大单异动与主力资金雷达:**\n"
                "• `/whales`\n"
                "  实时监测全球主力大单异动与关键资金流向。\n\n"
                "🎯 **5. 闪崩极速反弹猎手:**\n"
                "• `/flash_crash`\n"
                "  捕捉市场短线非理性踩踏后的黄金均值回归反弹机会。\n\n"
                "🔥 **6. 爆发前蓄势建仓雷达:**\n"
                "• `/pre_pump`\n"
                "  在主升浪展开前，精准识别潜在标的的主力低位吸筹信号。\n\n"
                "🏛️ **7. 柬埔寨证券交易所 (CSX) 量化雷达:**\n"
                "• `/csx`\n"
                "  实时 CSX 股市看板、高分红龙头与每日收盘全景报告。\n"
            )
        else:
            text = (
                "🟣 **ផ្នែកទី ៤ ៖ AI RADARS, ព័ត៌មាន & ការទស្សន៍ទាយទីផ្សារ** 🟣\n"
                "══════════════════════════════\n"
                "🧠 ដំណើរការដោយប្រព័ន្ធឆ្លាតវៃ Angkor Quant Quantitative AI Intelligence\n"
                "══════════════════════════════\n\n"
                "🧠 **១. 360° Comprehensive Market Analysis ៖**\n"
                "• `/analyze <COIN>`\n"
                "  _ឧទាហរណ៍ ៖_ `/analyze BTC` | `/analyze ETH`\n"
                "  វិភាគស្ថានភាពទីផ្សារគ្រប់ជ្រុងជ្រោយ (ទិសដៅ, កម្លាំងទិញលក់, Volume និងសុវត្ថិភាព)។\n\n"
                "📈 **២. 24h Market Trend & Forecast ៖**\n"
                "• `/predict <COIN>`\n"
                "  _ឧទាហរណ៍ ៖_ `/predict SOL` | `/predict NVDA`\n"
                "  ទស្សន៍ទាយទិសដៅតម្លៃទីផ្សាររយៈពេល ២៤ ម៉ោងខាងមុខ ជាមួយភាគរយជោគជ័យជាក់លាក់។\n\n"
                "📰 **៣. Financial News & Market Sentiment ៖**\n"
                "• `/news`\n"
                "  ព័ត៌មានហិរញ្ញវត្ថុ និង Crypto សង្ខេប ៣ កថាខណ្ឌខ្លីៗ វិភាគផលប៉ះពាល់លើទីផ្សារ Real-Time។\n\n"
                "🐋 **៤. Whale Capital Flow Radar ៖**\n"
                "• `/whales`\n"
                "  តាមដានចលនាលុយធំៗរបស់ស្ថាប័នវិនិយោគដែលកំពុងជួញដូរក្នុងទីផ្សារ។\n\n"
                "🎯 **៥. Reversal & Dip Hunter ៖**\n"
                "• `/flash_crash`\n"
                "  ស្ទាក់ចាប់ឱកាសកាក់ដែលធ្លាក់គំហុក ដើម្បីចូលទិញនៅចំណុចបាតមានសុវត្ថិភាព។\n\n"
                "🔥 **៦. Pre-Breakout Accumulation Radar ៖**\n"
                "• `/pre_pump`\n"
                "  រ៉ាដាចាប់សញ្ញាកាក់ដែលកំពុងមានការប្រមូលទិញទុក មុនពេលតម្លៃហោះឡើងខ្លាំង។\n\n"
                "🏛️ **៧. Cambodia Stock Exchange (CSX) Radar ៖**\n"
                "• `/csx`\n"
                "  រ៉ាដាផ្សារភាគហ៊ុនកម្ពុជា មើលទិន្នន័យ Volume, ភាគលាភខ្ពស់ និងរបាយការណ៍បិទផ្សារប្រចាំថ្ងៃ។\n"
            )

    keyboard = [
        [
            InlineKeyboardButton("🧠 5-Agent Analysis", callback_data="btn_analyze_prompt"),
            InlineKeyboardButton("📈 ML 24h Forecast", callback_data="btn_predict_prompt")
        ],
        [
            InlineKeyboardButton("📰 Crypto News", callback_data="btn_news_refresh"),
            InlineKeyboardButton("🐋 Whale Radar", callback_data="btn_whales_refresh")
        ],
        [
            InlineKeyboardButton("🏛️ CSX Stocks", callback_data="csx_view_overview"),
            InlineKeyboardButton("🔥 Top Gainers", callback_data="btn_top_gainers")
        ],
        [
            InlineKeyboardButton("🔙 Back to Smart Hub", callback_data="smart_hub_home"),
            InlineKeyboardButton("🎛️ Master Control Panel", callback_data="btn_menu_refresh")
        ]
    ]
    return text, InlineKeyboardMarkup(keyboard)


# ==============================================================================
# 6. PORTFOLIO & SECURITY VIEW
# ==============================================================================
def _build_security_view(is_admin: bool, lang: str, mode_badge: str) -> Tuple[str, InlineKeyboardMarkup]:
    if lang == "en":
        text = (
            "🔴 **CATEGORY 5: PORTFOLIO, RISK & ACCOUNT SECURITY** 🔴\n"
            "══════════════════════════════\n"
            "🔒 **Enterprise Security Architecture:** 2FA Security PIN, isolated API keys, and multi-tier emergency stop protocols.\n"
            "══════════════════════════════\n\n"
            "💼 **1. Unified Portfolio & Net PnL:**\n"
            "• `/portfolio`\n"
            "  Live inspection of total portfolio equity, active positions, and unrealized/realized PnL.\n\n"
            "💰 **2. Real-Time Multi-Wallet Balances:**\n"
            "• `/balance`\n"
            "  Inspects Binance Spot, USDT-M Futures, Capital.com, and MT5 available balances.\n\n"
            "📊 **3. Live Engine Status & Active Orders:**\n"
            "• `/status`\n"
            "  Real-time telemetry of all running autonomous bots across Spot, Futures, and TradFi.\n\n"
            "📓 **4. Trading Journal & Mistake Tagging:**\n"
            "• `/journal`\n"
            "  Logs every trade decision, emotional discipline rating, and quant mistake tagging.\n\n"
            "📊 **5. Institutional Multi-Timeframe Audit Report:**\n"
            "• `/report` | `/audit` | `/daily_audit`\n"
            "  Detailed daily and monthly audit breakdown with Sharpe Ratio and Max Drawdown.\n\n"
            "🛑 **6. Emergency Kill Switch (Stop Trading):**\n"
            "• `/stop ALL` - Instantly cancels orders and terminates all active bots.\n"
            "• `/stop <COIN>` - Safely closes positions and stops trading for a single asset.\n\n"
            "🔒 **7. Security 2FA PIN & Recovery:**\n"
            "• `/set_pin <PIN>` - Configure your 4-6 digit security PIN for critical executions.\n"
            "• `/reset_pin` - Emergency 2FA security PIN recovery protocol.\n\n"
            "🧪 **8. Simulation vs Live Real Trading Mode (Admin Only):**\n"
            "• `/paper_trading` - Toggle between Paper Simulation and Real Live Capital (Super Admin Only).\n\n"
            "📜 **9. Terms, Legal Agreement & Risk Waiver:**\n"
            "• `/about` | `/agreement` - Review client agreements, terms of service, and risk disclosures.\n"
        )
    elif lang == "zh":
        text = (
            "🔴 **模块 5：资产组合、账户安全与风控熔断** 🔴\n"
            "══════════════════════════════\n"
            "🔒 **企业级安全架构：** 2FA 安全 PIN 码、API 权限物理隔离与多级紧急平仓熔断协议。\n"
            "══════════════════════════════\n\n"
            "💼 **1. 统一投资组合与净盈亏 (PnL):**\n"
            "• `/portfolio`\n"
            "  实时查询账户总净值、所有进行中的持仓明细与未实现盈亏。\n\n"
            "💰 **2. 多钱包实时资金余额:**\n"
            "• `/balance`\n"
            "  实时查询 Binance 现货、合约钱包、Capital.com 与 MT5 可用资金。\n\n"
            "📊 **3. 运行中引擎与订单实时状态:**\n"
            "• `/status`\n"
            "  查看全天候运行中的各策略机器人健康度与活动订单。\n\n"
            "📓 **4. 交易日记与心理纪律标签 (Journal):**\n"
            "• `/journal`\n"
            "  自动记录每一笔交易归因、心态纪律评分与量化失误归类。\n\n"
            "📊 **5. 机构级多周期审计报表:**\n"
            "• `/report` | `/audit` | `/daily_audit`\n"
            "  每日/每月夏普比率、最大回撤与各引擎胜率全景审计。\n\n"
            "🛑 **6. 紧急一键平仓熔断 (Stop Trading):**\n"
            "• `/stop ALL` - 紧急一键撤销所有挂单并停止全部运行中的机器人。\n"
            "• `/stop <币种>` - 安全平仓指定币种并停用对应策略。\n\n"
            "🔒 **7. 2FA 安全 PIN 码与重置:**\n"
            "• `/set_pin <PIN>` - 设置 4-6 位敏感操作安全确认密码。\n"
            "• `/reset_pin` - 申请重置安全验证 PIN 码。\n\n"
            "🧪 **8. 模拟盘与实盘切换 (仅限超级管理员):**\n"
            "• `/paper_trading` - 在无风险模拟沙盒与真实本金实盘之间切换（仅限 Super Admin）。\n\n"
            "📜 **9. 服务条款、法律协议与风险披露:**\n"
            "• `/about` | `/agreement` - 查看客户服务协议、责任免除与合规声明。\n"
        )
    else:
        text = (
            "🔴 **ផ្នែកទី ៥ ៖ គ្រប់គ្រងគណនី, ទុន និងប្រព័ន្ធសុវត្ថិភាព** 🔴\n"
            "══════════════════════════════\n"
            "🔒 **ប្រព័ន្ធសុវត្ថិភាពស្ថាប័ន ៖** 2FA Security PIN, ការពារ API Key និងយន្តការបិទអាសន្នពេលទីផ្សារមានបញ្ហា។\n"
            "══════════════════════════════\n\n"
            "💼 **១. ពិនិត្យ Portfolio & PnL សរុប ៖**\n"
            "• `/portfolio`\n"
            "  មើលប្រាក់ចំណេញសរុប (PnL), Position កំពុងជួញដូរ និងទ្រព្យសម្បត្តិទាំងអស់។\n\n"
            "💰 **២. ឆែកសមតុល្យលុយក្នុងកាបូប (Balance) ៖**\n"
            "• `/balance`\n"
            "  ឆែកលុយ Real-Time ក្នុង Binance Spot, Futures, Capital.com និង MT5។\n\n"
            "📊 **៣. ស្ថានភាពដំណើរការ Bot (Live Status) ៖**\n"
            "• `/status`\n"
            "  ពិនិត្យស្ថានភាព Bot ទាំងអស់ដែលកំពុងរត់ 24/7 និង Order សកម្ម។\n\n"
            "📓 **៤. កំណត់ត្រាជួញដូរ (Trading Journal) ៖**\n"
            "• `/journal`\n"
            "  កត់ត្រាការជួញដូរ កែប្រែចិត្តសាស្ត្រ និងសម្គាល់កំហុសដើម្បីពង្រឹងវិន័យវិនិយោគ។\n\n"
            "📊 **៥. របាយការណ៍សវនកម្ម (Audit Report) ៖**\n"
            "• `/report` | `/audit` | `/daily_audit`\n"
            "  របាយការណ៍សវនកម្មប្រចាំថ្ងៃ និងប្រចាំខែ (Win Rate, PnL, Drawdown)។\n\n"
            "🛑 **៦. បិទ Bot អាសន្ន (Emergency Stop) ៖**\n"
            "• `/stop ALL` - បិទ និង Market Close គ្រប់ Bot ទាំងអស់ភ្លាមៗដើម្បីការពារដើមទុន។\n"
            "• `/stop <COIN>` - បិទការជួញដូរលើកាក់ជាក់លាក់មួយ។\n\n"
            "🔒 **៧. លេខកូដសម្ងាត់ 2FA Security PIN ៖**\n"
            "• `/set_pin <PIN>` - កំណត់លេខកូដសម្ងាត់ ៤-៦ ខ្ទង់មុនពេលបញ្ជាជួញដូរធំៗ។\n"
            "• `/reset_pin` - ផ្លាស់ប្តូរ ឬកំណត់លេខកូដសម្ងាត់ឡើងវិញពេលភ្លេច។\n\n"
            "🧪 **៨. ផ្លាស់ប្តូរ Paper Trading vs Real Live (Admin Only) ៖**\n"
            "• `/paper_trading` - ប្តូររវាង Simulation និង Real Live (សម្រាប់ Super Admin តែប៉ុណ្ណោះ)។\n\n"
            "📜 **៩. កិច្ចសន្យា និងលក្ខខណ្ឌច្បាប់ (Legal & Agreement) ៖**\n"
            "• `/about` | `/agreement` - ពិនិត្យកិច្ចព្រមព្រៀងសេវាកម្ម និងការប្រកាសហានិភ័យច្បាប់។\n"
        )

    keyboard = [
        [
            InlineKeyboardButton("💼 Portfolio PnL", callback_data="btn_menu_portfolio"),
            InlineKeyboardButton("💰 Live Balance", callback_data="btn_balance_refresh")
        ],
        [
            InlineKeyboardButton("📊 24H Audit Report", callback_data="btn_executive_report"),
            InlineKeyboardButton("📓 Trading Journal", callback_data="btn_journal")
        ],
        [
            InlineKeyboardButton("🧪 Paper / Live Mode", callback_data="btn_menu_papertrade"),
            InlineKeyboardButton("🛑 Stop ALL Trading", callback_data="btn_stop_all")
        ],
        [
            InlineKeyboardButton("🔙 Back to Smart Hub", callback_data="smart_hub_home"),
            InlineKeyboardButton("🎛️ Master Control Panel", callback_data="btn_menu_refresh")
        ]
    ]
    return text, InlineKeyboardMarkup(keyboard)


# ==============================================================================
# 7. SUPER ADMIN FLEET COMMAND VIEW (Strictly Authorized for Admins)
# ==============================================================================
def _build_admin_view(is_admin: bool, lang: str, mode_badge: str) -> Tuple[str, InlineKeyboardMarkup]:
    if not is_admin:
        if lang == "en":
            text = (
                "⛔ **ACCESS RESTRICTED: SUPER ADMIN FLEET COMMAND ONLY** ⛔\n"
                "══════════════════════════════\n"
                "The commands in this category are exclusively reserved for platform administrators to manage the global quant fleet.\n\n"
                "👉 Please use the button below to navigate to your VIP Trading Engines!"
            )
        elif lang == "zh":
            text = (
                "⛔ **权限受限：仅限超级管理员访问** ⛔\n"
                "══════════════════════════════\n"
                "本分类指令仅对平台超级管理员开放，用于管理全球量化舰队与系统治理。\n\n"
                "👉 请点击下方按钮返回您的 VIP 交易引擎！"
            )
        else:
            text = (
                "⛔ **ការកម្រិតសិទ្ធិ ៖ សម្រាប់តែ SUPER ADMIN ប៉ុណ្ណោះ** ⛔\n"
                "══════════════════════════════\n"
                "ពាក្យបញ្ជាក្នុងផ្នែកនេះ គឺសម្រាប់តែអ្នកគ្រប់គ្រងប្រព័ន្ធ (Administrators) បញ្ជាកងនាវាស្វ័យប្រវត្តទូទាំងពិភពលោកប៉ុណ្ណោះ។\n\n"
                "👉 សូមចុចប៊ូតុងខាងក្រោម ដើម្បីត្រឡប់ទៅកាន់ពាក្យបញ្ជា VIP របស់អ្នកវិញ!"
            )
        kb = [[InlineKeyboardButton("🔙 Back to Smart Hub", callback_data="smart_hub_home")]]
        return text, InlineKeyboardMarkup(kb)

    if lang == "en":
        text = (
            "👑 **CATEGORY 6: SUPER ADMIN MASTER FLEET COMMAND & CONTROL** 👑\n"
            "══════════════════════════════\n"
            "🛡️ **SECURITY CLEARANCE**: `LEVEL 5 SUPREME COMMANDER (FULL ACCESS)`\n"
            "⚡ **INFRASTRUCTURE**: `GCP e2-standard-4 (Tokyo asia-northeast1-a)`\n"
            "══════════════════════════════\n\n"
            "👥 **1. VIP User Directory & License Governance:**\n"
            "• `/admin_users` - View full registered users directory, VIP statuses & active engines\n"
            "• `/admin_license <chat_id> <days>` - Grant or extend VIP membership (e.g. `/admin_license 123456789 30`)\n"
            "• `/admin_agreements` - Review user signed contracts & legal PDF repository\n"
            "• `/admin_view_portfolio <chat_id>` - Audit any user's active portfolio & positions\n\n"
            "📢 **2. Urgent Global Broadcast & Signal Dispatch:**\n"
            "• `/admin_broadcast <message>` - Broadcast high-priority push alert to ALL registered users\n"
            "• `/admin_signal <COIN> <BUY/SELL> <AMOUNT>` - Dispatch institutional auto-follower signal\n\n"
            "🚂 **3. Master Locomotive Fleet Synchronization:**\n"
            "• `/master_sync` - Synchronize all active accounts to the Master Locomotive syndicate\n"
            "• `/master_protect` - Deploy emergency armor protection across the entire fleet\n"
            "• `/master_close_all` - Force immediate market closure across all user accounts in catastrophic dumps\n\n"
            "⚙️ **4. Platform Governance & System Parameters:**\n"
            "• `/admin_stats` - Total system trading volume, net PnL, active bots & server load\n"
            "• `/admin_config` - Modify live trading parameters, spread thresholds & risk margins\n"
            "• `/health` - Inspect VPS hardware vitals (CPU, 16GB RAM, SQLite WAL, network ping)\n"
            "• `/sync_brain` - Hot-reload 33 AI Swarm models & neural network weights without restart\n"
            "• `/hf_data` - Direct telemetry of Hugging Face cloud inference models & datasets\n"
            "• `/toggle_breaker` - Toggle Emergency Portfolio Circuit Breaker on/off\n\n"
            "🏢 **5. TradFi & MT5 Approvals:**\n"
            "• `/admin_capital` - Review, approve, or toggle user Capital.com accounts\n"
            "• `/admin_mt5` - Review, approve, or toggle user MT5 Tokyo bridge accounts\n\n"
            "☢️ **6. Panic Emergency Nuke (System-Wide Kill Switch):**\n"
            "• `/admin_nuke 1234` - Extreme Emergency Kill Switch: Terminates all bots & market-closes all positions\n"
        )
    elif lang == "zh":
        text = (
            "👑 **模块 6：超级管理员全球舰队指挥控制中心** 👑\n"
            "══════════════════════════════\n"
            "🛡️ **安全权限**: `5级最高统帅 (最高全权授权)`\n"
            "⚡ **基础设施**: `GCP e2-standard-4 (东京 asia-northeast1-a)`\n"
            "══════════════════════════════\n\n"
            "👥 **1. VIP 用户名录与授权治理:**\n"
            "• `/admin_users` - 查看所有注册用户、VIP 到期时间与运行策略\n"
            "• `/admin_license <用户ID> <天数>` - 授予或延长 VIP 授权 (如 `/admin_license 123456789 30`)\n"
            "• `/admin_agreements` - 审查用户签署的电子合同与 PDF 存档\n"
            "• `/admin_view_portfolio <用户ID>` - 实时审查任意用户的持仓组合\n\n"
            "📢 **2. 全球紧急广播与跟随信号下发:**\n"
            "• `/admin_broadcast <内容>` - 向全体用户推送高优先级置顶紧急广播\n"
            "• `/admin_signal <币种> <买/卖> <数量>` - 下发全自动跟随交易信号\n\n"
            "🚂 **3. 领航机车全球编队同步协同:**\n"
            "• `/master_sync` - 将所有用户账户与主战机车策略完全同步\n"
            "• `/master_protect` - 全网部署紧急防暴跌保护装甲\n"
            "• `/master_close_all` - 在极端单边黑天鹅行情下一键强平全网仓位\n\n"
            "⚙️ **4. 平台治理与参数调优:**\n"
            "• `/admin_stats` - 全平台总交易额、净利润、活跃机器人与服务器负载\n"
            "• `/admin_config` - 实时修改交易参数、点差阈值与风控限额\n"
            "• `/health` - 检查 VPS 硬件指标 (CPU, 16GB 内存, SQLite WAL, 网络延迟)\n"
            "• `/sync_brain` - 零停机热重载 33 大 AI 神经模型与权重\n"
            "• `/hf_data` - 检查 Hugging Face 云推理模型与数据集状态\n"
            "• `/toggle_breaker` - 开启/关闭紧急资产熔断保护开关\n\n"
            "🏢 **5. TradFi 与 MT5 机构审批:**\n"
            "• `/admin_capital` - 审批并激活用户 Capital.com 交易通道\n"
            "• `/admin_mt5` - 审批并激活用户 MT5 东京网桥账户\n\n"
            "☢️ **6. 终极紧急核按钮 (全网紧急停机):**\n"
            "• `/admin_nuke 1234` - 终极紧急平仓：强制平仓所有用户持仓并关闭所有机器人\n"
        )
    else:
        text = (
            "👑 **ផ្នែកទី ៦ ៖ SUPER ADMIN MASTER FLEET COMMAND & CONTROL** 👑\n"
            "══════════════════════════════\n"
            "🛡️ **SECURITY CLEARANCE** ៖ `LEVEL 5 SUPREME COMMANDER (FULL ACCESS)`\n"
            "⚡ **ហេដ្ឋារចនាសម្ព័ន្ធ ៖** `GCP e2-standard-4 (Tokyo asia-northeast1-a)`\n"
            "══════════════════════════════\n\n"
            "👥 **១. គ្រប់គ្រងសមាជិក VIP & អាជ្ញាប័ណ្ណ (User & Licensing) ៖**\n"
            "• `/admin_users` - មើលបញ្ជីឈ្មោះសមាជិកទាំងអស់, ថ្ងៃផុតកំណត់ VIP & Bot កំពុងរ៉ាន់\n"
            "• `/admin_license <chat_id> <days>` - ផ្តល់ ឬពន្យាពេល VIP (ឧ. `/admin_license 123456789 30`)\n"
            "• `/admin_agreements` - ពិនិត្យកិច្ចសន្យាច្បាប់ PDF ដែល User បានចុះហត្ថលេខា\n"
            "• `/admin_view_portfolio <chat_id>` - ពិនិត្យមើល Portfolio របស់ User ជាក់លាក់ណាមួយ\n\n"
            "📢 **២. ផ្ញើសារដំណឹងអាសន្នទូទាំងពិភពលោក (Global Broadcast) ៖**\n"
            "• `/admin_broadcast <សារ>` - ផ្ញើសារបន្ទាន់ទៅកាន់ទូរស័ព្ទរបស់ User ទាំងអស់ភ្លាមៗ\n"
            "• `/admin_signal <COIN> <BUY/SELL> <AMOUNT>` - បាញ់ Signal ជួញដូរស្វ័យប្រវត្តតាមប្រព័ន្ធ\n\n"
            "🚂 **៣. Master Locomotive Fleet Synchronizer (បញ្ជាកងនាវា) ៖**\n"
            "• `/master_sync` - ធ្វើសមកាលកម្មគណនីទាំងអស់ជាមួយក្បាលរថភ្លើង Master Locomotive\n"
            "• `/master_protect` - បើករបាំងការពារគ្រោះថ្នាក់លើកងនាវាទាំងអស់ទូទាំងពិភពលោក\n"
            "• `/master_close_all` - បង្ខំបិទ Position របស់ User ទាំងអស់ក្នុងទីផ្សារពេលមានវិបត្តិធំ\n\n"
            "⚙️ **៤. គ្រប់គ្រងប្រព័ន្ធ និងសុខភាព VPS (Governance & Health) ៖**\n"
            "• `/admin_stats` - ទំហំជួញដូរសរុប, ផលចំណេញសុទ្ធ, Bot សកម្ម & Server Load\n"
            "• `/admin_config` - កែប្រែប៉ារ៉ាម៉ែត្រជួញដូរ, Spread & Risk Margin ក្នុង Real-Time\n"
            "• `/health` - ឆែកសុខភាព hardware VPS (CPU, 16GB RAM, SQLite WAL, Ping Tokyo)\n"
            "• `/sync_brain` - ផ្ទុកឡើងវិញនូវម៉ូឌែល AI ទាំង ៣៣ ដោយមិនបាច់ Restart Server\n"
            "• `/hf_data` - ពិនិត្យទិន្នន័យ Hugging Face Cloud Inference Storage\n"
            "• `/toggle_breaker` - បើក/បិទ ស្វិតអាសន្ន Circuit Breaker\n\n"
            "🏢 **៥. ត្រួតពិនិត្យ និងអនុម័ត TradFi & MT5 ៖**\n"
            "• `/admin_capital` - អនុម័ត និងបើកសិទ្ធិគណនី Capital.com ជូន User\n"
            "• `/admin_mt5` - អនុម័ត និងបើកសិទ្ធិគណនី MT5 Tokyo Bridge ជូន User\n\n"
            "☢️ **៦. Panic Emergency Nuke (ប៊ូតុងអាសន្នបិទប្រព័ន្ធ) ៖**\n"
            "• `/admin_nuke 1234` - បិទ និង Market Close គ្រប់ Positions ទាំងអស់ក្នុងប្រព័ន្ធទាំងមូល\n"
        )

    keyboard = [
        [
            InlineKeyboardButton("👑 Admin Panel", callback_data="btn_admin_panel"),
            InlineKeyboardButton("👥 VIP Users Directory", callback_data="btn_admin_users_refresh")
        ],
        [
            InlineKeyboardButton("📊 System Stats & PnL", callback_data="btn_admin_stats_refresh"),
            InlineKeyboardButton("🩺 VPS Health & Diagnostics", callback_data="btn_health_refresh")
        ],
        [
            InlineKeyboardButton("📦 Hot-Reload AI Brain", callback_data="btn_sync_brain"),
            InlineKeyboardButton("📢 Urgent Broadcast Alert", callback_data="btn_admin_broadcast_prompt")
        ],
        [
            InlineKeyboardButton("🛡️ Circuit Breaker", callback_data="btn_toggle_breaker_toggle"),
            InlineKeyboardButton("☢️ Emergency Panic Nuke", callback_data="btn_admin_nuke")
        ],
        [
            InlineKeyboardButton("🔙 Back to Smart Hub", callback_data="smart_hub_home"),
            InlineKeyboardButton("🎛️ Master Control Panel", callback_data="btn_menu_refresh")
        ]
    ]
    return text, InlineKeyboardMarkup(keyboard)


# ==============================================================================
# 8. SELECTION GUIDE VIEW (FAQ & Decision Matrix)
# ==============================================================================
def _build_guide_view(is_admin: bool, lang: str, mode_badge: str) -> Tuple[str, InlineKeyboardMarkup]:
    if is_admin:
        # Super Admin FAQ View (Full Mathematical Thresholds & Ground Truths)
        if lang == "en":
            text = (
                "💡 **ZERO-CONFUSION TRADING SELECTION MATRIX (FAQ) [ADMIN VIEW]** 💡\n"
                "══════════════════════════════\n"
                "🎯 **Question 1: I am a conservative investor with small capital and want ZERO liquidation risk.**\n"
                "👉 **Solution:** Use **Spot Engines** (`/compound_grid` or `/infinity_matrix` or `/wealth SPOT ON 50`).\n"
                "  • Risk: 0.00% liquidation risk.\n"
                "  • Mechanics: Physical asset ownership on Binance Spot, compounding volatility into coin accumulation via dynamic ATR channels.\n\n"
                "🎯 **Question 2: I want daily automated cash profits using professional delta-neutral hedging.**\n"
                "👉 **Solution:** Use **Futures Engines** (`/wealth FUTURES ON 100` or `/turbo_hedge`).\n"
                "  • Risk: 10x Isolated Margin (strictly capped risk).\n"
                "  • Mechanics: Protected by Breakeven Armor (+3% ROI & +0.12% fee floor) and Golden 85% trailing ratchet.\n\n"
                "🎯 **Question 3: I want to trade Gold (XAUUSD), US Tech (NVDA, TSLA) or S&P 500 without crypto volatility.**\n"
                "👉 **Solution:** Use **TradFi Engines** (`/capital` or `/mt5`).\n"
                "  • Risk: In-Memory Stealth Breakout Radar, 10x Spread Hurdle, Delayed BE Armor ($2.50 & +8.5% ROI).\n"
                "  • Mechanics: Interbank session routing (London Open 14:00 ICT & NY Cash Open 20:30 ICT).\n\n"
                "🎯 **Question 4: What if I made a mistake or the market enters an extreme black swan crash?**\n"
                "👉 **Solution:** Send `/stop ALL` immediately. It instantly cancels all orders and market-closes all active positions to flat cash.\n"
            )
        elif lang == "zh":
            text = (
                "💡 **防混淆量化引擎决策矩阵 (常见疑问解答) [管理员深度模式]** 💡\n"
                "══════════════════════════════\n"
                "🎯 **疑问 1：我是稳健型投资者，资金较小，希望绝对 0% 爆仓风险？**\n"
                "👉 **最佳选择：** 使用 **现货投资引擎** (`/compound_grid` 或 `/infinity_matrix` 或 `/wealth SPOT ON 50`)。\n"
                "  • 风险: 0.00% 爆仓概率。\n"
                "  • 机制: 币安现货真实资产持有，网格自动逢低吸筹、高抛低吸复利再投资。\n\n"
                "🎯 **疑问 2：我希望获得 24/7 全自动高频收益，并拥有严格的对冲保护？**\n"
                "👉 **最佳选择：** 使用 **合约与对冲引擎** (`/wealth FUTURES ON 100` 或 `/turbo_hedge`)。\n"
                "  • 风险: 10x 逐仓保证金 (严禁全仓，严格隔离风险)。\n"
                "  • 机制: 浮盈达到 +3% ROI 自动触发保本装甲 (+0.12% 手续费)，85% 利润追踪锁定。\n\n"
                "🎯 **疑问 3：我想交易现货黄金 (XAUUSD)、美股科技股 (NVDA, TSLA) 或标普 500？**\n"
                "👉 **最佳选择：** 使用 **全球 TradFi 引擎** (`/capital` 或 `/mt5`)。\n"
                "  • 风险: 内存隐形突破雷达，10倍点差门槛，延迟保本 ($2.50 & +8.5% ROI)。\n"
                "  • 机制: 银行间黄金交易时间段自动寻优 (伦敦盘 14:00 与华尔街美盘 20:30)。\n\n"
                "🎯 **疑问 4：万一我操作失误或市场遭遇极端黑天鹅暴跌，怎么办？**\n"
                "👉 **最佳对策：** 立即发送 `/stop ALL`，系统将毫秒级撤销全部订单并全部市价平仓锁定现金！\n"
            )
        else:
            text = (
                "💡 **មគ្គុទ្ទេសក៍ជ្រើសរើសម៉ាស៊ីនជួញដូរ (សំណួរ-ចម្លើយ មិនឱ្យភ័ន្តច្រឡំ) [ADMIN VIEW]** 💡\n"
                "══════════════════════════════\n"
                "🎯 **សំណួរទី ១ ៖ ខ្ញុំចង់វិនិយោគដោយសុវត្ថិភាព មិនចង់ឱ្យមានហានិភ័យ Liquidation សោះ តើគួររើសមួយណា?**\n"
                "👉 **ចម្លើយ ៖** ជ្រើសរើស **Spot Engines** (`/compound_grid` ឬ `/infinity_matrix` ឬ `/wealth SPOT ON 50`)។\n"
                "  • ហានិភ័យ ៖ 0.00% Liquidation Risk (គ្មានការខ្ចីលុយ គ្មានការឆេះកុង)\n"
                "  • របៀបរ៉ាន់ ៖ កាន់កាក់ពិតប្រាកដក្នុង Spot ទិញពេលធ្លាក់ លក់ពេលឡើង តាម dynamic ATR bands។\n\n"
                "🎯 **សំណួរទី ២ ៖ ខ្ញុំចង់បានចំណូលប្រចាំថ្ងៃ 24/7 និងមានប្រព័ន្ធការពារហានិភ័យជាប់ជានិច្ច?**\n"
                "👉 **ចម្លើយ ៖** ជ្រើសរើស **Futures Engines** (`/wealth FUTURES ON 100` ឬ `/turbo_hedge`)។\n"
                "  • ហានិភ័យ ៖ 10x Isolated Margin (កាត់ផ្តាច់ហានិភ័យកាបូប)\n"
                "  • របៀបរ៉ាន់ ៖ ចំណេញដល់ +3% ROI ប្រព័ន្ធចាក់សោរ Breakeven Armor (+0.12% fee) ធានាថាមិនចាញ់ និងដេញចាប់ប្រាក់ចំណេញ 85%។\n\n"
                "🎯 **សំណួរទី ៣ ៖ ខ្ញុំចង់ជួញដូរមាស (XAUUSD), ប្រេងឆៅ និងភាគហ៊ុនអាមេរិក (NVDA, TSLA, Apple)?**\n"
                "👉 **ចម្លើយ ៖** ជ្រើសរើស **TradFi Engines** (`/capital` ឬ `/mt5`)។\n"
                "  • ហានិភ័យ ៖ In-Memory Stealth Breakout Radar, ចម្ងាយ TP ធំជាង Spread ១០ ដង, Delayed BE ($2.50 & 8.5% ROI)\n"
                "  • របៀបរ៉ាន់ ៖ ដំណើរការតាមម៉ោងមាស Session Kill Zones របស់ធនាគារពិភពលោក (London Open 14:00 & NY Open 20:30)។\n\n"
                "🎯 **សំណួរទី ៤ ៖ បើទីផ្សារមានវិបត្តិធ្លាក់ខ្លាំង ឬខ្ញុំចង់បញ្ឈប់ការជួញដូរទាំងអស់ តើត្រូវធ្វើដូចម្តេច?**\n"
                "👉 **ចម្លើយ ៖** វាយបញ្ជា `/stop ALL` ភ្លាមៗ! ប្រព័ន្ធនឹង Cancel Order និង Market Close គ្រប់ Position ទាំងអស់មកជាសាច់ប្រាក់សុទ្ធភ្លាមៗ។\n"
            )
    else:
        # Public VIP User FAQ View (Zero Technical Secrets - Intuitive & Protective)
        if lang == "en":
            text = (
                "💡 **ZERO-CONFUSION TRADING SELECTION MATRIX (FAQ)** 💡\n"
                "══════════════════════════════\n"
                "🎯 **Question 1: I am a conservative investor with small capital and want ZERO liquidation risk.**\n"
                "👉 **Solution:** Use **Spot Engines** (`/compound_grid` or `/infinity_matrix` or `/wealth SPOT ON 50`).\n"
                "  • Risk: 0.00% liquidation risk.\n"
                "  • Mechanics: Physical asset ownership on Binance Spot, compounding price swings into coin accumulation.\n\n"
                "🎯 **Question 2: I want daily automated cash profits using professional hedging.**\n"
                "👉 **Solution:** Use **Futures Engines** (`/wealth FUTURES ON 100` or `/turbo_hedge`).\n"
                "  • Risk: 10x Isolated Margin (strictly capped risk per trade).\n"
                "  • Mechanics: Protected by automated breakeven stop and dynamic profit locking.\n\n"
                "🎯 **Question 3: I want to trade Gold (XAUUSD), US Tech (NVDA, TSLA) or S&P 500 without crypto volatility.**\n"
                "👉 **Solution:** Use **TradFi Engines** (`/capital` or `/mt5`).\n"
                "  • Risk: Advanced spread protection and dynamic capital preservation armor.\n"
                "  • Mechanics: Optimal execution aligned with prime global market sessions.\n\n"
                "🎯 **Question 4: What if I made a mistake or the market enters an extreme black swan crash?**\n"
                "👉 **Solution:** Send `/stop ALL` immediately. It instantly cancels all orders and market-closes all active positions to flat cash.\n"
            )
        elif lang == "zh":
            text = (
                "💡 **防混淆量化引擎决策矩阵 (常见疑问解答)** 💡\n"
                "══════════════════════════════\n"
                "🎯 **疑问 1：我是稳健型投资者，资金较小，希望绝对 0% 爆仓风险？**\n"
                "👉 **最佳选择：** 使用 **现货投资引擎** (`/compound_grid` 或 `/infinity_matrix` 或 `/wealth SPOT ON 50`)。\n"
                "  • 风险: 0.00% 爆仓概率。\n"
                "  • 机制: 币安现货真实资产持有，网格自动逢低吸筹、高抛低吸复利再投资。\n\n"
                "🎯 **疑问 2：我希望获得 24/7 全自动高频收益，并拥有严格的对冲保护？**\n"
                "👉 **最佳选择：** 使用 **合约与对冲引擎** (`/wealth FUTURES ON 100` 或 `/turbo_hedge`)。\n"
                "  • 风险: 10x 逐仓保证金 (严禁全仓，严格隔离每笔交易风险)。\n"
                "  • 机制: 盈利后自动启动保本护盾，动态追踪锁定已实现收益。\n\n"
                "🎯 **疑问 3：我想交易现货黄金 (XAUUSD)、美股科技股 (NVDA, TSLA) 或标普 500？**\n"
                "👉 **最佳选择：** 使用 **全球 TradFi 引擎** (`/capital` 或 `/mt5`)。\n"
                "  • 风险: 先进点差优化与收益安全装甲，杜绝无谓磨损。\n"
                "  • 机制: 深度对齐全球主流交易时段，捕获高确定性趋势动能。\n\n"
                "🎯 **疑问 4：万一我操作失误或市场遭遇极端黑天鹅暴跌，怎么办？**\n"
                "👉 **最佳对策：** 立即发送 `/stop ALL`，系统将毫秒级撤销全部订单并全部市价平仓锁定现金！\n"
            )
        else:
            text = (
                "💡 **មគ្គុទ្ទេសក៍ជ្រើសរើសម៉ាស៊ីនជួញដូរ (សំណួរ-ចម្លើយ មិនឱ្យភ័ន្តច្រឡំ)** 💡\n"
                "══════════════════════════════\n"
                "🎯 **សំណួរទី ១ ៖ ខ្ញុំចង់វិនិយោគដោយសុវត្ថិភាព មិនចង់ឱ្យមានហានិភ័យ Liquidation សោះ តើគួររើសមួយណា?**\n"
                "👉 **ចម្លើយ ៖** ជ្រើសរើស **Spot Engines** (`/compound_grid` ឬ `/infinity_matrix` ឬ `/wealth SPOT ON 50`)។\n"
                "  • ហានិភ័យ ៖ 0.00% Liquidation Risk (គ្មានការខ្ចីលុយ គ្មានការឆេះកុង)\n"
                "  • របៀបរ៉ាន់ ៖ កាន់កាក់ពិតប្រាកដក្នុង Spot ទិញពេលធ្លាក់ លក់ពេលឡើង បង្កើនទុនបន្តបន្ទាប់។\n\n"
                "🎯 **សំណួរទី ២ ៖ ខ្ញុំចង់បានចំណូលប្រចាំថ្ងៃ 24/7 និងមានប្រព័ន្ធការពារហានិភ័យជាប់ជានិច្ច?**\n"
                "👉 **ចម្លើយ ៖** ជ្រើសរើស **Futures Engines** (`/wealth FUTURES ON 100` ឬ `/turbo_hedge`)។\n"
                "  • ហានិភ័យ ៖ 10x Isolated Margin (កាត់ផ្តាច់ហានិភ័យកាបូប មិនឱ្យប៉ះពាល់ដើមទុនផ្សេង)\n"
                "  • របៀបរ៉ាន់ ៖ យន្តការ Breakeven Armor ការពារដើមទុនស្វ័យប្រវត្ត និងចាក់សោរប្រាក់ចំណេញពេលទីផ្សារឡើងថ្លៃ។\n\n"
                "🎯 **សំណួរទី ៣ ៖ ខ្ញុំចង់ជួញដូរមាស (XAUUSD), ប្រេងឆៅ និងភាគហ៊ុនអាមេរិក (NVDA, TSLA, Apple)?**\n"
                "👉 **ចម្លើយ ៖** ជ្រើសរើស **TradFi Engines** (`/capital` ឬ `/mt5`)។\n"
                "  • ហានិភ័យ ៖ ប្រព័ន្ធការពារ Spread និងចាក់សោរប្រាក់ចំណេញសុវត្ថិភាព\n"
                "  • របៀបរ៉ាន់ ៖ ដំណើរការតាមពេលវេលាជួញដូរសកម្មបំផុតរបស់ទីផ្សារអន្តរជាតិធំៗ។\n\n"
                "🎯 **សំណួរទី ៤ ៖ បើទីផ្សារមានវិបត្តិធ្លាក់ខ្លាំង ឬខ្ញុំចង់បញ្ឈប់ការជួញដូរទាំងអស់ តើត្រូវធ្វើដូចម្តេច?**\n"
                "👉 **ចម្លើយ ៖** វាយបញ្ជា `/stop ALL` ភ្លាមៗ! ប្រព័ន្ធនឹង Cancel Order និង Market Close គ្រប់ Position ទាំងអស់មកជាសាច់ប្រាក់សុទ្ធភ្លាមៗ។\n"
            )

    keyboard = [
        [
            InlineKeyboardButton("🟢 Explore Spot Engines", callback_data="smart_cat_spot"),
            InlineKeyboardButton("🟡 Explore Futures Engines", callback_data="smart_cat_futures")
        ],
        [
            InlineKeyboardButton("🔵 Explore TradFi & MT5", callback_data="smart_cat_tradfi"),
            InlineKeyboardButton("🟣 Explore AI Radars", callback_data="smart_cat_radars")
        ],
        [
            InlineKeyboardButton("🔙 Back to Smart Hub", callback_data="smart_hub_home"),
            InlineKeyboardButton("🎛️ Master Control Panel", callback_data="btn_menu_refresh")
        ]
    ]
    return text, InlineKeyboardMarkup(keyboard)


# ==============================================================================
# 9. TELEGRAM HANDLER & CALLBACK DISPATCHER
# ==============================================================================
async def handle_smart_bot_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Main entry point for /smart, /commands, /smart_bot, /vip, /help, etc.
    """
    chat_id = update.effective_chat.id if update.effective_chat else None
    if not chat_id:
        return

    # Check category argument if user provided e.g. /smart spot, /smart futures, /smart admin
    args = context.args or []
    category = "home"
    if args:
        first_arg = str(args[0]).lower().strip()
        if first_arg in ["spot", "futures", "tradfi", "radars", "radar", "security", "risk", "admin", "guide", "faq"]:
            category = first_arg
            if category == "radar":
                category = "radars"
            elif category == "risk":
                category = "security"
            elif category == "faq":
                category = "guide"

    user_lang = get_user_lang(chat_id)
    text, reply_markup = build_smart_bot_payload(chat_id, user_lang, category)

    target_msg = update.effective_message or update.message
    if target_msg:
        try:
            await target_msg.reply_text(text=text, parse_mode="Markdown", reply_markup=reply_markup)
        except Exception:
            await target_msg.reply_text(text=text.replace("*", "").replace("`", "").replace("_", ""), reply_markup=reply_markup)


async def handle_smart_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    """
    Handles interactive callback queries for smart_cat_* and smart_hub_*.
    Returns True if handled, False otherwise.
    """
    query = update.callback_query
    if not query:
        return False

    data = str(query.data or "")
    if not (data.startswith("smart_cat_") or data.startswith("smart_hub_")):
        return False

    chat_id = query.message.chat.id if (query.message and query.message.chat) else update.effective_chat.id
    user_lang = get_user_lang(chat_id)

    # Tactile feedback toast (Invariant 22 standard)
    category = "home"
    toast_msg = "🧠 Angkor Quant Super Smart Hub"

    if data == "smart_cat_spot":
        category = "spot"
        toast_msg = "🟢 Spot Engines (100% Spot, 0% Liquidation Risk)"
    elif data == "smart_cat_futures":
        category = "futures"
        toast_msg = "🟡 Futures & Hedge Engines (Delta-Neutral & HFT)"
    elif data == "smart_cat_tradfi":
        category = "tradfi"
        toast_msg = "🔵 TradFi Global Markets & MT5 Tokyo Bridge"
    elif data == "smart_cat_radars":
        category = "radars"
        toast_msg = "🟣 AI Intelligence, Radars & ML 24h Forecasting"
    elif data == "smart_cat_security":
        category = "security"
        toast_msg = "🔴 Portfolio, Balance & Enterprise Risk Controls"
    elif data == "smart_cat_admin":
        category = "admin"
        toast_msg = "👑 Super Admin Fleet Command & Control Center"
    elif data == "smart_cat_guide":
        category = "guide"
        toast_msg = "💡 Zero-Confusion Selection Guide & Decision FAQ"
    elif data in ["smart_hub_home", "smart_hub_refresh"]:
        category = "home"
        toast_msg = "🧠 Angkor Quant Master Command Hub"

    try:
        await query.answer(toast_msg)
    except Exception:
        pass

    text, reply_markup = build_smart_bot_payload(chat_id, user_lang, category)

    try:
        await query.edit_message_text(text=text, parse_mode="Markdown", reply_markup=reply_markup)
    except Exception:
        try:
            await query.edit_message_text(text=text.replace("*", "").replace("`", "").replace("_", ""), reply_markup=reply_markup)
        except Exception:
            try:
                await query.message.reply_text(text=text, parse_mode="Markdown", reply_markup=reply_markup)
            except Exception:
                pass

    return True
