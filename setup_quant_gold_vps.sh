#!/bin/bash
# ==============================================================================
# 🚀 ANGKOR QUANT - QUANT GOLD GOOGLE CLOUD LINUX VPS INSTALLER & SERVICE SETUP
# Target: Google Cloud Linux VPS 'quant-gold' (us-central1-a, quant-gold-514007)
# Free 24/7/365 High-Performance Execution & Automated Systemd Daemon
# ==============================================================================

set -e

# Disable job control messages
set +m 2>/dev/null || true

echo "=========================================================================="
echo "  🥇 ANGKOR QUANT - QUANT GOLD VPS INSTALLER (GOOGLE CLOUD 'quant-gold')"
echo "=========================================================================="

APP_DIR="/opt/khmer-master-crypto-bot"
CURRENT_USER=$(whoami)

# 1. Ensure target directory exists
if [ ! -d "$APP_DIR" ]; then
    echo "📁 Creating application directory: $APP_DIR..."
    sudo mkdir -p "$APP_DIR"
    sudo chown -R "$CURRENT_USER:$CURRENT_USER" "$APP_DIR"
    cd "$APP_DIR"
    if [ ! -d ".git" ]; then
        echo "📥 Cloning latest repository from GitHub..."
        git clone https://github.com/hemsoknitha-sketch/khmer-master-crypto-bot.git .
    fi
else
    cd "$APP_DIR"
fi

sudo chown -R "$CURRENT_USER:$CURRENT_USER" "$APP_DIR" 2>/dev/null || true

# 2. System Packages & Python 3 Prerequisites
echo "📦 [1/6] Installing Essential Linux Packages..."
if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update -qq || true
    sudo apt-get install -y -qq python3 python3-pip python3-venv git curl htop jq build-essential || true
fi

# 3. Memory Optimization (Swapfile creation if < 2GB swap)
echo "💾 [2/6] Checking Linux Virtual Memory & Swapfile..."
SWAP_EXISTS=$(free -m | awk '/Swap/ {print $2}')
if [ "$SWAP_EXISTS" -lt 1024 ]; then
    echo "⚙️ Creating 2GB emergency Swapfile to prevent OOM memory crashes..."
    sudo fallocate -l 2G /swapfile 2>/dev/null || sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile 2>/dev/null || true
    if ! grep -q "/swapfile" /etc/fstab; then
        echo "/swapfile none swap sw 0 0" | sudo tee -a /etc/fstab >/dev/null
    fi
    echo "✅ 2GB Swapfile activated successfully."
else
    echo "✅ Adequate Swap already active: ${SWAP_EXISTS}MB."
fi

# 4. Python Virtual Environment Setup
echo "🐍 [3/6] Configuring Python Virtual Environment (venv)..."
if [ ! -f "$APP_DIR/.env" ]; then
    if [ -f "$APP_DIR/Quant Gold/.env.example" ]; then
        cp "$APP_DIR/Quant Gold/.env.example" "$APP_DIR/.env"
        echo "📝 [ENV] Initialized .env from Quant Gold/.env.example."
    elif [ -f "$APP_DIR/.env.example" ]; then
        cp "$APP_DIR/.env.example" "$APP_DIR/.env"
        echo "📝 [ENV] Initialized .env from .env.example."
    fi
fi
if [ ! -d "$APP_DIR/venv" ]; then
    python3 -m venv "$APP_DIR/venv"
fi
PYTHON_BIN="$APP_DIR/venv/bin/python"
PIP_BIN="$APP_DIR/venv/bin/pip"

"$PIP_BIN" install --upgrade pip setuptools wheel -q

# 5. Install Dependencies for Quant Gold and Angkor Quant
echo "📚 [4/6] Installing Quant Gold & Institutional Requirements..."
if [ -f "$APP_DIR/Quant Gold/requirements.txt" ]; then
    "$PIP_BIN" install -r "$APP_DIR/Quant Gold/requirements.txt" -q
fi
if [ -f "$APP_DIR/requirements.txt" ]; then
    "$PIP_BIN" install -r "$APP_DIR/requirements.txt" -q
fi
echo "✅ Python dependencies installed successfully."

# 6. Configure Systemd 24/7 Services
echo "⚙️ [5/6] Configuring Systemd 24/7 Services..."
SERVICE_QG="/etc/systemd/system/quant-gold.service"

sudo tee "$SERVICE_QG" > /dev/null <<EOF
[Unit]
Description=Angkor Quant - Quant Gold 24/7/365 Autonomous AI Trading Daemon
After=network.target network-online.target
Wants=network-online.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$APP_DIR
ExecStart=$PYTHON_BIN run_quant_gold.py
Restart=always
RestartSec=5
SuccessExitStatus=0
Environment=PYTHONUNBUFFERED=1
StandardOutput=journal
StandardError=journal
SyslogIdentifier=quant-gold
LimitNOFILE=65535
TimeoutStopSec=15
KillMode=mixed

[Install]
WantedBy=multi-user.target
EOF

# Reload and Enable Services
sudo systemctl daemon-reload
sudo systemctl enable quant-gold.service
sudo systemctl restart quant-gold.service || true

# 7. Configure 2-Minute Auto-Update Cron Job
echo "⏰ [6/6] Configuring 2-Minute Zero-Downtime Auto-Update Cron..."
chmod +x "$APP_DIR/auto_update_vps.sh" 2>/dev/null || true
(crontab -l 2>/dev/null | grep -v "auto_update_vps.sh" ; echo "*/2 * * * * cd $APP_DIR && bash auto_update_vps.sh > /dev/null 2>&1") | crontab -

echo ""
echo "=========================================================================="
echo "  🎉 SUCCESS! QUANT GOLD IS NOW RUNNING 24/7/365 ON GOOGLE CLOUD VPS!"
echo "=========================================================================="
echo "  Manage Quant Gold Daemon:"
echo "    👉 Check Status:   sudo systemctl status quant-gold.service"
echo "    👉 View Live Logs: journalctl -u quant-gold.service -n 50 -f"
echo "    👉 Restart Daemon: sudo systemctl restart quant-gold.service"
echo "    👉 Stop Daemon:    sudo systemctl stop quant-gold.service"
echo "=========================================================================="

