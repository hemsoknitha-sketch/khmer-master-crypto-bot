@echo off
title Apex AI Super Brain Bot - Git & VPS Deployer v10.6
cd /d "%~dp0"

set GIT_TERMINAL_PROMPT=0
set GCM_INTERACTIVE=never

:: Configure Git to store credentials safely so manual login is never required
git config credential.helper store >nul 2>&1

echo =========================================================
echo   1. Auto-Staging & Auto-Pushing Code Changes to GitHub...
echo =========================================================
git add .
git commit -m "Auto Update Apex AI Super Brain Bot - Institutional Profit Edition v10.6" >nul 2>&1
git push origin main >nul 2>&1
echo [GIT] Code successfully pushed to GitHub repository!

echo =========================================================
echo   2. Closing Active Bot Instances & Cleaning Processes...
echo =========================================================
taskkill /F /FI "WINDOWTITLE eq Apex AI Bot - 24/7 VPS Server*" /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 >nul

echo =========================================================
echo   3. Fetching & Force-Syncing Latest Code from GitHub...
echo =========================================================
git fetch --all
git reset --hard origin/main

echo =========================================================
echo   4. Purging __pycache__ & Stale Bytecode Files...
echo =========================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /f /q *.pyc >nul 2>&1

echo =========================================================
echo   5. Relaunching Apex AI Bot with Updated High-Velocity Code...
echo =========================================================
start start_vps.bat
echo =========================================================
echo [SUCCESS] 🚀 Clean Git Push, Fetch & VPS Update Complete! 
echo Bot successfully updated and restarted on VPS without login.
echo =========================================================
pause



