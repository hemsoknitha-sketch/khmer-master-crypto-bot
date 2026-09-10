import sys

bot_thread_path = r"e:\AI CODE PYTHON\Khmer Master Crypto\khmer-master-crypto-bot\bot_thread.py"

with open(bot_thread_path, "r", encoding="utf-8") as f:
    content = f.read()

# Marker 1: In STOP subcommand
stop_target = """                keys = db.get_user_api(chat_id)
                if keys and keys[0] and keys[1]:
                    if symbol == "ALL":
                        trading_engine.market_close_all_futures_positions(keys[0], keys[1])
                    else:
                        turbo_hedge_engine.execute_turbo_hedge_trade(keys[0], keys[1], symbol, 0, "CLOSE", 1, chat_id)
                if msg_target:
                    await msg_target.reply_text(f"🛑 [SMART X] Successfully stopped and market closed {symbol} positions!")
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return

            # Subcommand: SPOT Mode"""

assert stop_target in content, "Marker stop_target not found in bot_thread.py"

# Marker 2: End of smart_x_command before compound_grid_command
end_marker = """        async def compound_grid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):"""
assert end_marker in content, "Marker end_marker not found in bot_thread.py"

# Extract the block to replace
start_idx = content.find(stop_target)
end_idx = content.find(end_marker, start_idx)

original_subsegment = content[start_idx:end_idx]

