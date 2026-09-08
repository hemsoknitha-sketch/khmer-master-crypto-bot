@echo off
title Khmer Master Crypto - Windows Local Git & VPS Auto-Push v13.00
cd /d "%~dp0"

echo ======================================================================
echo   🚀 KHMER MASTER CRYPTO - WINDOWS LOCAL TO CLOUD VPS DEPLOYER
echo ======================================================================
echo.

:: 1. Check Git Status
echo [1/3] Checking modified files...
git status -s

:: 2. Auto Stage & Commit
echo.
echo [2/3] Staging and committing changes...
git add .
git commit -m "Auto Update: Khmer Master Crypto AGI Engine v13.00"

:: 3. Push to GitHub Main Branch
echo.
echo [3/3] Pushing changes to GitHub (origin/main)...
git push origin main

echo.
echo ======================================================================
echo   ✅ [ជោគជ័យ ១០០%%] កូដថ្មីត្រូវបាន Push ទៅ GitHub រួចរាល់!
echo.
echo   💡 របៀបឱ្យ VPS ដំណើរការកូដថ្មីនេះ (ជ្រើសរើស ១ ក្នុងចំណោម ២) ៖
echo.
echo   វិធីទី ១ (ងាយស្រួលបំផុត) ៖
echo      គ្រាន់តែចូលទៅកាន់ Telegram រួចវាយបញ្ជា /sync_brain នោះ Bot នឹង Update ភ្លាម!
echo.
echo   វិធីទី ២ (ប្រសិនបើចង់ Restart VPS ទាំងស្រុង) ៖
echo      សូមបើក Browser ចូល Google Cloud Console -^> ចុចប៊ូតុង SSH ពណ៌ខៀវ
echo      រួចវាយពាក្យបញ្ជា ៖
echo         cd /opt/khmer-master-crypto-bot
echo         git pull origin main
echo         sudo systemctl restart khmer-master-crypto-bot
echo ======================================================================
echo.
pause
