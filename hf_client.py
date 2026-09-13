"""
Async Hugging Face Microservice & Serverless Client for APEX AGI ENGINE v13.00.
Handles non-blocking REST API calls from GCP 1GB VPS Node to Hugging Face AI Super Brain.
Provides In-Memory RAM Caching with sub-0.1ms dispatch and 33 AI Models Swarm offloading.
"""

import os
import asyncio
import aiohttp
import time
from typing import Dict, Any, Optional

# Default Hugging Face Space & Router Endpoints
DEFAULT_HF_URL = os.getenv("HF_SPACE_URL", "https://hemsinath-khmer-master-crypto-bot.hf.space").rstrip("/")
HF_ROUTER_URL = "https://router.huggingface.co/hf-inference/models"
HF_TOKEN = os.getenv("HF_TOKEN", "").strip()


class InMemoryHighSpeedCache:
    """High-throughput In-Memory RAM cache with sub-0.1ms lookup."""
    def __init__(self, default_ttl: float = 60.0):
        self._cache: Dict[str, tuple[float, Any]] = {}
        self.default_ttl = default_ttl

    def get(self, key: str) -> Optional[Any]:
        entry = self._cache.get(key)
        if entry:
            exp_time, data = entry
            if time.time() < exp_time:
                return data
            else:
                self._cache.pop(key, None)
        return None

    def set(self, key: str, value: Any, ttl: Optional[float] = None, ttl_seconds: Optional[float] = None) -> None:
        duration = ttl_seconds if ttl_seconds is not None else (ttl if ttl is not None else self.default_ttl)
        expiry = time.time() + duration
        self._cache[key] = (expiry, value)

    def clear(self) -> None:
        self._cache.clear()


class HuggingFaceAIClient:
    def __init__(self, base_url: str = DEFAULT_HF_URL):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}
        if HF_TOKEN:
            self.headers["Authorization"] = f"Bearer {HF_TOKEN}"
        self.cache = InMemoryHighSpeedCache(default_ttl=45.0)

    async def ping_health(self, timeout_sec: int = 4) -> bool:
        """Pings HF Space health endpoint to verify status with cache."""
        cached = self.cache.get("hf_health")
        if cached is not None:
            return bool(cached)

        url = f"{self.base_url}/health"
        timeout = aiohttp.ClientTimeout(total=timeout_sec)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        is_online = data.get("status") == "online"
                        self.cache.set("hf_health", is_online, ttl=30.0)
                        return is_online
        except Exception:
            pass
        self.cache.set("hf_health", False, ttl=15.0)
        return False

    async def predict_market(self, symbol: str = "BTCUSDT", timeout_sec: int = 12) -> Dict[str, Any]:
        """Asynchronously calls Hugging Face Space /predict endpoint with sub-0.1ms cache."""
        cache_key = f"predict_{symbol.upper()}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{self.base_url}/predict"
        payload = {"symbol": symbol}
        timeout = aiohttp.ClientTimeout(total=timeout_sec)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=self.headers) as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        self.cache.set(cache_key, res, ttl=60.0)
                        return res
                    else:
                        return {"success": False, "error": f"HF Space HTTP {resp.status}"}
        except asyncio.TimeoutError:
            return {"success": False, "error": "HF_SPACE_SLEEP_TIMEOUT"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def analyze_market(self, symbol: str = "BTCUSDT", prompt: Optional[str] = None, gemini_key: Optional[str] = None, timeout_sec: int = 15) -> Dict[str, Any]:
        """Asynchronously calls Hugging Face Space /analyze endpoint with caching."""
        cache_key = f"analyze_{symbol.upper()}_{hash(prompt or '')}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{self.base_url}/analyze"
        payload = {
            "symbol": symbol,
            "prompt": prompt,
            "gemini_key": gemini_key or os.getenv("GEMINI_API_KEY")
        }
        timeout = aiohttp.ClientTimeout(total=timeout_sec)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=self.headers) as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        self.cache.set(cache_key, res, ttl=90.0)
                        return res
                    else:
                        return {"success": False, "error": f"HF Space HTTP {resp.status}"}
        except asyncio.TimeoutError:
            return {"success": False, "error": "HF_SPACE_SLEEP_TIMEOUT"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def fetch_news(self, symbol: Optional[str] = None, limit: int = 5, timeout_sec: int = 10) -> Dict[str, Any]:
        """Asynchronously calls Hugging Face Space /news endpoint with caching."""
        cache_key = f"news_{str(symbol or 'ALL').upper()}_{limit}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{self.base_url}/news"
        payload = {"symbol": symbol, "limit": limit}
        timeout = aiohttp.ClientTimeout(total=timeout_sec)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=self.headers) as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        self.cache.set(cache_key, res, ttl=120.0)
                        return res
                    else:
                        return {"success": False, "error": f"HF Space HTTP {resp.status}"}
        except asyncio.TimeoutError:
            return {"success": False, "error": "HF_SPACE_SLEEP_TIMEOUT"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def predict_moe_routing(self, symbol: str = "BTCUSDT", timeout_sec: int = 10) -> Dict[str, Any]:
        """Asynchronously calls Hugging Face Space /moe_predict endpoint."""
        cache_key = f"moe_{symbol.upper()}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{self.base_url}/moe_predict"
        payload = {"symbol": symbol}
        timeout = aiohttp.ClientTimeout(total=timeout_sec)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=self.headers) as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        self.cache.set(cache_key, res, ttl=60.0)
                        return res
                    else:
                        return {"success": False, "error": f"HF Space HTTP {resp.status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def predict_pinn_volatility(self, symbol: str = "BTCUSDT", timeout_sec: int = 10) -> Dict[str, Any]:
        """Asynchronously calls Hugging Face Space /pinn_volatility endpoint (PINN Jump-Diffusion)."""
        cache_key = f"pinn_{symbol.upper()}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{self.base_url}/pinn_volatility"
        payload = {"symbol": symbol}
        timeout = aiohttp.ClientTimeout(total=timeout_sec)

        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=self.headers) as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        self.cache.set(cache_key, res, ttl=60.0)
                        return res
                    else:
                        return {"success": False, "error": f"HF Space HTTP {resp.status}"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def score_finbert_sentiment(self, text: str, timeout_sec: int = 8) -> Dict[str, Any]:
        """Scores financial text sentiment via ProsusAI/finbert on HF Serverless API."""
        if not text or not HF_TOKEN:
            return {"sentiment": "NEUTRAL", "score": 0.50, "source": "local_fallback"}

        cache_key = f"finbert_{hash(text[:120])}"
        cached = self.cache.get(cache_key)
        if cached is not None:
            return cached

        url = f"{HF_ROUTER_URL}/ProsusAI/finbert"
        timeout = aiohttp.ClientTimeout(total=timeout_sec)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json={"inputs": text[:512]}, headers=self.headers) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        # Format: [[{'label': 'positive', 'score': 0.9}, ...]]
                        if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                            top_item = max(data[0], key=lambda x: x.get("score", 0.0))
                            lbl = top_item.get("label", "neutral").upper()
                            mapped_label = "BULLISH" if lbl == "POSITIVE" else ("BEARISH" if lbl == "NEGATIVE" else "NEUTRAL")
                            result = {
                                "sentiment": mapped_label,
                                "score": float(top_item.get("score", 0.75)),
                                "source": "finbert_hf"
                            }
                            self.cache.set(cache_key, result, ttl=300.0)
                            return result
        except Exception:
            pass

        return {"sentiment": "NEUTRAL", "score": 0.50, "source": "local_fallback"}


# Global Singleton Client Instance
hf_ai_client = HuggingFaceAIClient()

