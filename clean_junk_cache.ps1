<#
.SYNOPSIS
    Angkor Quant - Safe Disk Cleanup & Cache Purge Utility
    Author: HEM SINATH / Angkor Quant Quantitative Engineering
    Version: 1.0.0
    Description:
        Safely scans and purges unnecessary AI model caches, temporary compiler files,
        and deprecated editor caches while strictly protecting critical assets (.ssh, .vscode, .rustup, .gemini).
#>

[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$Host.UI.RawUI.WindowTitle = "Angkor Quant - Safe Disk Cleanup Utility"

Clear-Host
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "       ANGKOR QUANT - SAFE DISK CLEANUP & CACHE PURGE UTILITY           " -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Cyan
Write-Host "  [i] Scanning cache directories for safe cleanup targets...`n" -ForegroundColor Gray

# Define target paths with descriptions and category
$targets = @(
    @{
        Path = "C:\Users\sokni\.cache\huggingface\hub"
        Name = "HuggingFace Model Weights Cache (hub)"
        Category = "AI Model Weights (~6.8 GB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.cache\huggingface\xet"
        Name = "HuggingFace Temp Transfers (xet)"
        Category = "AI Temp Cache"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.cache\torch"
        Name = "PyTorch Kernel & Model Cache"
        Category = "PyTorch Cache (~114 MB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.codex"
        Name = "OpenAI Codex CLI Cache"
        Category = "AI Tool Cache (~609 MB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.grok"
        Name = "Grok Tool Cache"
        Category = "AI Tool Cache (~357 MB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.windsurf"
        Name = "Windsurf Editor Cache"
        Category = "Editor Cache (~250 MB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\output"
        Name = "Old Script Generated Outputs"
        Category = "Outputs/Exports (~36.8 MB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.solcx"
        Name = "Solidity Compiler Binaries"
        Category = "Solidity Cache (~8.8 MB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.codeium"
        Name = "Codeium AI Cache"
        Category = "AI Extension Cache (~5.4 MB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.matplotlib"
        Name = "Matplotlib Font Cache"
        Category = "Python Cache (~356 KB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.agents"
        Name = "AI Agents Logs & Cache"
        Category = "Agent Cache (~4.2 MB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.cagent"
        Name = "CAgent Cache"
        Category = "Agent Cache (~20 KB)"
        Safe = $true
    },
    @{
        Path = "C:\Users\sokni\.qwen"
        Name = "Qwen CLI Cache"
        Category = "AI Cache (~84 KB)"
        Safe = $true
    }
)

# Scan target sizes
$foundItems = @()
$totalBytes = 0

foreach ($t in $targets) {
    if (Test-Path -LiteralPath $t.Path) {
        try {
            $measure = Get-ChildItem -LiteralPath $t.Path -Recurse -Force -ErrorAction SilentlyContinue | Measure-Object -Property Length -Sum
            $bytes = if ($measure.Sum) { $measure.Sum } else { 0 }
            $sizeMB = [math]::Round($bytes / 1MB, 2)
            $sizeGB = [math]::Round($bytes / 1GB, 2)
            
            $foundItems += [PSCustomObject]@{
                Category = $t.Category
                Name     = $t.Name
                Path     = $t.Path
                SizeMB   = $sizeMB
                SizeGB   = $sizeGB
                Bytes    = $bytes
            }
            $totalBytes += $bytes
        } catch {
            Write-Warning "Could not measure size of: $($t.Path)"
        }
    }
}

if ($foundItems.Count -eq 0) {
    Write-Host " [OK] No junk cache found. Your disk is already clean!" -ForegroundColor Green
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

# Display results
Write-Host "Found the following safe cleanup items:" -ForegroundColor White
Write-Host "------------------------------------------------------------------------" -ForegroundColor DarkGray
$foundItems | Format-Table -Property Category, Name, SizeMB -AutoSize
Write-Host "------------------------------------------------------------------------" -ForegroundColor DarkGray
$totalMB = [math]::Round($totalBytes / 1MB, 2)
$totalGB = [math]::Round($totalBytes / 1GB, 2)
Write-Host "Total space to reclaim: $totalMB MB ($totalGB GB)" -ForegroundColor Green -BackgroundColor Black

Write-Host "`n[SAFETY GUARANTEE]" -ForegroundColor Yellow
Write-Host "  [+] PRESERVED: C:\Users\sokni\.ssh               (SSH Keys & VPS Access Protected 100%)" -ForegroundColor Green
Write-Host "  [+] PRESERVED: C:\Users\sokni\.cache\huggingface\token (Login Credentials Preserved)" -ForegroundColor Green
Write-Host "  [+] PRESERVED: C:\Users\sokni\.vscode            (VS Code Extensions Preserved)" -ForegroundColor Green
Write-Host "  [+] PRESERVED: C:\Users\sokni\.rustup            (Rust Toolchain Preserved)" -ForegroundColor Green
Write-Host "  [+] PRESERVED: C:\Users\sokni\.gemini            (Core Agent & IDE Settings Preserved)" -ForegroundColor Green
Write-Host "  [+] PRESERVED: All Project Source Code on Drive E: (100% Untouched)" -ForegroundColor Green

Write-Host "`nDo you want to proceed with purging these cache files? (y/n): " -ForegroundColor Cyan -NoNewline
$response = Read-Host

if ($response -notmatch '^[Yy]$') {
    Write-Host "`n[CANCELLED] Operation aborted by user. No files were deleted." -ForegroundColor Yellow
    Write-Host "Press any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 0
}

Write-Host "`nStarting cleanup..." -ForegroundColor Cyan
$freedBytes = 0

foreach ($item in $foundItems) {
    Write-Host "  Cleaning: $($item.Name)... " -NoNewline
    try {
        if (Test-Path -LiteralPath $item.Path) {
            Remove-Item -LiteralPath $item.Path -Recurse -Force -ErrorAction Stop
            Write-Host "[DONE] (Freed $($item.SizeMB) MB)" -ForegroundColor Green
            $freedBytes += $item.Bytes
        } else {
            Write-Host "[SKIPPED - Already removed]" -ForegroundColor Gray
        }
    } catch {
        Write-Host "[FAILED: $($_.Exception.Message)]" -ForegroundColor Red
    }
}

$freedMB = [math]::Round($freedBytes / 1MB, 2)
$freedGB = [math]::Round($freedBytes / 1GB, 2)

Write-Host "`n========================================================================" -ForegroundColor Green
Write-Host " CLEANUP COMPLETE! Total Freed Disk Space: $freedMB MB ($freedGB GB)" -ForegroundColor Yellow
Write-Host "========================================================================" -ForegroundColor Green
Write-Host "`nPress any key to close this window..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

