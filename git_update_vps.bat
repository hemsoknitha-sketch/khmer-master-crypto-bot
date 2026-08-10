@echo off
title Apex AI Bot - Git 1-Click Auto Update
cd /d "%~dp0"

echo =========================================================
echo       1. Pulling Latest Code from Git Repository...
echo =========================================================
git pull origin main
if errorlevel 1 (
    echo [WARNING] Git pull encountered conflicts or issue. Retrying with force checkout...
    git fetch --all
    git reset --hard origin/main
)

echo =========================================================
echo       2. Stopping old running Python process...
echo =========================================================
taskkill /F /IM python.exe /T >nul 2>&1

echo =========================================================
echo       3. Clearing __pycache__ & stale bytecode...
echo =========================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /f /q *.pyc >nul 2>&1

echo =========================================================
echo       4. Starting Apex AI Bot with Clean Updated Code...
echo =========================================================
start start_vps.bat
echo [SUCCESS] Git Update Complete! Bot successfully restarted.
pause
