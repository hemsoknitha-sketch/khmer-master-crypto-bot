#!/bin/bash
# ==============================================================================
# 🚀 CLOUDFLARE HTTPS TUNNEL BACKGROUND SERVICE & AUTO-CONFIG ENGINE
# Khmer Master Crypto - Telegram Mini App & Web GUI 24/7 HTTPS Engine
# ==============================================================================

set -e

echo "🚀 [1/5] Installing & Verifying Cloudflare Tunnel..."

# Find cloudflared binary
BIN_PATH=$(which cloudflared || echo "/usr/local/bin/cloudflared")
if [ ! -f "$BIN_PATH" ] && [ -f "/usr/bin/cloudflared" ]; then
    BIN_PATH="/usr/bin/cloudflared"
fi

if [ ! -f "$BIN_PATH" ]; then
    echo "📦 Downloading cloudflared for Linux AMD64..."
    curl -L --output /tmp/cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb
    sudo dpkg -i /tmp/cloudflared.deb
    BIN_PATH=$(which cloudflared || echo "/usr/bin/cloudflared")
fi

echo "🛡️ [2/5] Configuring systemd service: cloudflared-tunnel.service..."
sudo tee /etc/systemd/system/cloudflared-tunnel.service > /dev/null << EOF
[Unit]
Description=Cloudflare HTTPS Tunnel for Khmer Master Crypto WebApp
After=network.target

[Service]
Type=simple
User=root
ExecStart=$BIN_PATH tunnel --url http://127.0.0.1:8080
Restart=always
RestartSec=5
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now cloudflared-tunnel.service
sudo systemctl restart cloudflared-tunnel.service

echo "⏳ [3/5] Waiting for Cloudflare HTTPS Tunnel to initialize..."
sleep 4

# Extract the https trycloudflare url from journalctl
TUNNEL_URL=""
for i in {1..10}; do
    TUNNEL_URL=$(sudo journalctl -u cloudflared-tunnel -n 40 --no-pager | grep -o 'https://[a-zA-Z0-9-]*\.trycloudflare\.com' | tail -n 1 || true)
    if [ -n "$TUNNEL_URL" ]; then
        break
    fi
    echo "   ... waiting for tunnel endpoint (attempt $i/10)"
    sleep 2
done

if [ -z "$TUNNEL_URL" ]; then
    echo "⚠️ Could not auto-detect trycloudflare URL. Please run:"
    echo "   sudo journalctl -u cloudflared-tunnel -n 30 --no-pager"
    exit 1
fi

echo "🌐 [4/5] Active Cloudflare HTTPS Tunnel URL:"
echo "   $TUNNEL_URL"

# Write to temporary file and local state file
echo "$TUNNEL_URL" | sudo tee /tmp/cloudflared_url.txt > /dev/null
echo "$TUNNEL_URL" | sudo tee /opt/khmer-master-crypto-bot/.cloudflare_tunnel_url > /dev/null
sudo chmod 666 /tmp/cloudflared_url.txt /opt/khmer-master-crypto-bot/.cloudflare_tunnel_url 2>/dev/null || true

# Update .env file if it exists
ENV_FILE="/opt/khmer-master-crypto-bot/.env"
if [ -f "$ENV_FILE" ]; then
    echo "⚙️ [5/5] Updating $ENV_FILE and restarting bot..."
    if grep -q "TELEGRAM_MINI_APP_URL=" "$ENV_FILE"; then
        sudo sed -i "s|TELEGRAM_MINI_APP_URL=.*|TELEGRAM_MINI_APP_URL=$TUNNEL_URL|g" "$ENV_FILE"
    else
        echo "TELEGRAM_MINI_APP_URL=$TUNNEL_URL" | sudo tee -a "$ENV_FILE" > /dev/null
    fi
    
    # Restart bot so it immediately detects the new HTTPS URL
    sudo systemctl restart khmer-master-crypto-bot
    echo "✅ Bot service restarted with live HTTPS WebApp URL!"
fi

echo ""
echo "================================================================================"
echo "🎉 SUCCESS! TELEGRAM MINI APP IS NOW LIVE ON HTTPS!"
echo "🔗 WebApp HTTPS URL: $TUNNEL_URL"
echo "👉 Go to Telegram and type /webapp to open the Cyberpunk Mini App Dashboard!"
echo "================================================================================"
