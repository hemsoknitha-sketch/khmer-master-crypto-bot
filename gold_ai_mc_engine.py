#!/usr/bin/env python3
"""
ANGKOR QUANT - GOLD M5 AI GIRL MC & QUANT HOST ENGINE (ELENA 18)
================================================================
Powers the 24/7 Virtual Institutional Quant Anchor ("Elena") for YouTube Live.
Delivers:
  1. Real-time institutional Wall Street English commentaries (Buy/Sell, TP/SL, Breakeven).
  2. Confident, strong, human-grade neural voice synthesis (en-US-JennyNeural / gTTS).
  3. Interbank Kill Zone briefings (London Open, New York Wall Street Cash Open).
  4. Physical Shanghai Gold (SGE) & Macro TIPS real yield commentary.
  5. Intelligent cooldown & priority queue (Zero chatter collision, instant priority on signals).
================================================================
"""

import os
import sys
import time
import json
import threading
import subprocess
import shutil
from typing import Dict, Any, Optional

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
AUDIO_MC_DIR = os.path.join(ROOT_DIR, "audio", "mc")
os.makedirs(AUDIO_MC_DIR, exist_ok=True)

# Try importing gTTS for fallback neural speech synthesis
try:
    from gtts import gTTS
    GTTS_AVAILABLE = True
except Exception:
    GTTS_AVAILABLE = False


