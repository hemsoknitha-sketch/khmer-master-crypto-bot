#!/bin/bash
# ==============================================================================
# ANGKOR QUANT - STOP AUTO YOUTUBE LIVE STREAM
# ==============================================================================
echo "🛑 [ANGKOR QUANT] Stopping YouTube Live Stream..."

# Kill FFmpeg Streamer
pkill -f "ffmpeg.*x11grab.*rtmp" || true
# Kill Chromium Kiosk
pkill -f "chromium.*gold_live_view" || true
# Kill Stream Web Server
pkill -f "gold_youtube_stream_server.py" || true
fuser -k 8000/tcp 2>/dev/null || true
# Kill Xvfb :99
pkill -f "Xvfb :99" || true

echo "✅ All YouTube Live Stream processes cleanly stopped. (Trading Bot unaffected)"

