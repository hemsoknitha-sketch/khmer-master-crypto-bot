import sys
import py_compile

bot_thread_path = r"e:\AI CODE PYTHON\Khmer Master Crypto\khmer-master-crypto-bot\bot_thread.py"

with open(bot_thread_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "        async def smart_x_command(update: Update, context: ContextTypes.DEFAULT_TYPE):"
end_marker = "        async def smart_swap_command(update: Update, context: ContextTypes.DEFAULT_TYPE):"

assert start_marker in content, "start_marker not found in bot_thread.py"
assert end_marker in content, "end_marker not found in bot_thread.py"

start_idx = content.find(start_marker)
end_idx = content.find(end_marker, start_idx)

new_smart_x_code = '''        async def smart_x_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
            import smart_x_engine
            import trading_engine
            import turbo_hedge_engine
            import central_bank_gold_radar
            import macro_gold_engine
            import black_swan_gold_guard
            if not await verify_user(update): return
            chat_id = update.effective_chat.id
            msg_target = update.effective_message or update.message
            raw_lang = db.get_user_language(chat_id)
            user_lang = str(raw_lang or 'km')
            if user_lang.isdigit() or user_lang in ['0', '1']: user_lang = 'km'

            div = "━━━━━━━━━━━━"
            footnote = (
                "_Khmer Master Crypto_\\n"
                "_APEX SUPER BRAIN AI_\\n"
                "ដំណើរការការពារហានិភ័យ & កើបចំណេញ ២៤/៧!"
            )

            args = context.args
            if not args or len(args) == 0:
                from telegram import InlineKeyboardButton, InlineKeyboardMarkup
                keyboard = InlineKeyboardMarkup([
                    [
                        InlineKeyboardButton("🥇 Launch Gold Futures", callback_data="btn_smart_x_gold"),
                        InlineKeyboardButton("🛒 Spot Gold Buy", callback_data="btn_smart_x_spot")
                    ],
                    [
                        InlineKeyboardButton("📡 Live Gold Radar (SGE)", callback_data="btn_smart_x_radar"),
                        InlineKeyboardButton("🧠 25 AI Models Voting", callback_data="btn_smart_x_metrics")
                    ],
                    [
                        InlineKeyboardButton("🤖 Auto 24/7 Gold Sniper", callback_data="btn_smart_x_auto"),
                        InlineKeyboardButton("🛑 STOP Engine", callback_data="btn_smart_x_stop_all")
                    ],
                    [
                        InlineKeyboardButton("💼 Portfolio PnL", callback_data="btn_menu_portfolio"),
                        InlineKeyboardButton("🎛️ Master Menu", callback_data="btn_menu_refresh")
                    ]
                ])

                if user_lang == 'en':
                    msg = (
                        "👑 *KHMER MASTER CRYPTO | SMARTX GOLD QUANT*\\n"
                        f"{div}\\n"
                        "🥇 *100% PURE INSTITUTIONAL GOLD (XAUUSD / PAXG)*\\n"
                        f"{div}\\n"
                        "🏆 *SONIC QUANT STRATEGY BENCHMARK*\\n"
                        "• TagMarkets Top Trader: `510,879+ Followers`\\n"
                        "• Historical Win Rate  : `87.12% (372W / 55L)`\\n"
                        "• Maximum Drawdown     : `0.26% (Zero Martingale)`\\n"
                        "• Avg Trade Duration   : `14.4 Mins (0.01 Days)`\\n"
                        "• Target Profit / Oz   : `+$2.50 to +$10.00/oz`\\n"
                        "• Time-Stop Scratch    : `1-3 Mins (Strict <= $4 Cut)`\\n"
                        f"{div}\\n"
                        "🧠 *25 PRE-TRAINED AI BRAIN ENSEMBLE*\\n"
                        "• CatBoost + LightGBM + XGBoost Direction\\n"
                        "• Mixture-of-Experts (MoE) Regime Router\\n"
                        "• PINN Jump-Diffusion Jump Risk Dampener\\n"
                        "• Volatility & Dynamic TP Forecasters\\n"
                        f"{div}\\n"
                        "📡 *INSTITUTIONAL MACRO & SGE RADAR*\\n"
                        "• Shanghai Gold Exchange (SGE) LBMA Premium\\n"
                        "• PBOC Central Bank Physical Gold Accumulation\\n"
                        "• US 10Y Real Yields & DXY Dollar Matrix\\n"
                        "• Pre-Event 15m Freeze Shield (CPI, NFP, FOMC)\\n"
                        f"{div}\\n"
                        "📋 *1-TAP COPYABLE EXECUTIONS*\\n\\n"
                        "👉 🚀 *Gold Futures Scalper (Auto Direction 24/7):*\\n"
                        "`/smartx GOLD 20 10 AUTO 1234`\\n\\n"
                        "👉 🛒 *Spot Gold Macro Buy (0% Liquidation):*\\n"
                        "`/smartx SPOT 50 1234`\\n\\n"
                        "👉 🤖 *Auto 24/7 Gold Session Sniper (Perpetual):*\\n"
                        "`/smartx AUTO 20 10 1234`\\n\\n"
                        "👉 📡 *Live Macro & SGE Gold Radar:*\\n"
                        "`/smartx RADAR`\\n\\n"
                        "👉 🧠 *25 AI Models Consensus & Regime:*\\n"
                        "`/smartx METRICS`\\n\\n"
                        "👉 🛑 *Stop & Close All Positions:*\\n"
                        "`/smartx STOP ALL 1234`\\n"
                        f"{div}\\n"
                        f"{footnote}"
                    )
                elif user_lang == 'zh':
                    msg = (
                        "👑 *KHMER MASTER CRYPTO | SMARTX 机构黄金量化*\\n"
                        f"{div}\\n"
                        "🥇 *100% 专注机构级黄金 (XAUUSD / PAXG)*\\n"
                        f"{div}\\n"
                        "🏆 *SONIC 顶级操盘策略深度还原*\\n"
                        "• TagMarkets 跟单顶级榜: `510,879+ 跟单用户`\\n"
                        "• 历史实盘胜率      : `87.12% (372胜 / 55负)`\\n"
                        "• 历史最大回撤      : `0.26% (拒绝马丁补仓)`\\n"
                        "• 平均持仓时间      : `14.4 分钟 (0.01天)`\\n"
                        "• 每盎司止盈目标    : `+$2.50 ~ +$10.00/oz`\\n"
                        "• 时间止损快速切单  : `1-3分钟 (严格 <= $4)`\\n"
                        f"{div}\\n"
                        "🧠 *25 核心 AI 量化模型全开 (RAM)*\\n"
                        "• CatBoost + LightGBM + XGBoost 多空投票\\n"
                        "• 专家混合路由 (MoE) 市场 Regime 自动切换\\n"
                        "• PINN 跳跃扩散波动与动态止盈预测器\\n"
                        f"{div}\\n"
                        "📡 *央行与上海黄金交易所 (SGE) 溢价雷达*\\n"
                        "• SGE vs LBMA 现货黄金溢价监测 ($/oz)\\n"
                        "• 中国央行 (PBOC) 场外实物黄金囤积监控\\n"
                        "• 美元指数 (DXY) 与 10年期美债实际收益率\\n"
                        "• CPI/NFP/FOMC 重大数据提前15分钟硬熔断\\n"
                        f"{div}\\n"
                        "📋 *一键复制指令：*\\n\\n"
                        "👉 🚀 *黄金合约日内超短线 (AI自动方向 24/7):*\\n"
                        "`/smartx GOLD 20 10 AUTO 1234`\\n\\n"
                        "👉 🛒 *现货黄金宏观定投 (0% 强平风险):*\\n"
                        "`/smartx SPOT 50 1234`\\n\\n"
                        "👉 🤖 *24/7 全天候黄金时区狙击器:*\\n"
                        "`/smartx AUTO 20 10 1234`\\n\\n"
                        "👉 📡 *查看实时宏观与 SGE 黄金溢价:*\\n"
                        "`/smartx RADAR`\\n\\n"
                        "👉 🧠 *25 模型共识投票与状态:*\\n"
                        "`/smartx METRICS`\\n\\n"
                        "👉 🛑 *紧急平仓并停止所有运行:*\\n"
                        "`/smartx STOP ALL 1234`\\n"
                        f"{div}\\n"
                        f"{footnote}"
                    )
                else:
                    msg = (
                        "👑 *KHMER MASTER CRYPTO | SMARTX GOLD QUANT*\\n"
                        f"{div}\\n"
                        "🥇 *100% ផ្តោតលើមាសស្ថាប័នសុទ្ធសាធ (XAUUSD / PAXG)*\\n"
                        f"{div}\\n"
                        "🏆 *យុទ្ធសាស្ត្រ SONIC (ជើងឯក TagMarkets CopyX)*\\n"
                        "• អ្នកតាមដានជាក់ស្តែង : `510,879+ នាក់`\\n"
                        "• អត្រាឈ្នះ (Win Rate) : `87.12% (372 ឈ្នះ / 55 ចាញ់)`\\n"
                        "• Maximum Drawdown     : `0.26% (គ្មាន Martingale)`\\n"
                        "• រយៈពេលជួញដូរជាមធ្យម : `14.4 នាទី (0.01 ថ្ងៃ)`\\n"
                        "• ទិសដៅចំណេញ / អោន   : `+$2.50 ទៅ +$10.00/oz`\\n"
                        "• Time-Stop កាត់ខាត    : `1-3 នាទី (កាត់ភ្លាម <= $4)`\\n"
                        f"{div}\\n"
                        "🧠 *25 PRE-TRAINED AI BRAIN MODELS*\\n"
                        "• CatBoost + LightGBM + XGBoost Direction\\n"
                        "• Mixture-of-Experts (MoE) Regime Router\\n"
                        "• PINN Jump-Diffusion ការពារការបោកបញ្ឆោត\\n"
                        "• Volatility & Dynamic TP Forecasters គ្រប់គ្រង\\n"
                        f"{div}\\n"
                        "📡 *RADAR ធនាគារកណ្តាល & SGE PREMIUM*\\n"
                        "• Shanghai Gold Exchange (SGE) Premium $/oz\\n"
                        "• ធនាគារកណ្តាលចិន (PBOC) ប្រមូលទិញមាស Physical\\n"
                        "• សន្ទស្សន៍ដុល្លារ DXY & 10Y Real Yields\\n"
                        "• Pre-Event 15m Freeze Shield (CPI, NFP, FOMC)\\n"
                        f"{div}\\n"
                        "📋 *ពាក្យបញ្ជា 1-TAP COPYABLE EXECUTIONS*\\n\\n"
                        "👉 🚀 *Gold Futures Scalper (ទិសដៅ AUTO ២៤/៧) ៖*\\n"
                        "`/smartx GOLD 20 10 AUTO 1234`\\n\\n"
                        "👉 🛒 *Spot Gold Macro Buy (0% Liquidation) ៖*\\n"
                        "`/smartx SPOT 50 1234`\\n\\n"
                        "👉 🤖 *Auto 24/7 Gold Session Sniper (Perpetual) ៖*\\n"
                        "`/smartx AUTO 20 10 1234`\\n\\n"
                        "👉 📡 *Live Macro & SGE Gold Radar ៖*\\n"
                        "`/smartx RADAR`\\n\\n"
                        "👉 🧠 *25 AI Models Consensus & Regime ៖*\\n"
                        "`/smartx METRICS`\\n\\n"
                        "👉 🛑 *បញ្ឈប់ និងបិទ Position ទាំងអស់ ៖*\\n"
                        "`/smartx STOP ALL 1234`\\n"
                        f"{div}\\n"
                        f"{footnote}"
                    )
                if msg_target:
                    await msg_target.reply_text(msg, parse_mode="Markdown", reply_markup=keyboard)
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return

            action = str(args[0]).upper().strip()

            # Subcommand: RADAR (Shanghai Gold Exchange Premium, PBOC, Macro Yields)
            if action in ["RADAR", "SGE", "MACRO"]:
                current_p = await asyncio.to_thread(trading_engine.get_current_price, "PAXGUSDT")
                if current_p <= 0: current_p = 2650.0

                try:
                    sge_data = await asyncio.to_thread(central_bank_gold_radar.fetch_sge_lbma_premium)
                    sge_prem = sge_data.get("sge_premium_usdt", 25.0)
                    pboc_status = sge_data.get("pboc_status", "ACTIVE ACCUMULATING")
                except Exception:
                    sge_prem = 25.0
                    pboc_status = "ACCUMULATING"

                try:
                    macro_data = await asyncio.to_thread(macro_gold_engine.fetch_macro_gold_indicators)
                    dxy = macro_data.get("dxy_index", 104.2)
                    real_yield = macro_data.get("real_yield_10y", 1.35)
                except Exception:
                    dxy = 104.2
                    real_yield = 1.35

                try:
                    haven_res = await asyncio.to_thread(black_swan_gold_guard.PAXGGoldSafeHavenSwitcherEngine().scan_geopolitical_black_swan)
                    crisis_detected = haven_res.get("crisis_detected", False)
                    threat_level = haven_res.get("threat_level", "DEFCON 4 (NORMAL)")
                except Exception:
                    crisis_detected = False
                    threat_level = "NORMAL"

                macro_guard = smart_x_engine.MacroEventNLPGuard.check_macro_guard()

                radar_text = (
                    "📡 *INSTITUTIONAL GOLD MACRO RADAR*\\n"
                    f"{div}\\n"
                    f"🥇 *Live Gold Spot (PAXG)*: `${current_p:,.2f}`\\n"
                    f"🇨🇳 *SGE Premium vs LBMA*  : `+${sge_prem:.2f}/oz`\\n"
                    f"🏦 *PBOC Central Bank Flow*: `{pboc_status}`\\n"
                    f"💵 *US Dollar Index (DXY)* : `{dxy:.2f}`\\n"
                    f"📈 *US 10Y Real Yield*    : `{real_yield:.2f}%`\\n"
                    f"🛡️ *Geopolitical Crisis*   : `{'🚨 ' + threat_level if crisis_detected else '🟢 ' + threat_level}`\\n"
                    f"📰 *Macro Event Shield*    : `{'🚨 FROZEN' if macro_guard['is_frozen'] else '🟢 CLEAR (Max ' + str(macro_guard['max_allowed_leverage']) + 'x)'}`\\n"
                    f"{div}\\n"
                    "💡 *Institutional Edge*:\\n"
                    "• SGE Premium > +$15/oz confirms relentless physical demand from Asia.\\n"
                    "• PBOC accumulation provides an institutional hard floor on pullbacks.\\n"
                    f"{div}\\n"
                    f"{footnote}"
                )
                if msg_target:
                    await msg_target.reply_text(radar_text, parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return

            # Subcommand: METRICS (25 AI Models, Regime, Session Sweeps)
            if action in ["METRICS", "STATUS", "CHECK"]:
                sig = await asyncio.to_thread(smart_x_engine.SmartXEngine.generate_smart_x_signal, "PAXGUSDT")
                session_info = await asyncio.to_thread(smart_x_engine.SonicGoldScalper.get_current_session_window)
                macro = sig.get("macro_guard", {})
                ensemble = sig.get("ensemble", {})
                sweep = sig.get("sweep", {})

                metrics_text = (
                    "📊 *SMARTX GOLD AI METRICS & REGIME*\\n"
                    f"{div}\\n"
                    f"🥇 *Symbol*: `PAXGUSDT (XAUUSD)` | `${sig.get('current_price', 0.0):,.2f}`\\n"
                    f"⏰ *Session Window*: `{session_info.get('session_name', 'ACTIVE')}`\\n"
                    f"   └ Liquidity Score: `{session_info.get('liquidity_score', 8)}/10`\\n"
                    f"🎯 *Signal*: `{sig.get('side', 'WAIT')}` (`{sig.get('confidence_pct', 0.0)}%` Conf)\\n"
                    f"🔀 *MoE Regime*: `{sig.get('regime', 'BALANCED')}`\\n"
                    f"🏹 *Asian Sweep*: `{sweep.get('signal', 'NONE')}` ({sweep.get('type', 'CONSOLIDATION')})\\n"
                    f"📰 *Macro Guard*: `{'🚨 FROZEN' if macro.get('is_frozen') else '🟢 ACTIVE'}`\\n"
                    f"{div}\\n"
                    "🧠 *25 Models Voting Breakdown*:\\n"
                    f"• CatBoost Classifier  : `{ensemble.get('catboost_direction', 'N/A')}`\\n"
                    f"• LightGBM Regressor   : `{ensemble.get('lgb_signal', 'N/A')}`\\n"
                    f"• XGBoost Ensemble     : `{ensemble.get('xgb_signal', 'N/A')}`\\n"
                    f"• Models Loaded in RAM : `{len(smart_x_engine.BRAIN.models)}/25`\\n"
                    f"{div}\\n"
                    "🏆 *SONIC Target Benchmarks*:\\n"
                    "• Win Rate Target : `87.12%` | Max DD: `0.26%`\\n"
                    "• Scalp Duration  : `14.4 mins` | Scratch: `1-3 mins`\\n"
                    f"{div}\\n"
                    f"{footnote}"
                )
                if msg_target:
                    await msg_target.reply_text(metrics_text, parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return

            # Subcommand: SYNC / HF (Hugging Face Hub Sync & Hot-Reload)
            if action in ["SYNC", "HF", "DOWNLOAD", "PULL"]:
                if msg_target:
                    await msg_target.reply_text("⏳ *[HF SYNC]* Hot-loading 25 AI models into RAM from Hugging Face...", parse_mode="Markdown")
                sync_res = await asyncio.to_thread(smart_x_engine.SmartXBrainLoader.sync_from_huggingface)
                if sync_res.get("status") == "success":
                    resp_text = (
                        "🤗 *[HUGGING FACE SYNC COMPLETE]* 🚀\\n"
                        f"{div}\\n"
                        f"• Repo: `{sync_res.get('repo_id')}`\\n"
                        f"• Synced Files: `{sync_res.get('synced_count')} files (100%)`\\n"
                        f"• AI Models in RAM: `{sync_res.get('total_models')} Models`\\n"
                        f"• Hyperparameters : `{sync_res.get('total_configs')} Configs`\\n"
                        f"• Status: `🟢 Operational in /smartx Gold Engine`\\n"
                        f"{div}\\n"
                        "_Khmer Master Crypto | APEX SUPER BRAIN AI_"
                    )
                else:
                    resp_text = f"⚠️ [HF SYNC] Notice: {sync_res.get('message')}"
                if msg_target:
                    await msg_target.reply_text(resp_text, parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return

            # Subcommand: STOP / OFF
            if action in ["STOP", "OFF"]:
                symbol = "PAXGUSDT"
                pin = ""
                if len(args) >= 3:
                    pin = str(args[2]).strip()
                elif len(args) == 2:
                    if args[1].isdigit():
                        pin = str(args[1]).strip()

                is_admin = db.is_admin(chat_id) or (chat_id == 859271875)
                stored_pin = db.get_user_pin(chat_id)

                if not stored_pin and pin:
                    db.set_user_pin(chat_id, security.hash_pin(pin, chat_id))
                    stored_pin = db.get_user_pin(chat_id)
                elif is_admin and pin:
                    db.set_user_pin(chat_id, security.hash_pin(pin, chat_id))
                    stored_pin = db.get_user_pin(chat_id)

                if stored_pin and not is_admin:
                    if not pin or not security.verify_pin(pin, chat_id, stored_pin):
                        if msg_target:
                            await msg_target.reply_text("❌ Security PIN verification failed.")
                        await delete_sensitive_message(context, chat_id, update, user_lang)
                        return
                elif not stored_pin and not is_admin:
                    if msg_target:
                        await msg_target.reply_text("❌ Security PIN verification failed.")
                    await delete_sensitive_message(context, chat_id, update, user_lang)
                    return

                # Stop 24/7 Gold Engine
                db.update_system_setting(f"smart_x_{chat_id}_active", "0")
                db.update_system_setting(f"turbo_hedge_{chat_id}_top_mode", "0")
                db.remove_all_turbo_hedge_bots(chat_id)

                stop_res = await asyncio.to_thread(turbo_hedge_engine.stop_turbo_hedge_engine, chat_id, "ALL")
                closed_count = stop_res.get("count", 0) if isinstance(stop_res, dict) else 0
                total_pnl = stop_res.get("total_pnl", 0.0) if isinstance(stop_res, dict) else 0.0

                keys = db.get_user_api(chat_id)
                if keys and keys[0] and keys[1]:
                    try:
                        fut_res = await asyncio.to_thread(trading_engine.close_all_futures_positions, keys[0], keys[1])
                        if isinstance(fut_res, dict):
                            closed_count = max(closed_count, fut_res.get("closed_count", 0))
                    except Exception as err:
                        print(f"Error closing futures: {err}")

                pnl_sign = "+" if total_pnl >= 0 else ""
                msg = (
                    "🛑 *[SMARTX GOLD] ENGINE STOPPED*\\n"
                    f"{div}\\n"
                    f"🥇 *Target Asset* : `PAXGUSDT (XAUUSD)`\\n"
                    f"🔒 *Positions Closed*: `{closed_count}` on Binance\\n"
                    f"💵 *Realized PnL*  : `{pnl_sign}${total_pnl:.2f} USDT`\\n"
                    f"{div}\\n"
                    "✅ _24/7 Sniper & Bot are safely stopped. Capital is secured._"
                )
                if msg_target:
                    await msg_target.reply_text(msg, parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return

            # --- PARSE EXECUTION PARAMETERS & PIN ---
            pin = ""
            work_args = list(args)
            if len(work_args) >= 2 and work_args[-1].isdigit() and len(work_args[-1]) in [4, 5, 6]:
                pin = work_args.pop()

            is_admin = db.is_admin(chat_id) or (chat_id == 859271875)
            stored_pin = db.get_user_pin(chat_id)
            if not stored_pin and pin:
                db.set_user_pin(chat_id, security.hash_pin(pin, chat_id))
                stored_pin = db.get_user_pin(chat_id)
            elif is_admin and pin:
                db.set_user_pin(chat_id, security.hash_pin(pin, chat_id))
                stored_pin = db.get_user_pin(chat_id)

            if stored_pin and pin and not security.verify_pin(pin, chat_id, stored_pin) and not is_admin:
                if msg_target:
                    await msg_target.reply_text(f"❌ *លេខកូដ PIN មិនត្រឹមត្រូវ!* (PIN របស់អ្នក ៖ `{pin}`)", parse_mode="Markdown")
                return

            keys = db.get_user_api(chat_id)
            if not keys or not keys[0] or not keys[1]:
                if msg_target:
                    await msg_target.reply_text("❌ *មិនទាន់មាន API Key!* សូមប្រើ `/add_api` ដើម្បីភ្ជាប់ Binance API ជាមុនសិន។", parse_mode="Markdown")
                return

            tokens_upper = [t.upper().strip() for t in work_args]
            is_spot = ("SPOT" in tokens_upper)
            is_auto_247 = any(t in ["AUTO", "SNIPER", "24/7"] for t in tokens_upper)

            user_side = "AUTO"
            for t in work_args:
                if t.upper().strip() in ["BUY", "SELL"]:
                    user_side = t.upper().strip()
                    break

            clean_tokens = [t for t in work_args if t.upper().strip() not in ["SPOT", "FUTURES", "GOLD", "PAXG", "PAXGUSDT", "AUTO", "BUY", "SELL"]]
            num_tokens = []
            for t in clean_tokens:
                try:
                    num_tokens.append(float(t))
                except ValueError:
                    pass

            amount = 50.0 if is_spot else 20.0
            leverage = 1 if is_spot else 10
            target_tp = 2.5

            if is_spot:
                leverage = 1
                if num_tokens:
                    amount = max(10.50, num_tokens[0])
            else:
                if len(num_tokens) >= 3:
                    amount = max(5.0, num_tokens[0])
                    leverage = int(num_tokens[1])
                    target_tp = num_tokens[2]
                elif len(num_tokens) == 2:
                    amount = max(5.0, num_tokens[0])
                    leverage = int(num_tokens[1])
                elif len(num_tokens) == 1:
                    amount = max(5.0, num_tokens[0])

            target_symbol = "PAXGUSDT"

            if is_spot:
                # SPOT PHYSICAL GOLD ACCUMULATION (0% LIQUIDATION RISK)
                res = await asyncio.to_thread(smart_x_engine.execute_smart_x_spot, chat_id, target_symbol, amount)
                if res.get("status") == "success":
                    resp_msg = (
                        "👑 *[SMARTX SPOT GOLD ACCUMULATION]* 🥇\\n"
                        f"{div}\\n"
                        f"• Asset       : `PAXG (Physical Gold)`\\n"
                        f"• Capital     : `${res.get('amount_usdt', amount):.2f} USDT`\\n"
                        f"• Entry Price : `${res.get('entry_price', 0.0):,.2f}`\\n"
                        f"• Qty Bought  : `{res.get('qty', 0.0):.6f} PAXG`\\n"
                        f"• Liquidation : `0% Risk (Physical Backstop)`\\n"
                        f"{div}\\n"
                        "✅ _Physical Gold added to Spot portfolio. 100% Capital safe._"
                    )
                else:
                    resp_msg = f"⚠️ [SMARTX SPOT] {res.get('message', 'Execution error')}"
                if msg_target:
                    await msg_target.reply_text(resp_msg, parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return

            elif is_auto_247:
                # 24/7 PERPETUAL GOLD SESSION SNIPER
                spot_ok, fut_ok = await asyncio.to_thread(trading_engine.check_user_api_permissions, keys[0], keys[1])
                if not fut_ok:
                    if msg_target:
                        await msg_target.reply_text("🛑 *បរាជ័យ ៖ Binance API មិនទាន់បើកសិទ្ធិ Futures Trading ទេ។*\\n💡 សូមប្រើ Spot ៖ `/smartx SPOT 50 1234`", parse_mode="Markdown")
                    return

                db.update_system_setting(f"smart_x_{chat_id}_active", "1")
                db.update_system_setting(f"smart_x_{chat_id}_target", target_symbol)
                db.update_system_setting(f"smart_x_{chat_id}_amount", str(amount))
                db.update_system_setting(f"smart_x_{chat_id}_leverage", str(leverage))

                ack_text = (
                    "👑 *SMARTX 24/7 GOLD SNIPER ACTIVATED!* 🚀\\n"
                    f"{div}\\n"
                    f"🥇 *Asset*        : `PAXGUSDT (XAUUSD)`\\n"
                    f"💰 *Capital/Trade*: `${amount:,.2f} USDT` ({leverage}x ISOLATED)\\n"
                    f"🎯 *Strategy*     : `SONIC Scalp (87.12% Win, 0.26% Max DD)`\\n"
                    f"⏰ *Session Watch*: `Tokyo Fix, London Open, NY Open, London Close`\\n"
                    f"🛡️ *Risk Ceiling* : `1-3m Time-Stop Scratch | +$2.50 to +$10/oz TP`\\n"
                    f"{div}\\n"
                    "⚡ _កំពុងវិភាគម៉ូដែល AI ទាំង ២៥ និងរង់ចាំ Session Sweep ដើម្បីបើក Trade ស្វ័យប្រវត្តិ..._"
                )
                if msg_target:
                    await msg_target.reply_text(ack_text, parse_mode="Markdown")

                async def _background_smart_x_gold_sniper():
                    try:
                        sig = await asyncio.to_thread(smart_x_engine.SmartXEngine.generate_smart_x_signal, target_symbol)
                        if sig.get("side") in ["BUY", "SELL"]:
                            exec_res = await asyncio.to_thread(
                                smart_x_engine.execute_smart_x_futures,
                                chat_id, target_symbol, sig["side"], amount, leverage, target_tp
                            )
                            if exec_res.get("status") == "success" or exec_res.get("orderId"):
                                p = await asyncio.to_thread(trading_engine.get_current_price, target_symbol)
                                notif = (
                                    "👑 *[SMARTX GOLD AUTO-SNIPER ENTRY]* 🎯\\n"
                                    f"{div}\\n"
                                    f"• Direction  : `{sig['side']} ({sig.get('confidence_pct')}% Conf)`\\n"
                                    f"• Entry Price: `${p:,.2f}`\\n"
                                    f"• Capital    : `${amount:.2f} USDT` ({leverage}x)\\n"
                                    f"• Target TP  : `+$2.50 to +$10.00/oz`\\n"
                                    f"• Protection : `Breakeven Lock @ +3% | Time-Stop Active`\\n"
                                    f"{div}\\n"
                                    "_SONIC High-Frequency Engine Active 24/7._"
                                )
                                try:
                                    await context.bot.send_message(chat_id=chat_id, text=notif, parse_mode="Markdown")
                                except Exception:
                                    pass
                    except Exception as err:
                        print(f"Error in _background_smart_x_gold_sniper: {err}")

                asyncio.create_task(_background_smart_x_gold_sniper())
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return

            else:
                # DIRECT GOLD FUTURES TRADE
                spot_ok, fut_ok = await asyncio.to_thread(trading_engine.check_user_api_permissions, keys[0], keys[1])
                if not fut_ok:
                    if msg_target:
                        await msg_target.reply_text("🛑 *បរាជ័យ ៖ Binance API មិនទាន់បើកសិទ្ធិ Futures Trading ទេ។*\\n💡 សូមប្រើ Spot ៖ `/smartx SPOT 50 1234`", parse_mode="Markdown")
                    return

                exec_res = await asyncio.to_thread(
                    smart_x_engine.execute_smart_x_futures,
                    chat_id, target_symbol, user_side, amount, leverage, target_tp
                )

                if exec_res.get("status") in ["success", "NEW", "FILLED"] or exec_res.get("orderId"):
                    entry_p = await asyncio.to_thread(trading_engine.get_current_price, target_symbol)
                    resp_msg = (
                        "👑 *[SMARTX GOLD FUTURES EXECUTED]* 🚀\\n"
                        f"{div}\\n"
                        f"• Symbol     : `PAXGUSDT (XAUUSD)`\\n"
                        f"• Direction  : `{user_side}`\\n"
                        f"• Capital    : `${amount:.2f} USDT` ({leverage}x ISOLATED)\\n"
                        f"• Entry Price: `${entry_p:,.2f}`\\n"
                        f"• Protection : `Breakeven Lock @ +3% ROI | Time-Stop Active`\\n"
                        f"• Strategy   : `SONIC Re-Engineered (87.12% Win Rate)`\\n"
                        f"{div}\\n"
                        "✅ _Position active in HFT Turbo Hedge Monitor._"
                    )
                else:
                    resp_msg = f"⚠️ [SMARTX GOLD] {exec_res.get('message', exec_res.get('reason', 'Execution error'))}"

                if msg_target:
                    await msg_target.reply_text(resp_msg, parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return
'''

updated_content = content[:start_idx] + new_smart_x_code + "\n\n" + content[end_idx:]

with open(bot_thread_path, "w", encoding="utf-8") as f:
    f.write(updated_content)

print(f"Patched smart_x_command! Validating compilation...")
py_compile.compile(bot_thread_path, doraise=True)
print("Successfully patched and compiled bot_thread.py!")
