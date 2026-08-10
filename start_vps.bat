@echo off
cd /d "%~dp0"
title Apex AI Bot - 24/7 VPS Server
color 0A

echo =========================================================
echo       Apex AI Bot is starting in 24/7 VPS Mode...
echo       Auto-Restart is ENABLED. 
echo       Logs are safely stored in vps_crash_logs.txt
echo =========================================================

:: Try Hardcoded VPS Python Path First
set PYTHON_CMD=C:\Users\Administrator\AppData\Local\Programs\Python\Python311\python.exe
if not exist "%PYTHON_CMD%" (
    :: Fallback to local python command for testing on local computer
    set PYTHON_CMD=python
    python --version >nul 2>&1
    if errorlevel 1 (
        echo [ERROR] Python is not installed or not in PATH! >> vps_crash_logs.txt
        echo [ERROR] Python is not installed or not in PATH!
        pause
        exit /b 1
    )
)

:loop
echo [%date% %time%] Starting Bot... >> vps_crash_logs.txt
echo [INFO] Bot is running... Do not close this window!

:: Fix Windows console encoding crashes (Emojis)
set PYTHONIOENCODING=utf-8
set PYTHONUTF8=1

:: Removed headless mode to show Admin Desktop
"%PYTHON_CMD%" self_healing_watchdog.py 2>> vps_crash_logs.txt

echo [%date% %time%] Bot Crashed or Stopped! Restarting in 10 seconds... >> vps_crash_logs.txt
echo [WARNING] Bot crashed or closed. Restarting in 10 seconds...
timeout /t 10
goto loop
