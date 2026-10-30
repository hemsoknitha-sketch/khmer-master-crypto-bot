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

# Ensure UTF-8 across all subshells & background python processes
export PYTHONIOENCODING=utf-8
export PYTHONUNBUFFERED=1
export LC_ALL=C.UTF-8
export LANG=C.UTF-8

# 1. Load Stream Key from .env safely (strip CRLF \r, quotes, whitespace)
if [ -f .env ]; then
    RAW_KEY=$(grep -E '^YOUTUBE_STREAM_KEY=' .env | cut -d'=' -f2- | tr -d '\r"' | tr -d "'" | xargs)
    if [ -n "$RAW_KEY" ]; then
        export YOUTUBE_STREAM_KEY="$RAW_KEY"
    fi
    RAW_URL=$(grep -E '^YOUTUBE_STREAM_URL=' .env | cut -d'=' -f2- | tr -d '\r"' | tr -d "'" | xargs 2>/dev/null || true)
    if [ -n "$RAW_URL" ]; then
        export YOUTUBE_STREAM_URL="$RAW_URL"
    fi
    RAW_PORT=$(grep -E '^YOUTUBE_WEB_PORT=' .env | cut -d'=' -f2- | tr -d '\r"' | tr -d "'" | xargs 2>/dev/null || true)
    if [ -n "$RAW_PORT" ]; then
        export YOUTUBE_WEB_PORT="$RAW_PORT"
    fi
fi

