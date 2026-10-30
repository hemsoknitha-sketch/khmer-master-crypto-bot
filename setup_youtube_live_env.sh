#!/bin/bash
# ==============================================================================
# ANGKOR QUANT - SETUP AUTO YOUTUBE LIVE STREAMING ENVIRONMENT (UBUNTU / DEBIAN)
# ==============================================================================
# Installs headless display (Xvfb), audio subsystem (PulseAudio), Chromium browser,
# FFmpeg with H.264 / AAC codecs, and generates studio audio chime assets.
# ==============================================================================

set -e

echo "=========================================================="
echo "🚀 [ANGKOR QUANT] Starting YouTube Live 24/7 Setup..."
echo "=========================================================="

# 1. Update Package Repository
echo "📦 Updating apt packages..."
sudo apt-get update -y

# 2. Install Core Headless Packages & FFmpeg
echo "📦 Installing Xvfb, FFmpeg, PulseAudio, Chromium and Fonts..."
sudo apt-get install -y \
    xvfb \
    ffmpeg \
    pulseaudio \
    pulseaudio-utils \
    alsa-utils \
    chromium-browser \
    fonts-liberation \
    fonts-noto \
    fonts-noto-color-emoji \
    fonts-roboto \
    socat \
    procps \
    curl \
    wget

# 3. Configure PulseAudio Virtual Null Sink (Zero-Hardware Audio Bus)
echo "🎵 Configuring PulseAudio virtual null sink..."
mkdir -p ~/.config/pulse
pulseaudio --start --exit-idle-time=-1 || true

# Check if null-sink module is loaded; if not, load it
if ! pactl list short sinks | grep -q "sink_stream"; then
    echo "🔊 Loading module-null-sink (sink_name=sink_stream)..."
    pactl load-module module-null-sink sink_name=sink_stream sink_properties=device.description=Virtual_Stream_Sink || true
    pactl set-default-sink sink_stream || true
    echo "✅ PulseAudio sink_stream successfully activated!"
fi

# 4. Generate Studio-Grade Audio Chime Assets
echo "🎵 Generating institutional audio alert assets..."
python3 generate_stream_audio.py

# 5. Create Runtime Directories
mkdir -p logs
mkdir -p music
mkdir -p audio

echo "=========================================================="
echo "✅ [ANGKOR QUANT] Environment Setup Completed Successfully!"
echo "👉 Next step: Configure YOUTUBE_STREAM_KEY in .env and run ./start_youtube_stream.sh"
echo "=========================================================="

