//+------------------------------------------------------------------+
//|                                  KhmerMasterCrypto_Bridge.mq5    |
//|                 Copyright 2026, Khmer Master Crypto & Apex AGI   |
//|                                https://t.me/KhmerMasterCrypto    |
//+------------------------------------------------------------------+
#property copyright   "Khmer Master Crypto & Apex AGI"
#property link        "https://t.me/KhmerMasterCrypto"
#property version     "13.00"
#property description "Institutional Ultra-Fast ZeroMQ/TCP Bridge EA for MetaTrader 5."
#property description "Connects directly to Linux Tokyo VPS AI Swarm with Zero DLL imports."
#property description "Wall Street Prop Firm Compliance Fortress (FTMO / FundedNext Ready)."
#property strict

// Standard MQL5 Trade Libraries
#include <Trade\Trade.mqh>
#include <Trade\PositionInfo.mqh>
#include <Trade\AccountInfo.mqh>
#include <Trade\SymbolInfo.mqh>

//--- INPUT PARAMETERS
input group "=== 🌐 TOKYO LINUX VPS CONNECTION ==="
input string   InpHost              = "34.153.209.188";    // Linux VPS IP Address (Tokyo GCP)
input int      InpPort              = 5555;                // TCP Bridge Port (Default: 5555)
input string   InpSecretKey         = "KhmerMasterCrypto_PropBridge_Fortress_2026"; // Shared Secret Key
input int      InpTimeoutMs         = 3000;                // Socket Connection Timeout (ms)

input group "=== 🏛️ PROP FIRM & RISK CITADEL ==="
input string   InpFirmName          = "FTMO";              // Prop Firm (FTMO, FundedNext, IC_Markets)
input double   InpMaxDailyLossPct   = 3.5;                 // Hard Daily Loss Clamp % (FTMO Rule: -3.5%)
input double   InpMaxDrawdownPct    = 7.0;                 // Max Overall Drawdown Clamp % (-7.0%)
input ulong    InpMagicNumber       = 888999;              // EA Magic Number
input ulong    InpMaxSlippage       = 20;                  // Max Slippage in Points
input string   InpOrderComment      = "APEX_AI_BRIDGE";    // Order Comment Tag

input group "=== 📊 ON-CHART HEADS-UP DISPLAY (HUD) ==="
input bool     InpShowHUD           = true;                // Show Institutional Dashboard
input color    InpTextColor         = clrAqua;             // Primary Text Color
input color    InpBgColor           = C'10,14,24';         // HUD Background Color

//--- GLOBAL ENGINE STATE
CTrade         m_trade;
CPositionInfo  m_position;
CAccountInfo   m_account;
CSymbolInfo    m_symbol;

int            g_socket              = INVALID_HANDLE;
bool           g_connected           = false;
ulong          g_last_connect_try_ms = 0;
ulong          g_last_heartbeat_ms   = 0;
int            g_last_error_code     = 0;
double         g_daily_start_equity  = 0.0;
double         g_initial_balance     = 0.0;
int            g_day_of_year         = -1;
bool           g_prop_breached       = false;
string         g_rx_buffer           = "";
ulong          g_orders_executed     = 0;
double         g_last_ping_ms        = 0.0;

#define HUD_PREFIX "KMC_BRIDGE_"

//+------------------------------------------------------------------+
//| Expert initialization function                                   |
//+------------------------------------------------------------------+
int OnInit()
{
   // Configure MQL5 Trade Engine
   m_trade.SetExpertMagicNumber(InpMagicNumber);
   m_trade.SetDeviationInPoints(InpMaxSlippage);
   m_trade.SetTypeFillingBySymbol(_Symbol);

   g_initial_balance = m_account.Balance();
   g_daily_start_equity = m_account.Equity();
   
   MqlDateTime dt;
   TimeLocal(dt);
   g_day_of_year = dt.day_of_year;

   Print("🚀 [KMC BRIDGE] Initializing Apex Institutional MT5 Bridge v13.00...");
   PrintFormat("🏛️ [PROP SHIELD] Baseline Balance: $%.2f | Daily Equity: $%.2f | Firm: %s", 
               g_initial_balance, g_daily_start_equity, InpFirmName);

   // Create On-Chart HUD
   if(InpShowHUD)
      CreateHUD();

   // Attempt initial connection to Linux VPS
   ConnectToBridge();

   // Set fast 1-second timer for heartbeats & background checks
   EventSetTimer(1);

   return(INIT_SUCCEEDED);
}

