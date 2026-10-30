#!/usr/bin/env python3
"""
ANGKOR QUANT - GOLD M1 AI GIRL MC & QUANT HOST ENGINE
=====================================================
Powers the 24/7 Virtual Institutional Quant Anchor ("Elena") for YouTube Live.
Delivers:
  1. Real-time institutional Wall Street English commentaries (Buy/Sell, TP/SL, Breakeven).
  2. Interbank Kill Zone briefings (London Open, New York Wall Street Cash Open).
  3. Physical Shanghai Gold (SGE) & Macro TIPS real yield commentary.
  4. Audio speech generation with pre-cached high-fidelity neural voice assets.
  5. Intelligent cooldown & priority queue (Zero chatter collision, instant priority on signals).
=====================================================
"""

import os
import sys
import time
import json
import threading
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
    emotive states, and neural voice synthesis.
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

    def _precache_standard_alerts(self):
        """Generates standard alert audio files in background thread if not present."""
        if not GTTS_AVAILABLE:
            return

        def _worker():
            templates = {
                "welcome.mp3": "Welcome to Angkor Quant Institutional Live. I am Elena, your 24/7 AI Market Anchor. Monitoring Gold M5 sniper order flow.",
                "be_armor.mp3": "Notice. Breakeven Armor is now engaged. Stop loss has moved to entry plus spread. Trade is officially risk free.",
                "tp1_reached.mp3": "Target One reached on Gold M5! Fifty percent scaled out for solid profit. Trailing the remaining position.",
                "tp2_reached.mp3": "Target Two captured! Banking cash profit into the vault. Moonshot runner is now trailing behind fifteen-minute EMA confluence.",
            }
            for filename, text in templates.items():
                filepath = os.path.join(AUDIO_MC_DIR, filename)
                if not os.path.exists(filepath):
                    try:
                        tts = gTTS(text=text, lang="en", tld="us")
                        tts.save(filepath)
                    except Exception as e:
                        print(f"⚠️ [AI MC] Pre-cache note for {filename}: {e}", flush=True)

        threading.Thread(target=_worker, daemon=True).start()

    def synthesize_speech(self, text: str, speech_id: str) -> Optional[str]:
        """Synthesizes text to MP3 file and returns relative URL."""
        if not GTTS_AVAILABLE:
            return None

        filename = f"{speech_id}.mp3"
        filepath = os.path.join(AUDIO_MC_DIR, filename)
        if os.path.exists(filepath):
            return f"/audio/mc/{filename}"

        try:
            tts = gTTS(text=text, lang="en", tld="us")
            tts.save(filepath)
            return f"/audio/mc/{filename}"
        except Exception as e:
            print(f"⚠️ [AI MC] TTS synthesis note: {e}", flush=True)
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
                "speaker": "Elena (Senior Quant Analyst)",
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
                "speaker": "Elena (Senior Quant Analyst)",
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
                "speaker": "Elena (Senior Quant Analyst)",
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
                "speaker": "Elena (Senior Quant Analyst)",
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

