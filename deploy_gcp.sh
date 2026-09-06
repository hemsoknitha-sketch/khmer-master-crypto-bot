#!/bin/bash
# ==============================================================================
# 🚀 APEX AGI ENGINE v13.00 - GOOGLE CLOUD VPS AUTOMATED DEPLOYMENT SCRIPT
# Instance Target: Google Cloud Compute Engine e2-micro (1GB RAM, 30GB Disk, 24/7/365 Free)
# App Name: khmer-master-crypto-bot
# ==============================================================================

set -e

echo "🚀 Starting Khmer Master Crypto APEX AGI Engine v13.00 VPS Setup..."

# 1. Update OS Packages & Install Prerequisites
echo "📦 Updating OS packages and installing system tools..."
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y python3 python3-pip python3-venv git curl htop systemd cloud-guest-utils
sudo growpart /dev/sda 1 2>/dev/null || sudo growpart /dev/vda 1 2>/dev/null || true
sudo resize2fs /dev/sda1 2>/dev/null || sudo resize2fs /dev/vda1 2>/dev/null || true

# 2. Configure 4GB High-Speed SSD Swapfile & Linux Kernel Memory Tuning
echo "🛡️ Setting up 4GB Swapfile & Zero-OOM Shield for 6.5GB Effective RAM..."
if [ ! -f /swapfile ] || [ $(stat -c%s /swapfile 2>/dev/null || echo 0) -lt 3000000000 ]; then
    sudo swapoff -a 2>/dev/null || true
    sudo rm -f /swapfile
    sudo fallocate -l 4G /swapfile || sudo dd if=/dev/zero of=/swapfile bs=1M count=4096 status=none
    sudo chmod 600 /swapfile
    sudo mkswap /swapfile
    sudo swapon /swapfile
    sudo sed -i '/\/swapfile/d' /etc/fstab
    echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
    echo "✅ 4GB Swapfile configured successfully."
else
    echo "ℹ️ 4GB Swapfile already active."
fi

# Kernel memory optimization
sudo tee /etc/sysctl.d/99-apex-vps-memory.conf > /dev/null << 'EOF'
vm.swappiness=60
vm.vfs_cache_pressure=50
vm.dirty_background_ratio=5
vm.dirty_ratio=10
vm.overcommit_memory=1
EOF
sudo sysctl -p /etc/sysctl.d/99-apex-vps-memory.conf > /dev/null 2>&1 || true

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
    pip install --no-cache-dir aiohttp httpx huggingface_hub python-dotenv
fi

# 5. Check .env File & Pre-configure Hedge Fund Parameters
if [ ! -f ".env" ]; then
    echo "⚙️ Initializing Institutional .env configuration..."
    cat <<EOT > .env
# 1. Telegram Bot Token
TELEGRAM_BOT_TOKEN=YOUR_TELEGRAM_BOT_TOKEN_HERE

# 2. Gemini API Key
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE

# 3. Master Key for API Security
MASTER_KEY=YOUR_MASTER_KEY_HERE

# 4. Paper Trading Flag (False = Real Capital Trading)
PAPER_TRADING=False

# 5. Hugging Face Institutional Model Hub Config
HF_TOKEN=YOUR_HF_TOKEN_HERE
HF_MODEL_REPO=hemsinath/apex-ai-brain-models
HF_SPACE_URL=https://hemsinath-khmer-master-crypto-bot.hf.space
EOT
fi

# 6. Synchronize All 25 Institutional AI Models from Hugging Face Hub
echo "🧠 Synchronizing all 25 Institutional AI Brain Models from Hugging Face..."
python sync_local_models.py || true

# 7. Run Pre-Flight System Audit (Zero Technical Negligence Verification)
echo "🛡️ Running Institutional Pre-Flight Audit..."
python audit_system.py || true

chmod +x "$BOT_WORKING_DIR/auto_update_vps.sh" 2>/dev/null || true

# 8. Configure Systemd 24/7 Daemon Service
SERVICE_FILE="/etc/systemd/system/khmer-master-crypto-bot.service"
echo "⚙️ Creating Systemd service at $SERVICE_FILE..."

sudo tee $SERVICE_FILE > /dev/null <<EOT
[Unit]
Description=Khmer Master Crypto APEX AGI Engine v13.00 Service
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$BOT_WORKING_DIR
ExecStart=$BOT_WORKING_DIR/venv/bin/python main.py --cli
Restart=on-failure
RestartSec=5
SuccessExitStatus=0
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOT

# 7. Enable and Start Service & Auto-Update Cron
echo "🚀 Enabling and starting khmer-master-crypto-bot service..."
sudo systemctl daemon-reload
sudo systemctl enable khmer-master-crypto-bot.service
sudo systemctl restart khmer-master-crypto-bot.service

# 8. Setup Auto-Sync Cron Job (Checks GitHub & HF every 5 minutes)
echo "⏰ Setting up 5-minute Auto-Update Cron Job for GitHub & Hugging Face..."
(crontab -l 2>/dev/null | grep -v "auto_update_vps.sh" ; echo "*/5 * * * * bash $BOT_WORKING_DIR/auto_update_vps.sh > /dev/null 2>&1") | crontab -

echo ""
echo "========================================================================="
echo "🎉 DEPLOYMENT COMPLETE! APEX AGI ENGINE v13.00 IS NOW ACTIVE 24/7/365!"
echo "========================================================================="
echo "📊 Check Service Status: sudo systemctl status khmer-master-crypto-bot"
echo "📜 View Real-time Logs:   sudo journalctl -u khmer-master-crypto-bot -f"
echo "🔄 Auto-Update Script:   bash $BOT_WORKING_DIR/auto_update_vps.sh"
echo "========================================================================="

