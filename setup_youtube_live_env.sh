#!/bin/bash
# ==============================================================================
# ANGKOR QUANT - SETUP AUTO YOUTUBE LIVE STREAMING ENVIRONMENT (UBUNTU / DEBIAN)
# ==============================================================================
# Installs headless display (Xvfb), audio subsystem (PulseAudio), Chromium browser,
# FFmpeg with H.264 / AAC codecs, and generates studio audio chime assets.
# Auto-detects Debian vs Ubuntu package naming and active Python virtualenv.
# ==============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=========================================================="
echo "🚀 [ANGKOR QUANT] Starting YouTube Live 24/7 Setup..."
echo "=========================================================="

# 1. Update Package Repository
echo "📦 Updating apt packages..."
sudo apt-get update -y || true

# 2. Install Core Headless Packages & FFmpeg
echo "📦 Installing Xvfb, FFmpeg, PulseAudio and System Fonts..."
sudo apt-get install -y \
    xvfb \
    ffmpeg \
    pulseaudio \
    pulseaudio-utils \
    alsa-utils \
    fonts-liberation \
    fonts-noto \
    fonts-noto-color-emoji \
    fonts-roboto \
    socat \
    procps \
    curl \
    wget

# 3. Install Chromium (Debian uses 'chromium', Ubuntu uses 'chromium-browser' or 'chromium')
echo "📦 Installing Chromium browser..."
if apt-cache show chromium >/dev/null 2>&1; then
    sudo apt-get install -y chromium || true
elif apt-cache show chromium-browser >/dev/null 2>&1; then
    sudo apt-get install -y chromium-browser || true
fi

# 4. Detect Python Interpreter (prefer virtualenv)
if [ -f "$SCRIPT_DIR/venv/bin/python3" ]; then
    PYTHON_BIN="$SCRIPT_DIR/venv/bin/python3"
elif [ -f "$SCRIPT_DIR/venv/bin/python" ]; then
    PYTHON_BIN="$SCRIPT_DIR/venv/bin/python"
elif [ -f "/opt/khmer-master-crypto-bot/venv/bin/python3" ]; then
    PYTHON_BIN="/opt/khmer-master-crypto-bot/venv/bin/python3"
elif command -v python3 >/dev/null 2>&1; then
    PYTHON_BIN="$(command -v python3)"
else
    PYTHON_BIN="python3"
fi
echo "🐍 Detected Python Interpreter: $PYTHON_BIN"

# 4.1 Ensure edge-tts and gTTS are installed for AI Girl MC Confident Neural Voice
echo "🎙️ Verifying Edge-TTS and gTTS Neural Voice Engines..."
$PYTHON_BIN -m pip install edge-tts gtts --quiet || true

# 5. Configure PulseAudio Virtual Null Sink (Zero-Hardware Audio Bus)
echo "🎵 Configuring PulseAudio virtual null sink..."
mkdir -p ~/.config/pulse
pulseaudio --start --exit-idle-time=-1 || true

if ! pactl list short sinks 2>/dev/null | grep -q "sink_stream"; then
    echo "🔊 Loading module-null-sink (sink_name=sink_stream)..."
    pactl load-module module-null-sink sink_name=sink_stream sink_properties=device.description=Virtual_Stream_Sink || true
    pactl set-default-sink sink_stream || true
    echo "✅ PulseAudio sink_stream successfully activated!"
fi

# 6. Generate Studio-Grade Audio Chime Assets
echo "🎵 Generating institutional audio alert assets..."
$PYTHON_BIN generate_stream_audio.py

# 7. Create Runtime Directories
mkdir -p logs
mkdir -p music
mkdir -p audio

# 8. Auto-Configure Systemd Service with Current User & Directory
CURRENT_USER=$(whoami)
APP_DIR="$SCRIPT_DIR"
SERVICE_FILE="/etc/systemd/system/angkor-gold-youtube-live.service"

echo "⚙️ Configuring Systemd 24/7 service at $SERVICE_FILE..."
sudo tee "$SERVICE_FILE" > /dev/null <<EOF
[Unit]
Description=Angkor Quant - Auto YouTube Live Stream 24/7 (Gold M5 Sniper Scalping & AI Elena)
After=network.target sound.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$APP_DIR
EnvironmentFile=-$APP_DIR/.env
Environment=PYTHONIOENCODING=utf-8
Environment=LC_ALL=C.UTF-8
Environment=LANG=C.UTF-8
ExecStart=/bin/bash $APP_DIR/start_youtube_stream.sh
ExecStop=/bin/bash $APP_DIR/stop_youtube_stream.sh
Restart=always
RestartSec=10

# CPU Affinity: Strictly Pin to Core 2 and 3 (Leaves Core 0 & 1 for HFT Bot)
CPUAffinity=2 3

# Scheduling Priority: Low priority (Nice=10) so Trading Bot always takes precedence
Nice=10

# OOM Protection: Sacrifice Streamer first before touching Trading Bot
OOMScoreAdjust=500

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
echo "✅ Systemd service updated and reloaded successfully!"

echo "=========================================================="
echo "✅ [ANGKOR QUANT] Environment Setup Completed Successfully!"
echo "👉 You can now run: sudo systemctl restart angkor-gold-youtube-live"
echo "=========================================================="
