# ==============================================================================
# APEX HUGGING FACE VIP SPACE PROVISIONER & ORCHESTRATION CITADEL
# ==============================================================================
# Autonomous Provisioner that spawns isolated Hugging Face Docker Spaces (Free 16GB RAM)
# for VIP Users, connecting them to Tokyo Master VPS Bridge with Zero VPS Overhead.
# ==============================================================================

import os
import sys
import time
import logging
import urllib.request
from typing import Dict, Any, List, Optional

logger = logging.getLogger("APEX_HF_SPACES")

try:
    from huggingface_hub import HfApi
except ImportError:
    logger.warning("⚠️ huggingface_hub not installed. Installing dynamically...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub"])
    from huggingface_hub import HfApi

import database as db

HF_TOKEN = os.getenv("HF_TOKEN", "").strip()
HF_USERNAME = os.getenv("HF_USERNAME", "hemsinath").strip()
DEFAULT_TEMPLATE_SPACE = f"{HF_USERNAME}/apex-mt5-edge-node"
DEFAULT_VPS_IP = os.getenv("VPS_PUBLIC_IP", "34.153.209.188").strip()
BRIDGE_PORT = int(os.getenv("MT5_BRIDGE_PORT", "5555"))
SHARED_SECRET_KEY = os.getenv("MT5_SECRET_KEY", "KHMER_MASTER_CRYPTO_SECRET_KEY_2026").strip()

# Path to the bundled worker directory
WORKER_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hf_mt5_worker")