PORT="${YOUTUBE_WEB_PORT:-8000}"
STREAM_URL="${YOUTUBE_STREAM_URL:-rtmp://a.rtmp.youtube.com/live2}"
# Convert rtmps:// to rtmp:// to avoid OpenSSL handshake drops with FLV muxer
if [[ "$STREAM_URL" == rtmps://* ]]; then
    STREAM_URL="rtmp://a.rtmp.youtube.com/live2"
fi
# Strip trailing slashes
STREAM_URL="${STREAM_URL%/}"

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
echo "📡 Target Stream URL: $STREAM_URL"
mkdir -p "$SCRIPT_DIR/logs"

# 2. Start PulseAudio Virtual Audio Bus
pulseaudio --start --exit-idle-time=-1 || true
if ! pactl list short sinks 2>/dev/null | grep -q "sink_stream"; then
    pactl load-module module-null-sink sink_name=sink_stream sink_properties=device.description=Virtual_Stream_Sink || true
    pactl set-default-sink sink_stream || true
fi

# 3. Start Xvfb Virtual Framebuffer (1920x1080 24-bit TrueColor) on Core 2,3
if ! pgrep -f "Xvfb :99" > /dev/null; then
    echo "🖥️ Starting Xvfb Virtual Display (:99)..."
    # Clean up any stale X11 lock files from killed sessions
    rm -f /tmp/.X99-lock /tmp/.X11-unix/X99 2>/dev/null || true
    taskset -c 2,3 Xvfb :99 -screen 0 1920x1080x24 -ac +extension GLX +render -noreset > "$SCRIPT_DIR/logs/xvfb.log" 2>&1 &
    sleep 1
else
    echo "🖥️ Xvfb Virtual Display (:99) already running."
fi
export DISPLAY=:99

# 4. Start Gold M1 Stream Web Server (Unbuffered output)
if ! pgrep -f "gold_youtube_stream_server.py" > /dev/null; then
    echo "📡 Starting Gold M1 Stream Server (Port $PORT)..."
    # Ensure port is released from any zombie process
    fuser -k ${PORT}/tcp 2>/dev/null || true
    pkill -f "gold_youtube_stream_server.py" 2>/dev/null || true
    taskset -c 2,3 $PYTHON_BIN -u "$SCRIPT_DIR/gold_youtube_stream_server.py" > "$SCRIPT_DIR/logs/stream_server.log" 2>&1 &
    
    # Wait up to 5s for server health endpoint to come up
    for i in {1..5}; do
        if curl -s "http://localhost:${PORT}/api/health" | grep -q "ok"; then
            echo "✅ Gold M1 Stream Server active and verified on Port $PORT."
            break
        fi
        sleep 0.5
    done

    if ! pgrep -f "gold_youtube_stream_server.py" > /dev/null; then
        echo "⚠️ Gold M1 Stream Server failed to stay alive! Inspecting logs/stream_server.log:"
        tail -n 15 "$SCRIPT_DIR/logs/stream_server.log" 2>/dev/null || true
    fi
else
    echo "📡 Gold M1 Stream Server already running."
fi

# 5. Start Chromium in Kiosk Mode on :99
if ! pgrep -f "$CHROMIUM_BIN.*gold_live_view" > /dev/null && ! pgrep -f "chromium.*gold_live_view" > /dev/null; then
    echo "🌐 Starting Headless Chromium Kiosk on DISPLAY :99..."
    # Purge stale chromium singleton locks
    rm -rf /tmp/chromium-stream-profile/Singleton* 2>/dev/null || true
    taskset -c 2,3 $CHROMIUM_BIN \
        --user-data-dir=/tmp/chromium-stream-profile \
        --display=:99 \
        --ozone-platform=x11 \
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
        http://localhost:${PORT}/gold_live_view > "$SCRIPT_DIR/logs/chromium.log" 2>&1 &
    sleep 2
else
    echo "🌐 Chromium Kiosk already running."
fi

# 6. Audio Routing: Combine PulseAudio Alerts & Ambient Sound
PULSE_AVAILABLE=false
if pactl list short sources 2>/dev/null | grep -q "sink_stream.monitor"; then
    PULSE_AVAILABLE=true
fi

if [ -f "music/lofi_stream.mp3" ]; then
    LOFI_FILE="music/lofi_stream.mp3"
elif [ -f "audio/lofi_ambient.wav" ]; then
    LOFI_FILE="audio/lofi_ambient.wav"
else
    LOFI_FILE=""
fi

if [ "$PULSE_AVAILABLE" = true ] && [ -n "$LOFI_FILE" ]; then
    echo "🎵 Mixed Audio Mode: PulseAudio alerts + ambient soundtrack ($LOFI_FILE)"
    AUDIO_INPUT="-f pulse -i sink_stream.monitor -stream_loop -1 -i $LOFI_FILE"
    AUDIO_MAP="-filter_complex [1:a]aformat=channel_layouts=stereo:sample_rates=44100,volume=1.0[a1];[2:a]aformat=channel_layouts=stereo:sample_rates=44100,volume=0.35[a2];[a1][a2]amix=inputs=2:duration=first:dropout_transition=2[aout] -map 0:v -map [aout]"
elif [ "$PULSE_AVAILABLE" = true ]; then
    echo "🎵 PulseAudio Monitor Only Mode"
    AUDIO_INPUT="-f pulse -i sink_stream.monitor"
    AUDIO_MAP="-map 0:v -map 1:a"
elif [ -n "$LOFI_FILE" ]; then
    echo "🎵 Ambient Soundtrack Only Mode ($LOFI_FILE)"
    AUDIO_INPUT="-stream_loop -1 -i $LOFI_FILE"
    AUDIO_MAP="-map 0:v -map 1:a"
else
    echo "🔇 Fallback Silent Audio Mode"
    AUDIO_INPUT="-f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100"
    AUDIO_MAP="-map 0:v -map 1:a"
fi

# 7. Start FFmpeg In-Memory RTMP Streamer to YouTube Live
echo "📡 Broadcasting In-Memory RTMP Stream to YouTube (Zero Disk Write)..."
echo "💡 Cores Pinned: taskset -c 2,3 (Zero HFT Engine Interference)"

taskset -c 2,3 ffmpeg -hide_banner -loglevel info -stats \
    -f x11grab -draw_mouse 0 -framerate 30 -video_size 1920x1080 -i :99.0 \
    $AUDIO_INPUT \
    $AUDIO_MAP \
    -c:v libx264 -preset veryfast -tune zerolatency -b:v 2800k -maxrate 3200k -bufsize 6000k \
    -pix_fmt yuv420p -g 60 -c:a aac -b:a 128k -ar 44100 \
    -flvflags no_duration_filesize \
    -f flv "${STREAM_URL}/${YOUTUBE_STREAM_KEY}" > "$SCRIPT_DIR/logs/ffmpeg.log" 2>&1

EXIT_CODE=$?
echo "⚠️ [FFMPEG EXITED] Return code: $EXIT_CODE"
if [ -f "$SCRIPT_DIR/logs/ffmpeg.log" ]; then
    echo "📄 Last 10 lines of logs/ffmpeg.log:"
    tail -n 10 "$SCRIPT_DIR/logs/ffmpeg.log"
fi
exit $EXIT_CODE
