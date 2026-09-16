#!/bin/bash
# ==============================================================================
# 🚀 CLOUDFLARE HTTPS TUNNEL BACKGROUND SERVICE INSTALLER
# Khmer Master Crypto - Telegram Mini App & Web GUI 24/7 HTTPS Engine
# ==============================================================================

set -e

echo "🚀 Installing Cloudflare Tunnel 24/7 Background Systemd Service..."

# Find cloudflared binary
BIN_PATH=$(which cloudflared || echo "/usr/local/bin/cloudflared")
if [ ! -f "$BIN_PATH" ] && [ -f "/usr/bin/cloudflared" ]; then
    BIN_PATH="/usr/bin/cloudflared"
fi

if [ ! -f "$BIN_PATH" ]; then
    echo "📦 Downloading cloudflared..."
    curl -L --output /tmp/cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i /tmp/cloudflared.deb
    BIN_PATH=$(which cloudflared || echo "/usr/bin/cloudflared")
fi

echo "🛡️ Configuring systemd service: cloudflared-tunnel.service..."
sudo tee /etc/systemd/system/cloudflared-tunnel.service > /dev/null << EOF
[Unit]
Description=Cloudflare HTTPS Tunnel for Khmer Master Crypto WebApp
After=network.target

[Service]
Type=simple
User=root
ExecStart=$BIN_PATH tunnel --url http://localhost:8080
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now cloudflared-tunnel.service
echo "✅ Cloudflare Tunnel Background Service is now running 24/7!"
echo "🔍 To view tunnel live URL in logs, run:"
echo "   sudo journalctl -u cloudflared-tunnel -n 25 --no-pager"