//+------------------------------------------------------------------+
//| Expert deinitialization function                                 |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
{
   EventKillTimer();
   DisconnectBridge();
   RemoveHUD();
   Print("🛑 [KMC BRIDGE] Expert Advisor deinitialized. Reason: ", reason);
}

//+------------------------------------------------------------------+
//| Expert timer function (Every 1 Second)                           |
//+------------------------------------------------------------------+
void OnTimer()
{
   ulong now_ms = GetTickCount64();

   // 1. Rollover Check for UTC/Broker Daily Equity Baseline using local clock
   datetime local_now = TimeLocal();
   MqlDateTime dt;
   TimeToStruct(local_now, dt);
   if(dt.day_of_year != g_day_of_year)
   {
      g_day_of_year = dt.day_of_year;
      g_daily_start_equity = m_account.Equity();
      g_prop_breached = false;
      PrintFormat("🔄 [DAILY ROLLOVER] Reset Daily Equity Baseline to $%.2f", g_daily_start_equity);
   }

   // 2. Prop Firm Local Hard Circuit Breaker Check
   EvaluateLocalPropCompliance();

   // 3. Connection State Machine & Reconnect (Every 3000 ms)
   if(!g_connected)
   {
      if(now_ms - g_last_connect_try_ms >= 3000)
      {
         g_last_connect_try_ms = now_ms;
         ConnectToBridge();
      }
   }
   else
   {
      // 4. Send Periodic Heartbeat (Every 3 seconds)
      if(now_ms - g_last_heartbeat_ms >= 3000)
      {
         g_last_heartbeat_ms = now_ms;
         SendHeartbeat();
      }

      // 5. Read incoming commands from Linux VPS
      ReadSocketData();
   }

   // 6. Refresh HUD
   if(InpShowHUD)
      UpdateHUD();
}

//+------------------------------------------------------------------+
//| Expert tick function (High-Frequency Low Latency Trigger)        |
//+------------------------------------------------------------------+
void OnTick()
{
   if(g_connected)
   {
      // Poll socket on every tick for sub-millisecond command execution
      ReadSocketData();
   }
}

//+------------------------------------------------------------------+
//| Connects to Linux VPS Native TCP Bridge                          |
//+------------------------------------------------------------------+
bool ConnectToBridge()
{
   if(g_socket != INVALID_HANDLE)
   {
      SocketClose(g_socket);
      g_socket = INVALID_HANDLE;
   }

   g_socket = SocketCreate();
   if(g_socket == INVALID_HANDLE)
   {
      Print("❌ [SOCKET CREATE] Failed to create socket. Error: ", GetLastError());
      g_connected = false;
      return false;
   }

   uint start_time = GetTickCount();
   if(!SocketConnect(g_socket, InpHost, InpPort, InpTimeoutMs))
   {
      g_last_error_code = GetLastError();
      // Error 5273 = Host unreachable / Firewall blocked, 4014 = Function not allowed
      PrintFormat("⚠️ [CONNECT FAILED] Unable to connect to %s:%d (Error: %d). Retrying...", InpHost, InpPort, g_last_error_code);
      SocketClose(g_socket);
      g_socket = INVALID_HANDLE;
      g_connected = false;
      return false;
   }

   g_last_error_code = 0;
   g_last_ping_ms = (double)(GetTickCount() - start_time);
   g_connected = true;
   g_rx_buffer = "";
   PrintFormat("⚡ [CONNECTED] Established TCP link to %s:%d in %.1f ms!", InpHost, InpPort, g_last_ping_ms);

   // Send Authentication Handshake Packet
   SendAuthHandshake();
   return true;
}

