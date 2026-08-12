@echo off
title Apex AI Super Brain Bot - Git & VPS Deployer
cd /d "%~dp0"

echo =========================================================
echo       1. Committing & Pushing Latest Fixed Code to GitHub...
echo =========================================================
git add .
git commit -m "APEX AGI SUPER BRAIN BOT - Spot/Futures Profit Refactor & Bug Fixes"
git push origin main

echo =========================================================
echo       2. Force Closing running Bot & Old Command Windows...
echo =========================================================
taskkill /F /FI "WINDOWTITLE eq Apex AI Bot - 24/7 VPS Server*" /T >nul 2>&1
taskkill /F /IM python.exe /T >nul 2>&1
timeout /t 2 >nul

echo =========================================================
echo       3. Fetching & Syncing Latest Code from GitHub...
echo =========================================================
git fetch --all
git reset --hard origin/main

echo =========================================================
echo       4. Clearing __pycache__ & stale bytecode...
echo =========================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /f /q *.pyc >nul 2>&1

echo =========================================================
echo       5. Starting Apex AI Bot with Clean Updated Code...
echo =========================================================
start start_vps.bat
echo [SUCCESS] Clean Git Push & Update Complete! Bot successfully restarted.
pause

