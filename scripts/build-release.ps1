$ErrorActionPreference = "Stop"

Write-Host "Building Reality Route Helper for local Windows..." -ForegroundColor Cyan

python -m pip install -U pip pyinstaller

$Arch = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString().ToLower()

switch ($Arch) {
    "x64"   { $ArchName = "amd64" }
    "arm64" { $ArchName = "arm64" }
    default {
        throw "Unsupported architecture: $Arch"
    }
}

$Name = "rrh-windows-$ArchName"

python -m PyInstaller --clean --onefile --name $Name rrh.py

Write-Host "Build complete:" -ForegroundColor Green
Write-Host "dist\$Name.exe"