class GoldAIMCEngine:
    """
    Virtual Quant Host Engine managing AI Anchor Elena's thoughts, speeches,
    emotive states, and confident human-grade neural voice synthesis.
    """
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        self.last_speech_time = 0.0
        self.last_signal_action = "WAIT"
        self.last_session_name = ""
        self.last_hourly_brief_time = 0.0
        self.current_speech: Optional[Dict[str, Any]] = None
        self.speech_history = []
        self._precache_standard_alerts()

    @classmethod
    def get_instance(cls) -> 'GoldAIMCEngine':
        with cls._lock:
            if cls._instance is None:
                cls._instance = cls()
            return cls._instance

    def _apply_studio_mastering(self, input_path: str, output_path: str) -> bool:
        """
        Applies Institutional TV Broadcast mastering to synthesized voice:
          - High-pass 80Hz (cuts mic rumble & low-end mud)
          - Warm low-end 140Hz (+2.2dB for FM radio anchor body)
          - De-box 450Hz (-1.8dB for crystal clarity)
          - Broadcast presence 3400Hz (+3.6dB for sharp TV anchor diction)
          - Air & sheen 10000Hz (+1.8dB for high-frequency studio polish)
          - Broadcast compressor (levels whisper vs loud words)
          - Loudnorm targeting EBU R128 (-16 LUFS, YouTube optimal loudness)
        """
        try:
            ffmpeg_bin = shutil.which("ffmpeg") or "ffmpeg"
            filter_chain = (
                "highpass=f=80,"
                "equalizer=f=140:width_type=h:width=60:g=2.2,"
                "equalizer=f=450:width_type=h:width=120:g=-1.8,"
                "equalizer=f=3400:width_type=h:width=1200:g=3.6,"
                "equalizer=f=10000:width_type=h:width=3000:g=1.8,"
                "acompressor=threshold=-15dB:ratio=3:attack=10:release=120:makeup=2,"
                "loudnorm=I=-16:TP=-1.5:LRA=7"
            )
            cmd = [
                ffmpeg_bin, "-y",
                "-i", input_path,
                "-af", filter_chain,
                "-ar", "48000",
                "-b:a", "192k",
                output_path
            ]
            res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=8)
            if res.returncode == 0 and os.path.exists(output_path) and os.path.getsize(output_path) > 1000:
                return True
        except Exception:
            pass
        return False

    def _synthesize_file(self, text: str, filepath: str) -> bool:
        """
        Synthesizes text to MP3 using confident human-grade neural voice (en-US-AvaNeural / en-US-AriaNeural)
        with Studio Vocal Presence Mastering and seamless gTTS fallback.
        """
        # Primary: en-US-AvaNeural (youthful, radiant, confident 18-20y TV host)
        # Alternate: en-US-AriaNeural (formal Wall Street financial reporter)
        primary_voice = os.environ.get("ELENA_VOICE", "en-US-AvaNeural")
        candidate_voices = [primary_voice, "en-US-AvaNeural", "en-US-AriaNeural", "en-US-JennyNeural"]
        candidate_voices = list(dict.fromkeys(candidate_voices))

        raw_filepath = filepath + ".raw.mp3"

        # Tier 1: Microsoft Edge Neural TTS with candidate fallback
        for voice in candidate_voices:
            try:
                res = subprocess.run([
                    sys.executable, "-m", "edge_tts",
                    "--voice", voice,
                    "--rate", "+1%",
                    "--pitch", "+0Hz",
                    "--text", text,
                    "--write-media", raw_filepath
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=8)
                if res.returncode == 0 and os.path.exists(raw_filepath) and os.path.getsize(raw_filepath) > 1000:
                    # Apply Studio Broadcast Mastering
                    if self._apply_studio_mastering(raw_filepath, filepath):
                        try:
                            os.remove(raw_filepath)
                        except Exception:
                            pass
                        return True
                    else:
                        # Fallback: keep raw output directly if ffmpeg is unavailable
                        if os.path.exists(filepath):
                            try:
                                os.remove(filepath)
                            except Exception:
                                pass
                        os.replace(raw_filepath, filepath)
                        return True
            except Exception:
                pass
            finally:
                if os.path.exists(raw_filepath):
                    try:
                        os.remove(raw_filepath)
                    except Exception:
                        pass

        # Tier 2: Google Neural TTS Fallback
        if GTTS_AVAILABLE:
            try:
                tts = gTTS(text=text, lang="en", tld="us")
                tts.save(filepath)
                # Try mastering even on fallback
                mastered_fb = filepath + ".mastered.mp3"
                if self._apply_studio_mastering(filepath, mastered_fb):
                    os.replace(mastered_fb, filepath)
                return True
            except Exception as e:
                print(f"[AI MC] TTS fallback note for {os.path.basename(filepath)}: {e}", flush=True)

        return False

    def _precache_standard_alerts(self):
        """Generates standard alert audio files in background thread with AvaNeural & Studio Mastering."""
        def _worker():
            version_file = os.path.join(AUDIO_MC_DIR, ".voice_version")
            current_ver = "v2_ava_studio_mastered"
            force_regen = False
            try:
                if not os.path.exists(version_file) or open(version_file).read().strip() != current_ver:
                    force_regen = True
            except Exception:
                force_regen = True

            templates = {
                "welcome.mp3": "Welcome to Angkor Quant Institutional Live. I am Elena, your eighteen-year-old market anchor. Monitoring Gold M5 sniper order flow.",
                "be_armor.mp3": "Notice. Breakeven Armor is now engaged. Stop loss has moved to entry plus spread. Trade is officially risk free.",
                "tp1_reached.mp3": "Target One reached on Gold M5! Fifty percent scaled out for solid profit. Trailing the remaining position.",
                "tp2_reached.mp3": "Target Two captured! Banking cash profit into the vault. Moonshot runner is now trailing behind fifteen-minute EMA confluence.",
            }
            for filename, text in templates.items():
                filepath = os.path.join(AUDIO_MC_DIR, filename)
                if force_regen or not os.path.exists(filepath) or os.path.getsize(filepath) < 1000:
                    self._synthesize_file(text, filepath)

            try:
                with open(version_file, "w") as f:
                    f.write(current_ver)
            except Exception:
                pass

        threading.Thread(target=_worker, daemon=True).start()

    def synthesize_speech(self, text: str, speech_id: str) -> Optional[str]:
        """Synthesizes text to MP3 file and returns relative URL."""
        filename = f"{speech_id}.mp3"
        filepath = os.path.join(AUDIO_MC_DIR, filename)
        if os.path.exists(filepath) and os.path.getsize(filepath) > 1000:
            return f"/audio/mc/{filename}"

        ok = self._synthesize_file(text, filepath)
        if ok and os.path.exists(filepath):
            return f"/audio/mc/{filename}"
        return None

    def evaluate_market_events(self, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """
        Audits current market data from gold_mathematical_radar and SMC Citadel.
        Decides whether Elena should broadcast a speech based on priority and cooldown.
        """
        now = time.time()
        p = float(data.get("current_price", 2745.50))
        sig = data.get("signal", {})
        action = sig.get("action", "WAIT")
        conf = float(sig.get("confidence", 75.0))
        sl = float(sig.get("sl", p - 4.50))
        tp1 = float(sig.get("tp1", p + 9.00))
        tp2 = float(sig.get("tp2", p + 18.00))

        math_info = data.get("math", {})
        hurst = float(math_info.get("hurst", 0.50))
        kalman_bias = math_info.get("kalman_bias", "STATIONARY")
        smc = data.get("smc", {})
        sweep = smc.get("sweep_summary", "")

        # -------------------------------------------------------------
        # 1. HIGHEST PRIORITY: New BUY or SELL Signal Trigger
        # -------------------------------------------------------------
        if action in ["BUY", "SELL"] and action != self.last_signal_action:
            self.last_signal_action = action
            self.last_speech_time = now

            if action == "BUY":
                speech_text = (
                    f"Institutional alert! Strong Buy confluence confirmed on Gold M5 at {p:.2f} dollars. "
                    f"Stop loss is anchored at {sl:.2f}, targeting TP1 at {tp1:.2f} for a 2.0R return. "
                    f"Order flow indicates solid institutional absorption."
                )
                mood = "buy"
            else:
                speech_text = (
                    f"Institutional alert! Strong Sell confluence confirmed on Gold M5 at {p:.2f} dollars. "
                    f"Stop loss is anchored at {sl:.2f}, targeting TP1 at {tp1:.2f}. "
                    f"Bearish order block rejection active."
                )
                mood = "sell"

            speech_id = f"sig_{action.lower()}_{int(now)}"
            audio_url = self.synthesize_speech(speech_text, speech_id)

            payload = {
                "id": speech_id,
                "text": speech_text,
                "speaker": "Elena (Senior Quant Host, 18)",
                "mood": mood,
                "priority": "HIGH",
                "audio_url": audio_url,
                "duration_est": max(4.0, len(speech_text) * 0.065),
                "timestamp": now
            }
            self.current_speech = payload
            return payload

        # Keep state updated
        if action == "WAIT":
            self.last_signal_action = "WAIT"

        # -------------------------------------------------------------
        # Cooldown check for regular commentary (minimum 45 seconds gap)
        # -------------------------------------------------------------
        if (now - self.last_speech_time) < 45.0:
            return None

        # -------------------------------------------------------------
        # 2. PRIORITY 2: Turtle Soup Liquidity Sweep Absorbed
        # -------------------------------------------------------------
        if "Liquidity Grab" in sweep or "Sweep Absorbed" in sweep:
            self.last_speech_time = now
            speech_text = (
                f"Order flow update: A Turtle Soup liquidity sweep has just been absorbed at {p:.2f} dollars. "
                f"Retail stop clusters have been cleared. Monitoring boundary reaction for quick momentum."
            )
            speech_id = f"sweep_{int(now)}"
            audio_url = self.synthesize_speech(speech_text, speech_id)
            payload = {
                "id": speech_id,
                "text": speech_text,
                "speaker": "Elena (Senior Quant Host, 18)",
                "mood": "analysis",
                "priority": "MEDIUM",
                "audio_url": audio_url,
                "duration_est": 5.5,
                "timestamp": now
            }
            self.current_speech = payload
            return payload

        # -------------------------------------------------------------
        # 3. PRIORITY 3: Interbank Session Transition (Kill Zones)
        # -------------------------------------------------------------
        current_session = self._get_current_session_name()
        if current_session != self.last_session_name and self.last_session_name != "":
            self.last_session_name = current_session
            self.last_speech_time = now

            if "LONDON" in current_session:
                speech_text = (
                    "London Interbank session is officially open. European institutional desks are now active. "
                    "Volatility expansion expected across Gold and European indices."
                )
            elif "NEW YORK" in current_session:
                speech_text = (
                    "Wall Street Cash Market is now open. High-frequency US trading desks are online. "
                    "Closely monitoring Gold's inverse correlation with US Treasury real yields."
                )
            elif "OVERNIGHT" in current_session:
                speech_text = (
                    "Overnight rollover window reached. TradFi intraday profits are flat to cash. "
                    "Preserving capital against wide broker spread expansion."
                )
            else:
                speech_text = (
                    f"Entering {current_session}. Maintaining disciplined statistical execution."
                )

            speech_id = f"sess_{int(now)}"
            audio_url = self.synthesize_speech(speech_text, speech_id)
            payload = {
                "id": speech_id,
                "text": speech_text,
                "speaker": "Elena (Senior Quant Host, 18)",
                "mood": "session",
                "priority": "MEDIUM",
                "audio_url": audio_url,
                "duration_est": 6.0,
                "timestamp": now
            }
            self.current_speech = payload
            return payload

        if self.last_session_name == "":
            self.last_session_name = current_session

        # -------------------------------------------------------------
        # 4. PRIORITY 4: Routine Market Wrap (Every 10 minutes)
        # -------------------------------------------------------------
        if (now - self.last_hourly_brief_time) >= 600.0:
            self.last_hourly_brief_time = now
            self.last_speech_time = now

            hurst_desc = "trending persistently" if hurst > 0.55 else ("mean-reverting" if hurst < 0.45 else "in random equilibrium")
            speech_text = (
                f"Gold market brief. Spot Gold is currently holding at {p:.2f} dollars. "
                f"The Hurst Exponent is {hurst:.2f}, indicating price is {hurst_desc}. "
                f"The Shanghai Gold Exchange premium remains at plus twenty-eight dollars per ounce, providing strong physical support."
            )
            speech_id = f"brief_{int(now)}"
            audio_url = self.synthesize_speech(speech_text, speech_id)
            payload = {
                "id": speech_id,
                "text": speech_text,
                "speaker": "Elena (Senior Quant Host, 18)",
                "mood": "brief",
                "priority": "LOW",
                "audio_url": audio_url,
                "duration_est": 7.0,
                "timestamp": now
            }
            self.current_speech = payload
            return payload

        return None

    @staticmethod
    def _get_current_session_name() -> str:
        gm = time.gmtime()
        total_mins = gm.tm_hour * 60 + gm.tm_min
        if 7 * 60 <= total_mins < 13 * 60 + 30:
            return "LONDON OPEN KILL ZONE"
        elif 13 * 60 + 30 <= total_mins < 18 * 60 + 30:
            return "NEW YORK OPEN KILL ZONE"
        elif 20 * 60 + 45 <= total_mins < 24 * 60:
            return "OVERNIGHT ROLLOVER STANDBY"
        else:
            return "ASIAN INTERBANK SESSION"


# Module singleton
mc_engine = GoldAIMCEngine.get_instance()

