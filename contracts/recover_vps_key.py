"""
Khmer Master Crypto - Autonomous VPS Key Recovery & Gas Sweeper Engine
======================================================================
Searches VPS systemd journal, /proc, log files, backups, and bash history
to find the original Private Key belonging to 0x3D1eef56843ABBDc5a6e9E46dDAA8CC76df453f9.
Once found, automatically restores it to .env and transfers the ETH gas to 0xe3833d...
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
    if not Account:
        return False
    try:
        k = cand if cand.startswith("0x") else "0x" + cand
        acct = Account.from_key(k)
        if acct.address.lower() == TARGET_ADDRESS:
            return k
    except Exception:
        pass
    return None

def main():
    print("=" * 70)
    print("  KHMER MASTER CRYPTO - FORENSIC VPS KEY RECOVERY ENGINE")
    print(f"  Target Wallet Address: {TARGET_ADDRESS}")
    print("=" * 70)

    if not Account:
        print("❌ eth_account is not installed. Please run inside venv.")
        return

    found_key = None

    # Source 1: Check all .env files and backups in /opt/khmer-master-crypto-bot
    search_dirs = [
        "/opt/khmer-master-crypto-bot",
        "/opt/khmer-master-crypto-bot/backups",
        "/opt/khmer-master-crypto-bot/logs",
        os.getcwd()
    ]

    print("\n[STEP 1] Scanning files, backups, and logs for candidate private keys...")
    for sdir in search_dirs:
        if not os.path.exists(sdir):
            continue
        for root, dirs, files in os.walk(sdir):
            dirs[:] = [d for d in dirs if d not in ['venv', '.git', '__pycache__', 'node_modules']]
            for fname in files:
                fpath = os.path.join(root, fname)
                # Check text/config files
                if any(fname.startswith(p) for p in ['.env', 'bot', 'keeper', 'deploy']) or fname.endswith(('.log', '.txt', '.bak', '.old', '~', '.swp')):
                    try:
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as fp:
                            content = fp.read()
                            for m in hex64_pattern.findall(content):
                                res = test_key(m)
                                if res:
                                    print(f"🎉 FOUND IN FILE: {fpath}")
                                    found_key = res
                                    break
                    except Exception:
                        pass
                if found_key:
                    break
            if found_key:
                break
        if found_key:
            break

    # Source 2: Check journalctl logs
    if not found_key:
        print("\n[STEP 2] Scanning systemd journalctl logs (khmer-master-crypto-bot)...")
        try:
            cmd = ["journalctl", "-u", "khmer-master-crypto-bot", "--no-pager", "-n", "10000"]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=15)
            if proc.stdout:
                for m in hex64_pattern.findall(proc.stdout):
                    res = test_key(m)
                    if res:
                        print("🎉 FOUND IN JOURNALCTL SYSTEM LOGS!")
                        found_key = res
                        break
        except Exception as e:
            print(f"Notice querying journalctl: {e}")

    # Source 3: Check /proc/*/environ
    if not found_key and os.path.exists("/proc"):
        print("\n[STEP 3] Scanning running processes /proc/*/environ...")
        try:
            for pid in os.listdir("/proc"):
                if pid.isdigit():
                    env_file = f"/proc/{pid}/environ"
                    if os.path.exists(env_file):
                        try:
                            with open(env_file, "rb") as ef:
                                data = ef.read().decode('utf-8', errors='ignore')
                                for m in hex64_pattern.findall(data):
                                    res = test_key(m)
                                    if res:
                                        print(f"🎉 FOUND IN PROCESS /proc/{pid}/environ!")
                                        found_key = res
                                        break
                        except Exception:
                            pass
                if found_key:
                    break
        except Exception as e:
            print(f"Notice scanning /proc: {e}")

    # Source 4: Check bash history
    if not found_key:
        print("\n[STEP 4] Scanning user bash history (~/.bash_history)...")
        home = os.path.expanduser("~")
        hist_file = os.path.join(home, ".bash_history")
        if os.path.exists(hist_file):
            try:
                with open(hist_file, "r", encoding="utf-8", errors="ignore") as hf:
                    for line in hf:
                        for m in hex64_pattern.findall(line):
                            res = test_key(m)
                            if res:
                                print("🎉 FOUND IN BASH HISTORY!")
                                found_key = res
                                break
                        if found_key:
                            break
            except Exception:
                pass

    if found_key:
        print("\n" + "=" * 70)
        print("🎯 BINGO! RECOVERED THE EXACT PRIVATE KEY FOR 0x3D1eef...!")
        print(f"🔑 Private Key: {found_key}")
        print("=" * 70)

        # Update .env file on VPS
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
                new_lines.append(f"\n# Recovered Funded Keeper Relayer Key (0x3D1eef...)\nKEEPER_RELAYER_PRIVATE_KEY={found_key}\n")

            with open(env_path, "w", encoding="utf-8") as f:
                f.writelines(new_lines)
            print(f"💾 Restored private key directly into {env_path} successfully!")

        # Now sweep gas directly to owner
        print("\n[STEP 5] Sweeping gas directly to Owner Wallet...")
        try:
            from contracts.transfer_keeper_gas import sweep_gas_to_owner
            sweep_gas_to_owner(recipient=TARGET_OWNER, explicit_private_key=found_key)
        except Exception as e:
            print(f"Notice running gas sweeper: {e}")

    else:
        print("\n" + "=" * 70)
        print("❌ មិនអាចរកឃើញ Private Key នៃ 0x3D1eef... នៅក្នុង VPS Storage ឡើយ!")
        print("=" * 70)
        print("💡 មូលហេតុ ៖ ពាក្យបញ្ជា sed -i ពីមុនបានសរសេរជាន់លើ .env ដោយមិនបានបង្កើត backup (.env.bak)។")
        print(f"👉 សំណូមពរ ៖ សូមលោកអ្នកពិនិត្យមើលកាបូប MetaMask ឬ Exchange របស់អ្នក ថាតើ Address {TARGET_ADDRESS}")
        print("   ត្រូវបាន Import ចេញពី MetaMask Account មួយណា (Account 1, Account 2, ឬ Account 3...)។")

if __name__ == "__main__":
    main()