//+------------------------------------------------------------------+
//| Disconnects from Linux VPS                                       |
//+------------------------------------------------------------------+
void DisconnectBridge()
{
   if(g_socket != INVALID_HANDLE)
   {
      SocketClose(g_socket);
      g_socket = INVALID_HANDLE;
   }
   g_connected = false;
}

//+------------------------------------------------------------------+
//| Sends Authentication Handshake                                   |
//+------------------------------------------------------------------+
void SendAuthHandshake()
{
   if(!g_connected || g_socket == INVALID_HANDLE) return;

   datetime real_time = TimeGMT();
   if(real_time <= 0) real_time = TimeLocal();

   string json = StringFormat(
      "{\"type\":\"AUTH\",\"account_id\":\"%d\",\"broker\":\"%s\",\"firm_name\":\"%s\",\"balance\":%.2f,\"equity\":%.2f,\"currency\":\"%s\",\"secret_key\":\"%s\",\"timestamp\":%d}\n",
      (int)m_account.Login(),
      m_account.Company(),
      InpFirmName,
      m_account.Balance(),
      m_account.Equity(),
      m_account.Currency(),
      InpSecretKey,
      (int)real_time
   );

   SendRawString(json);
}

//+------------------------------------------------------------------+
//| Sends Periodic Telemetry Heartbeat                               |
//+------------------------------------------------------------------+
void SendHeartbeat()
{
   if(!g_connected || g_socket == INVALID_HANDLE) return;

   datetime real_time = TimeGMT();
   if(real_time <= 0) real_time = TimeLocal();
   ulong now_ms = GetTickCount64();

   string json = StringFormat(
      "{\"type\":\"HEARTBEAT\",\"account_id\":\"%d\",\"broker\":\"%s\",\"firm_name\":\"%s\",\"balance\":%.2f,\"equity\":%.2f,\"daily_start_equity\":%.2f,\"initial_balance\":%.2f,\"secret_key\":\"%s\",\"timestamp\":%d,\"timestamp_ms\":%I64u}\n",
      (int)m_account.Login(),
      m_account.Company(),
      InpFirmName,
      m_account.Balance(),
      m_account.Equity(),
      g_daily_start_equity,
      g_initial_balance,
      InpSecretKey,
      (int)real_time,
      now_ms
   );

   SendRawString(json);
}

//+------------------------------------------------------------------+
//| Sends Raw UTF-8 String over Socket                               |
//+------------------------------------------------------------------+
bool SendRawString(const string msg)
{
   if(!g_connected || g_socket == INVALID_HANDLE) return false;

   uchar data[];
   int len = StringToCharArray(msg, data, 0, WHOLE_ARRAY, CP_UTF8);
   if(len > 1) // exclude null terminator
   {
      int sent = SocketSend(g_socket, data, len - 1);
      if(sent < 0)
      {
         Print("⚠️ [SOCKET SEND] Error sending data: ", GetLastError());
         DisconnectBridge();
         return false;
      }
      return true;
   }
   return false;
}

//+------------------------------------------------------------------+
//| Reads and buffers incoming TCP data from Linux VPS               |
//+------------------------------------------------------------------+
void ReadSocketData()
{
   if(!g_connected || g_socket == INVALID_HANDLE) return;

   uint readable = SocketIsReadable(g_socket);
   if(readable > 0)
   {
      uchar buffer[];
      ArrayResize(buffer, 4096);
      int bytes_read = SocketRead(g_socket, buffer, 4096, 20);
      if(bytes_read > 0)
      {
         string chunk = CharArrayToString(buffer, 0, bytes_read, CP_UTF8);
         g_rx_buffer += chunk;

         // Extract newline-delimited JSON packets
         int newline_pos = StringFind(g_rx_buffer, "\n");
         while(newline_pos >= 0)
         {
            string line = StringSubstr(g_rx_buffer, 0, newline_pos);
            g_rx_buffer = StringSubstr(g_rx_buffer, newline_pos + 1);
            StringTrimLeft(line);
            StringTrimRight(line);

            if(StringLen(line) > 0)
            {
               ExecuteCommand(line);
            }
            newline_pos = StringFind(g_rx_buffer, "\n");
         }
      }
      else if(bytes_read < 0)
      {
         Print("🔌 [SOCKET READ] Connection lost. Reconnecting...");
         DisconnectBridge();
      }
   }
}

