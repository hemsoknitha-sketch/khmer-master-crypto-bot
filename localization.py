# localization.py

# Default fallback language is khmer
DEFAULT_LANG = 'khmer'

MESSAGES = {
    'khmer': {
        'access_denied': "❌ សុំទោស អ្នកមិនមានសិទ្ធិប្រើប្រាស់មុខងារ AI នេះទេ។\nសូមទាក់ទង Admin ដើម្បីស្នើសុំសិទ្ធិជាសមាជិក VIP។",
        'welcome_msg': "👋 ស្វាគមន៍មកកាន់ Apex AI Bot (VIP Member)!\nខ្ញុំគឺជា Super Smart AI ដែលអាចនិយាយភាសា (English, ខ្មែរ, 中文)។\nសូមផ្ញើទិន្នន័យទីផ្សារមកកាន់ខ្ញុំ ដើម្បីអោយខ្ញុំវិភាគ, ឬប្រើប្រាស់ `/analyze <ឈ្មោះកាក់>`។",
        'analyze_usage': "❌ សូមបញ្ចូលឈ្មោះកាក់។ ឧទាហរណ៍: `/analyze BTC`",
        'fetching_live_data': "🔍 កំពុងទាញយកទិន្នន័យផ្ទាល់សម្រាប់ {symbol} ពី Binance...",
        'generating_chart': "📊 កំពុងបង្កើតតារាង, ទស្សន៍ទាយ ML Prediction & វិភាគហានិភ័យ Macro AI...",
        'processing_request': "🤖 កំពុងដំណើរការសំណើរបស់អ្នក...",
        'alert_usage': "❌ របៀបប្រើប្រាស់: `/alert <កាក់> < > <តម្លៃ>`\nឧទាហរណ៍: `/alert BTC < 60000`",
        'price_must_be_number': "❌ តម្លៃត្រូវតែជាលេខសុទ្ធ។",
        'condition_invalid': "❌ លក្ខខណ្ឌត្រូវតែជា '<' ឫ '>'.",
        'alert_set': "✅ ការរំលឹកត្រូវបានកំណត់: ខ្ញុំនឹងរំលឹកអ្នកនៅពេល **{symbol}** ទៅដល់ **{condition} ${price}**.",
        'help_text': (
            "🤖 **Apex AI Bot - មឺនុយបញ្ជា (Menu)**\n\n"
            "💼 **គ្រប់គ្រងគណនី (Account & Portfolio)**\n"
            "👉 `/start` - បើកដំណើរការប្រព័ន្ធ\n"
            "👉 `/portfolio` - ពិនិត្យប្រាក់ចំណេញ និងកាក់ដែលកំពុងកាន់\n"
            "👉 `/balance` - ឆែកលុយក្នុងកាបូប Binance\n"
            "👉 `/stop` - បញ្ឈប់ប្រព័ន្ធដែលកំពុងដើរ\n\n"
            "📊 **AI វិភាគទីផ្សារ (AI Analysis)**\n"
            "👉 `/analyze <កាក់>` - វិភាគនិន្នាការទីផ្សារ\n"
            "👉 `/predict <កាក់>` - ទស្សន៍ទាយតម្លៃកាក់\n"
            "👉 `/scan` - ស្កេនរកកាក់កំពុងឡើង/ចុះខ្លាំង\n"
            "👉 `/top` - មើលកាក់ឡើងថ្លៃខ្លាំងប្រចាំថ្ងៃ\n\n"
            "⚡ **ជួញដូរស្វ័យប្រវត្តិ 24/7 (Auto-Trading & HFT)**\n"
            "👉 `/hyper_trade ON <ទុន> <PIN>` - AI ស្កេន 15s/1m HFT Scalper (Win Rate ≥ 85%)\n"
            "👉 `/auto_arb ON <ទុន> <PIN>` - Risk-Free Gold Spread & Funding Yield Harvester\n"
            "👉 `/infinity_matrix ON <ទុន> <PIN>` - Dynamic 100-200 Grid Matrix + Auto-Compound\n"
            "👉 `/sweep_auto ON <ទុន> <PIN>` - Liquidity Sweep & Bottom Wick Rebound Sniper\n"
            "👉 `/funding_harvester ON <ទុន> <PIN>` - 8-Hour Perpetual Funding Yield Harvester (Delta-Neutral 1:1)\n"
            "👉 `/auto_trade ON <Amount> <PIN>` - បើកទិញលក់ស្វ័យប្រវត្តិ\n"
            "👉 `/smart_dca <កាក់> <Amount> <PIN>` - បើកប្រព័ន្ធទិញ DCA\n"
            "👉 `/infinity_grid <កាក់> <ទុន> <ក្រឡា> <ចំណេញ> <PIN>` - Infinity Grid\n"
            "👉 `/compound_grid <កាក់> <ទុន> <ក្រឡា> <ចំណេញ> <PIN>` - Compound Grid\n"
            "👉 `/scalp <កាក់> <ទុន> <ចំណេញ> <PIN>` - AI Scalper\n"
            "👉 `/auto_snipe ON <Amount> <PIN>` - ប្រព័ន្ធទិញកាក់ថ្មីស្វ័យប្រវត្តិ\n"
            "👉 `/hedge_mode ON <Amount> <PIN>` - ការពារហានិភ័យ (Short)\n\n\n"
            "👉 `/defender ON` - បើកខែលការពារឆេះគណនី (Liquidation Defender)\n"
            "👉 `/trailing_guard ON <PIN>` - AI Trailing Profit (+1.5%) & Auto-Liquidation Guard (>50% Distance)\n\n\n"
            "👉 `/dynamic_leverage ON` - បិទ/បើក Dynamic Leverage តាមហានិភ័យ\n\n\n"
            "👉 `/delta_neutral ON <Amount>` - បើកយុទ្ធសាស្ត្រស៊ីការប្រាក់ Funding ចំណេញ ១០០%\n\n\n"
            "👉 `/sweep_sniper ON <Amount>` - ស្ទាក់ចាប់ត្រីបាឡែននៅបាត (Liquidity Sweep)\n\n\n"
            "👉 `/wave_rider ON|OFF` - បើកមុខងារជិះរលក AI Trailing Take-Profit ទម្រង់រលក\n\n"
            "🔔 **រំលឹកតម្លៃ & ព័ត៌មាន (Alerts & News)**\n"
            "👉 `/alert <កាក់> < > <តម្លៃ>` - កំណត់រំលឹកតម្លៃ\n"
            "👉 `/my_alerts` - មើលបញ្ជីរំលឹកតម្លៃរបស់អ្នក\n"
            "👉 `/cancel_alert <ID>` - លុបការរំលឹកតម្លៃ\n"
            "👉 `/news` - សង្ខេបព័ត៌មានទីផ្សារទូទៅ\n\n"
            "⚙️ **ការកំណត់ (Settings & Security)**\n"
            "👉 `/add_api` - ភ្ជាប់គណនី Binance\n"
            "👉 `/set_pin` - កំណត់លេខកូដសម្ងាត់ (PIN)\n"
            "👉 `/language` - កំណត់ភាសា\n"
            "👉 `/status` - ពិនិត្យស្ថានភាពប្រព័ន្ធ\n"
            "👉 `/help` - បង្ហាញការណែនាំនេះ\n\n"
            "👨‍💻 **ត្រូវការជំនួយ?** ទាក់ទង Admin: @HemSinath\n\n"
            "🛡️ **ការណែនាំសុវត្ថិភាព Binance API:**\n"
            "✅ **Enable Reading** (ចាំបាច់ត្រូវបើក)\n"
            "✅ **Enable Spot & Margin Trading** (ចាំបាច់ត្រូវបើក សម្រាប់ទិញលក់)\n"
            "✅ **Enable Futures** (បើកសម្រាប់តែពេលចង់លេងកាក់ចុះ/Short)\n"
            "❌ **Enable Withdrawals** (បម្រាម: ហាមបើកដាច់ខាត)\n"
            "🔒 **IP Restrictions**: ជ្រើសយក 'Unrestricted' ប្រសិនបើគ្មាន IP ថេរ។"
        ),
        'no_alerts': "🤷‍♂️ អ្នកមិនមានការរំលឹកតម្លៃ (Alerts) ដែលកំពុងដំណើរការទេ។",
        'alert_list_header': "⏰ **បញ្ជីរំលឹកតម្លៃរបស់អ្នក:**\n\n",
        'alert_cancel_usage': "\n💡 ប្រើបញ្ជា `/cancel_alert <លេខID>` ដើម្បីលុបចោល។",
        'cancel_alert_usage': "❌ សូមបញ្ចូលលេខ ID នៃការរំលឹកតម្លៃ។ ឧទាហរណ៍៖ `/cancel_alert 1`",
        'id_must_be_number': "❌ លេខ ID ត្រូវតែជាលេខសុទ្ធ។",
        'alert_cancelled': "✅ ការរំលឹកតម្លៃ ID {alert_id} ត្រូវបានលុបចោលដោយជោគជ័យ!",
        'alert_not_found': "❌ រកមិនឃើញលេខ ID នេះទេ ឬវាមិនមែនជារបស់អ្នក។",
        'fetching_top': "🔍 កំពុងទាញយកទិន្នន័យកាក់ឡើងថ្លៃខ្លាំងពី Binance...",
        'ai_analysis_header': "🤖 **ការវិភាគពី AI:**\n",
        'fetching_news': "📰 កំពុងវិភាគស្ថានភាពទីផ្សារសកល...",
        'language_current': "🌐 ភាសាបច្ចុប្បន្នរបស់អ្នកគឺ៖ **{lang}**\n\nដើម្បីផ្លាស់ប្តូរ សូមវាយបញ្ជា៖\n`/language khmer`\n`/language english`\n`/language chinese`\n`/language auto` (ប្តូរតាមភាសាដែលសួរ)",
        'language_invalid': "❌ សូមជ្រើសរើសភាសាឱ្យបានត្រឹមត្រូវ៖ `khmer`, `english`, `chinese`, ឬ `auto`",
        'language_set': "✅ ភាសាត្រូវបានកំណត់ទៅជា៖ **{lang}**",
        'add_api_usage': "❌ របៀបប្រើប្រាស់: `/add_api <API_KEY> <API_SECRET>`\n\n*បញ្ជាក់: ព័ត៌មានរបស់អ្នកត្រូវបានរក្សាទុកយ៉ាងមានសុវត្ថិភាពបំផុត និងមិនបញ្ជូនទៅភាគីទី៣ឡើយ។*",
        'api_added': "✅ គណនី Binance របស់អ្នកត្រូវបានភ្ជាប់ដោយជោគជ័យ! (API Keys រក្សាទុកដោយសុវត្ថិភាព)\n\n🤖 ពេលនេះ Bot អាចជួយទិញលក់ និងការពារប្រាក់ចំណេញជូនអ្នកដោយស្វ័យប្រវត្តិហើយ!",
        'api_invalid': "❌ API Key របស់អ្នកមិនត្រឹមត្រូវទេ ឬមិនទាន់បានបើកសិទ្ធិ (Enable Futures Trading) នៅឡើយ។ សូមពិនិត្យម្តងទៀត!",
        'broadcast_header': "📢 **សេចក្តីប្រកាសព័ត៌មាន (ANNOUNCEMENT)**\n\n",
        'price_alert_trigger': "🚨 **ទីផ្សារលោតដល់គោលដៅ (PRICE ALERT)** 🚨\n\n🪙 កាក់: {symbol}\n🎯 គោលដៅ: {condition} ${target_price}\n💵 តម្លៃបច្ចុប្បន្ន: ${current_price}",
        'sentiment_sniper_alert': "⚡ **FLASH TRADING SIGNAL (SENTIMENT SNIPER)** ⚡\n\n🎯 **រកឃើញពាក្យគន្លឹះគ្រោះថ្នាក់:** `{trigger_word}`\n📈 **និន្នាការប៉ាន់ស្មាន:** {sentiment}\n\n📰 **ចំណងជើង:** {title}\n\n⚠️ *ចំណាំ: ស្ថាប័នធំៗអាចនឹងកំពុងបញ្ជាទិញ/លក់ដោយស្វ័យប្រវត្តិ (Flash Trade) ផ្អែកលើព័ត៌មាននេះ!*",
        'auto_buy_start': "🤖 **Auto-Trading Engine:** កំពុងដាក់បញ្ជាទិញ {symbol} ស្វ័យប្រវត្តិ...",
        'auto_buy_success': "✅ **ទិញបានជោគជ័យ (SIMULATION)!**\n🪙 កាក់: {symbol}\n💵 តម្លៃទិញ: ${buy_price:,.2f}\n📉 Stop-Loss ដំបូង: ${initial_stop_loss:,.2f}\n\n🛡️ *Trailing Stop-Loss ត្រូវបានបើកដំណើរការដោយស្វ័យប្រវត្តិ!*",
        'auto_buy_fail': "❌ បរាជ័យក្នុងការទិញ: {error}",
        'trailing_stop_triggered': "🚨 **TRAILING STOP-LOSS TRIGGERED!** 🚨\n\n🤖 Bot បានលក់ {symbol} ចេញដោយស្វ័យប្រវត្តិ!\n💵 តម្លៃលក់: ${current_price:,.2f}\n📉 លទ្ធផល: {emoji} {result_msg} ({pl_pct:+.2f}%)\n\n*យើងមិនអោយខាតធំ ហើយយើងក៏មិនអោយបាត់ចំណេញដែរ!*",
        'scale_out_success': "✅ **SCALE-OUT TAKE PROFIT (Level {level})!** 📈\n\n🤖 Bot បានប្រមូលចំណេញ {symbol} ជាកាំជណ្តើរ!\n💵 តម្លៃលក់: ${price:,.2f} (+{profit_pct:+.2f}%)\n💰 លក់ចំនួន: {sold_qty} (នៅសល់ {remaining_qty})\n\n*ចំណេញត្រូវតែកើបដាក់ហោប៉ៅខ្លះ!*",
        'mirror_trade_success': "🐋 **SMART MONEY MIRROR TRADE!**\n\n🤖 Bot បាន Copy Trade តាម {whale}!\n🪙 កាក់: {symbol}\n💵 តម្លៃទិញ: ${price:,.2f}\n\n🛡️ *Trailing Stop-Loss ត្រូវបានបើកដោយស្វ័យប្រវត្តិ!*",
        'profit': "ចំណេញ",
        'break_even': "កាត់ខាតតិចតួច (ការពារដើម)",
        'economic_alert': "🚨 **ដំណឹងសេដ្ឋកិច្ចសំខាន់ (High Impact Event)** 🚨\n\n🇺🇸 ព្រឹត្តិការណ៍: {event_title}\n⏰ ម៉ោងចេញ: {event_time}\n\n⚠️ **បំរាម:** ទីផ្សារគ្រីបតូអាចនឹងលោតឡើងចុះខ្លាំងនៅម៉ោងនេះ។ សូមប្រុងប្រយ័ត្ន!",
        'whale_alert': "🐋 **WHALE ALERT (ត្រីបាឡែនធ្វើសកម្មភាព)** 🐋\n\n🪙 {coin}\n💰 ចំនួន: {amount_str} 🪙 (~${amount_usd_str})\n🔄 ពី: `{from_addr}`\n➡️ ទៅ: `{to_addr}`\n\n⚠️ *ការប្រុងប្រយ័ត្ន: {warning}*",
        'funding_rate_alert': "🚨 **រ៉ាដាចាប់សញ្ញា Funding Rate គ្រោះថ្នាក់** 🚨\n\n🪙 កាក់: **{symbol}**\n📈 Funding Rate: **{rate}%**\n\n⚠️ {message}",
        'smart_money_alert': "🐋 **SMART MONEY TRACKER ALERT** 🐋\n\n👤 **កាបូបមហាសេដ្ឋី:** Vitalik Buterin\n🔄 **សកម្មភាព:** {action}\n💰 **ចំនួន:** {value_eth:,.2f} ETH\n📍 **ទៅកាន់ (To):** `{to_addr}`\n\n🔗 [មើលប្រតិបត្តិការលើ Blockscout]({tx_link})",
        'action_sent': "📤 ផ្ទេរចេញពីកាបូប (Sent)",
        'action_received': "📥 ទទួលចូលកាបូប (Received)",
        'bullish': "BULLISH 🚀",
        'bearish': "BEARISH 🩸",
        'above': "លើសពី (Above)",
        'below': "ក្រោម (Below)",
        'please_wait_processing': "⏳ សូមរង់ចាំបន្តិច ខ្ញុំកំពុងវិភាគសំណួរមុនរបស់អ្នក...",
        'timeout_blocked': "🚫 អ្នកកំពុងផ្ញើសារលឿនពេក (Spam)! ប្រព័ន្ធការពារបានផ្អាកសិទ្ធិអ្នកចំនួន ៥ នាទី។",
        'pin_set_success': "✅ ជោគជ័យ! លេខកូដ PIN របស់អ្នកត្រូវបានកំណត់។ សូមចងចាំវាអោយបានច្បាស់។",
        'pin_incorrect': "❌ លេខកូដ PIN មិនត្រឹមត្រូវ! សិទ្ធិត្រូវបានបដិសេធ។",
        'pin_required': "❌ លោកអ្នកមិនទាន់បានបង្កើតលេខ PIN សុវត្ថិភាពនៅឡើយទេ។ សូមបង្កើតវាជាមុនសិន ដោយវាយពាក្យបញ្ជា /set_pin 5679 (អាចប្តូរ 5679 ទៅជាលេខ ៤ខ្ទង់ ផ្សេងទៀតដែលលោកអ្នកពេញចិត្ត)។",
        'set_pin_usage': "❌ របៀបប្រើ: `/set_pin <លេខ៤ខ្ទង់>` ឬ `/set_pin <លេខចាស់> <លេខថ្មី>`",
        'weak_pin_error': "❌ លេខសម្ងាត់ខ្សោយពេក! សូមកុំប្រើលេខជាន់គ្នា (1111) ឬលេខរៀង (1234) ដើម្បីសុវត្ថិភាពខ្ពស់។",
        'add_api_usage_pin': "❌ របៀបប្រើ: `/add_api <API_KEY> <API_SECRET> <PIN>`",
        'api_private_only': "⚠️ **បដិសេធ (Security Alert)**\n\nដើម្បីសុវត្ថិភាពខ្ពស់ ការដាក់បញ្ចូល API Key អនុញ្ញាតតែនៅក្នុងការឆាតផ្ទាល់ (Private Chat) ប៉ុណ្ណោះ។ សូមលុបសាររបស់អ្នកចេញពី Group នេះភ្លាមៗដើម្បីសុវត្ថិភាព!",
        'msg_auto_deleted': "🗑️ *(សុវត្ថិភាព: សាររបស់អ្នកត្រូវបានលុបចោលដោយស្វ័យប្រវត្តិ)*",
        'auto_trade_usage': "❌ របៀបប្រើប្រាស់: `/auto_trade ON <Amount_USDT> <PIN>` ឬ `/auto_trade OFF <PIN>`\nឧទាហរណ៍: `/auto_trade ON 50 1234`",
        'auto_trade_enabled': "✅ មុខងារជួញដូរស្វ័យប្រវត្តិ (Auto-Trade) ត្រូវបានបើក!\n💵 ទំហំទឹកប្រាក់: ${amount} USDT\n🛡️ Trailing Stop-Loss: {trailing}%\n\n*បញ្ជាក់: រាល់ពេល AI ចេញលទ្ធផល BUY Bot នឹងទិញអោយអ្នកដោយស្វ័យប្រវត្តិ!*",
        'auto_trade_disabled': "🚫 មុខងារជួញដូរស្វ័យប្រវត្តិ (Auto-Trade) ត្រូវបានបិទ។",
        'hyper_trade_usage': "❌ របៀបប្រើប្រាស់: `/hyper_trade ON <Amount_USDT> <PIN>` ឬ `/hyper_trade OFF <PIN>`\nឧទាហរណ៍: `/hyper_trade ON 10 1234`",
        'hyper_trade_enabled': "🚀 **Apex Hyper-Trade Engine ត្រូវបានបើកដំណើរការ (24/7 HFT Active)!**\n\n💵 ទំហំទុនក្នុង១ដៃ: ${amount} USDT\n🎯 គោលដៅចំណេញ Take-Profit: 0.3% - 0.8%\n⚡ ប្រេកង់ស្កេន (Timeframe): 15s / 1m HFT\n🧠 Win Rate Threshold: ≥ 85.0%\n\n*AI នឹងស្កេន និងទិញ-លក់ស្វ័យប្រវត្តិបន្តបន្ទាប់ 24/7 គ្មានថ្ងៃសម្រាក!*",
        'hyper_trade_disabled': "🚫 **Apex Hyper-Trade Engine ត្រូវបានបិទ។**",
        'auto_arb_usage': "❌ របៀបប្រើប្រាស់: `/auto_arb ON <Amount_USDT> <PIN>` ឬ `/auto_arb OFF <PIN>`\nឧទាហរណ៍: `/auto_arb ON 50 1234`",
        'auto_arb_enabled': "⚡ **Delta-Neutral Arbitrage Auto-Harvester ត្រូវបានបើក (Risk-Free Active)!**\n\n💵 ទំហំទុនកេងចំណេញ: ${amount} USDT\n🛡️ យុទ្ធសាស្ត្រ: PAXG/Gold Spread + Funding Yield Arbitrage\n⚖️ Delta Exposure: 0% (Delta-Neutral Hedged)\n\n*AI នឹងស្កេន និងប្រមូលចំណេញ Risk-Free ស្វ័យប្រវត្តិរៀងរាល់ ១០ វិនាទី!*",
        'auto_arb_disabled': "🚫 **Delta-Neutral Arbitrage Auto-Harvester ត្រូវបានបិទ。**",
        'infinity_matrix_usage': "❌ របៀបប្រើប្រាស់: `/infinity_matrix ON <ទុនសរុប_USDT> <PIN>` ឬ `/infinity_matrix OFF <PIN>`\nឧទាហរណ៍: `/infinity_matrix ON 500 1234`",
        'infinity_matrix_enabled': "🎯 **AI Dynamic Auto-Compounding Grid ត្រូវបានបើកដំណើរការ!**\n\n💵 ដើមទុនរាយសំណាញ់: ${capital} USDT\n🕸️ ចំនួនក្រឡា Matrix: {grids} Grids\n🪙 និមិត្តសញ្ញាកាក់: {symbol}\n📈 ចន្លោះតម្លៃ Matrix: ${lower} - ${upper}\n♻️ យន្តការ: Auto-Compounding Profit Multiplier (ពហុគុណទុន)\n\n*AI នឹងរាយសំណាញ់ទិញថោក លក់ថ្លៃ និងបូកចំណេញចូលដើមទុនស្វ័យប្រវត្តិ!*",
        'infinity_matrix_disabled': "🚫 **AI Dynamic Auto-Compounding Grid ត្រូវបានបិទ。**",
        'sweep_auto_usage': "❌ របៀបប្រើប្រាស់: `/sweep_auto ON <Amount_USDT> <PIN>` ឬ `/sweep_auto OFF <PIN>`\nឧទាហរណ៍: `/sweep_auto ON 50 1234`",
        'sweep_auto_enabled': "🛡️ **Apex AI Liquidity Sweep Sniper ត្រូវបានបើក (Wick Sniper Active)!**\n\n💵 ទំហំទុនស្ទាក់ទិញ: ${amount} USDT\n🎯 គោលដៅ: Liquidation Dumps & Sudden Wicks (≥ 0.4% Drop)\n⚡ Rebound Target: 5 - 10 Seconds V-Shape Exit\n⚙️ Dynamic Leverage: 5x Futures\n\n*AI នឹងស្កេនស្ទាក់ទិញនៅបាតជើង Candle វែងៗ និងលក់កាត់ចំណេញស្វ័យប្រវត្តិ!*",
        'sweep_auto_disabled': "🚫 **Apex AI Liquidity Sweep Sniper ត្រូវបានបិទ。**",
        'trailing_guard_usage': "❌ របៀបប្រើប្រាស់: `/trailing_guard ON <PIN>` ឬ `/trailing_guard OFF <PIN>`\nឧទាហរណ៍: `/trailing_guard ON 1234`",
        'trailing_guard_enabled': "🛡️ **Dynamic Trailing Profit & Auto-Liquidation Guard ត្រូវបានបើក!**\n\n🎯 Dynamic Trailing Threshold: +1.5% Profit Trigger\n📈 Max Profit Ride: Trailing Stop តាមពីក្រោយ 0.5%\n🛡️ Auto-Liquidation Safety: គណនាតាម Leverage ជាក់ស្តែង (<30% Buffer Guard)\n\n*ប្រព័ន្ធនឹងការពារគណនី Futures របស់អ្នកពី Liquidation និងប្រមូលចំណេញខ្ពស់បំផុត!*",
        'trailing_guard_disabled': "🚫 **Dynamic Trailing Profit & Auto-Liquidation Guard ត្រូវបានបិទ។**",
        'trailing_guard_tp_triggered': "💎 **TRAILING GUARD PROFIT LOCKED!** 💎\n\n🪙 **{symbol}**\n📈 **Peak PnL:** +{peak_pnl:.2f}%\n💰 **Locked PnL:** +{locked_pnl:.2f}%\n💵 **Exit Price:** ${exit_price:,.2f}\n\n*Apex AI នឹងការពារចំណេញ និងមិនបណ្តោយឱ្យចំណេញប្រែជាខាតឡើយ!*",
        'liquidation_guard_alert': "🛡️ **AUTO-LIQUIDATION GUARD TRIGGERED!** 🛡️\n\n🪙 **{symbol}** ({side})\n📉 **Prev Liquidation Distance:** {old_distance:.2f}%\n⚡ **Action Taken:** De-leveraged / Reduced position size by 30%\n✅ **New Liquidation Distance:** {new_distance:.2f}% (Safe Zone Extended)\n\n*គណនី Futures របស់អ្នកត្រូវបានការពារពី Liquidation ដោយសុវត្ថិភាព!*",
        'daily_executive_summary_report': (
            "📊 **APEX AI 24-HOUR EXECUTIVE SUMMARY REPORT** 📊\n"
            "───────────────────────────────\n"
            "🏦 **PORTFOLIO BALANCE & EQUITY:**\n"
            "💵 Spot Balance: **${spot_bal:,.2f} USDT**\n"
            "📈 Futures Balance: **${futures_bal:,.2f} USDT**\n\n"
            "💰 **24-HOUR PERFORMANCE:**\n"
            "💎 Realized PnL: **+${total_pnl:,.2f} USDT**\n"
            "⚡ Micro-Trades Executed: **{trades_24h} Trades**\n"
            "🎯 AI Strategy Win Rate: **{win_rate:.1f}%**\n\n"
            "🤖 **SUPER SMART ENGINES STATUS (24/7 Silent):**\n"
            "🚀 Hyper-Trade Scalper: {hyper_status}\n"
            "⚡ Delta-Neutral Arbitrage: {arb_status}\n"
            "🛡️ Liquidity Sweep Sniper: {sweep_status}\n"
            "🌾 Perpetual Funding Harvester: {funding_status}\n"
            "🛡️ Auto-Liquidation Guard: {guard_status}\n\n"
            "⚙️ *Apex Super Brain កំពុងដំណើរការស្វ័យប្រវត្តិ ២៤ម៉ោង/ថ្ងៃ ដោយសុវត្ថិភាព 0% Risk!*"
        ),

        'whale_deposit_alert': "🚨 **ON-CHAIN RED ALERT (INFLOW)** 🚨\n\n🐋 ត្រីបាឡែនទើបតែផ្ទេរលុយចូល **Binance**!\n💰 ទំហំសាច់ប្រាក់: **${value:,.2f} {symbol}**\n\n⚠️ *ចំណាំ: នេះអាចជាសញ្ញានៃការត្រៀមទិញកាក់ធំៗ ឬអាចជាការទម្លាក់លក់ (Dump)!*",
        'whale_withdrawal_alert': "💸 **ON-CHAIN GREEN ALERT (OUTFLOW)** 💸\n\n🐋 ត្រីបាឡែនទើបតែដកលុយចេញពី **Binance**!\n💰 ទំហំសាច់ប្រាក់: **${value:,.2f} {symbol}**\n\n🟢 *ចំណាំ: ការដកសាច់ប្រាក់ចេញច្រើន អាចមានន័យថាពួកគេកំពុងប្រមូលទិញហើយយកទៅលាក់ទុក (Accumulation)!*",
        'smart_dca_usage': "❌ របៀបប្រើប្រាស់: `/smart_dca <ឈ្មោះកាក់> <ទំហំប្រាក់> <PIN>`\nឧទាហរណ៍: `/smart_dca BTC 100 1234`",
        'smart_dca_set': "✅ **Smart DCA ត្រូវបានចាប់ផ្តើម!**\n🤖 ខ្ញុំកំពុងតាមដាន **{symbol}** ចាប់ពីតម្លៃ **${entry_price:,.2f}**។ បើវាធ្លាក់ចុះខ្លាំង ខ្ញុំនឹងប្រើប្រាស់យុទ្ធសាស្រ្ត Martingale គុណលុយទិញជាកាំជណ្តើរភ្លាមៗ!",
        'smart_dca_buy_success': "🤖 **SMART DCA ដំណើរការ!** 🤖\n\nទិញបានសម្រេច: **${amount:,.2f} នៃ {symbol}** ក្នុងតម្លៃ {buy_price}។ (DCA Drop Level: {level})\n\n🛡 មុខងារ Auto-Trade & Trailing Stop នឹងគ្រប់គ្រងការលក់កាត់ចំណេញដោយស្វ័យប្រវត្តិ!",
        'smart_dca_deactivated': "✅ **SMART DCA ត្រូវបានបិទ!** គ្រប់កម្រិតនៃការធ្លាក់ចុះនៃ {symbol} ត្រូវបានប្រមូលទិញអស់ហើយ។",
        'grid_bot_usage': "❌ របៀបប្រើប្រាស់: `/grid_bot <កាក់> <តម្លៃទាប> <តម្លៃខ្ពស់> <ចំនួនជួរ> <ទឹកប្រាក់> <PIN>`\nឧទាហរណ៍: `/grid_bot BTC 60000 70000 10 1000 1234`",
        'grid_bot_set': "✅ **Grid Bot បានចាប់ផ្តើមរាយសំណាញ់!**\n🤖 ខ្ញុំបានរាយខ្សែទិញ/លក់ {grids} ជួរ សម្រាប់ {symbol} ក្នុងចន្លោះតម្លៃ ${lower} - ${upper}。",
        'grid_bot_arbitrage': "⚡ **GRID ARBITRAGE!** ⚡\n✅ ទើបតែកេងចំណេញបានពីការលោតចុះឡើងនៃ {symbol} នៅតម្លៃ ${price:,.2f}!",
        'hedge_mode_usage': "❌ របៀបប្រើប្រាស់: `/hedge_mode ON <Amount> <PIN>` ឬ `/hedge_mode OFF <PIN>`",
        'hedge_mode_enabled': "✅ **មុខងារការពារហានិភ័យ (Hedge Mode) ត្រូវបានបើក!**\n\n💵 ទំហំលុយ: ${amount}\n⚙️ Leverage: {leverage}x\n\n*ពេល AI ឃើញថាទីផ្សារនឹងធ្លាក់ចុះ វាទាញយកប្រាក់ចំណេញពីការ Short មកប៉ះប៉ូវកាក់ដែលចាញ់!*",
        'hedge_mode_disabled': "🚫 **Hedge Mode ត្រូវបានបិទ!**",
        'hedge_short_start': "🤖 **Hedge Fund Engine:** កំពុងបើកទីផ្សារ Short (Futures) លើ {symbol} ដោយស្វ័យប្រវត្តិដើម្បីការពារហានិភ័យ...",
        'hedge_short_success': "✅ **HEDGE SHORT ACTIVE!** 📉\n\n🪙 កាក់: {symbol}\n💵 តម្លៃ Short: ${price:,.2f}\n⚙️ Leverage: {leverage}x\n\n*Bot កំពុងរកលុយពីការធ្លាក់ចុះទីផ្សារ!*",
        'hedge_short_dynamic_alert': "🤖 _AI Dynamic Risk: កំណត់ Leverage {leverage}x ដោយស្វ័យប្រវត្តិ ផ្អែកលើទំហំនៃការប្រែប្រួលទីផ្សារ (Volatility) និងពិន្ទុភាពប្រាកដ (Confidence: {confidence}%)!_",
        'hedge_short_fail': "❌ បរាជ័យក្នុងការ Short: {error}",
        'hedge_short_closed': "{emoji} **HEDGE SHORT {result}!**\n\n🤖 Bot បានបិទការ Short {symbol}\n💵 តម្លៃបិទ: ${price:,.2f}\n📉 លទ្ធផល: {pnl_pct:+.2f}%",
        'remove_api_usage': "❌ របៀបប្រើប្រាស់: `/remove_api <PIN>`\nឧទាហរណ៍: `/remove_api 1234`",
        'remove_api_success': "✅ ជោគជ័យ! API Key របស់អ្នកត្រូវបានលុបចេញពីប្រព័ន្ធទាំងស្រុង។ មុខងារ Auto-Trading ទាំងអស់ត្រូវបានបិទ (Kill Switch)។",
        'remove_api_not_found': "🤷‍♂️ អ្នកមិនទាន់បានភ្ជាប់ API ណាមួយនៅឡើយទេ ឫ API ត្រូវបានលុបរួចហើយ។",
    },
    'english': {
        'access_denied': "❌ Sorry, you do not have permission to use this AI feature.\nPlease contact the Admin to request VIP access.",
        'welcome_msg': "👋 Welcome to Apex AI Bot (VIP Member)!\nI am a Super Smart AI (English, ខ្មែរ, 中文).\nSend me any market data to analyze, or use `/analyze <symbol>`.",
        'analyze_usage': "❌ Please provide a symbol. Example: `/analyze BTC`",
        'fetching_live_data': "🔍 Fetching Live Data for {symbol} from Binance...",
        'generating_chart': "📊 Generating Chart, ML Prediction & Macro AI Risk Analysis...",
        'processing_request': "🤖 Processing your request...",
        'alert_usage': "❌ Usage: `/alert <SYMBOL> < > <PRICE>`\nExample: `/alert BTC < 60000`",
        'price_must_be_number': "❌ Price must be a number.",
        'condition_invalid': "❌ Condition must be '<' or '>'.",
        'alert_set': "✅ Alert Set: I will notify you when **{symbol}** goes **{condition} ${price}**.",
        'help_text': (
            "🤖 **Apex AI Bot - Command Menu**\n\n"
            "💼 **Account & Portfolio**\n"
            "👉 `/start` - Start the bot\n"
            "👉 `/portfolio` - Check your PnL & active positions\n"
            "👉 `/balance` - Check Binance spot balance\n"
            "👉 `/stop` - Stop active trading bots\n\n"
            "📊 **AI Analysis**\n"
            "👉 `/analyze <symbol>` - Market Analysis\n"
            "👉 `/predict <symbol>` - Predict price trend\n"
            "👉 `/scan` - Scan for top gainers/losers\n"
            "👉 `/top` - View daily top gainers\n\n"
            "⚡ **24/7 Auto-Trading & HFT Engine**\n"
            "👉 `/hyper_trade ON <Amount> <PIN>` - AI 15s/1m HFT Scalper (Win Rate ≥ 85%)\n"
            "👉 `/auto_arb ON <Amount> <PIN>` - Risk-Free Gold Spread & Funding Yield Harvester\n"
            "👉 `/infinity_matrix ON <Capital> <PIN>` - Dynamic 100-200 Grid Matrix + Auto-Compound\n"
            "👉 `/sweep_auto ON <Amount> <PIN>` - Liquidity Sweep & Bottom Wick Rebound Sniper\n"
            "👉 `/auto_trade ON <Amount> <PIN>` - Enable Auto-Trading\n"
            "👉 `/smart_dca <Symbol> <Amount> <PIN>` - Enable Smart DCA\n"
            "👉 `/infinity_grid <Symbol> ... <PIN>` - Infinity Grid Bot\n"
            "👉 `/compound_grid <Symbol> ... <PIN>` - Compound Grid Bot\n"
            "👉 `/scalp <Symbol> ... <PIN>` - AI Scalper (Ping-Pong)\n"
            "👉 `/auto_snipe ON <Amount> <PIN>` - Auto Snipe New Listings\n"
            "👉 `/hedge_mode ON <Amount> <PIN>` - Enable Hedge Mode (Short)\n\n\n"
            "👉 `/defender ON` - Enable AI Liquidation Defender\n\n\n"
            "👉 `/dynamic_leverage ON` - Enable AI Dynamic Leverage\n\n\n"
            "👉 `/delta_neutral ON <Amount>` - Enable Delta-Neutral Funding Arbitrage\n\n\n"
            "👉 `/sweep_sniper ON <Amount>` - Hunt Whales at the bottom (Liquidity Sweep)\n\n\n"
            "👉 `/wave_rider ON|OFF` - Enable AI Dynamic Wave Riding Trailing-Stop\n\n"
            "🔔 **Alerts & News**\n"
            "👉 `/alert <symbol> < > <price>` - Price Alert\n"
            "👉 `/my_alerts` - View your price alerts\n"
            "👉 `/cancel_alert <ID>` - Cancel a price alert\n"
            "👉 `/news` - Global market summary\n\n"
            "⚙️ **Settings & Security**\n"
            "👉 `/add_api` - Connect Binance API\n"
            "👉 `/set_pin` - Set PIN code\n"
            "👉 `/language` - Set language\n"
            "👉 `/status` - Check system status\n"
            "👉 `/help` - Show this help message\n\n"
            "👨‍💻 **Need Help?** Contact Admin: @HemSinath\n\n"
            "🛡️ **Binance API Security Guide:**\n"
            "✅ **Enable Reading** (Required)\n"
            "✅ **Enable Spot & Margin Trading** (Required for Auto-Trading)\n"
            "✅ **Enable Futures** (Required for Hedge Mode/Shorts)\n"
            "❌ **Enable Withdrawals** (CRITICAL: Must be DISABLED)\n"
            "🔒 **IP Restrictions**: Select 'Unrestricted' if no static IP."
        ),
        'no_alerts': "🤷‍♂️ You don't have any active price alerts.",
        'alert_list_header': "⏰ **Your Price Alerts:**\n\n",
        'alert_cancel_usage': "\n💡 Use `/cancel_alert <ID>` to remove.",
        'cancel_alert_usage': "❌ Please enter the alert ID. Example: `/cancel_alert 1`",
        'id_must_be_number': "❌ ID must be a number.",
        'alert_cancelled': "✅ Alert ID {alert_id} has been cancelled successfully!",
        'alert_not_found': "❌ Alert ID not found or doesn't belong to you.",
        'fetching_top': "🔍 Fetching top gainers from Binance...",
        'ai_analysis_header': "🤖 **AI Analysis:**\n",
        'fetching_news': "📰 Analyzing global macro market...",
        'language_current': "🌐 Your current language is: **{lang}**\n\nTo change, use:\n`/language khmer`\n`/language english`\n`/language chinese`\n`/language auto`",
        'language_invalid': "❌ Invalid language. Choose `khmer`, `english`, `chinese`, or `auto`.",
        'language_set': "✅ Language set to: **{lang}**",
        'add_api_usage': "❌ Usage: `/add_api <API_KEY> <API_SECRET>`\n\n*Note: Your credentials are kept securely and not shared with 3rd parties.*",
        'api_added': "✅ Your Binance API is connected successfully! (Keys stored securely)\n\n🤖 The Bot can now auto-trade and manage trailing stops for you!",
        'api_invalid': "❌ Your API Key is invalid or Futures Trading is not enabled! Please check again.",
        'broadcast_header': "📢 **ANNOUNCEMENT**\n\n",
        'price_alert_trigger': "🚨 **PRICE ALERT** 🚨\n\n🪙 Coin: {symbol}\n🎯 Target: {condition} ${target_price}\n💵 Current Price: ${current_price}",
        'sentiment_sniper_alert': "⚡ **FLASH TRADING SIGNAL (SENTIMENT SNIPER)** ⚡\n\n🎯 **Keyword Detected:** `{trigger_word}`\n📈 **Sentiment:** {sentiment}\n\n📰 **Headline:** {title}\n\n⚠️ *Note: High-Frequency Trading bots might be reacting to this news!*",
        'auto_buy_start': "🤖 **Auto-Trading Engine:** Placing automated market buy for {symbol}...",
        'auto_buy_success': "✅ **BUY SUCCESS (SIMULATION)!**\n🪙 Coin: {symbol}\n💵 Buy Price: ${buy_price:,.2f}\n📉 Initial SL: ${initial_stop_loss:,.2f}\n\n🛡️ *Trailing Stop-Loss is now active!*",
        'auto_buy_fail': "❌ Buy Failed: {error}",
        'trailing_stop_triggered': "🚨 **TRAILING STOP-LOSS TRIGGERED!** 🚨\n\n🤖 Bot auto-sold {symbol}!\n💵 Sell Price: ${current_price:,.2f}\n📉 Result: {emoji} {result_msg} ({pl_pct:+.2f}%)\n\n*We don't allow huge losses, and we secure profits!*",
        'scale_out_success': "✅ **SCALE-OUT TAKE PROFIT (Level {level})!** 📈\n\n🤖 Bot took partial profit for {symbol}!\n💵 Sell Price: ${price:,.2f} (+{profit_pct:+.2f}%)\n💰 Sold Qty: {sold_qty} (Remaining: {remaining_qty})\n\n*Always secure some profits!*",
        'mirror_trade_success': "🐋 **SMART MONEY MIRROR TRADE!**\n\n🤖 Bot copied {whale}'s trade!\n🪙 Coin: {symbol}\n💵 Buy Price: ${price:,.2f}\n\n🛡️ *Trailing Stop-Loss active!*",
        'profit': "PROFIT",
        'break_even': "BREAK-EVEN (Capital Protected)",
        'economic_alert': "🚨 **High Impact Economic Event** 🚨\n\n🇺🇸 Event: {event_title}\n⏰ Time: {event_time}\n\n⚠️ **Warning:** Crypto markets might be highly volatile at this time. Trade with caution!",
        'whale_alert': "🐋 **WHALE ALERT** 🐋\n\n🪙 {coin}\n💰 Amount: {amount_str} 🪙 (~${amount_usd_str})\n🔄 From: `{from_addr}`\n➡️ To: `{to_addr}`\n\n⚠️ *Caution: {warning}*",
        'funding_rate_alert': "🚨 **Extreme Funding Rate Detected** 🚨\n\n🪙 Coin: **{symbol}**\n📈 Funding Rate: **{rate}%**\n\n⚠️ {message}",
        'smart_money_alert': "🐋 **SMART MONEY TRACKER ALERT** 🐋\n\n👤 **Whale:** Vitalik Buterin\n🔄 **Action:** {action}\n💰 **Amount:** {value_eth:,.2f} ETH\n📍 **To:** `{to_addr}`\n\n🔗 [View on Blockscout]({tx_link})",
        'action_sent': "📤 Sent",
        'action_received': "📥 Received",
        'bullish': "BULLISH 🚀",
        'bearish': "BEARISH 🩸",
        'above': "Above",
        'below': "Below",
        'please_wait_processing': "⏳ Please wait, I am currently processing your previous request...",
        'timeout_blocked': "🚫 You are sending messages too fast (Spam)! The security system has temporarily blocked you for 5 minutes.",
        'pin_set_success': "✅ Success! Your PIN code has been set. Please remember it.",
        'pin_incorrect': "❌ Incorrect PIN code! Access denied.",
        'pin_required': "❌ This is a sensitive command. Please provide your 4-digit PIN.",
        'set_pin_usage': "❌ Usage: `/set_pin <4-digit-pin>` or `/set_pin <old_pin> <new_pin>`",
        'weak_pin_error': "❌ Weak PIN! Please avoid repeating (1111) or sequential (1234) numbers for higher security.",
        'add_api_usage_pin': "❌ Usage: `/add_api <API_KEY> <API_SECRET> <PIN>`",
        'api_private_only': "⚠️ **Security Alert**\n\nTo ensure your security, adding an API Key is only allowed in Private Chat. Please delete your message from this group immediately!",
        'msg_auto_deleted': "🗑️ *(Security: Your message was automatically deleted)*",
        'auto_trade_usage': "❌ Usage: `/auto_trade ON <Amount_USDT> <PIN>` or `/auto_trade OFF <PIN>`\nExample: `/auto_trade ON 50 1234`",
        'auto_trade_enabled': "✅ Auto-Trade enabled!\n💵 Amount: ${amount} USDT\n🛡️ Trailing Stop-Loss: {trailing}%\n\n*Note: Bot will auto-buy whenever AI outputs a BUY signal!*",
        'auto_trade_disabled': "🚫 Auto-Trade has been disabled.",
        'trailing_guard_usage': "❌ Usage: `/trailing_guard ON <PIN>` or `/trailing_guard OFF <PIN>`\nExample: `/trailing_guard ON 1234`",
        'trailing_guard_enabled': "🛡️ **Dynamic Trailing Profit & Auto-Liquidation Guard ENABLED!**\n\n🎯 Dynamic Trailing Threshold: +1.5% Profit Trigger\n📈 Max Profit Ride: 0.5% Trailing Step\n🛡️ Auto-Liquidation Safety: Leverage-Calibrated (<30% Buffer Guard)\n\n*AI will continuously ride profits and shield your Futures account from liquidation!*",
        'trailing_guard_disabled': "🚫 **Dynamic Trailing Profit & Auto-Liquidation Guard DISABLED.**",
        'trailing_guard_tp_triggered': "💎 **TRAILING GUARD PROFIT LOCKED!** 💎\n\n🪙 **{symbol}**\n📈 **Peak PnL:** +{peak_pnl:.2f}%\n💰 **Locked PnL:** +{locked_pnl:.2f}%\n💵 **Exit Price:** ${exit_price:,.2f}\n\n*Apex AI secured your maximum profit run!*",
        'liquidation_guard_alert': "🛡️ **AUTO-LIQUIDATION GUARD TRIGGERED!** 🛡️\n\n🪙 **{symbol}** ({side})\n📉 **Prev Liquidation Distance:** {old_distance:.2f}%\n⚡ **Action Taken:** De-leveraged / Reduced position by 30%\n✅ **New Liquidation Distance:** {new_distance:.2f}% (Safe Zone Extended)\n\n*Your Futures position is completely safe from liquidation!*",
        'daily_executive_summary_report': (
            "📊 **APEX AI 24-HOUR EXECUTIVE SUMMARY REPORT** 📊\n"
            "───────────────────────────────\n"
            "🏦 **PORTFOLIO BALANCE & EQUITY:**\n"
            "💵 Spot Balance: **${spot_bal:,.2f} USDT**\n"
            "📈 Futures Balance: **${futures_bal:,.2f} USDT**\n\n"
            "💰 **24-HOUR PERFORMANCE:**\n"
            "💎 Realized PnL: **+${total_pnl:,.2f} USDT**\n"
            "⚡ Micro-Trades Executed: **{trades_24h} Trades**\n"
            "🎯 AI Strategy Win Rate: **{win_rate:.1f}%**\n\n"
            "🤖 **SUPER SMART ENGINES STATUS (24/7 Silent):**\n"
            "🚀 Hyper-Trade Scalper: {hyper_status}\n"
            "⚡ Delta-Neutral Arbitrage: {arb_status}\n"
            "🛡️ Liquidity Sweep Sniper: {sweep_status}\n"
            "🌾 Perpetual Funding Harvester: {funding_status}\n"
            "🛡️ Auto-Liquidation Guard: {guard_status}\n\n"
            "⚙️ *Apex Super Brain is running autonomously 24/7 with zero notification spam!*"
        ),

        'whale_deposit_alert': "🚨 **ON-CHAIN RED ALERT (INFLOW)** 🚨\n\n🐋 A whale just deposited into **Binance**!\n💰 Amount: **${value:,.2f} {symbol}**\n\n⚠️ *Note: This could indicate a massive buy order preparation or a potential market dump!*",
        'whale_withdrawal_alert': "💸 **ON-CHAIN GREEN ALERT (OUTFLOW)** 💸\n\n🐋 A whale just withdrew from **Binance**!\n💰 Amount: **${value:,.2f} {symbol}**\n\n🟢 *Note: Massive outflows often indicate accumulation and storage!*",
        'smart_dca_usage': "❌ Usage: `/smart_dca <SYMBOL> <AMOUNT> <PIN>`\nExample: `/smart_dca BTC 100 1234`",
        'smart_dca_set': "✅ **Smart DCA Activated!**\n🤖 I am monitoring **{symbol}** from **${entry_price:,.2f}**. If it drops significantly, I will execute a Martingale ladder buy strategy!",
        'smart_dca_buy_success': "🤖 **SMART DCA TRIGGERED!** 🤖\n\nSuccessfully bought: **${amount:,.2f} of {symbol}** at {buy_price}. (DCA Drop Level: {level})\n\n🛡 Auto-Trade & Trailing Stop is now managing this trade!",
        'smart_dca_deactivated': "✅ **SMART DCA DEACTIVATED!** All drop levels for {symbol} have been accumulated.",
        'grid_bot_usage': "❌ Usage: `/grid_bot <SYMBOL> <LOWER> <UPPER> <GRIDS> <INVESTMENT> <PIN>`\nExample: `/grid_bot BTC 60000 70000 10 1000 1234`",
        'grid_bot_set': "✅ **Grid Bot Started!**\n🤖 I have deployed {grids} grids for {symbol} between ${lower} - ${upper}.",
        'grid_bot_arbitrage': "⚡ **GRID ARBITRAGE!** ⚡\n✅ Successfully captured volatility profit for {symbol} at ${price:,.2f}!",
        'hedge_mode_usage': "❌ Usage: `/hedge_mode ON <Amount> <PIN>` or `/hedge_mode OFF <PIN>`",
        'hedge_mode_enabled': "✅ **Delta-Neutral Hedge Mode ENABLED!**\n\n💵 Amount: ${amount}\n⚙️ Leverage: {leverage}x\n\n*When AI predicts a crash, the bot will Short the market to protect your portfolio!*",
        'hedge_mode_disabled': "🚫 **Hedge Mode DISABLED!**",
        'hedge_short_start': "🤖 **Hedge Fund Engine:** Placing automated Futures Short for {symbol} to protect portfolio...",
        'hedge_short_success': "✅ **HEDGE SHORT ACTIVE!** 📉\n\n🪙 Coin: {symbol}\n💵 Entry Price: ${price:,.2f}\n⚙️ Leverage: {leverage}x\n\n*Bot is profiting from the market crash!*",
        'hedge_short_dynamic_alert': "🤖 _AI Dynamic Risk: Automatically selected {leverage}x Leverage based on market volatility and confidence ({confidence}%)!_",
        'hedge_short_fail': "❌ Short Failed: {error}",
        'hedge_short_closed': "{emoji} **HEDGE SHORT {result}!**\n\n🤖 Bot closed Short for {symbol}\n💵 Exit Price: ${price:,.2f}\n📉 Result: {pnl_pct:+.2f}%",
        'remove_api_usage': "❌ Usage: `/remove_api <PIN>`\nExample: `/remove_api 1234`",
        'remove_api_success': "✅ Success! Your API Keys have been completely deleted. All Auto-Trading features are now OFF (Kill Switch).",
        'remove_api_not_found': "🤷‍♂️ You have not connected any API yet, or it has already been removed.",
    },
    'chinese': {
        'access_denied': "❌ 抱歉，您没有权限使用此 AI 功能。\n请联系管理员申请 VIP 权限。",
        'welcome_msg': "👋 欢迎使用 Apex AI Bot (VIP 成员)!\n我是一个超级智能 AI (支持 English, ខ្មែរ, 中文)。\n发送任何市场数据让我分析，或使用 `/analyze <代币>`。",
        'analyze_usage': "❌ 请提供代币名称。例如: `/analyze BTC`",
        'fetching_live_data': "🔍 正在从 Binance 获取 {symbol} 的实时数据...",
        'generating_chart': "📊 正在生成图表、ML 预测和宏观 AI 风险分析...",
        'processing_request': "🤖 正在处理您的请求...",
        'alert_usage': "❌ 用法: `/alert <代币> < > <价格>`\n例如: `/alert BTC < 60000`",
        'price_must_be_number': "❌ 价格必须是数字。",
        'condition_invalid': "❌ 条件必须是 '<' 或 '>'。",
        'alert_set': "✅ 警报已设置: 当 **{symbol}** 达到 **{condition} ${price}** 时，我将通知您。",
        'help_text': (
            "🤖 **Apex AI Bot - 命令菜单 (Menu)**\n\n"
            "💼 **账户和投资组合 (Account & Portfolio)**\n"
            "👉 `/start` - 启动机器人\n"
            "👉 `/portfolio` - 查看您的投资组合和利润\n"
            "👉 `/balance` - 检查 Binance 余额\n"
            "👉 `/stop` - 停止运行中的机器人\n\n"
            "📊 **AI 市场分析 (AI Analysis)**\n"
            "👉 `/analyze <代币>` - 市场趋势分析\n"
            "👉 `/predict <代币>` - 预测价格趋势\n"
            "👉 `/scan` - 扫描涨幅/跌幅最大代币\n"
            "👉 `/top` - 查看每日涨幅榜\n\n"
            "⚡ **自动交易 (Auto-Trading)**\n"
            "👉 `/auto_trade ON <Amount> <PIN>` - 启用自动交易\n"
            "👉 `/smart_dca <代币> <金额> <PIN>` - 启用 Smart DCA\n"
            "👉 `/infinity_grid <代币> ... <PIN>` - 无限网格\n"
            "👉 `/compound_grid <代币> ... <PIN>` - 复合网格\n"
            "👉 `/scalp <代币> ... <PIN>` - 剥头皮交易 (Ping-Pong)\n"
            "👉 `/auto_snipe ON <Amount> <PIN>` - 自动打新机器人\n"
            "👉 `/hedge_mode ON <Amount> <PIN>` - 启用对冲模式 (Short)\n\n\n"
            "👉 `/defender ON` - 启用 AI 防爆仓护盾 (Liquidation Defender)\n\n\n"
            "👉 `/dynamic_leverage ON` - 启用 AI 动态杠杆 (Dynamic Leverage)\n\n\n"
            "👉 `/delta_neutral ON <Amount>` - 启用 资金费率无风险套利 (Delta-Neutral)\n\n\n"
            "👉 `/sweep_sniper ON <Amount>` - 猎杀庄家插针底部 (Liquidity Sweep)\n\n\n"
            "👉 `/wave_rider ON|OFF` - 启用 AI 冲浪移动止盈 (Dynamic Wave Riding)\n\n"
            "🔔 **价格警报和新闻 (Alerts & News)**\n"
            "👉 `/alert <代币> < > <价格>` - 价格警报\n"
            "👉 `/my_alerts` - 查看您的警报\n"
            "👉 `/cancel_alert <ID>` - 取消警报\n"
            "👉 `/news` - 宏观市场摘要\n\n"
            "⚙️ **设置和安全 (Settings & Security)**\n"
            "👉 `/add_api` - 连接 Binance API\n"
            "👉 `/set_pin` - 设置 PIN 码\n"
            "👉 `/language` - 设置语言\n"
            "👉 `/status` - 检查系统状态\n"
            "👉 `/help` - 显示此帮助信息\n\n"
            "👨‍💻 **需要帮助吗？** 联系管理员: @HemSinath\n\n"
            "🛡️ **Binance API 安全指南:**\n"
            "✅ **Enable Reading** (必须启用)\n"
            "✅ **Enable Spot & Margin Trading** (自动交易必须启用)\n"
            "✅ **Enable Futures** (对冲/做空必须启用)\n"
            "❌ **Enable Withdrawals** (警告: 严禁启用)\n"
            "🔒 **IP Restrictions**: 如果没有静态 IP，请选择 'Unrestricted'。"
        ),
        'no_alerts': "🤷‍♂️ 您没有活动的警报。",
        'alert_list_header': "⏰ **您的价格警报:**\n\n",
        'alert_cancel_usage': "\n💡 使用 `/cancel_alert <ID>` 取消。",
        'cancel_alert_usage': "❌ 请输入警报 ID。例如: `/cancel_alert 1`",
        'id_must_be_number': "❌ ID 必须是数字。",
        'alert_cancelled': "✅ 警报 ID {alert_id} 已成功取消!",
        'alert_not_found': "❌ 找不到该警报 ID 或它不属于您。",
        'fetching_top': "🔍 正在从 Binance 获取涨幅榜数据...",
        'ai_analysis_header': "🤖 **AI 分析:**\n",
        'fetching_news': "📰 正在分析全球宏观市场...",
        'language_current': "🌐 您当前的语言是: **{lang}**\n\n要更改语言，请使用:\n`/language khmer`\n`/language english`\n`/language chinese`\n`/language auto`",
        'language_invalid': "❌ 无效语言。请选择 `khmer`, `english`, `chinese`, 或 `auto`。",
        'language_set': "✅ 语言已设置为: **{lang}**",
        'add_api_usage': "❌ 用法: `/add_api <API_KEY> <API_SECRET>`\n\n*注意: 您的凭证将被安全保存，绝不会与第三方共享。*",
        'api_added': "✅ 您的 Binance API 已成功连接！(密钥安全存储)\n\n🤖 机器人现在可以自动为您交易并管理追踪止损！",
        'api_invalid': "❌ 您的 API 密钥无效或未启用合约交易！请重新检查。",
        'broadcast_header': "📢 **公告**\n\n",
        'price_alert_trigger': "🚨 **价格警报** 🚨\n\n🪙 代币: {symbol}\n🎯 目标: {condition} ${target_price}\n💵 当前价格: ${current_price}",
        'sentiment_sniper_alert': "⚡ **闪电交易信号 (情绪狙击手)** ⚡\n\n🎯 **检测到关键词:** `{trigger_word}`\n📈 **市场情绪:** {sentiment}\n\n📰 **新闻标题:** {title}\n\n⚠️ *注意: 机构高频交易机器人可能正在对此新闻做出反应！*",
        'auto_buy_start': "🤖 **自动交易引擎:** 正在自动市价买入 {symbol}...",
        'auto_buy_success': "✅ **买入成功 (模拟)!**\n🪙 代币: {symbol}\n💵 买入价: ${buy_price:,.2f}\n📉 初始止损: ${initial_stop_loss:,.2f}\n\n🛡️ *追踪止损现已激活!*",
        'auto_buy_fail': "❌ 买入失败: {error}",
        'trailing_stop_triggered': "🚨 **追踪止损触发!** 🚨\n\n🤖 机器人已自动卖出 {symbol}!\n💵 卖出价: ${current_price:,.2f}\n📉 结果: {emoji} {result_msg} ({pl_pct:+.2f}%)\n\n*我们控制损失，并锁定利润！*",
        'action_sent': "📤 发送",
        'action_received': "📥 接收",
        'bullish': "BULLISH 🚀",
        'bearish': "BEARISH 🩸",
        'above': "高于 (Above)",
        'below': "低于 (Below)",
        'please_wait_processing': "⏳ 请稍候，我正在处理您之前的请求...",
        'timeout_blocked': "🚫 您发送消息太快 (Spam)！安全系统已暂时屏蔽您 5 分钟。",
        'pin_set_success': "✅ 成功！您的 PIN 码已设置，请牢记。",
        'pin_incorrect': "❌ PIN 码不正确！访问被拒绝。",
        'pin_required': "❌ 这是一个敏感命令。请提供您的 4 位 PIN 码。",
        'set_pin_usage': "❌ 用法: `/set_pin <4位PIN>` 或 `/set_pin <旧PIN> <新PIN>`",
        'weak_pin_error': "❌ PIN码太弱！为确保安全，请避免使用重复 (1111) 或连续 (1234) 的数字。",
        'add_api_usage_pin': "❌ 用法: `/add_api <API_KEY> <API_SECRET> <PIN>`",
        'api_private_only': "⚠️ **安全警报**\n\n为了您的安全，只能在私聊 (Private Chat) 中添加 API 密钥。请立即从此群组中删除您的消息！",
        'msg_auto_deleted': "🗑️ *(安全提示: 您的消息已被自动删除)*",
        'auto_trade_usage': "❌ 用法: `/auto_trade ON <Amount_USDT> <PIN>` 或 `/auto_trade OFF <PIN>`\n例如: `/auto_trade ON 50 1234`",
        'auto_trade_enabled': "✅ 自动交易已开启!\n💵 金额: ${amount} USDT\n🛡️ 追踪止损: {trailing}%\n\n*注意：每当 AI 输出 BUY 信号时，Bot 都会自动买入！*",
        'auto_trade_disabled': "🚫 自动交易已关闭。",
        'whale_deposit_alert': "🚨 **链上红色警报 (资金流入)** 🚨\n\n🐋 巨鲸刚刚向 **Binance** 存入资金!\n💰 金额: **${value:,.2f} {symbol}**\n\n⚠️ *注意: 这可能表明正在准备大规模买单，或者是潜在的抛售 (Dump)!*",
        'whale_withdrawal_alert': "💸 **链上绿色警报 (资金流出)** 💸\n\n🐋 巨鲸刚刚从 **Binance** 提取资金!\n💰 金额: **${value:,.2f} {symbol}**\n\n🟢 *注意: 大规模资金流出通常表明巨鲸正在囤积代币!*",
        'smart_dca_usage': "❌ 用法: `/smart_dca <代币> <金额> <PIN>`\n例如: `/smart_dca BTC 100 1234`",
        'smart_dca_set': "✅ **Smart DCA 已启动!**\n🤖 正在从 **${entry_price:,.2f}** 监控 **{symbol}**。如果大幅下跌，将执行马丁格尔阶梯买入策略!",
        'smart_dca_buy_success': "🤖 **SMART DCA 已触发!** 🤖\n\n已成功买入: {buy_price} 的 **${amount:,.2f} {symbol}**。(DCA 下跌等级: {level})\n\n🛡 自动交易和追踪止损现在正在管理这笔交易!",
        'smart_dca_deactivated': "✅ **SMART DCA 已停用!** {symbol} 的所有下跌等级均已建仓。",
        'grid_bot_usage': "❌ 用法: `/grid_bot <代币> <最低价> <最高价> <网格数> <投资额> <PIN>`\n例如: `/grid_bot BTC 60000 70000 10 1000 1234`",
        'grid_bot_set': "✅ **网格机器人已启动!**\n🤖 我已在 ${lower} - ${upper} 之间为 {symbol} 部署了 {grids} 个网格。",
        'grid_bot_arbitrage': "⚡ **网格套利!** ⚡\n✅ 成功在 ${price:,.2f} 捕获 {symbol} 的波动利润!",
        'hedge_mode_usage': "❌ 用法: `/hedge_mode ON <Amount> <PIN>` 或 `/hedge_mode OFF <PIN>`",
        'hedge_mode_enabled': "✅ **对冲模式已启用!**\n\n💵 金额: ${amount}\n⚙️ 杠杆: {leverage}x\n\n*当 AI 预测市场崩溃时，机器人将做空市场以保护您的投资组合！*",
        'hedge_mode_disabled': "🚫 **对冲模式已停用!**",
        'hedge_short_start': "🤖 **对冲基金引擎:** 正在为 {symbol} 自动下达期货做空订单以保护投资组合...",
        'hedge_short_success': "✅ **对冲做空已启动!** 📉\n\n🪙 代币: {symbol}\n💵 做空价格: ${price:,.2f}\n⚙️ 杠杆: {leverage}x\n\n*机器人正在从市场崩盘中获利!*",
        'hedge_short_dynamic_alert': "🤖 _AI 动态风险管理: 根据市场波动率和信心指数 ({confidence}%) 自动选择 {leverage}x 杠杆!_",
        'hedge_short_fail': "❌ 做空失败: {error}",
        'hedge_short_closed': "{emoji} **对冲做空 {result}!**\n\n🤖 机器人平仓做空 {symbol}\n💵 平仓价格: ${price:,.2f}\n📉 结果: {pnl_pct:+.2f}%",
        'remove_api_usage': "❌ 用法: `/remove_api <PIN>`\n例如: `/remove_api 1234`",
        'remove_api_success': "✅ 成功！您的 API 密钥已被完全删除。所有自动交易功能现已关闭（紧急开关）。",
        'remove_api_not_found': "🤷‍♂️ 您尚未连接任何 API，或者它已被删除。",
        'funding_harvester_usage': "❌ របៀបប្រើប្រាស់: `/funding_harvester ON <ទុន> <PIN>` ឬ `/funding_harvester OFF <PIN>`",
        'funding_harvester_enabled': "🌾 **8-Hour Perpetual Funding Yield Harvester បានបើក!**\n\n💵 ទុនស្ទាក់ទិញ: `${amount:.2f} USDT`\n🛡️ យុទ្ធសាស្ត្រ: 1:1 Delta-Neutral (0% Risk-Free)\n\n*AI នឹងស្កេនរកកាក់ដែលមាន Funding Rate ខ្ពស់បំផុត ១០ នាទីមុនពេល settlement រៀងរាល់ ៨ ម៉ោងម្តងដើម្បីប្រមូលសាច់ប្រាក់!*",
        'funding_harvester_disabled': "🚫 **8-Hour Perpetual Funding Yield Harvester ត្រូវបានបិទ!**"
    }
}

LANG_MAP = {
    'km': 'khmer',
    'khmer': 'khmer',
    'en': 'english',
    'english': 'english',
    'zh': 'chinese',
    'chinese': 'chinese',
    'auto': 'khmer'
}

def normalize_lang(language: str) -> str:
    if not language:
        return DEFAULT_LANG
    clean = str(language).lower().strip()
    return LANG_MAP.get(clean, DEFAULT_LANG)

def get_text(language: str, key: str, **kwargs) -> str:
    lang_key = normalize_lang(language)
    
    if lang_key not in MESSAGES or key not in MESSAGES[lang_key]:
        # Fallback to English, then Khmer
        if key in MESSAGES.get('english', {}):
            lang_key = 'english'
        elif key in MESSAGES.get('khmer', {}):
            lang_key = 'khmer'
        else:
            return f"[{key} NOT FOUND]"
            
    text = MESSAGES[lang_key][key]
    
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass # Ignore if formatting fails
            
    return text

