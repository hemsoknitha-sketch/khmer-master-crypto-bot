import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import sys
import os
import socket

# BUG FIX: Smart DNS over HTTPS (DoH) for Binance
# Bypasses local ISP blocks or broken VPS IPv4/IPv6 DNS by using Google DNS API.
import urllib.request
import json

old_getaddrinfo = socket.getaddrinfo
DNS_CACHE = {}

def new_getaddrinfo(host, port, family=0, type=0, proto=0, flags=0):
    host_str = host.decode('utf-8') if isinstance(host, bytes) else str(host)
    if "binance.com" in host_str:
        if host_str in DNS_CACHE:
            ip = DNS_CACHE[host_str]
            return [(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, '', (ip, port))]
        try:
            req = urllib.request.Request(f"https://dns.google/resolve?name={host_str}&type=A")
            with urllib.request.urlopen(req, timeout=3) as response:
                data = json.loads(response.read().decode())
                ip = next((ans['data'] for ans in data.get('Answer', []) if ans['type'] == 1), None)
                if ip:
                    DNS_CACHE[host_str] = ip
                    return [(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, '', (ip, port))]
        except Exception:
            pass # Fallback to normal resolution
            
    try:
        return old_getaddrinfo(host, port, socket.AF_INET, type, proto, flags)
    except Exception:
        return old_getaddrinfo(host, port, family, type, proto, flags)

socket.getaddrinfo = new_getaddrinfo

# Institutional Single-Instance Lock Guard
LOCK_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bot_instance.lock")

def acquire_single_instance_lock():
    """Guarantees only ONE instance of Apex AI Bot runs to prevent Telegram Conflict errors."""
    try:
        if os.path.exists(LOCK_FILE):
            with open(LOCK_FILE, "r") as f:
                old_pid_str = f.read().strip()
                if old_pid_str.isdigit():
                    old_pid = int(old_pid_str)
                    if old_pid != os.getpid():
                        try:
                            import psutil
                            if psutil.pid_exists(old_pid):
                                print(f"⚠️ [SINGLE INSTANCE GUARD] Bot instance PID {old_pid} is already running. Exiting new duplicate process to prevent Telegram Conflict Error.")
                                sys.exit(0)
                        except Exception:
                            pass
        with open(LOCK_FILE, "w") as f:
            f.write(str(os.getpid()))
    except Exception as e:
        print(f"Single instance lock check notice: {e}")

acquire_single_instance_lock()

from dotenv import load_dotenv

# Load Environment Variables from .env file BEFORE importing local modules
load_dotenv()

is_cli_mode = ("--cli" in sys.argv or "--no-gui" in sys.argv or "--vps" in sys.argv or "--headless" in sys.argv or "-vps" in sys.argv)

try:
    from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget, QLabel, QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView, QRadioButton, QHBoxLayout, QMessageBox, QAbstractItemView, QSystemTrayIcon, QMenu, QAction, QStyle, QComboBox, QListWidget, QListWidgetItem)
    from PyQt5.QtCore import Qt, QThread, pyqtSignal
    from PyQt5.QtGui import QIcon
except ImportError:
    class QThread: pass
    def pyqtSignal(*args, **kwargs): return lambda: None
    QApplication = QMainWindow = QWidget = object

from ai_engine import AIInvestmentEngine
from bot_thread import TelegramBotThread
import database as db

class DraftReplyWorker(QThread):
    finished_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)

    def __init__(self, ai_engine, prompt):
        super().__init__()
        self.ai_engine = ai_engine
        self.prompt = prompt

    def run(self):
        try:
            draft = self.ai_engine.analyze_opportunity(self.prompt)
            self.finished_signal.emit(draft)
        except Exception as e:
            self.error_signal.emit(str(e))