//+------------------------------------------------------------------+
//| Extracts JSON String Value by Key                                |
//+------------------------------------------------------------------+
string ExtractJsonValue(const string json, const string key)
{
   string pattern = "\"" + key + "\":";
   int pos = StringFind(json, pattern);
   if(pos < 0) return "";

   int start = pos + StringLen(pattern);
   while(start < StringLen(json) && (StringSubstr(json, start, 1) == " " || StringSubstr(json, start, 1) == "\""))
      start++;

   int end = start;
   bool in_quotes = (StringSubstr(json, pos + StringLen(pattern), 1) == "\"" || StringSubstr(json, pos + StringLen(pattern) + 1, 1) == "\"");
   
   while(end < StringLen(json))
   {
      string ch = StringSubstr(json, end, 1);
      if(in_quotes && ch == "\"") break;
      if(!in_quotes && (ch == "," || ch == "}" || ch == "]" || ch == "\n" || ch == "\r")) break;
      end++;
   }

   return StringSubstr(json, start, end - start);
}

//+------------------------------------------------------------------+
//| Parses and Executes Inbound Command from Linux AI Brain          |
//+------------------------------------------------------------------+
void ExecuteCommand(const string json)
{
   string type = ExtractJsonValue(json, "type");
   StringToUpper(type);

   if(type == "ORDER_SEND")
   {
      HandleOrderSend(json);
   }
   else if(type == "ORDER_CLOSE")
   {
      HandleOrderClose(json);
   }
   else if(type == "MODIFY_STOPS")
   {
      HandleModifyStops(json);
   }
   else if(type == "PROP_CIRCUIT_BREAKER")
   {
      Print("🚨 [PROP BREACH HALT] Emergency circuit breaker command received from Linux Brain!");
      g_prop_breached = true;
      CloseAllBridgeTrades("PROP_BREACH_HALT");
   }
   else if(type == "PONG")
   {
      // Heartbeat roundtrip acknowledged
   }
}

