#!/bin/bash
# ==============================================================================
# ANGKOR QUANT - START AUTO YOUTUBE LIVE STREAM (24/7/365 HEADLESS PIPELINE)
# ==============================================================================
# Architecture:
#   1. Virtual Display: Xvfb :99 @ 1920x1080x24 in RAM
#   2. Audio Engine: PulseAudio sink_stream (Browser alerts + Ambient Lofi)
#   3. Web GUI Server: python gold_youtube_stream_server.py (Port 8000)
#   4. Browser: Chromium Kiosk Mode (1920x1080)
#   5. RTMP Encoder: FFmpeg (libx264 veryfast, zerolatency, 30fps)
#   6. CPU Pinning: taskset -c 2,3 (Preserving Cores 0 & 1 for HFT Engine)
# ==============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# 1. Load Stream Key from .env
if [ -f .env ]; then
    export $(grep -v '^#' .env | grep -E '^YOUTUBE_STREAM_KEY=' | xargs)
    export $(grep -v '^#' .env | grep -E '^YOUTUBE_WEB_PORT=' | xargs 2>/dev/null || true)
fi

PORT="${YOUTUBE_WEB_PORT:-8000}"

if [ -z "$YOUTUBE_STREAM_KEY" ] || [ "$YOUTUBE_STREAM_KEY" == "YOUR_YOUTUBE_STREAM_KEY_HERE" ]; then
    echo "❌ [ERROR] YOUTUBE_STREAM_KEY is not configured in .env!"
    echo "👉 Please set YOUTUBE_STREAM_KEY=xxxx-xxxx-xxxx-xxxx-xxxx in your .env file."
    exit 1
fi

# Detect Python interpreter (prefer virtualenv)
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

# Detect Chromium executable
if command -v chromium >/dev/null 2>&1; then
    CHROMIUM_BIN="$(command -v chromium)"
elif command -v chromium-browser >/dev/null 2>&1; then
    CHROMIUM_BIN="$(command -v chromium-browser)"
elif command -v google-chrome-stable >/dev/null 2>&1; then
    CHROMIUM_BIN="$(command -v google-chrome-stable)"
elif command -v google-chrome >/dev/null 2>&1; then
    CHROMIUM_BIN="$(command -v google-chrome)"
else
    CHROMIUM_BIN="chromium"
fi

echo "🚀 [ANGKOR QUANT] Launching YouTube Live 24/7 Engine..."
echo "🐍 Python Interpreter: $PYTHON_BIN"
echo "🌐 Chromium Executable: $CHROMIUM_BIN"
mkdir -p logs

# 2. Start PulseAudio Virtual Audio Bus
pulseaudio --start --exit-idle-time=-1 || true
if ! pactl list short sinks 2>/dev/null | grep -q "sink_stream"; then
    pactl load-module module-null-sink sink_name=sink_stream sink_properties=device.description=Virtual_Stream_Sink || true
    pactl set-default-sink sink_stream || true
fi

# 3. Start Xvfb Virtual Framebuffer (1920x1080 24-bit TrueColor) on Core 2,3
if ! pgrep -f "Xvfb :99" > /dev/null; then
    echo "🖥️ Starting Xvfb Virtual Display (:99)..."
    taskset -c 2,3 Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset > logs/xvfb.log 2>&1 &
    sleep 2
else
    echo "🖥️ Xvfb Virtual Display (:99) already running."
fi
export DISPLAY=:99

# 4. Start Gold M1 Stream Web Server
if ! pgrep -f "gold_youtube_stream_server.py" > /dev/null; then
    echo "📡 Starting Gold M1 Stream Server (Port $PORT)..."
    taskset -c 2,3 $PYTHON_BIN gold_youtube_stream_server.py > logs/stream_server.log 2>&1 &
    sleep 3
    if ! pgrep -f "gold_youtube_stream_server.py" > /dev/null; then
        echo "⚠️ Gold M1 Stream Server failed to stay alive! Inspecting logs/stream_server.log:"
        tail -n 15 logs/stream_server.log 2>/dev/null || true
    else
        echo "✅ Gold M1 Stream Server running on Port $PORT."
    fi
else
    echo "📡 Gold M1 Stream Server already running."
fi

# 5. Start Chromium in Kiosk Mode on :99
if ! pgrep -f "$CHROMIUM_BIN.*gold_live_view" > /dev/null && ! pgrep -f "chromium.*gold_live_view" > /dev/null; then
    echo "🌐 Starting Headless Chromium Kiosk on DISPLAY :99..."
    taskset -c 2,3 $CHROMIUM_BIN \
        --kiosk \
        --window-position=0,0 \
        --window-size=1920,1080 \
        --no-sandbox \
        --disable-infobars \
        --disable-notifications \
        --disable-session-crashed-bubble \
        --autoplay-policy=no-user-gesture-required \
        --disable-dev-shm-usage \
        --disable-gpu-sandbox \
        --hide-scrollbars \
        http://localhost:${PORT}/gold_live_view > logs/chromium.log 2>&1 &
    sleep 4
else
    echo "🌐 Chromium Kiosk already running."
fi

# 6. Check for Background Lofi Audio
AUDIO_INPUT="-f pulse -i sink_stream.monitor"
AMIX_FILTER=""
if [ -f "music/lofi_stream.mp3" ]; then
    echo "🎵 Background Lofi MP3 detected: music/lofi_stream.mp3"
    AUDIO_INPUT="-f pulse -i sink_stream.monitor -stream_loop -1 -i music/lofi_stream.mp3"
    AMIX_FILTER="-filter_complex [0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout] -map 0:v -map [aout]"
elif [ -f "audio/lofi_ambient.wav" ]; then
    echo "🎵 Ambient Drone Loop detected: audio/lofi_ambient.wav"
    AUDIO_INPUT="-f pulse -i sink_stream.monitor -stream_loop -1 -i audio/lofi_ambient.wav"
    AMIX_FILTER="-filter_complex [0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2[aout] -map 0:v -map [aout]"
fi

# 7. Start FFmpeg In-Memory RTMP Streamer to YouTube Live
echo "📡 Broadcasting In-Memory RTMP Stream to YouTube (Zero Disk Write)..."
echo "💡 Cores Pinned: taskset -c 2,3 (Zero HFT Engine Interference)"

if [ -n "$AMIX_FILTER" ]; then
    taskset -c 2,3 ffmpeg -hide_banner -loglevel warning \
        -f x11grab -draw_mouse 0 -framerate 30 -video_size 1920x1080 -i :99.0 \
        $AUDIO_INPUT \
        $AMIX_FILTER \
        -c:v libx264 -preset veryfast -tune zerolatency -b:v 2800k -maxrate 3200k -bufsize 6000k \
        -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -ar 44100 \
        -f flv "rtmp://a.rtmp.youtube.com/live2/${YOUTUBE_STREAM_KEY}"
else
    taskset -c 2,3 ffmpeg -hide_banner -loglevel warning \
        -f x11grab -draw_mouse 0 -framerate 30 -video_size 1920x1080 -i :99.0 \
        $AUDIO_INPUT \
        -c:v libx264 -preset veryfast -tune zerolatency -b:v 2800k -maxrate 3200k -bufsize 6000k \
        -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -ar 44100 \
        -f flv "rtmp://a.rtmp.youtube.com/live2/${YOUTUBE_STREAM_KEY}"
fi