class HuggingFaceSpaceManager:
    """Institutional-grade Orchestrator for Hugging Face Free Edge Workers."""

    @staticmethod
    def get_api() -> Optional[HfApi]:
        """Returns authenticated HfApi client."""
        token = HF_TOKEN or os.getenv("HF_TOKEN", "").strip()
        if not token:
            logger.warning("⚠️ [HF SPACES] HF_TOKEN is not configured in environment!")
            return None
        return HfApi(token=token)

    @classmethod
    def resolve_vps_ip(cls) -> str:
        """Dynamically discovers VPS public IP with fast fallback."""
        if DEFAULT_VPS_IP and DEFAULT_VPS_IP != "0.0.0.0" and DEFAULT_VPS_IP != "127.0.0.1":
            return DEFAULT_VPS_IP
        try:
            req = urllib.request.Request("https://api.ipify.org", headers={"User-Agent": "curl/7.68.0"})
            with urllib.request.urlopen(req, timeout=3) as resp:
                discovered = resp.read().decode("utf-8").strip()
                if discovered:
                    return discovered
        except Exception:
            pass
        return "34.153.209.188"

    @classmethod
    def ensure_master_template_space(cls) -> Dict[str, Any]:
        """Ensures the master template space exists and is updated on Hugging Face."""
        api = cls.get_api()
        if not api:
            return {"success": False, "reason": "MISSING_HF_TOKEN"}

        try:
            # Check or create template space
            api.create_repo(
                repo_id=DEFAULT_TEMPLATE_SPACE,
                repo_type="space",
                space_sdk="docker",
                private=True,
                exist_ok=True
            )
            # Upload worker code
            if os.path.exists(WORKER_DIR):
                api.upload_folder(
                    folder_path=WORKER_DIR,
                    repo_id=DEFAULT_TEMPLATE_SPACE,
                    repo_type="space",
                    commit_message="Sync APEX MT5 Edge Worker template"
                )
            logger.info(f"✅ [HF SPACES] Master template space ready: {DEFAULT_TEMPLATE_SPACE}")
            return {
                "success": True,
                "space_id": DEFAULT_TEMPLATE_SPACE,
                "url": f"https://huggingface.co/spaces/{DEFAULT_TEMPLATE_SPACE}"
            }
        except Exception as e:
            logger.error(f"❌ [HF SPACES ERROR] Failed to ensure master template space: {e}")
            return {"success": False, "reason": str(e)}

    @classmethod
    def provision_vip_worker_space(
        cls,
        chat_id: int,
        account_id: str,
        password: str,
        server: str,
        broker: str = "GTCFX",
        is_cent: bool = False
    ) -> Dict[str, Any]:
        """
        Deploys an autonomous private Hugging Face Space for a VIP user.
        Injects credentials into Space Secrets so they are completely encrypted.
        Connects outward to Tokyo Master VPS with ZERO VPS RAM/CPU/Disk load!
        """
        api = cls.get_api()
        if not api:
            return {
                "success": False,
                "reason": "HF_TOKEN_NOT_CONFIGURED",
                "message": "Hugging Face Access Token (HF_TOKEN) is not configured in .env!"
            }

        account_id = str(account_id).strip()
        space_repo_name = f"mt5-edge-{account_id}"
        full_space_id = f"{HF_USERNAME}/{space_repo_name}"
        space_url = f"https://{HF_USERNAME}-{space_repo_name}.hf.space"
        vps_ip = cls.resolve_vps_ip()

        try:
            logger.info(f"🚀 [HF SPACES] Provisioning VIP Edge Worker Space '{full_space_id}' for Account #{account_id}...")

            # 1. Create Private Docker Space on Hugging Face
            api.create_repo(
                repo_id=full_space_id,
                repo_type="space",
                space_sdk="docker",
                private=True,
                exist_ok=True
            )

            # 2. Upload Worker Code
            if os.path.exists(WORKER_DIR):
                api.upload_folder(
                    folder_path=WORKER_DIR,
                    repo_id=full_space_id,
                    repo_type="space",
                    commit_message=f"Deploy MT5 Edge Worker for Account {account_id}"
                )

            # 3. Securely Inject Space Secrets (AES KMS Encrypted by Hugging Face)
            secrets_to_set = {
                "BRIDGE_HOST": vps_ip,
                "BRIDGE_PORT": str(BRIDGE_PORT),
                "MT5_ACCOUNT": str(account_id),
                "MT5_PASSWORD": str(password),
                "MT5_SERVER": str(server),
                "BROKER_NAME": str(broker),
                "SECRET_KEY": SHARED_SECRET_KEY,
                "CHAT_ID": str(chat_id),
                "IS_CENT": "true" if is_cent else "false"
            }

            for sec_k, sec_v in secrets_to_set.items():
                try:
                    api.add_space_secret(repo_id=full_space_id, key=sec_k, value=sec_v)
                except Exception as ex_sec:
                    logger.debug(f"Secret set note ({sec_k}): {ex_sec}")

            # 4. Record Worker in SQLite Database
            db.record_vip_hf_worker(
                account_id=account_id,
                chat_id=chat_id,
                space_id=full_space_id,
                space_url=space_url,
                broker=broker,
                server=server,
                status="BUILDING"
            )

            logger.info(f"🎉 [HF SPACES SUCCESS] Space '{full_space_id}' provisioned! URL: {space_url}")
            return {
                "success": True,
                "account_id": account_id,
                "space_id": full_space_id,
                "space_url": space_url,
                "status": "BUILDING",
                "vps_ip": vps_ip,
                "vps_port": BRIDGE_PORT
            }

        except Exception as e:
            logger.error(f"❌ [HF SPACES ERROR] Failed to provision space for Account #{account_id}: {e}")
            return {"success": False, "reason": str(e)}

    @classmethod
    def get_vip_worker_runtime(cls, account_id: str) -> Dict[str, Any]:
        """Queries Hugging Face API for the live container runtime state."""
        api = cls.get_api()
        if not api:
            return {"status": "UNKNOWN", "reason": "NO_API"}

        space_id = f"{HF_USERNAME}/mt5-edge-{account_id}"
        try:
            runtime = api.get_space_runtime(repo_id=space_id)
            stage = getattr(runtime, "stage", "UNKNOWN")
            hardware = getattr(runtime, "hardware", "cpu-basic")
            return {
                "space_id": space_id,
                "stage": stage,
                "hardware": hardware,
                "raw": str(runtime)
            }
        except Exception as e:
            return {"space_id": space_id, "stage": "ERROR", "error": str(e)}

    @classmethod
    def restart_vip_worker(cls, account_id: str) -> bool:
        """Restarts the Hugging Face Space for an account."""
        api = cls.get_api()
        if not api:
            return False
        space_id = f"{HF_USERNAME}/mt5-edge-{account_id}"
        try:
            api.restart_space(repo_id=space_id)
            logger.info(f"🔄 [HF SPACES] Restarted Space {space_id}")
            return True
        except Exception as e:
            logger.error(f"❌ [HF SPACES] Restart failed for {space_id}: {e}")
            return False

    @classmethod
    def destroy_vip_worker(cls, account_id: str) -> bool:
        """Deletes the Hugging Face Space and cleans database entry."""
        api = cls.get_api()
        space_id = f"{HF_USERNAME}/mt5-edge-{account_id}"
        if api:
            try:
                api.delete_repo(repo_id=space_id, repo_type="space")
                logger.info(f"🗑️ [HF SPACES] Deleted Space {space_id}")
            except Exception as e:
                logger.warning(f"⚠️ [HF SPACES] Delete repo notice ({space_id}): {e}")

        # Delete from database
        try:
            db.delete_vip_hf_worker(account_id)
        except Exception:
            pass
        return True

    @classmethod
    def ping_all_active_workers(cls) -> int:
        """Sends lightweight GET /ping to all active HF Spaces to prevent 48h sleep."""
        workers = db.get_all_vip_hf_workers()
        pinged = 0
        for w in workers:
            s_url = w.get("space_url", "")
            if not s_url:
                continue
            ping_target = f"{s_url.rstrip('/')}/ping"
            try:
                req = urllib.request.Request(ping_target, headers={"User-Agent": "ApexMasterBot/1.0"})
                with urllib.request.urlopen(req, timeout=3) as resp:
                    if resp.status == 200:
                        pinged += 1
                        db.update_vip_hf_worker_status(w["account_id"], status="ONLINE")
            except Exception:
                pass
        return pinged
