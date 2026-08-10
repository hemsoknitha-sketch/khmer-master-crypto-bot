@echo off
title Apex AI Bot - Git 1-Click Clean Auto Update
cd /d "%~dp0"

echo =========================================================
echo       1. Force Closing all running Python & Bot processes...
echo =========================================================
taskkill /F /IM python.exe /T >nul 2>&1
taskkill /F /FI "WINDOWTITLE eq Apex AI Bot*" /T >nul 2>&1
timeout /t 2 >nul

echo =========================================================
echo       2. Fetching & Resetting to Latest Code from GitHub...
echo =========================================================
git fetch --all
git reset --hard origin/main

echo =========================================================
echo       3. Clearing __pycache__ & stale bytecode...
echo =========================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /f /q *.pyc >nul 2>&1

echo =========================================================
echo       4. Starting Apex AI Bot with Clean Updated Code...
echo =========================================================
start start_vps.bat
echo [SUCCESS] Clean Git Update Complete! Bot successfully restarted.
pause
