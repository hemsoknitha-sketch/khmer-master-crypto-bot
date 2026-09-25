"""
mt5_bridge_engine.py
==============================================================================
KHMER MASTER CRYPTO / APEX SUPER BRAIN AGI
INSTITUTIONAL ZEROMQ & NATIVE TCP MT5 PROP FIRM BRIDGE ENGINE
==============================================================================
High-frequency, decoupled Wall Street bridge connecting Python AI Swarm
on Google Cloud Tokyo Linux VPS to MetaTrader 5 (MT5) on Windows / Laptop / VPS.

Architecture Pillars:
1. Sub-Millisecond Event-Driven Networking (Native Async TCP + ZeroMQ PUB/SUB).
2. Cryptographic Security Citadel (HMAC-SHA256 Payload Signature & Anti-Replay Nonce).
3. Wall Street Prop Firm Compliance Fortress (FTMO / FundedNext -3.5% Daily Loss & -7.0% Max Drawdown Shield).
4. Pure Native MQL5 Compatibility (Zero DLL Dependencies required on MT5).
==============================================================================
"""

import os
import sys
import time
import json
import uuid
import hmac
import hashlib
import socket
import select
import logging
import threading
from typing import Dict, Any, Optional, List, Tuple
from datetime import datetime

# Database and Core Security Citadel
import database as db
import system_security_citadel as sc
import ui_standards as ui
import notification_manager

# ZeroMQ high-speed messaging
try:
    import zmq
    ZMQ_AVAILABLE = True
except ImportError:
    ZMQ_AVAILABLE = False

logger = logging.getLogger("MT5BridgeEngine")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(logging.Formatter("[%(asctime)s][MT5_BRIDGE][%(levelname)s] %(message)s"))
    logger.addHandler(ch)

class MT5ClientSession:
    """Represents a connected MT5 terminal instance."""
    def __init__(self, account_id: str, socket_conn: Optional[socket.socket] = None, addr: str = ""):
        self.account_id = account_id
        self.chat_id: int = 0
        self.broker: str = "Unknown"
        self.firm_name: str = "FTMO"
        self.balance: float = 0.0
        self.equity: float = 0.0
        self.currency: str = "USD"
        self.daily_start_equity: float = 0.0
        self.initial_balance: float = 0.0
        self.ping_ms: float = 0.0
        self.is_prop_compliant: bool = True
        self.last_heartbeat: float = time.time()
        self.socket_conn = socket_conn
        self.addr = addr
        self.authenticated: bool = False
        self.status: str = "ONLINE"

