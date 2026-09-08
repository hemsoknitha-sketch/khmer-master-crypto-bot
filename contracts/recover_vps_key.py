"""
Ultra-Fast Targeted VPS Key Recovery Engine (Runs in under 3 seconds)
====================================================================
Targets only high-probability configuration sources:
1. git stash show -p (recent stashed changes on VPS)
2. git reflog / git diff
3. /proc/[pid]/environ of running python / bot processes
4. systemctl environment
5. ~/.bash_history
6. Specific .env backup files (NOT massive sqlite databases)
"""

import os
import sys
import re
import subprocess

sys.stdout.reconfigure(encoding='utf-8')

TARGET_ADDRESS = "0x3D1eef56843ABBDc5a6e9E46dDAA8CC76df453f9".lower()
TARGET_OWNER = "0xe3833dDaf7fb92b3F0e0a57169C98bd9482e9560"

try:
    from eth_account import Account
except ImportError:
    Account = None

hex64_pattern = re.compile(r'\b(?:0x)?([a-fA-F0-9]{64})\b')

def test_key(cand: str):
    if not Account or not cand:
        return None
    try:
        k = cand if cand.startswith("0x") else "0x" + cand
        acct = Account.from_key(k)
        if acct.address.lower() == TARGET_ADDRESS:
            return k
    except Exception:
        pass
    return None

def main():
    print("=" * 65)
    print("  ULTRA-FAST TARGETED VPS KEY FINDER (< 3 SECONDS)")
    print(f"  Target: {TARGET_ADDRESS}")
    print("=" * 65)

    if not Account:
        print("❌ eth_account not installed.")
        return

    found_key = None
    candidate_pool = set()

    # Source 1: Check git stash on VPS
    print("🔍 [1/6] Inspecting git stash history...")
    try:
        res = subprocess.run(["git", "stash", "list"], capture_output=True, text=True, timeout=5)
        if res.stdout:
            for line in res.stdout.splitlines():
                stash_id = line.split(":")[0].strip()
                diff_res = subprocess.run(["git", "stash", "show", "-p", stash_id], capture_output=True, text=True, timeout=5)
                for m in hex64_pattern.findall(diff_res.stdout):
                    candidate_pool.add(m)
    except Exception as e:
        pass

    # Source 2: Check git diff / git reflog
    print("🔍 [2/6] Inspecting git reflog...")
    try:
        res = subprocess.run(["git", "reflog", "-n", "30", "-p"], capture_output=True, text=True, timeout=5)
        if res.stdout:
            for m in hex64_pattern.findall(res.stdout):
                candidate_pool.add(m)
    except Exception:
        pass

    # Source 3: Check running python processes in /proc
    print("🔍 [3/6] Inspecting running process memory (/proc)...")
    if os.path.exists("/proc"):
        for pid in os.listdir("/proc"):
            if pid.isdigit():
                try:
                    cmd_path = f"/proc/{pid}/cmdline"
                    if os.path.exists(cmd_path):
                        with open(cmd_path, "rb") as cf:
                            cmd_data = cf.read().decode('utf-8', errors='ignore')
                            if "python" in cmd_data or "bot" in cmd_data:
                                env_path = f"/proc/{pid}/environ"
                                if os.path.exists(env_path):
                                    with open(env_path, "rb") as ef:
                                        env_data = ef.read().decode('utf-8', errors='ignore')
                                        for m in hex64_pattern.findall(env_data):
                                            candidate_pool.add(m)
                except Exception:
                    pass

    # Source 4: Check systemd service environment & recent logs
    print("🔍 [4/6] Inspecting systemd service environment...")
    try:
        cmd = ["journalctl", "-u", "khmer-master-crypto-bot", "--no-pager", "-n", "300"]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=5)
        if proc.stdout:
            for m in hex64_pattern.findall(proc.stdout):
                candidate_pool.add(m)
    except Exception:
        pass

    # Source 5: Check bash history
    print("🔍 [5/6] Inspecting ~/.bash_history...")
    home = os.path.expanduser("~")
    hist_file = os.path.join(home, ".bash_history")
    if os.path.exists(hist_file):
        try:
            with open(hist_file, "r", encoding="utf-8", errors="ignore") as hf:
                for m in hex64_pattern.findall(hf.read()):
                    candidate_pool.add(m)
        except Exception:
            pass

    # Source 6: Check explicit .env files only (no binary .db files!)
    print("🔍 [6/6] Inspecting .env files...")
    potential_envs = [
        "/opt/khmer-master-crypto-bot/.env",
        "/opt/khmer-master-crypto-bot/.env.bak",
        "/opt/khmer-master-crypto-bot/.env.old",
        "/opt/khmer-master-crypto-bot/.env.backup",
        os.path.join(os.getcwd(), ".env"),
        os.path.join(os.getcwd(), ".env.bak")
    ]
    for pe in potential_envs:
        if os.path.exists(pe):
            try:
                with open(pe, "r", encoding="utf-8", errors="ignore") as f:
                    for m in hex64_pattern.findall(f.read()):
                        candidate_pool.add(m)
            except Exception:
                pass

    print(f"\n📊 Total high-probability candidates to verify: {len(candidate_pool)}")
    for idx, cand in enumerate(candidate_pool):
        found = test_key(cand)
        if found:
            found_key = found
            break

    if found_key:
        print("\n" + "=" * 65)
        print("🎉 BINGO! RECOVERED PRIVATE KEY FOR 0x3D1eef...!")
        print(f"🔑 Key: {found_key}")
        print("=" * 65)

        # Restore to .env
        env_path = "/opt/khmer-master-crypto-bot/.env"
        if not os.path.exists(env_path):
            env_path = os.path.join(os.getcwd(), ".env")

        if os.path.exists(env_path):
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
            new_lines = []
            replaced = False
            for line in lines:
                if line.strip().startswith("KEEPER_RELAYER_PRIVATE_KEY="):
                    if not replaced:
                        new_lines.append(f"KEEPER_RELAYER_PRIVATE_KEY={found_key}\n")
                        replaced = True
                else:
                    new_lines.append(line)
            if not replaced:
                new_lines.append(f"\nKEEPER_RELAYER_PRIVATE_KEY={found_key}\n")
            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"💾 Restored into {env_path} successfully!")

        print("\n🚀 Transferring Gas ETH to Owner Wallet...")
        try:
            from contracts.transfer_keeper_gas import sweep_gas_to_owner
            sweep_gas_to_owner(recipient=TARGET_OWNER, explicit_private_key=found_key)
        except Exception as e:
            print(f"Transfer notice: {e}")
    else:
        print("\n❌ ពុំទាន់រកឃើញ Private Key នៃ 0x3D1eef... ក្នុង System Memory ឡើយ។")
        print("💡 មូលហេតុ ៖ កូដអាចត្រូវបានបង្កើតឡើងក្នុង Memory នៃ Python កំឡុងពេល Deploy ដោយមិនបានកត់ត្រាចូល File។")

if __name__ == "__main__":
    main()