//+------------------------------------------------------------------+
//| Handles Trade Order Execution                                    |
//+------------------------------------------------------------------+
void HandleOrderSend(const string json)
{
   // Prop Firm Shield Pre-Flight Enforcement
   if(g_prop_breached)
   {
      Print("🛡️ [ORDER BLOCKED] Prop Firm Daily/Max Drawdown Breached! Order rejected.");
      return;
   }

   string signal_id = ExtractJsonValue(json, "signal_id");
   string symbol_req = ExtractJsonValue(json, "symbol");
   string action_req = ExtractJsonValue(json, "action");
   double lot_req    = StringToDouble(ExtractJsonValue(json, "lot"));
   double sl_req     = StringToDouble(ExtractJsonValue(json, "sl"));
   double tp_req     = StringToDouble(ExtractJsonValue(json, "tp"));
   ulong  magic_req  = (ulong)StringToInteger(ExtractJsonValue(json, "magic"));
   string comment    = ExtractJsonValue(json, "comment");

   if(magic_req <= 0) magic_req = InpMagicNumber;
   if(StringLen(comment) == 0) comment = InpOrderComment;

   // 1. Normalize Symbol (Support broker prefixes/suffixes: XAUUSD.pro, GOLD, etc.)
   string symbol = MatchBrokerSymbol(symbol_req);
   if(symbol == "")
   {
      PrintFormat("❌ [SYMBOL ERROR] Symbol '%s' not supported by broker!", symbol_req);
      return;
   }

   if(!SymbolInfoInteger(symbol, SYMBOL_SELECT))
      SymbolSelect(symbol, true);

   // 2. Normalize Lot Size
   double min_lot = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MIN);
   double max_lot = SymbolInfoDouble(symbol, SYMBOL_VOLUME_MAX);
   double lot_step = SymbolInfoDouble(symbol, SYMBOL_VOLUME_STEP);

   double lot = MathMax(min_lot, MathMin(max_lot, lot_req));
   lot = MathFloor(lot / lot_step) * lot_step;

   // 3. Normalize Digits & Prices
   int digits = (int)SymbolInfoInteger(symbol, SYMBOL_DIGITS);
   double ask = SymbolInfoDouble(symbol, SYMBOL_ASK);
   double bid = SymbolInfoDouble(symbol, SYMBOL_BID);

   double sl = (sl_req > 0.0) ? NormalizeDouble(sl_req, digits) : 0.0;
   double tp = (tp_req > 0.0) ? NormalizeDouble(tp_req, digits) : 0.0;

   m_trade.SetExpertMagicNumber(magic_req);

   bool success = false;
   ulong ticket = 0;
   double fill_price = 0.0;

   StringToUpper(action_req);
   if(action_req == "BUY")
   {
      success = m_trade.Buy(lot, symbol, ask, sl, tp, comment);
      fill_price = ask;
   }
   else if(action_req == "SELL")
   {
      success = m_trade.Sell(lot, symbol, bid, sl, tp, comment);
      fill_price = bid;
   }

   if(success)
   {
      ticket = m_trade.ResultOrder();
      if(ticket == 0) ticket = m_trade.ResultDeal();
      g_orders_executed++;
      PrintFormat("🎯 [ORDER FILLED] #%d | %s %s %.2f @ %.5f | SL: %.5f TP: %.5f", 
                  ticket, action_req, symbol, lot, fill_price, sl, tp);

      // Report confirmation back to Linux VPS
      string confirm_json = StringFormat(
         "{\"type\":\"ORDER_CONFIRM\",\"signal_id\":\"%s\",\"ticket\":%d,\"open_price\":%.5f,\"status\":\"FILLED\",\"secret_key\":\"%s\"}\n",
         signal_id, ticket, fill_price, InpSecretKey
      );
      SendRawString(confirm_json);
   }
   else
   {
      PrintFormat("❌ [ORDER FAILED] Error: %d (%s)", m_trade.ResultRetcode(), m_trade.ResultRetcodeDescription());
   }
}

//+------------------------------------------------------------------+
//| Handles Position Close Command                                   |
//+------------------------------------------------------------------+
void HandleOrderClose(const string json)
{
   ulong ticket = (ulong)StringToInteger(ExtractJsonValue(json, "ticket"));
   if(ticket > 0 && PositionSelectByTicket(ticket))
   {
      double close_price = (PositionGetInteger(POSITION_TYPE) == POSITION_TYPE_BUY) ? 
                           SymbolInfoDouble(PositionGetString(POSITION_SYMBOL), SYMBOL_BID) : 
                           SymbolInfoDouble(PositionGetString(POSITION_SYMBOL), SYMBOL_ASK);
      double pnl = PositionGetDouble(POSITION_PROFIT);

      if(m_trade.PositionClose(ticket))
      {
         PrintFormat("💰 [POSITION CLOSED] #%d | Close Price: %.5f | PnL: $%.2f", ticket, close_price, pnl);
         string close_json = StringFormat(
            "{\"type\":\"ORDER_CLOSED\",\"ticket\":%d,\"close_price\":%.5f,\"pnl\":%.2f,\"status\":\"CLOSED\",\"secret_key\":\"%s\"}\n",
            ticket, close_price, pnl, InpSecretKey
         );
         SendRawString(close_json);
      }
   }
}

