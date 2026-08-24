"""
Async Hugging Face Microservice Client for APEX AGI ENGINE v11.0.
Handles non-blocking REST API calls from GCP VPS Node to Hugging Face AI Super Brain Node.
"""

import os
import asyncio
import aiohttp
import time
from typing import Dict, Any, Optional

# Default Hugging Face Space Endpoint
DEFAULT_HF_URL = os.getenv("HF_SPACE_URL", "https://hemsinath-khmer-master-crypto-bot.hf.space").rstrip("/")
HF_TOKEN = os.getenv("HF_TOKEN", "")


class HuggingFaceAIClient:
    def __init__(self, base_url: str = DEFAULT_HF_URL):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}
        if HF_TOKEN:
            self.headers["Authorization"] = f"Bearer {HF_TOKEN}"
            
    async def ping_health(self, timeout_sec: int = 5) -> bool:
        """Pings HF Space health endpoint to keep space awake and verify status."""
        url = f"{self.base_url}/health"
        timeout = aiohttp.ClientTimeout(total=timeout_sec)
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.get(url) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        return data.get("status") == "online"
        except Exception as e:
            # print(f"⚠️ [HF CLIENT PING] {url} notice: {e}")
            pass
        return False

    async def predict_market(self, symbol: str = "BTCUSDT", timeout_sec: int = 15) -> Dict[str, Any]:
        """Asynchronously calls Hugging Face Space /predict endpoint."""
        url = f"{self.base_url}/predict"
        payload = {"symbol": symbol}
        timeout = aiohttp.ClientTimeout(total=timeout_sec)
        
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=self.headers) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        return {"success": False, "error": f"HF Space HTTP {resp.status}"}
        except asyncio.TimeoutError:
            return {"success": False, "error": "HF_SPACE_SLEEP_TIMEOUT"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def analyze_market(self, symbol: str = "BTCUSDT", prompt: Optional[str] = None, gemini_key: Optional[str] = None, timeout_sec: int = 20) -> Dict[str, Any]:
        """Asynchronously calls Hugging Face Space /analyze endpoint."""
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
                        return await resp.json()
                    else:
                        return {"success": False, "error": f"HF Space HTTP {resp.status}"}
        except asyncio.TimeoutError:
            return {"success": False, "error": "HF_SPACE_SLEEP_TIMEOUT"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def fetch_news(self, symbol: Optional[str] = None, limit: int = 5, timeout_sec: int = 12) -> Dict[str, Any]:
        """Asynchronously calls Hugging Face Space /news endpoint."""
        url = f"{self.base_url}/news"
        payload = {"symbol": symbol, "limit": limit}
        timeout = aiohttp.ClientTimeout(total=timeout_sec)
        
        try:
            async with aiohttp.ClientSession(timeout=timeout) as session:
                async with session.post(url, json=payload, headers=self.headers) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    else:
                        return {"success": False, "error": f"HF Space HTTP {resp.status}"}
        except asyncio.TimeoutError:
            return {"success": False, "error": "HF_SPACE_SLEEP_TIMEOUT"}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Global Singleton Client Instance
hf_ai_client = HuggingFaceAIClient()