replacement_subsegment = """                db.update_system_setting(f"turbo_hedge_{chat_id}_top_mode", "0")
                keys = db.get_user_api(chat_id)
                if keys and keys[0] and keys[1]:
                    if symbol == "ALL":
                        trading_engine.market_close_all_futures_positions(keys[0], keys[1])
                    else:
                        turbo_hedge_engine.execute_turbo_hedge_trade(keys[0], keys[1], symbol, 0, "CLOSE", 1, chat_id)
                db.remove_all_turbo_hedge_bots(chat_id)
                if msg_target:
                    await msg_target.reply_text(f"🛑 [SMART X] Successfully stopped 24/7 scanner and closed {symbol} positions!")
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return

            # --- FLEXIBLE TOKEN PARSER FOR /smartx & 24/7 PERPETUAL ENGINE ---
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
                    await msg_target.reply_text(f"❌ **លេខកូដ PIN មិនត្រឹមត្រូវ!** (PIN របស់អ្នក ៖ `{pin}` មិនត្រូវគ្នានឹង PIN ក្នុងប្រព័ន្ធឡើយ)", parse_mode="Markdown")
                return

            keys = db.get_user_api(chat_id)
            if not keys:
                if msg_target:
                    await msg_target.reply_text("❌ **មិនទាន់មាន API Key!** សូមប្រើប្រាស់ពាក្យបញ្ជា `/add_api` ដើម្បីភ្ជាប់ Binance API ជាមុនសិន។", parse_mode="Markdown")
                return

            tokens_upper = [t.upper().strip() for t in work_args]
            is_spot = ("SPOT" in tokens_upper)
            is_futures = ("FUTURES" in tokens_upper)
            if is_spot:
                work_args = [t for t in work_args if t.upper().strip() != "SPOT"]
            elif is_futures:
                work_args = [t for t in work_args if t.upper().strip() != "FUTURES"]

            tokens_upper = [t.upper().strip() for t in work_args]
            is_gold = any(t in ["GOLD", "PAXG", "PAXGUSDT"] for t in tokens_upper)
            is_btc = any(t in ["BTC", "BTCUSDT"] for t in tokens_upper)

            user_side = "SPOT" if is_spot else "AUTO"
            filtered_tokens = []
            for t in work_args:
                u = t.upper().strip()
                if u in ["BUY", "SELL", "AUTO"]:
                    user_side = u if not is_spot else "SPOT"
                else:
                    filtered_tokens.append(t)

            non_num_tokens = [t.upper().strip() for t in filtered_tokens if not t.replace('.', '', 1).isdigit()]
            num_tokens = [float(t) for t in filtered_tokens if t.replace('.', '', 1).isdigit()]

            is_top_scan = False
            target_symbol = "TOP" if is_spot else "AUTO"
            hold_count = 1 if is_spot else 10
            scan_pool = 20
            amount = 50.0 if is_spot else 20.0
            leverage = 1 if is_spot else 10
            target_tp = 2.5

            if any(t in ["TOP", "SCAN", "AUTO"] for t in non_num_tokens) or not non_num_tokens:
                is_top_scan = True
                target_symbol = "TOP"
            elif is_gold:
                target_symbol = "PAXGUSDT"
            elif is_btc:
                target_symbol = "BTCUSDT"
            elif non_num_tokens:
                sym_cand = non_num_tokens[0]
                target_symbol = sym_cand if sym_cand.endswith("USDT") else f"{sym_cand}USDT"

            if is_spot:
                leverage = 1
                user_side = "SPOT"
                if is_top_scan:
                    if len(num_tokens) >= 2:
                        if num_tokens[0] in [1.0, 2.0, 3.0, 4.0, 5.0]:
                            hold_count = int(num_tokens[0])
                            amount = num_tokens[1]
                        elif num_tokens[0] >= 10.0 and num_tokens[1] >= 10.0:
                            scan_pool = int(num_tokens[0])
                            amount = num_tokens[1]
                            hold_count = 1
                        else:
                            amount = num_tokens[0]
                            target_tp = num_tokens[1]
                    elif len(num_tokens) == 1:
                        amount = num_tokens[0]
                        hold_count = 1
                else:
                    if num_tokens:
                        amount = num_tokens[0]
                        if len(num_tokens) >= 2:
                            target_tp = num_tokens[1]
                    hold_count = 1
            else:
                if is_top_scan:
                    if len(num_tokens) >= 4:
                        scan_pool = int(num_tokens[0])
                        hold_count = min(10, int(num_tokens[0]))
                        leverage = int(num_tokens[1])
                        amount = num_tokens[2]
                        target_tp = num_tokens[3]
                    elif len(num_tokens) == 3:
                        if num_tokens[0] > 15:
                            scan_pool = int(num_tokens[0])
                            hold_count = min(10, int(num_tokens[0]))
                            leverage = int(num_tokens[1])
                            amount = num_tokens[2]
                        else:
                            amount = num_tokens[0]
                            leverage = int(num_tokens[1])
                            target_tp = num_tokens[2]
                    elif len(num_tokens) == 2:
                        amount = num_tokens[0]
                        leverage = int(num_tokens[1])
                    elif len(num_tokens) == 1:
                        amount = num_tokens[0]
                else:
                    if len(num_tokens) >= 3:
                        amount = num_tokens[0]
                        leverage = int(num_tokens[1])
                        target_tp = num_tokens[2]
                    elif len(num_tokens) == 2:
                        amount = num_tokens[0]
                        leverage = int(num_tokens[1])
                    elif len(num_tokens) == 1:
                        amount = num_tokens[0]

            amount = max(10.50 if is_spot else 5.0, amount)

            # Strict API Permission Guard: Check Futures permission if trading Futures
            if not is_spot:
                spot_ok, fut_ok = await asyncio.to_thread(trading_engine.check_user_api_permissions, keys[0], keys[1])
                if not fut_ok:
                    db.update_system_setting(f"turbo_hedge_{chat_id}_top_mode", "0")
                    if msg_target:
                        await msg_target.reply_text("🛑 **បរាជ័យ ៖ Binance API Key របស់អ្នកមិនទាន់បានបើកសិទ្ធិ Futures Trading ទេ។**\\n💡 សូមប្រើប្រាស់ពាក្យបញ្ជា Spot ៖ `/smartx SPOT TOP 20 AUTO 50 1234`", parse_mode="Markdown")
                    return

            if is_top_scan:
                # 🚀 24/7 PERPETUAL AUTO-SCANNER INITIALIZATION
                db.update_system_setting(f"turbo_hedge_{chat_id}_top_mode", "1")
                db.update_system_setting(f"turbo_hedge_{chat_id}_top_count", str(hold_count))
                db.update_system_setting(f"turbo_hedge_{chat_id}_top_amount", str(amount))
                db.update_system_setting(f"turbo_hedge_{chat_id}_top_leverage", str(leverage))
                db.update_system_setting(f"turbo_hedge_{chat_id}_top_side", user_side)
                db.update_system_setting(f"turbo_hedge_{chat_id}_top_tp", str(target_tp))

                mode_badge = "BINANCE SPOT (0% LIQUIDATION RISK)" if is_spot else f"BINANCE FUTURES ({leverage}x ISOLATED)"
                ack_text = (
                    f"👑 **APEX SMART X | 24/7 QUANT SUITE ACTIVATED!** 🚀\\n"
                    f"───────────────────────────────\\n\\n"
                    f"🪙 Mode / Engine ៖ `{mode_badge}`\\n"
                    f"🎯 Candidate Pool ៖ `Top 1-{scan_pool} Sweet-Spot Breakout Coins`\\n"
                    f"🛡️ Max Active Coins ៖ `{hold_count} Coin{'s' if hold_count > 1 else ''} (Auto-Reinvest 24/7)`\\n"
                    f"💰 Capital / Coin ៖ `${amount:,.2f} USDT`\\n"
                    f"🎯 Target Profit ៖ `+{target_tp}%`\\n"
                    f"🛡️ Protection Armor ៖ `Breakeven Lock @ +3% | Micro-Scalp TP1 50%`\\n"
                    f"⚡ Status ៖ `កំពុងស្កេន Binance API ស្វែងរកកាក់ Sweet-Spot ភ្លាមៗ...`\\n\\n"
                    f"_ប្រព័ន្ធ AGI កំពុងរត់ស្កេន Binance 24/7 និងបើកកាក់ស្វ័យប្រវត្តិតាម Wall Street AI Brain!_"
                )
                ack_msg = None
                if msg_target:
                    try:
                        ack_msg = await msg_target.reply_text(ack_text, parse_mode="Markdown")
                    except Exception:
                        try:
                            ack_msg = await msg_target.reply_text(ack_text)
                        except Exception:
                            pass

                async def _background_smart_x_scanner():
                    try:
                        if is_spot:
                            avail_bal = await asyncio.to_thread(trading_engine.get_spot_balance, keys[0], keys[1], "USDT")
                            top_coins = turbo_hedge_engine.get_active_high_velocity_spot_coins(limit=scan_pool)
                        else:
                            avail_bal = await asyncio.to_thread(trading_engine.get_futures_available_balance, keys[0], keys[1])
                            if avail_bal <= 0.0:
                                avail_bal = await asyncio.to_thread(trading_engine.get_futures_free_margin, keys[0], keys[1])
                            top_coins = turbo_hedge_engine.get_active_high_velocity_coins(limit=scan_pool)

                        if not top_coins:
                            top_coins = ["PAXGUSDT", "BTCUSDT", "ETHUSDT", "SOLUSDT", "BNBUSDT", "DOGEUSDT"]

                        eff_amt = max(10.50 if is_spot else 5.0, amount)
                        safe_avail_bal = avail_bal * (0.95 if is_spot else 0.60)

                        if safe_avail_bal < eff_amt or avail_bal < eff_amt:
                            num_coins = 0
                        else:
                            num_coins = max(1, min(hold_count, int(safe_avail_bal / eff_amt)))

                        executed_syms = []
                        success_count = 0
                        for c_sym in top_coins:
                            if success_count >= num_coins:
                                break

                            eval_res = await asyncio.to_thread(turbo_hedge_engine.scan_and_evaluate_symbol, c_sym, leverage, avail_bal, is_spot_mode=is_spot)
                            ai_side = eval_res.get("side", "SKIP") if isinstance(eval_res, dict) else "SKIP"
                            ai_conf = float(eval_res.get("confidence_pct", 50.0) if isinstance(eval_res, dict) else 50.0)

                            if is_spot:
                                if ai_side not in ["BUY", "SPOT"] or ai_conf < 55.0:
                                    continue
                                c_side = "SPOT"
                            else:
                                if user_side in ["BUY", "SELL"]:
                                    if ai_side != user_side or ai_conf < 60.0:
                                        continue
                                    c_side = user_side
                                else:
                                    if ai_side == "SKIP" or ai_side not in ["BUY", "SELL", "SPOT"] or ai_conf < 60.0:
                                        continue
                                    c_side = ai_side

                            exec_res = await asyncio.to_thread(
                                turbo_hedge_engine.execute_turbo_hedge_trade,
                                keys[0], keys[1], c_sym, eff_amt, c_side, leverage, chat_id
                            )

                            is_order_success = False
                            if isinstance(exec_res, dict):
                                if exec_res.get("status") in ["success", "NEW", "FILLED"] or exec_res.get("orderId") or (isinstance(exec_res.get("res"), dict) and exec_res["res"].get("orderId")):
                                    is_order_success = True

                            if is_order_success:
                                db.add_turbo_hedge_bot(chat_id, c_sym, eff_amt, leverage, c_side, target_tp, is_bot_initiated=True)
                                db.update_system_setting(f"turbo_hedge_{chat_id}_{c_sym}_initiated_by_bot", "1")
                                entry_p = await asyncio.to_thread(trading_engine.get_current_price, c_sym)
                                if entry_p > 0:
                                    db.update_system_setting(f"turbo_hedge_{chat_id}_{c_sym}_entry_price", str(entry_p))
                                executed_syms.append(c_sym)
                                success_count += 1

                        opened_str = ', '.join([c.replace('USDT', '') for c in executed_syms]) if executed_syms else "កំពុងស្កេនទុនរង់ចាំចូលទិញ 24/7..."
                        final_msg = (
                            f"👑 **SUPER SMART X {'SPOT' if is_spot else 'FUTURES'} 24/7 ENGINE ACTIVATED!** 🛡️\\n"
                            f"───────────────────────────────\\n\\n"
                            f"🪙 កាក់ដែលទើបចូលវិនិយោគ ({len(executed_syms)}) ៖ `{opened_str}`\\n"
                            f"💵 Available Balance ស្កេនឃើញ ៖ `${avail_bal:,.2f} USDT`\\n"
                            f"💰 ដើមទុន / កាក់ ៖ `${eff_amt:,.2f} USDT`\\n"
                            f"🚀 Leverage កំណត់ ៖ `{leverage}x`\\n"
                            f"🎯 យុទ្ធសាស្ត្រ ៖ `Super Smart Sweet-Spot (+3% ដល់ +12%)`\\n"
                            f"🛡️ ខែលការពារ ៖ `Breakeven Armor @ +3% | Micro-Scalp TP1 50%`\\n"
                            f"⚡ Binance Status ៖ `{success_count} Coin{'s' if success_count > 1 else ''} Executed Instant (<100ms)`\\n"
                            f"🔄 **Perpetual Auto-Reinvest 24/7** ៖ `ACTIVE (ស្កេន 24/7 រក្សា {hold_count} កាក់រហូត)`\\n\\n"
                            f"_AI ស្កេន Binance Spot រៀងរាល់ ១០ វិនាទី ពេលកាក់ចាស់ឡើងដល់ TP កើបប្រាក់ចំណេញចប់ នឹងស្កេនទិញកាក់ Sweet-Spot ថ្មីអូតូ 24/7 មិនសម្រាកឡើយ!_"
                        )
                        if ack_msg:
                            try:
                                await ack_msg.edit_text(final_msg, parse_mode="Markdown")
                            except Exception:
                                try:
                                    await ack_msg.edit_text(final_msg)
                                except Exception:
                                    pass
                        elif msg_target:
                            try:
                                await msg_target.reply_text(final_msg, parse_mode="Markdown")
                            except Exception:
                                try:
                                    await msg_target.reply_text(final_msg)
                                except Exception:
                                    pass
                    except Exception as e:
                        print(f"Error in _background_smart_x_scanner: {e}")

                asyncio.create_task(_background_smart_x_scanner())
                return
            else:
                # Direct Single-Asset Execution (GOLD, BTC, or specific symbol)
                trade_side = "SPOT" if is_spot else (user_side if user_side in ["BUY", "SELL"] else "BUY")
                exec_res = await asyncio.to_thread(
                    turbo_hedge_engine.execute_turbo_hedge_trade,
                    keys[0], keys[1], target_symbol, amount, trade_side, leverage, chat_id
                )
                is_order_success = False
                if isinstance(exec_res, dict):
                    if exec_res.get("status") in ["success", "NEW", "FILLED"] or exec_res.get("orderId") or (isinstance(exec_res.get("res"), dict) and exec_res["res"].get("orderId")):
                        is_order_success = True

                if is_order_success:
                    db.add_turbo_hedge_bot(chat_id, target_symbol, amount, leverage, trade_side, target_tp, is_bot_initiated=True)
                    db.update_system_setting(f"turbo_hedge_{chat_id}_{target_symbol}_initiated_by_bot", "1")
                    entry_p = await asyncio.to_thread(trading_engine.get_current_price, target_symbol)
                    if entry_p > 0:
                        db.update_system_setting(f"turbo_hedge_{chat_id}_{target_symbol}_entry_price", str(entry_p))
                    resp_msg = (
                        f"👑 **[SMART X { 'SPOT' if is_spot else 'FUTURES'} EXECUTION SUCCESS]** 🚀\\n"
                        f"• Symbol: `{target_symbol}`\\n"
                        f"• Direction: `{trade_side}`\\n"
                        f"• Capital: `${amount:.2f} USDT` ({leverage}x Lev)\\n"
                        f"• Entry Price: `${entry_p:.4f}`\\n"
                        f"• Armor: `Breakeven Lock @ +3% ROI | Micro-Scalp TP1 50%`\\n"
                        f"• 24/7 Monitoring: `ACTIVE in HFT Turbo Hedge Monitor`"
                    )
                else:
                    resp_msg = f"⚠️ [SMART X] {exec_res.get('message', exec_res.get('reason', 'Execution notice'))}"

                if msg_target:
                    await msg_target.reply_text(resp_msg, parse_mode="Markdown")
                await delete_sensitive_message(context, chat_id, update, user_lang)
                return

"""

new_content = content[:start_idx] + replacement_subsegment + content[end_idx:]

with open(bot_thread_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Successfully patched smart_x_command in bot_thread.py!")
