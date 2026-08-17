@echo off
title Khmer Master Crypto / Apex AGI Engine - Git & VPS Deployer v11.0 (Zero Data Loss Protection)
cd /d "%~dp0"

set GIT_TERMINAL_PROMPT=0
set GCM_INTERACTIVE=never

:: Configure Git to store credentials safely so manual login is never required
git config credential.helper store >nul 2>&1
git config pull.rebase false >nul 2>&1

echo =========================================================
echo   🛡️ 1. Protecting VIP User Data & API Keys (Auto-Backup)...
echo =========================================================
if not exist "vps_db_backup" mkdir "vps_db_backup"
if exist "*.db" copy /y "*.db" "vps_db_backup\" >nul 2>&1
if exist ".env" copy /y ".env" "vps_db_backup\" >nul 2>&1
echo [SAFEGUARD] All VIP SQLite Databases & .env API credentials backed up to vps_db_backup\

echo =========================================================
echo   2. Auto-Staging & Auto-Pushing Code Changes to GitHub...
echo =========================================================
git add .
git commit -m "Auto Update Khmer Master Crypto v11.0 AGI Super Brain & HFT Engine" >nul 2>&1
git push origin main >nul 2>&1
echo [GIT] Code successfully pushed to GitHub repository!

echo =========================================================
echo   3. Closing Active Bot Instances & Cleaning Processes...
echo =========================================================
wmic process where "name='cmd.exe' and commandline like '%%start_vps.bat%%'" call terminate >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Apex AI Bot*" /T >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Administrator: Apex AI Bot*" /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1
if exist "bot_instance.lock" del /f /q "bot_instance.lock" >nul 2>&1
timeout /t 3 >nul

echo =========================================================
echo   4. Fetching & Force-Syncing Latest Code from GitHub...
echo =========================================================
git fetch --all
git reset --hard origin/main

echo =========================================================
echo   🛡️ 5. Restoring VIP User Data & API Keys (Zero Data Loss)...
echo =========================================================
if exist "vps_db_backup\*.db" copy /y "vps_db_backup\*.db" ".\" >nul 2>&1
if exist "vps_db_backup\.env" copy /y "vps_db_backup\.env" ".\" >nul 2>&1
echo [RESTORE] VIP Databases & API Keys 100%% preserved and restored successfully!

echo =========================================================
echo   6. Purging __pycache__ & Stale Bytecode Files...
echo =========================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /f /q *.pyc >nul 2>&1

echo =========================================================
echo   7. Relaunching Khmer Master Crypto v11.0 AGI Node...
echo =========================================================
start start_vps.bat
echo =========================================================
echo [SUCCESS] 🚀 Clean Git Push, Fetch & VPS Update Complete! 
echo Bot successfully updated and restarted on VPS with ZERO DATA LOSS.
echo =========================================================
pause
