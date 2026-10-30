#!/bin/bash
# ==============================================================================
# ANGKOR QUANT - STOP AUTO YOUTUBE LIVE STREAM
# ==============================================================================
echo "🛑 [ANGKOR QUANT] Stopping YouTube Live Stream..."

# Kill FFmpeg Streamer
pkill -9 -f "ffmpeg.*x11grab" 2>/dev/null || true
pkill -f "ffmpeg.*rtmp" 2>/dev/null || true

# Kill Chromium Kiosk & Purge Cache
pkill -9 -f "chromium.*gold_live_view" 2>/dev/null || true
pkill -9 -f "chrome.*gold_live_view" 2>/dev/null || true
rm -rf /tmp/chromium-stream-profile/Singleton* /tmp/chromium-stream-profile/Default/Cache* /tmp/chromium-stream-profile/Default/Code\ Cache* 2>/dev/null || true

# Kill Stream Web Server
pkill -9 -f "gold_youtube_stream_server.py" 2>/dev/null || true
fuser -k 8000/tcp 2>/dev/null || true

# Kill Xvfb :99 and remove stale X11 lock files
pkill -9 -f "Xvfb :99" 2>/dev/null || true
rm -f /tmp/.X99-lock /tmp/.X11-unix/X99 2>/dev/null || true

echo "✅ All YouTube Live Stream processes cleanly stopped & locks purged. (Trading Bot unaffected)"

