$ErrorActionPreference = "Stop"

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

Write-Host "== Reality Route Helper local safe test ==" -ForegroundColor Cyan
Write-Host "Project: $ProjectRoot"

$TempRoot = Join-Path $env:TEMP ("rrh-test-" + [guid]::NewGuid())
$ConfigPath = Join-Path $TempRoot "config.json"
$BackupDir = Join-Path $TempRoot "backups"

New-Item -ItemType Directory -Path $TempRoot -Force | Out-Null

$env:RRH_CONFIG_PATH = $ConfigPath
$env:RRH_BACKUP_DIR = $BackupDir
$env:RRH_DISABLE_RESTART = "1"
$env:PYTHONPATH = $ProjectRoot

try {
    Write-Host ""
    Write-Host "1. Python version" -ForegroundColor Yellow
    python --version

    Write-Host ""
    Write-Host "2. Compile Python files" -ForegroundColor Yellow
    Get-ChildItem -Recurse -Filter "*.py" |
        Where-Object {
            $_.FullName -notmatch "\\\.venv\\" -and
            $_.FullName -notmatch "\\build\\" -and
            $_.FullName -notmatch "\\dist\\"
        } |
        ForEach-Object {
            python -m py_compile $_.FullName
        }

    Write-Host ""
    Write-Host "3. Run smoke tests in sandbox" -ForegroundColor Yellow
    python .\tests\smoke_test.py

    Write-Host ""
    Write-Host "4. Run menu flow tests in sandbox" -ForegroundColor Yellow
    python .\tests\menu_flow_test.py

    Write-Host ""
    Write-Host "5. Sandbox files" -ForegroundColor Yellow
    if (Test-Path $TempRoot) {
        Get-ChildItem -Recurse $TempRoot | ForEach-Object {
            Write-Host $_.FullName
        }
    }

    Write-Host ""
    Write-Host "Safe test completed successfully." -ForegroundColor Green
}
finally {
    Remove-Item Env:\RRH_CONFIG_PATH -ErrorAction SilentlyContinue
    Remove-Item Env:\RRH_BACKUP_DIR -ErrorAction SilentlyContinue
    Remove-Item Env:\RRH_DISABLE_RESTART -ErrorAction SilentlyContinue

    if (Test-Path $TempRoot) {
        Remove-Item -Recurse -Force $TempRoot -ErrorAction SilentlyContinue
    }
}
