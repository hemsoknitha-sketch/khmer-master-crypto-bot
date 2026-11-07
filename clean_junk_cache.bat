@echo off
title Angkor Quant - Safe Disk Cleanup Utility
echo Running PowerShell Cleanup Script with Elevated Rights if Needed...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0clean_junk_cache.ps1"
pause

