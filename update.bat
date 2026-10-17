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
echo   វិធីទី ១ (ស្វ័យប្រវត្ត ១០០%% ដោយមិនបាច់ធ្វើអ្វី) ៖
echo      នៅលើ Google Cloud VPS ប្រព័ន្ធ Cron Job ដំណើរការ auto_update_vps.sh
echo      រៀងរាល់ ២ នាទីម្តងដោយស្វ័យប្រវត្ត (Auto-Pull ^& Safe Restart Zero Data Loss)!
echo.
echo   វិធីទី ២ (ប្រសិនបើចង់ Update ភ្លាមៗលើ VPS តាម SSH) ៖
echo      សូមបើក Browser ចូល Google Cloud Console -^> ចុចប៊ូតុង SSH
echo      រួចវាយពាក្យបញ្ជា ៖
echo         cd /opt/khmer-master-crypto-bot ^&^& bash auto_update_vps.sh
echo.
echo   💡 ចំណាំ ៖ ពាក្យបញ្ជា /sync_brain ក្នុង Telegram គឺសម្រាប់ Hot-Reload ទម្ងន់
echo      AI Models ពី Hugging Face Hub។ ចំណែកកូដ Python គឺ Update តាមវិធីខាងលើ!
echo ======================================================================
echo.
pause

