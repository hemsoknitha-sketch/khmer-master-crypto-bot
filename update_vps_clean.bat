@echo off
title Apex AI Bot Clean Updater
cd /d "%~dp0"

echo =========================================================
echo       1. Stopping all running Python process on VPS...
echo =========================================================
taskkill /F /IM python.exe /T >nul 2>&1

echo =========================================================
echo       2. Clearing all __pycache__ & stale .pyc files...
echo =========================================================
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"
del /f /q *.pyc >nul 2>&1
del /f /q *.py.bak >nul 2>&1

echo =========================================================
echo       3. Verifying latest python code integrity...
echo =========================================================
set PYTHON_CMD=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe
if not exist "%PYTHON_CMD%" (
    set PYTHON_CMD=python
)

"%PYTHON_CMD%" -c "import trading_engine; import bot_thread; print('✅ All latest code syntax verified OK!')"

echo =========================================================
echo       4. Starting Apex AI Bot with Latest Code...
echo =========================================================
start start_vps.bat
pause
