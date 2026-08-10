@echo off
title Auto Update via Download
echo =========================================
echo    Downloading new updates...
echo =========================================

cd /d "%~dp0"

:: ទាញយកកូដថ្មីជា .zip ពី URL (ប្តូរ URL ទៅកាន់ Link Download របស់អ្នក)
powershell -Command "Invoke-WebRequest -Uri 'https://yoursite.com/update.zip' -OutFile 'update.zip'"

:: ពន្លា File zip (Extract) រួច Replace ពីលើ File ចាស់ដោយស្វ័យប្រវត្តិ
powershell -Command "Expand-Archive -Path 'update.zip' -DestinationPath '.' -Force"

:: លុប File zip ចោលវិញបន្ទាប់ពីពន្លារួច
del update.zip

:: ដំឡើង Library ថ្មីៗ
echo Updating dependencies...
pip install -r requirements.txt

echo Update Done!
pause