class BotDashboard(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("⚡ APEX TURBO AGI v9.8 | INSTITUTIONAL ADMIN DESKTOP EXECUTIVE DASHBOARD 🚀")
        self.setGeometry(100, 100, 1100, 750)
        
        # Apply Modern Dark Mode & Glassmorphic Theme QSS Styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #0b0e14;
                color: #e0e6ed;
            }
            QTabWidget::pane {
                border: 1px solid #1f293d;
                background-color: #121824;
                border-radius: 8px;
            }
            QTabBar::tab {
                background: #1a2234;
                color: #8a99ad;
                padding: 10px 18px;
                font-weight: bold;
                font-size: 13px;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                margin-right: 2px;
            }
            QTabBar::tab:selected {
                background: #00e676;
                color: #0b0e14;
                font-weight: bold;
            }
            QTabBar::tab:hover {
                background: #253147;
                color: #ffffff;
            }
            QPushButton {
                background-color: #1f293d;
                color: #ffffff;
                border: 1px solid #2e3c54;
                padding: 8px 14px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #00b0ff;
                color: #ffffff;
                border-color: #00e676;
            }
            QTextEdit, QTableWidget, QListWidget {
                background-color: #0d111a;
                color: #00e676;
                border: 1px solid #1f293d;
                border-radius: 6px;
                font-family: 'Consolas', 'Segoe UI', monospace;
            }
            QHeaderView::section {
                background-color: #1a2234;
                color: #00e676;
                padding: 6px;
                font-weight: bold;
                border: 1px solid #1f293d;
            }
            QLabel {
                color: #e0e6ed;
                font-weight: bold;
            }
        """)

        # Initialize the database immediately before any UI loads data from it
        db.init_db()
        
        # Perform Zero Data Loss Boot Backup
        import backup_manager
        backup_manager.perform_backup(is_boot=True)

        # Tab Widget
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.bot_thread = None
        self.BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.GEMINI_KEY = os.getenv("GEMINI_API_KEY")
        self.is_quitting = False

        self.init_dashboard_tab()
        self.init_users_tab()
        self.init_broadcast_tab()
        self.init_help_center_tab()
        self.init_settings_tab()
        
        self.init_tray_icon()
        
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(1000, self.start_system)

    def init_tray_icon(self):
        try:
            if not QSystemTrayIcon.isSystemTrayAvailable():
                self.tray_icon = None
                return
            self.tray_icon = QSystemTrayIcon(self)
            icon = self.style().standardIcon(QStyle.SP_ComputerIcon)
            self.tray_icon.setIcon(icon)
            
            tray_menu = QMenu()
            show_action = QAction("Open Executive Dashboard", self)
            show_action.triggered.connect(self.showNormal)
            tray_menu.addAction(show_action)
            
            quit_action = QAction("Quit System", self)
            quit_action.triggered.connect(self.quit_app)
            tray_menu.addAction(quit_action)
            
            self.tray_icon.setContextMenu(tray_menu)
            self.tray_icon.activated.connect(self.tray_icon_activated)
            self.tray_icon.show()
        except Exception:
            self.tray_icon = None

    def tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

    def quit_app(self):
        print("⚠️ Initiating Final Shutdown Backup...")
        try:
            import backup_manager
            import requests
            import os
            
            backup_path = backup_manager.perform_backup(is_boot=False)
            if backup_path and os.path.exists(backup_path) and self.BOT_TOKEN and self.BOT_TOKEN != "your_telegram_bot_token_here":
                url = f"https://api.telegram.org/bot{self.BOT_TOKEN}/sendDocument"
                with open(backup_path, 'rb') as doc:
                    requests.post(
                        url,
                        data={'chat_id': '859271875', 'caption': '🛑 **[SYSTEM STOPPED]** ប្រព័ន្ធត្រូវបានបិទ! នេះគឺជាទិន្នន័យ Database ចុងក្រោយបំផុត។', 'parse_mode': 'Markdown'},
                        files={'document': doc},
                        timeout=10
                    )
                print("✅ Final backup successfully sent to Admin.")
        except Exception as e:
            print(f"❌ Failed to send final backup: {e}")
            
        self.is_quitting = True
        self.close()

    def init_settings_tab(self):
        self.settings_tab = QWidget()
        layout = QVBoxLayout()
        
        layout.addWidget(QLabel("⚙️ Dynamic Executive TURBO AGI System Prompt (ai_prompt.txt):"))
        
        self.prompt_editor = QTextEdit()
        self.prompt_editor.setStyleSheet("font-size: 13px; font-family: Consolas; color: #00e676; background-color: #0d111a;")
        
        try:
            prompt_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai_prompt.txt")
            with open(prompt_file, "r", encoding="utf-8") as f:
                self.prompt_editor.setPlainText(f.read())
        except Exception:
            pass
            
        layout.addWidget(self.prompt_editor)
        
        self.save_prompt_btn = QPushButton("💾 Save & Apply System Prompt Real-Time")
        self.save_prompt_btn.setStyleSheet("padding: 12px; font-size: 14px; background-color: #7c4dff; color: white; font-weight: bold;")
        self.save_prompt_btn.clicked.connect(self.save_ai_prompt)
        layout.addWidget(self.save_prompt_btn)
        
        self.settings_tab.setLayout(layout)
        self.tabs.addTab(self.settings_tab, "⚙️ AI Settings")

    def save_ai_prompt(self):
        new_prompt = self.prompt_editor.toPlainText().strip()
        if not new_prompt:
            QMessageBox.warning(self, "Error", "Prompt cannot be empty!")
            return
            
        try:
            prompt_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ai_prompt.txt")
            with open(prompt_file, "w", encoding="utf-8") as f:
                f.write(new_prompt)
            QMessageBox.information(self, "Success", "TURBO AGI Executive Prompt updated! Will apply on next AI request.")
            self.append_log("⚙️ TURBO AGI System Prompt dynamically updated by Admin.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save prompt: {e}")

    def init_dashboard_tab(self):
        self.dashboard_tab = QWidget()
        layout = QVBoxLayout()

        self.status_label = QLabel("⚡ System Status: Standby ⏸️ (TURBO AGI Ready)")
        self.status_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #00b0ff; padding: 6px;")
        layout.addWidget(self.status_label)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        self.log_output.document().setMaximumBlockCount(1000)
        self.log_output.setStyleSheet("background-color: #090c10; color: #00e676; font-family: Consolas; font-size: 12px; border: 1px solid #1f293d;")
        layout.addWidget(self.log_output)

        btn_bar = QHBoxLayout()
        self.start_btn = QPushButton("🚀 Launch TURBO AGI Telegram Bot Node")
        self.start_btn.setStyleSheet("padding: 12px; font-size: 14px; background-color: #00e676; color: #0b0e14; font-weight: bold; border-radius: 6px;")
        self.start_btn.clicked.connect(self.start_system)

        self.stop_btn = QPushButton("🛑 Emergency Kill-Switch (All Bots)")
        self.stop_btn.setStyleSheet("padding: 12px; font-size: 14px; background-color: #ff1744; color: white; font-weight: bold; border-radius: 6px;")
        self.stop_btn.clicked.connect(self.trigger_emergency_stop)

        btn_bar.addWidget(self.start_btn)
        btn_bar.addWidget(self.stop_btn)
        layout.addLayout(btn_bar)

        self.dashboard_tab.setLayout(layout)
        self.tabs.addTab(self.dashboard_tab, "🖥️ Executive Control Console")

    def trigger_emergency_stop(self):
        reply = QMessageBox.question(self, 'Confirm Emergency Kill-Switch',
                                     "Are you sure you want to stop all active bots and trading engines?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.append_log("🚨 Emergency Kill-Switch triggered from Admin Desktop Console!")
            if self.bot_thread and self.bot_thread.isRunning():
                self.bot_thread.stop()
            self.status_label.setText("System Status: Stopped 🛑")
            self.status_label.setStyleSheet("font-size: 15px; font-weight: bold; color: #ff1744;")
            self.start_btn.setEnabled(True)

    def init_users_tab(self):
        self.users_tab = QWidget()
        layout = QVBoxLayout()

        # Users Table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(6)
        self.users_table.setHorizontalHeaderLabels(["Chat ID", "Username", "Joined Date", "VIP Status", "License Expiry", "Phone Number"])
        self.users_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.users_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        layout.addWidget(self.users_table)

        btn_layout = QHBoxLayout()
        self.refresh_btn = QPushButton("🔄 Refresh Users")
        self.refresh_btn.clicked.connect(self.load_users_from_db)
        
        self.license_combo = QComboBox()
        self.license_combo.addItems(["1 Day", "3 Days", "1 Month", "2 Months", "3 Months", "1 Year", "2 Years", "3 Years", "Lifetime", "Administrator", "Revoke VIP"])
        self.license_combo.setStyleSheet("padding: 5px; font-size: 14px;")
        
        self.apply_license_btn = QPushButton("⭐ Apply License")
        self.apply_license_btn.setStyleSheet("background-color: #f39c12; color: white; font-weight: bold; padding: 5px;")
        self.apply_license_btn.clicked.connect(self.apply_selected_license)
        
        self.delete_user_btn = QPushButton("🗑️ Delete User")
        self.delete_user_btn.setStyleSheet("background-color: #e74c3c; color: white; font-weight: bold; padding: 5px;")
        self.delete_user_btn.clicked.connect(self.delete_selected_user)
        
        btn_layout.addWidget(self.refresh_btn)
        btn_layout.addWidget(QLabel("Select License:"))
        btn_layout.addWidget(self.license_combo)
        btn_layout.addWidget(self.apply_license_btn)
        btn_layout.addWidget(self.delete_user_btn)
        layout.addLayout(btn_layout)

        self.users_tab.setLayout(layout)
        self.tabs.addTab(self.users_tab, "👥 User Management")
        self.load_users_from_db()

    def init_broadcast_tab(self):
        self.broadcast_tab = QWidget()
        layout = QVBoxLayout()

        layout.addWidget(QLabel("📢 Write your Announcement/Signal here:"))
        
        self.broadcast_text = QTextEdit()
        self.broadcast_text.setStyleSheet("font-size: 14px;")
        layout.addWidget(self.broadcast_text)

        # Radio buttons for target
        target_layout = QHBoxLayout()
        self.radio_all = QRadioButton("All Users")
        self.radio_vip = QRadioButton("VIPs Only")
        self.radio_vip.setChecked(True) # Default to VIP
        target_layout.addWidget(QLabel("Target Audience:"))
        target_layout.addWidget(self.radio_all)
        target_layout.addWidget(self.radio_vip)
        target_layout.addStretch()
        layout.addLayout(target_layout)

        self.send_broadcast_btn = QPushButton("🚀 Send Broadcast")
        self.send_broadcast_btn.setStyleSheet("padding: 10px; font-size: 14px; background-color: #27ae60; color: white; font-weight: bold;")
        self.send_broadcast_btn.clicked.connect(self.trigger_broadcast)
        layout.addWidget(self.send_broadcast_btn)

        self.broadcast_tab.setLayout(layout)
        self.tabs.addTab(self.broadcast_tab, "📢 Broadcast Center")

    def init_help_center_tab(self):
        self.help_center_tab = QWidget()
        layout = QHBoxLayout()
        
        # Left Panel (User List)
        left = QVBoxLayout()
        left.addWidget(QLabel("👤 Select User:"))
        self.help_users_list = QListWidget()
        self.help_users_list.itemClicked.connect(self.load_user_help_profile)
        left.addWidget(self.help_users_list)
        
        self.refresh_help_btn = QPushButton("🔄 Refresh List")
        self.refresh_help_btn.clicked.connect(self.load_help_users)
        left.addWidget(self.refresh_help_btn)
        
        # Right Panel (Activity & Chat)
        right = QVBoxLayout()
        right.addWidget(QLabel("📊 AI Activity Report & Chat History:"))
        self.user_activity_display = QTextEdit()
        self.user_activity_display.setReadOnly(True)
        right.addWidget(self.user_activity_display)
        
        right.addWidget(QLabel("✍️ Reply / Message:"))
        self.reply_input = QTextEdit()
        self.reply_input.setMaximumHeight(100)
        right.addWidget(self.reply_input)
        
        btn_layout = QHBoxLayout()
        self.ai_draft_btn = QPushButton("✨ AI Draft Reply")
        self.ai_draft_btn.setStyleSheet("background-color: #9b59b6; color: white; font-weight: bold; padding: 10px;")
        self.ai_draft_btn.clicked.connect(self.draft_ai_reply)
        
        self.send_reply_btn = QPushButton("📤 Send Direct Message")
        self.send_reply_btn.setStyleSheet("background-color: #3498db; color: white; font-weight: bold; padding: 10px;")
        self.send_reply_btn.clicked.connect(self.send_direct_message)
        
        btn_layout.addWidget(self.ai_draft_btn)
        btn_layout.addWidget(self.send_reply_btn)
        right.addLayout(btn_layout)
        
        layout.addLayout(left, 1)
        layout.addLayout(right, 2)
        
        self.help_center_tab.setLayout(layout)
        self.tabs.addTab(self.help_center_tab, "💬 AI Help Center")
        
        self.load_help_users()

    def load_help_users(self):
        self.help_users_list.clear()
        users = db.get_all_users()
        for u in users:
            c_id, uname, is_vip, joined, expiry, phone = u
            item = QListWidgetItem(f"[{c_id}] @{uname}")
            item.setData(Qt.UserRole, c_id)
            self.help_users_list.addItem(item)

    def load_user_help_profile(self, item):
        chat_id = item.data(Qt.UserRole)
        summary = db.get_user_activity_summary(chat_id)
        
        chat_history = db.get_chat_history(chat_id, limit=20)
        history_text = "\n\n--- Chat History ---\n"
        if not chat_history:
            history_text += "No recent chat."
        else:
            # chat_history format: (role, content, timestamp)
            for role, content, ts in reversed(chat_history):
                history_text += f"[{ts}] {role.upper()}: {content}\n"
                
        self.user_activity_display.setText(summary + history_text)

    def draft_ai_reply(self):
        if not self.bot_thread or not self.bot_thread.ai_engine:
            QMessageBox.warning(self, "Error", "Bot must be running to use AI Drafting.")
            return
            
        item = self.help_users_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Please select a user first.")
            return
            
        profile_data = self.user_activity_display.toPlainText()
        prompt = (f"You are the Apex AI Bot's Lead Customer Success Expert and a highly skilled Crypto Arbitrage Specialist. "
                  f"Look at this user's activity and chat history:\n\n{profile_data}\n\n"
                  f"Draft a highly persuasive, confident, and personalized response to this user in Khmer. "
                  f"Provide expert advice on using our High-Volatility Arbitrage systems like /infinity_grid and /scalp. "
                  f"Don't mention internal technical details, just sound like a billionaire-tier professional helping them win. "
                  f"Output ONLY the message text you want to send.")
        
        self.reply_input.setText("✨ AI is thinking... Please wait...")
        self.ai_draft_btn.setEnabled(False)
        
        self.draft_worker = DraftReplyWorker(self.bot_thread.ai_engine, prompt)
        self.draft_worker.finished_signal.connect(self.on_draft_success)
        self.draft_worker.error_signal.connect(self.on_draft_error)
        self.draft_worker.start()

    def on_draft_success(self, draft):
        self.reply_input.setText(draft)
        self.ai_draft_btn.setEnabled(True)

    def on_draft_error(self, error):
        self.reply_input.setText("")
        QMessageBox.critical(self, "Error", f"Failed to draft reply: {error}")
        self.ai_draft_btn.setEnabled(True)

    def send_direct_message(self):
        if not self.bot_thread or not self.bot_thread.isRunning():
            QMessageBox.warning(self, "Error", "Bot must be running to send messages.")
            return
            
        item = self.help_users_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Please select a user first.")
            return
            
        chat_id = item.data(Qt.UserRole)
        text = self.reply_input.toPlainText().strip()
        if not text:
            return
            
        self.bot_thread.direct_message_signal.emit(chat_id, text)
        QMessageBox.information(self, "Sent", f"Message sent to User {chat_id}!")
        self.reply_input.clear()

    def load_users_from_db(self):
        users = db.get_all_users()
        self.users_table.setRowCount(0)
        for row_idx, row_data in enumerate(users):
            self.users_table.insertRow(row_idx)
            chat_id, username, is_vip, joined, license_expiry, phone_number = row_data
            
            self.users_table.setItem(row_idx, 0, QTableWidgetItem(str(chat_id)))
            self.users_table.setItem(row_idx, 1, QTableWidgetItem(username))
            self.users_table.setItem(row_idx, 2, QTableWidgetItem(joined))
            
            vip_text = "⭐ VIP" if is_vip else "❌ Not VIP"
            vip_item = QTableWidgetItem(vip_text)
            if is_vip:
                vip_item.setForeground(Qt.darkGreen)
            else:
                vip_item.setForeground(Qt.red)
            self.users_table.setItem(row_idx, 3, vip_item)
            
            expiry_text = str(license_expiry) if license_expiry else "None"
            self.users_table.setItem(row_idx, 4, QTableWidgetItem(expiry_text))
            
            phone_text = str(phone_number) if phone_number else "No Phone"
            self.users_table.setItem(row_idx, 5, QTableWidgetItem(phone_text))

    def delete_selected_user(self):
        selected_items = self.users_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No User Selected", "Please select a user from the table first.")
            return
            
        row = selected_items[0].row()
        chat_id = int(self.users_table.item(row, 0).text())
        username = self.users_table.item(row, 1).text()
        
        reply = QMessageBox.question(self, 'Confirm Deletion', 
                                     f"Are you sure you want to completely delete {username} (ID: {chat_id}) and wipe all their data?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            db.delete_user_data(chat_id)
            self.load_users_from_db()
            self.append_log(f"🗑️ Deleted User and Wiped Data: {username} (ID: {chat_id})")

    def apply_selected_license(self):
        selected_items = self.users_table.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No User Selected", "Please select a user from the table first.")
            return
            
        row = selected_items[0].row()
        chat_id = int(self.users_table.item(row, 0).text())
        duration = self.license_combo.currentText()
        
        db.set_user_license(chat_id, duration)
        self.load_users_from_db()
        self.append_log(f"⭐ Applied License '{duration}' for Chat ID {chat_id}")

    def trigger_broadcast(self):
        if not self.bot_thread or not self.bot_thread.isRunning():
            QMessageBox.critical(self, "Bot Not Running", "You must Start the Telegram Bot first before broadcasting!")
            return
            
        text = self.broadcast_text.toPlainText().strip()
        if not text:
            QMessageBox.warning(self, "Empty Message", "Please write a message to broadcast.")
            return
            
        target = "VIPs Only" if self.radio_vip.isChecked() else "All Users"
        reply = QMessageBox.question(self, 'Confirm Broadcast', 
                                     f"Are you sure you want to send this message to {target}?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
        if reply == QMessageBox.Yes:
            self.bot_thread.broadcast_message(text, target)
            self.broadcast_text.clear()

    def append_log(self, text: str):
        self.log_output.append(text)

    def start_system(self):
        if not self.BOT_TOKEN or self.BOT_TOKEN == "your_telegram_bot_token_here":
            self.append_log("❌ Error: Please put your actual TELEGRAM_BOT_TOKEN in the .env file!")
            return
            
        if not self.GEMINI_KEY or self.GEMINI_KEY == "your_gemini_api_key_here":
            self.append_log("❌ Error: Please put your actual GEMINI_API_KEY in the .env file!")
            return

        self.append_log("🚀 Initializing Apex Architecture...")
        
        # Engines are now started inside bot_thread.py (to attach to the correct asyncio event loop)
            
        self.ai_engine = AIInvestmentEngine(api_key=self.GEMINI_KEY)
        
        # Run Telegram Bot on a separate Thread
        self.bot_thread = TelegramBotThread(self.BOT_TOKEN, self.ai_engine)
        self.bot_thread.log_signal.connect(self.append_log)
        self.bot_thread.start()

        self.status_label.setText("System Status: Fully Operational 🟢 (Bot & AI Active)")
        self.status_label.setStyleSheet("font-size: 14px; font-weight: bold; color: green;")
        self.start_btn.setEnabled(False)

    def closeEvent(self, event):
        """Handle Window close (X button). Minimize to tray if not explicitly quitting."""
        if not self.is_quitting:
            event.ignore()
            self.hide()
            if self.tray_icon:
                try:
                    self.tray_icon.showMessage(
                        "Apex AI Bot",
                        "The system is still running in the background. Right-click the tray icon to quit.",
                        QSystemTrayIcon.Information,
                        2000
                    )
                except Exception:
                    pass
        else:
            if self.bot_thread and self.bot_thread.isRunning():
                self.append_log("⚠️ Shutting down system, please wait...")
                self.bot_thread.stop()
            event.accept()

class ApexVPSHeadlessEngine:
    def __init__(self):
        print("🚀 Initializing Apex Super AGI v9.8 (24/7 Pure Headless VPS Engine)...")
        db.init_db()
        import backup_manager
        backup_manager.perform_backup(is_boot=True)
        
        self.BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.GEMINI_KEY = os.getenv("GEMINI_API_KEY")
        
        if not self.BOT_TOKEN or self.BOT_TOKEN == "your_telegram_bot_token_here":
            print("❌ Error: Please put your actual TELEGRAM_BOT_TOKEN in the .env file!")
            sys.exit(1)
            
        if not self.GEMINI_KEY or self.GEMINI_KEY == "your_gemini_api_key_here":
            print("❌ Error: Please put your actual GEMINI_API_KEY in the .env file!")
            sys.exit(1)

        self.ai_engine = AIInvestmentEngine(api_key=self.GEMINI_KEY)
        self.bot_thread = TelegramBotThread(self.BOT_TOKEN, self.ai_engine)
        self.bot_thread.log_signal.connect(self.log_vps)
        self.bot_thread.start()
        print("🛡️ [24/7 VPS ENGINE] Telegram Bot & AGI Engines active and running 24/7!")

    def log_vps(self, text: str):
        print(text)

    def quit_app(self):
        print("🛑 Shutting down VPS Headless Engine cleanly...")
        if hasattr(self, 'bot_thread') and self.bot_thread and self.bot_thread.isRunning():
            self.bot_thread.stop()

if __name__ == "__main__":
    import signal

    is_cli_mode = ("--cli" in sys.argv or "--no-gui" in sys.argv or "--vps" in sys.argv or "--headless" in sys.argv or "-vps" in sys.argv)
    
    if is_cli_mode:
        print("🚀 Initializing Khmer Master Crypto / Apex TURBO AGI Engine v11.0 Super Brain Edition (24/7 Pure Python Headless CLI Mode)...")
        db.init_db()
        import backup_manager
        backup_manager.perform_backup(is_boot=True)
        
        bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        gemini_key = os.getenv("GEMINI_API_KEY")
        
        if not bot_token or bot_token == "your_telegram_bot_token_here":
            print("❌ Error: Please put your actual TELEGRAM_BOT_TOKEN in the .env file!")
            sys.exit(1)
            
        if not gemini_key or gemini_key == "your_gemini_api_key_here":
            print("❌ Error: Please put your actual GEMINI_API_KEY in the .env file!")
            sys.exit(1)

        from ai_engine import AIInvestmentEngine
        from bot_thread import TelegramBotThread
        
        ai_engine = AIInvestmentEngine(api_key=gemini_key)
        bot_service = TelegramBotThread(bot_token, ai_engine)
        
        def sigint_handler(signum, frame):
            print("\nCtrl+C detected! Shutting down system cleanly...")
            bot_service.stop()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, sigint_handler)
        
        print("🛡️ [24/7 VPS ENGINE] Telegram Bot & AGI Engines active and running 24/7 in Pure Python!")
        bot_service.run()
    else:
        try:
            from PyQt5.QtWidgets import QApplication
            from PyQt5.QtCore import QTimer
        except ImportError:
            print("❌ Error: PyQt5 is not installed. Run with --cli for Headless VPS Mode.")
            sys.exit(1)

        app = QApplication(sys.argv)
        app.setQuitOnLastWindowClosed(False)
        
        window = BotDashboard()
        
        def sigint_handler(signum, frame):
            print("\nCtrl+C detected! Shutting down system cleanly...")
            window.quit_app()
            QApplication.quit()
            
        signal.signal(signal.SIGINT, sigint_handler)
        
        timer = QTimer()
        timer.start(500)
        timer.timeout.connect(lambda: None)
        
        window.show()
        sys.exit(app.exec_())