class MT5BridgeEngine:
    _instance = None
    _lock = threading.Lock()

    @classmethod
    def get_instance(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def __init__(self):
        self.is_running = False
        self.tcp_host = os.getenv("MT5_BRIDGE_HOST", "0.0.0.0")
        self.tcp_port = int(os.getenv("MT5_BRIDGE_TCP_PORT", "5555"))
        self.zmq_pub_port = int(os.getenv("MT5_BRIDGE_ZMQ_PUB_PORT", "5556"))
        self.zmq_rep_port = int(os.getenv("MT5_BRIDGE_ZMQ_REP_PORT", "5557"))
        
        # Shared Secret Key for HMAC-SHA256 Signatures
        self.secret_key = os.getenv("MT5_BRIDGE_SECRET", "KhmerMasterCrypto_PropBridge_Fortress_2026")
        
        # Prop Firm Zero-Breach Compliance Limits
        self.prop_daily_limit_pct = -3.5   # Daily Hard Stop (-3.5%)
        self.prop_max_limit_pct = -7.0     # Max Total Trailing Drawdown (-7.0%)
        
        # Anti-Replay Nonce Cache: {nonce: expire_timestamp}
        self._nonce_cache: Dict[str, float] = {}
        self._nonce_lock = threading.Lock()
        
        # Connected Client Registry: {account_id: MT5ClientSession}
        self.clients: Dict[str, MT5ClientSession] = {}
        self._clients_lock = threading.Lock()
        
        # Sockets
        self.tcp_server_sock: Optional[socket.socket] = None
        self.zmq_context = None
        self.zmq_pub_sock = None
        
        # Background Threads
        self.tcp_thread: Optional[threading.Thread] = None
        self.cleanup_thread: Optional[threading.Thread] = None
        
        logger.info(f"🏛️ [MT5 BRIDGE] Initialized. TCP Port: {self.tcp_port}, ZMQ PUB: {self.zmq_pub_port}")

    # =========================================================================
    # 1. CRYPTOGRAPHIC SIGNATURE & ANTI-REPLAY CITADEL
    # =========================================================================
    def generate_signature(self, payload: Dict[str, Any]) -> str:
        """Generates deterministic HMAC-SHA256 signature for outbound packet."""
        clean_copy = {k: v for k, v in payload.items() if k != "signature"}
        raw_bytes = json.dumps(clean_copy, sort_keys=True, separators=(',', ':')).encode("utf-8")
        return hmac.new(self.secret_key.encode("utf-8"), raw_bytes, hashlib.sha256).hexdigest()

    def verify_signature(self, payload: Dict[str, Any]) -> Tuple[bool, str]:
        """Validates HMAC-SHA256 signature, timestamp window, and anti-replay nonce."""
        sig = payload.get("signature", "")
        if not sig:
            # Fallback to simple secret token match if EA sends direct token
            token = payload.get("token", "") or payload.get("secret_key", "")
            if token and token == self.secret_key:
                return True, "TOKEN_MATCH"
            return False, "MISSING_SIGNATURE"

        # 1. Verify Timestamp Window (+/- 15 seconds tolerance)
        pkt_time = payload.get("timestamp", 0)
        now_time = int(time.time())
        if abs(now_time - pkt_time) > 15:
            return False, f"TIMESTAMP_OUT_OF_WINDOW (diff: {abs(now_time - pkt_time)}s)"

        # 2. Verify Anti-Replay Nonce
        nonce = str(payload.get("nonce", ""))
        if nonce:
            with self._nonce_lock:
                if nonce in self._nonce_cache:
                    return False, "REPLAY_ATTACK_DETECTED"
                self._nonce_cache[nonce] = time.time() + 60.0

        # 3. Verify HMAC-SHA256 Digest
        expected_sig = self.generate_signature(payload)
        if not hmac.compare_digest(sig, expected_sig):
            # Check if secret token fallback matches
            token = payload.get("token", "")
            if token and token == self.secret_key:
                return True, "TOKEN_FALLBACK_OK"
            return False, "INVALID_HMAC_SIGNATURE"

        return True, "SIGNATURE_VALID"

    # =========================================================================
    # 2. LIFECYCLE MANAGEMENT (START / STOP)
    # =========================================================================
    def start(self):
        """Starts background TCP listener and ZeroMQ publisher."""
        if self.is_running:
            return
        self.is_running = True

        # Initialize ZeroMQ PUB socket
        if ZMQ_AVAILABLE:
            try:
                self.zmq_context = zmq.Context()
                self.zmq_pub_sock = self.zmq_context.socket(zmq.PUB)
                self.zmq_pub_sock.bind(f"tcp://{self.tcp_host}:{self.zmq_pub_port}")
                logger.info(f"⚡ [ZEROMQ PUB] Bound to tcp://{self.tcp_host}:{self.zmq_pub_port}")
            except Exception as e:
                logger.warning(f"⚠️ [ZEROMQ PUB] Failed to bind: {e}")

        # Start Native TCP Non-Blocking Server Thread
        self.tcp_thread = threading.Thread(target=self._run_tcp_server, name="MT5_TCP_Bridge", daemon=True)
        self.tcp_thread.start()

        # Start Nonce & Stale Client Cleanup Thread
        self.cleanup_thread = threading.Thread(target=self._cleanup_loop, name="MT5_Bridge_Cleanup", daemon=True)
        self.cleanup_thread.start()

        logger.info("🚀 [MT5 BRIDGE] Engine started successfully.")

    def stop(self):
        """Stops bridge engine gracefully."""
        self.is_running = False
        if self.tcp_server_sock:
            try:
                self.tcp_server_sock.close()
            except Exception:
                pass
        if self.zmq_pub_sock:
            try:
                self.zmq_pub_sock.close()
            except Exception:
                pass
        if self.zmq_context:
            try:
                self.zmq_context.term()
            except Exception:
                pass
        logger.info("🛑 [MT5 BRIDGE] Engine stopped.")

    # =========================================================================
    # 3. NATIVE ASYNC TCP SERVER (ZERO DLL FOR FTMO/PROP FIRMS)
    # =========================================================================
    def _run_tcp_server(self):
        """High-performance, non-blocking TCP server using select loop."""
        try:
            self.tcp_server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_server_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            # Disable Nagle's algorithm for sub-millisecond execution
            self.tcp_server_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
            self.tcp_server_sock.bind((self.tcp_host, self.tcp_port))
            self.tcp_server_sock.listen(20)
            self.tcp_server_sock.setblocking(False)
            logger.info(f"🌐 [NATIVE TCP BRIDGE] Listening on {self.tcp_host}:{self.tcp_port}")
        except Exception as e:
            logger.error(f"❌ [NATIVE TCP BRIDGE] Bind error: {e}")
            return

        inputs = [self.tcp_server_sock]
        client_buffers: Dict[socket.socket, str] = {}
        sock_to_account: Dict[socket.socket, str] = {}

        while self.is_running:
            try:
                readable, _, exceptional = select.select(inputs, [], inputs, 0.2)
                for s in readable:
                    if s is self.tcp_server_sock:
                        # Accept new connection from MT5 EA
                        client_sock, client_addr = self.tcp_server_sock.accept()
                        client_sock.setblocking(False)
                        client_sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
                        inputs.append(client_sock)
                        client_buffers[client_sock] = ""
                        logger.info(f"🔌 [MT5 BRIDGE] New connection from {client_addr[0]}:{client_addr[1]}")
                    else:
                        # Data received from connected MT5 EA
                        try:
                            data = s.recv(4096)
                            if data:
                                client_buffers[s] += data.decode("utf-8", errors="ignore")
                                # Process newline-delimited JSON packets
                                while "\n" in client_buffers[s]:
                                    line, client_buffers[s] = client_buffers[s].split("\n", 1)
                                    line = line.strip()
                                    if line:
                                        self._process_raw_line(s, line, sock_to_account)
                            else:
                                # Connection closed by client
                                self._disconnect_client(s, inputs, client_buffers, sock_to_account)
                        except (ConnectionResetError, ConnectionAbortedError):
                            self._disconnect_client(s, inputs, client_buffers, sock_to_account)
                        except Exception as e:
                            logger.error(f"⚠️ [TCP READ] Error: {e}")
                            self._disconnect_client(s, inputs, client_buffers, sock_to_account)

                for s in exceptional:
                    self._disconnect_client(s, inputs, client_buffers, sock_to_account)

            except Exception as e:
                if self.is_running:
                    logger.error(f"⚠️ [SELECT LOOP] Unexpected exception: {e}")
                time.sleep(0.1)

    def _disconnect_client(self, sock, inputs, buffers, sock_to_account):
        """Cleans up disconnected MT5 socket."""
        try:
            if sock in inputs:
                inputs.remove(sock)
            if sock in buffers:
                del buffers[sock]
            account_id = sock_to_account.pop(sock, None)
            if account_id:
                with self._clients_lock:
                    if account_id in self.clients:
                        self.clients[account_id].status = "DISCONNECTED"
                        self.clients[account_id].socket_conn = None
                logger.info(f"🔌 [MT5 BRIDGE] Account {account_id} disconnected.")
            sock.close()
        except Exception:
            pass

    def _process_raw_line(self, sock: socket.socket, line: str, sock_to_account: Dict[socket.socket, str]):
        """Parses and executes an incoming JSON packet from MT5."""
        try:
            payload = json.loads(line)
        except Exception:
            logger.warning(f"⚠️ [MT5 PACKET] Non-JSON payload received: {line[:50]}")
            return

        # 1. Security Check
        valid, reason = self.verify_signature(payload)
        if not valid:
            logger.warning(f"🛡️ [SECURITY CITADEL] Dropped invalid packet from MT5: {reason}")
            err_reply = {
                "type": "AUTH_ERROR",
                "reason": reason,
                "timestamp": int(time.time())
            }
            self._send_raw_socket(sock, err_reply)
            return

        msg_type = payload.get("type", "").upper()
        account_id = str(payload.get("account_id", "") or payload.get("account", ""))

        if not account_id:
            account_id = sock_to_account.get(sock, "UNKNOWN_ACCOUNT")

        # Associate socket with account
        if account_id and account_id != "UNKNOWN_ACCOUNT":
            sock_to_account[sock] = account_id

        # 2. Message Dispatcher
        if msg_type in ["AUTH", "HANDSHAKE"]:
            self._handle_auth(sock, payload, account_id)
        elif msg_type == "HEARTBEAT":
            self._handle_heartbeat(sock, payload, account_id)
        elif msg_type == "ORDER_CONFIRM":
            self._handle_order_confirm(payload, account_id)
        elif msg_type == "ORDER_CLOSED":
            self._handle_order_closed(payload, account_id)
        elif msg_type == "PING":
            pong = {"type": "PONG", "timestamp": int(time.time()), "echo_time": payload.get("timestamp", 0)}
            self._send_raw_socket(sock, pong)

    # =========================================================================
    # 4. PACKET HANDLERS & PROP FIRM COMPLIANCE FORTRESS
    # =========================================================================
    def _handle_auth(self, sock: socket.socket, payload: Dict[str, Any], account_id: str):
        """Processes authentication packet from MT5 EA."""
        broker = str(payload.get("broker", "Generic_MT5"))
        firm_name = str(payload.get("firm_name", "FTMO"))
        balance = float(payload.get("balance", 0.0))
        equity = float(payload.get("equity", balance))
        currency = str(payload.get("currency", "USD"))
        chat_id = int(payload.get("chat_id", 0))

        with self._clients_lock:
            session = self.clients.get(account_id)
            if not session:
                session = MT5ClientSession(account_id, socket_conn=sock)
                self.clients[account_id] = session
            session.socket_conn = sock
            session.broker = broker
            session.firm_name = firm_name
            session.balance = balance
            session.equity = equity
            session.currency = currency
            session.chat_id = chat_id
            session.authenticated = True
            session.status = "ONLINE"
            session.last_heartbeat = time.time()
            if session.daily_start_equity <= 0:
                session.daily_start_equity = equity
            if session.initial_balance <= 0:
                session.initial_balance = balance

        # Upsert in SQLite DB
        db.upsert_mt5_bridge_client(
            account_id=account_id,
            chat_id=chat_id,
            broker=broker,
            firm_name=firm_name,
            balance=balance,
            equity=equity,
            currency=currency,
            ping_ms=0.0,
            daily_start_equity=equity,
            is_prop_compliant=True,
            status="ONLINE"
        )

        ack = {
            "type": "AUTH_SUCCESS",
            "account_id": account_id,
            "status": "AUTHENTICATED",
            "timestamp": int(time.time()),
            "message": "Connected to Khmer Master Crypto Tokyo VPS Bridge."
        }
        self._send_raw_socket(sock, ack)
        logger.info(f"✅ [MT5 AUTH] Account {account_id} ({broker} / {firm_name}) authenticated successfully! Balance: ${balance:,.2f}")

    def _handle_heartbeat(self, sock: socket.socket, payload: Dict[str, Any], account_id: str):
        """Processes periodic telemetry and runs Wall Street Prop Firm compliance check."""
        balance = float(payload.get("balance", 0.0))
        equity = float(payload.get("equity", balance))
        broker = str(payload.get("broker", ""))
        firm_name = str(payload.get("firm_name", "FTMO"))
        daily_start = float(payload.get("daily_start_equity", 0.0))
        initial_bal = float(payload.get("initial_balance", balance))
        chat_id = int(payload.get("chat_id", 0))
        
        # Calculate Latency
        pkt_time_ms = payload.get("timestamp_ms", 0)
        ping_ms = 0.0
        if pkt_time_ms > 0:
            ping_ms = max(1.0, round((time.time() * 1000.0) - pkt_time_ms, 2))

        with self._clients_lock:
            session = self.clients.get(account_id)
            if not session:
                session = MT5ClientSession(account_id, socket_conn=sock)
                self.clients[account_id] = session
            session.balance = balance
            session.equity = equity
            session.ping_ms = ping_ms
            session.last_heartbeat = time.time()
            session.status = "ONLINE"
            if broker:
                session.broker = broker
            if firm_name:
                session.firm_name = firm_name
            if daily_start > 0:
                session.daily_start_equity = daily_start
            elif session.daily_start_equity <= 0:
                session.daily_start_equity = equity
            if initial_bal > 0:
                session.initial_balance = initial_bal
            elif session.initial_balance <= 0:
                session.initial_balance = balance

            # =================================================================
            # WALL STREET PROP FIRM COMPLIANCE CITADEL (FTMO -3.5% / -7.0%)
            # =================================================================
            compliant, details = sc.security_citadel.evaluate_prop_firm_compliance(
                account_id=account_id,
                current_equity=equity,
                daily_start_equity=session.daily_start_equity,
                initial_balance=session.initial_balance
            )
            session.is_prop_compliant = compliant

            if not compliant:
                session.status = "LOCKED_PROP_BREACH"
                logger.error(f"🚨 [PROP BREACH] Account {account_id} breached limit: {details}")
                # Send Emergency Alert to MT5
                emergency_msg = {
                    "type": "PROP_CIRCUIT_BREAKER",
                    "account_id": account_id,
                    "action": "HALT_TRADING",
                    "reason": details.get("action", "PROP_BREACH"),
                    "details": details,
                    "timestamp": int(time.time())
                }
                self._send_raw_socket(sock, emergency_msg)

        # Update SQLite DB
        db.upsert_mt5_bridge_client(
            account_id=account_id,
            chat_id=chat_id,
            broker=broker,
            firm_name=firm_name,
            balance=balance,
            equity=equity,
            ping_ms=ping_ms,
            daily_start_equity=daily_start if daily_start > 0 else equity,
            is_prop_compliant=compliant,
            status=session.status
        )

    def _handle_order_confirm(self, payload: Dict[str, Any], account_id: str):
        """Processes trade entry fill confirmation from MT5."""
        signal_id = str(payload.get("signal_id", ""))
        ticket = int(payload.get("ticket", 0))
        open_price = float(payload.get("open_price", 0.0) or payload.get("price", 0.0))
        status = str(payload.get("status", "FILLED"))

        db.update_mt5_bridge_order_fill(signal_id=signal_id, ticket=ticket, open_price=open_price, status=status)
        logger.info(f"🎯 [MT5 FILL] Account {account_id} filled order! Ticket: #{ticket}, Price: {open_price}")

    def _handle_order_closed(self, payload: Dict[str, Any], account_id: str):
        """Processes trade close confirmation from MT5."""
        ticket = int(payload.get("ticket", 0))
        close_price = float(payload.get("close_price", 0.0) or payload.get("price", 0.0))
        pnl = float(payload.get("pnl", 0.0))
        status = str(payload.get("status", "CLOSED"))

        db.update_mt5_bridge_order_close(ticket=ticket, close_price=close_price, pnl=pnl, status=status)
        logger.info(f"💰 [MT5 CLOSED] Account {account_id} closed #{ticket}! Close Price: {close_price}, PnL: ${pnl:+,.2f}")

    # =========================================================================
    # 5. TRADE SIGNAL DISPATCH API (SUB-MILLISECOND EXECUTION)
    # =========================================================================
    def dispatch_order(
        self,
        symbol: str,
        action: str,
        lot: float,
        sl: float = 0.0,
        tp: float = 0.0,
        comment: str = "APEX_AI",
        magic: int = 888999,
        target_account: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Dispatches a high-speed trade order signal simultaneously across
        all connected MT5 terminals (or a targeted account).
        """
        signal_id = f"SIG-{int(time.time()*1000)}-{uuid.uuid4().hex[:6]}"
        sym_norm = str(symbol).strip().upper()
        act_norm = "BUY" if str(action).strip().upper() in ["BUY", "LONG"] else "SELL"
        lot_norm = max(0.01, round(float(lot), 2))
        sl_norm = round(float(sl), 5) if sl > 0 else 0.0
        tp_norm = round(float(tp), 5) if tp > 0 else 0.0

        # Construct Signed Payload
        payload = {
            "type": "ORDER_SEND",
            "signal_id": signal_id,
            "symbol": sym_norm,
            "action": act_norm,
            "lot": lot_norm,
            "sl": sl_norm,
            "tp": tp_norm,
            "magic": int(magic),
            "comment": str(comment),
            "timestamp": int(time.time()),
            "nonce": time.time_ns()
        }
        payload["signature"] = self.generate_signature(payload)

        # Record in SQLite Database
        db.record_mt5_bridge_order(
            signal_id=signal_id,
            account_id=target_account or "BROADCAST",
            symbol=sym_norm,
            action=act_norm,
            lot=lot_norm,
            sl=sl_norm,
            tp=tp_norm,
            magic=magic,
            comment=comment,
            status="SENT"
        )

        clients_reached = 0
        with self._clients_lock:
            for acc_id, session in self.clients.items():
                if target_account and acc_id != target_account:
                    continue
                # Prop Firm Compliance Guard: Never route to breached account
                if not session.is_prop_compliant:
                    logger.warning(f"🛡️ [DISPATCH GUARD] Skipped account {acc_id} due to Prop Firm Breach status.")
                    continue
                if session.socket_conn:
                    if self._send_raw_socket(session.socket_conn, payload):
                        clients_reached += 1

        # Also broadcast via ZeroMQ PUB if available
        if self.zmq_pub_sock and ZMQ_AVAILABLE:
            try:
                topic = b"TRADE_SIGNAL "
                packet_bytes = json.dumps(payload).encode("utf-8")
                self.zmq_pub_sock.send_multipart([topic, packet_bytes])
            except Exception as e:
                logger.error(f"⚠️ [ZMQ PUB SEND] Error: {e}")

        logger.info(f"⚡ [MT5 DISPATCH] Signal {signal_id} ({act_norm} {lot_norm} {sym_norm} SL:{sl_norm} TP:{tp_norm}) dispatched to {clients_reached} terminals!")
        return {
            "success": True,
            "signal_id": signal_id,
            "clients_reached": clients_reached,
            "symbol": sym_norm,
            "action": act_norm,
            "lot": lot_norm
        }

    def dispatch_close(
        self,
        ticket: int,
        symbol: Optional[str] = None,
        comment: str = "AI_CLOSE",
        target_account: Optional[str] = None
    ) -> Dict[str, Any]:
        """Dispatches an atomic close signal for an active position."""
        payload = {
            "type": "ORDER_CLOSE",
            "ticket": int(ticket),
            "symbol": str(symbol).upper() if symbol else "",
            "comment": str(comment),
            "timestamp": int(time.time()),
            "nonce": time.time_ns()
        }
        payload["signature"] = self.generate_signature(payload)

        clients_reached = 0
        with self._clients_lock:
            for acc_id, session in self.clients.items():
                if target_account and acc_id != target_account:
                    continue
                if session.socket_conn:
                    if self._send_raw_socket(session.socket_conn, payload):
                        clients_reached += 1

        return {"success": True, "ticket": ticket, "clients_reached": clients_reached}

    def dispatch_modify(
        self,
        ticket: int,
        new_sl: float,
        new_tp: float = 0.0,
        target_account: Optional[str] = None
    ) -> Dict[str, Any]:
        """Dispatches dynamic Trailing Stop or Take Profit modification."""
        payload = {
            "type": "MODIFY_STOPS",
            "ticket": int(ticket),
            "sl": round(float(new_sl), 5),
            "tp": round(float(new_tp), 5),
            "timestamp": int(time.time()),
            "nonce": time.time_ns()
        }
        payload["signature"] = self.generate_signature(payload)

        clients_reached = 0
        with self._clients_lock:
            for acc_id, session in self.clients.items():
                if target_account and acc_id != target_account:
                    continue
                if session.socket_conn:
                    if self._send_raw_socket(session.socket_conn, payload):
                        clients_reached += 1

        return {"success": True, "ticket": ticket, "new_sl": new_sl, "new_tp": new_tp, "clients_reached": clients_reached}

    # =========================================================================
    # 6. LOW-LEVEL NETWORK HELPERS & TELEMETRY
    # =========================================================================
    def _send_raw_socket(self, sock: socket.socket, data_dict: Dict[str, Any]) -> bool:
        """Sends newline-delimited JSON over non-blocking socket."""
        try:
            line = json.dumps(data_dict) + "\n"
            sock.sendall(line.encode("utf-8"))
            return True
        except Exception as e:
            logger.warning(f"⚠️ [SOCKET SEND] Failed to send to client: {e}")
            return False

    def _cleanup_loop(self):
        """Purges expired anti-replay nonces and flags stale client sessions."""
        while self.is_running:
            time.sleep(30.0)
            now = time.time()
            # 1. Clean Nonces
            with self._nonce_lock:
                expired = [k for k, exp in self._nonce_cache.items() if now > exp]
                for k in expired:
                    del self._nonce_cache[k]

            # 2. Flag Stale Clients (> 45s without heartbeat)
            with self._clients_lock:
                for acc_id, session in self.clients.items():
                    if session.status == "ONLINE" and (now - session.last_heartbeat) > 45.0:
                        session.status = "OFFLINE"
                        logger.warning(f"⚠️ [HEARTBEAT TIMEOUT] Account {acc_id} marked OFFLINE (stale heartbeat).")

    def get_bridge_status(self) -> Dict[str, Any]:
        """Provides executive telemetry summary for Telegram UI and audits."""
        with self._clients_lock:
            total_clients = len(self.clients)
            online_clients = sum(1 for c in self.clients.values() if c.status == "ONLINE")
            breached_clients = sum(1 for c in self.clients.values() if not c.is_prop_compliant)
            pings = [c.ping_ms for c in self.clients.values() if c.status == "ONLINE" and c.ping_ms > 0]
            avg_ping = round(sum(pings) / len(pings), 1) if pings else 0.0

            clients_summary = []
            for acc_id, c in self.clients.items():
                clients_summary.append({
                    "account_id": acc_id,
                    "broker": c.broker,
                    "firm_name": c.firm_name,
                    "balance": c.balance,
                    "equity": c.equity,
                    "ping_ms": c.ping_ms,
                    "compliant": c.is_prop_compliant,
                    "status": c.status
                })

        return {
            "is_running": self.is_running,
            "tcp_port": self.tcp_port,
            "zmq_pub_port": self.zmq_pub_port,
            "total_clients": total_clients,
            "online_clients": online_clients,
            "breached_clients": breached_clients,
            "avg_ping_ms": avg_ping,
            "clients": clients_summary
        }

# Global Singleton Instance
mt5_bridge = MT5BridgeEngine.get_instance()