//+------------------------------------------------------------------+
//| Handles Trailing Stop / SL Modification                          |
//+------------------------------------------------------------------+
void HandleModifyStops(const string json)
{
   ulong ticket = (ulong)StringToInteger(ExtractJsonValue(json, "ticket"));
   double sl = StringToDouble(ExtractJsonValue(json, "sl"));
   double tp = StringToDouble(ExtractJsonValue(json, "tp"));

   if(ticket > 0 && PositionSelectByTicket(ticket))
   {
      string sym = PositionGetString(POSITION_SYMBOL);
      int digits = (int)SymbolInfoInteger(sym, SYMBOL_DIGITS);
      double cur_sl = PositionGetDouble(POSITION_SL);
      double cur_tp = PositionGetDouble(POSITION_TP);

      double new_sl = (sl > 0.0) ? NormalizeDouble(sl, digits) : cur_sl;
      double new_tp = (tp > 0.0) ? NormalizeDouble(tp, digits) : cur_tp;

      if(m_trade.PositionModify(ticket, new_sl, new_tp))
      {
         PrintFormat("🛡️ [STOPS MODIFIED] #%d | New SL: %.5f | New TP: %.5f", ticket, new_sl, new_tp);
      }
   }
}

//+------------------------------------------------------------------+
//| Matches generic symbol name with broker-specific symbol name     |
//+------------------------------------------------------------------+
string MatchBrokerSymbol(const string base_sym)
{
   if(SymbolInfoDouble(base_sym, SYMBOL_BID) > 0)
      return base_sym;

   // Common aliases
   string variations[];
   ArrayResize(variations, 7);
   variations[0] = base_sym + ".pro";
   variations[1] = base_sym + "m";
   variations[2] = base_sym + ".m";
   variations[3] = base_sym + "_i";
   variations[4] = base_sym + "c";
   variations[5] = "r" + base_sym;
   variations[6] = (base_sym == "XAUUSD") ? "GOLD" : "";

   for(int i = 0; i < ArraySize(variations); i++)
   {
      if(variations[i] != "" && SymbolInfoDouble(variations[i], SYMBOL_BID) > 0)
         return variations[i];
   }

   // Search symbol list in Market Watch
   int total = SymbolsTotal(false);
   for(int i = 0; i < total; i++)
   {
      string s = SymbolName(i, false);
      if(StringFind(s, base_sym) >= 0)
         return s;
   }

   return "";
}

//+------------------------------------------------------------------+
//| Local Prop Firm Hard Circuit Breaker                             |
//+------------------------------------------------------------------+
void EvaluateLocalPropCompliance()
{
   double equity = m_account.Equity();
   if(g_daily_start_equity <= 0 || g_initial_balance <= 0) return;

   double daily_dd_pct = ((equity - g_daily_start_equity) / g_daily_start_equity) * 100.0;
   double total_dd_pct = ((equity - g_initial_balance) / g_initial_balance) * 100.0;

   if(daily_dd_pct <= -InpMaxDailyLossPct || total_dd_pct <= -InpMaxDrawdownPct)
   {
      if(!g_prop_breached)
      {
         g_prop_breached = true;
         PrintFormat("🚨 [LOCAL PROP SHIELD BREACH] Daily DD: %.2f%% (Limit: -%.1f%%) | Total DD: %.2f%%. Halting all EA trading!",
                     daily_dd_pct, InpMaxDailyLossPct, total_dd_pct);
         CloseAllBridgeTrades("LOCAL_PROP_BREACH_HALT");
      }
   }
}

//+------------------------------------------------------------------+
//| Closes all active trades opened by this bridge                   |
//+------------------------------------------------------------------+
void CloseAllBridgeTrades(const string reason)
{
   for(int i = PositionsTotal() - 1; i >= 0; i--)
   {
      if(m_position.SelectByIndex(i))
      {
         if(m_position.Magic() == InpMagicNumber)
         {
            m_trade.PositionClose(m_position.Ticket());
            PrintFormat("🛑 [EMERGENCY CLOSE] Closed position #%d (%s)", m_position.Ticket(), reason);
         }
      }
   }
}

