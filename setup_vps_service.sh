#!/bin/bash
# ==============================================================================
# 🚀 KHMER MASTER CRYPTO - SYSTEMD 24/7 SERVICE INSTALLER & REPAIR TOOL
# Configures systemd daemon for both 'khmer-master-crypto-bot' and 'khmer-crypto-bot'
# ==============================================================================

set -e

APP_DIR="/opt/khmer-master-crypto-bot"
if [ ! -d "$APP_DIR" ]; then
    APP_DIR="$(pwd)"
fi

cd "$APP_DIR"

# 1. Detect Python executable
if [ -f "$APP_DIR/venv/bin/python" ]; then
    PYTHON_BIN="$APP_DIR/venv/bin/python"
elif [ -f "$APP_DIR/venv/bin/python3" ]; then
    PYTHON_BIN="$APP_DIR/venv/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
else
    PYTHON_BIN="/usr/bin/python3"
fi

CURRENT_USER=$(whoami)
SERVICE_PRIMARY="/etc/systemd/system/khmer-master-crypto-bot.service"
SERVICE_ALIAS="/etc/systemd/system/khmer-crypto-bot.service"

echo "⚙️ Configuring Systemd 24/7 service for user: $CURRENT_USER..."
echo "📍 Working Directory: $APP_DIR"
echo "🐍 Python Interpreter: $PYTHON_BIN"

# 2. Write Primary Service File (/etc/systemd/system/khmer-master-crypto-bot.service)
sudo tee "$SERVICE_PRIMARY" > /dev/null <<EOF
[Unit]
Description=Khmer Master Crypto APEX AGI Engine v13.00 Service
After=network.target
Wants=network-online.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_BIN main.py --cli
Restart=always
RestartSec=5
SuccessExitStatus=0
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
Alias=khmer-crypto-bot.service
EOF

# 3. Create Fallback/Alias Service File (/etc/systemd/system/khmer-crypto-bot.service)
sudo tee "$SERVICE_ALIAS" > /dev/null <<EOF
[Unit]
Description=Khmer Master Crypto APEX AGI Engine (Alias Service)
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_BIN main.py --cli
Restart=always
RestartSec=5
SuccessExitStatus=0
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

# 4. Reload and Enable Both Services
echo "🔄 Reloading systemd daemon..."
sudo systemctl daemon-reload

echo "✅ Enabling services on system boot..."
sudo systemctl enable khmer-master-crypto-bot.service
sudo systemctl enable khmer-crypto-bot.service

echo "🚀 Restarting bot service..."
sudo systemctl restart khmer-master-crypto-bot.service

echo ""
echo "========================================================================="
echo "🎉 SUCCESS! Service is installed, enabled, and running 24/7!"
echo "========================================================================="
echo "You can now control the bot using EITHER command:"
echo "  👉 sudo systemctl restart khmer-master-crypto-bot"
echo "  👉 sudo systemctl restart khmer-crypto-bot"
echo ""
echo "Check Status:"
echo "  👉 sudo systemctl status khmer-master-crypto-bot"
echo "========================================================================="
