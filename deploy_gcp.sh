#!/bin/bash
# ==============================================================================
# 🚀 APEX AGI ENGINE v11.0 - GOOGLE CLOUD VPS AUTOMATED DEPLOYMENT SCRIPT
# Instance Target: Google Cloud Compute Engine e2-micro (1GB RAM, 30GB Disk, 24/7/365 Free)
# App Name: khmer-master-crypto-bot
# ==============================================================================

set -e

echo "🚀 Starting Khmer Master Crypto APEX AGI Engine v11.0 VPS Setup..."

# 1. Update OS Packages & Install Prerequisites
echo "📦 Updating OS packages and installing system tools..."
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip python3-venv git curl htop systemd

# 2. Configure 2GB Swapfile (Prevents OS RAM Spikes on 1GB VPS)
if [ ! -f /swapfile ]; then
    echo "🛡️ Setting up 2GB Swapfile for memory safety..."
    sudo fallocate -l 2G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=2048
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "✅ Swapfile enabled."
else
    echo "ℹ️ Swapfile already exists."
fi

# 3. Setup Project Workspace
APP_DIR="/opt/khmer-master-crypto-bot"
echo "📁 Setting up project directory at $APP_DIR..."

if [ ! -d "$APP_DIR" ]; then
    sudo git clone https://github.com/hemsoknitha-sketch/khmer-master-crypto-bot.git "$APP_DIR"
    sudo chown -R $USER:$USER "$APP_DIR"
else
    cd "$APP_DIR"
    git pull origin main || true
fi

cd "$APP_DIR"

# Navigate to inner bot folder if present
if [ -d "Khmer Master Crypto/Apex_AI_Bot" ]; then
    cd "Khmer Master Crypto/Apex_AI_Bot"
elif [ -d "Apex_AI_Bot" ]; then
    cd "Apex_AI_Bot"
fi

BOT_WORKING_DIR=$(pwd)
echo "📍 Working directory: $BOT_WORKING_DIR"

# 4. Setup Python Virtual Environment
echo "🐍 Creating Python Virtual Environment..."
export TMPDIR=/var/tmp
python3 -m venv venv
source venv/bin/activate
pip install --no-cache-dir --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install --no-cache-dir -r requirements.txt
    pip install --no-cache-dir aiohttp httpx
fi

# 5. Check .env File
if [ ! -f ".env" ]; then
    echo "⚠️ Warning: .env file not found. Creating template .env..."
    cat <<EOT > .env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
GEMINI_API_KEY=your_gemini_api_key_here
HF_SPACE_URL=https://khmer-master-crypto-bot.hf.space
EOT
    echo "❗ Please edit $BOT_WORKING_DIR/.env with your actual Telegram Token and API keys!"
fi

# 6. Configure Systemd 24/7 Daemon Service
SERVICE_FILE="/etc/systemd/system/khmer-master-crypto-bot.service"
echo "⚙️ Creating Systemd service at $SERVICE_FILE..."

sudo tee $SERVICE_FILE > /dev/null <<EOT
[Unit]
Description=Khmer Master Crypto APEX AGI Engine v11.0 Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BOT_WORKING_DIR
ExecStart=$BOT_WORKING_DIR/venv/bin/python main.py --cli
Restart=always
RestartSec=5
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOT

# 7. Enable and Start Service
echo "🚀 Enabling and starting khmer-master-crypto-bot service..."
sudo systemctl daemon-reload
sudo systemctl enable khmer-master-crypto-bot.service
sudo systemctl restart khmer-master-crypto-bot.service

echo ""
echo "========================================================================="
echo "🎉 DEPLOYMENT COMPLETE! APEX AGI ENGINE v11.0 IS NOW ACTIVE 24/7/365!"
echo "========================================================================="
echo "📊 Check Service Status: sudo systemctl status khmer-master-crypto-bot"
echo "📜 View Real-time Logs:   sudo journalctl -u khmer-master-crypto-bot -f"
echo "========================================================================="