//+------------------------------------------------------------------+
//| HUD DISPLAY FUNCTIONS                                            |
//+------------------------------------------------------------------+
void CreateHUD()
{
   int x = 15;
   int y = 25;
   int row = 18;

   CreateLabel(HUD_PREFIX + "TITLE", "💎 KHMER MASTER CRYPTO | APEX AGI BRIDGE", x, y, clrGold, 10, true);
   CreateLabel(HUD_PREFIX + "DIV1", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", x, y + row*1, clrDarkSlateGray, 8);
   CreateLabel(HUD_PREFIX + "STATUS", "📡 Status: INITIALIZING...", x, y + row*2, clrYellow, 9);
   CreateLabel(HUD_PREFIX + "SERVER", "🌐 Server: " + InpHost + ":" + IntegerToString(InpPort), x, y + row*3, clrWhite, 9);
   CreateLabel(HUD_PREFIX + "FIRM", "🏛️ Prop Firm: " + InpFirmName + " Shield Active", x, y + row*4, clrCyan, 9);
   CreateLabel(HUD_PREFIX + "EQUITY", "💰 Equity: $0.00 | Balance: $0.00", x, y + row*5, clrLightGreen, 9);
   CreateLabel(HUD_PREFIX + "RISK", "🛡️ Daily Drawdown: 0.00% [SAFE]", x, y + row*6, clrLime, 9);
   CreateLabel(HUD_PREFIX + "STATS", "⚡ Bridged Orders: 0 Orders Executed", x, y + row*7, clrWhite, 9);
   CreateLabel(HUD_PREFIX + "DIV2", "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━", x, y + row*8, clrDarkSlateGray, 8);
}

void UpdateHUD()
{
   string status_str = "";
   color status_col = clrRed;
   if(g_connected)
   {
      status_str = StringFormat("📡 Status: 🟢 CONNECTED (%.1f ms)", g_last_ping_ms);
      status_col = clrLime;
   }
   else
   {
      if(g_last_error_code > 0)
         status_str = StringFormat("📡 Status: 🔴 DISCONNECTED (Err: %d | Retrying...)", g_last_error_code);
      else
         status_str = "📡 Status: 🔴 DISCONNECTED (Auto-reconnecting...)";
      status_col = clrRed;
   }

   SetLabelText(HUD_PREFIX + "STATUS", status_str, status_col);

   string eq_str = StringFormat("💰 Equity: $%.2f | Balance: $%.2f", m_account.Equity(), m_account.Balance());
   SetLabelText(HUD_PREFIX + "EQUITY", eq_str, clrLightGreen);

   double daily_dd_pct = (g_daily_start_equity > 0) ? ((m_account.Equity() - g_daily_start_equity) / g_daily_start_equity) * 100.0 : 0.0;
   string risk_str = StringFormat("🛡️ Daily Drawdown: %+.2f%% (Limit: -%.1f%%) %s", 
                                  daily_dd_pct, InpMaxDailyLossPct, 
                                  g_prop_breached ? "[🚨 HALTED]" : "[✅ PASS]");
   color risk_col = g_prop_breached ? clrRed : (daily_dd_pct < -2.0 ? clrOrange : clrLime);
   SetLabelText(HUD_PREFIX + "RISK", risk_str, risk_col);

   string stats_str = StringFormat("⚡ Bridged Orders: %d Orders Executed", g_orders_executed);
   SetLabelText(HUD_PREFIX + "STATS", stats_str, clrWhite);
}

void CreateLabel(string name, string text, int x, int y, color col, int font_size, bool bold = false)
{
   ObjectDelete(0, name);
   ObjectCreate(0, name, OBJ_LABEL, 0, 0, 0);
   ObjectSetInteger(0, name, OBJPROP_XDISTANCE, x);
   ObjectSetInteger(0, name, OBJPROP_YDISTANCE, y);
   ObjectSetInteger(0, name, OBJPROP_COLOR, col);
   ObjectSetInteger(0, name, OBJPROP_FONTSIZE, font_size);
   ObjectSetString(0, name, OBJPROP_FONT, bold ? "Arial Black" : "Consolas");
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_CORNER, CORNER_LEFT_UPPER);
   ObjectSetInteger(0, name, OBJPROP_SELECTABLE, false);
}

void SetLabelText(string name, string text, color col)
{
   ObjectSetString(0, name, OBJPROP_TEXT, text);
   ObjectSetInteger(0, name, OBJPROP_COLOR, col);
}

void RemoveHUD()
{
   ObjectsDeleteAll(0, HUD_PREFIX);
}
//+------------------------------------------------------------------+
