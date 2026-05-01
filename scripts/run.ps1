$ErrorActionPreference = "Stop"

$Repo = "forgottenlab/reality-route-helper"
$TempDir = Join-Path $env:TEMP ("reality-route-helper-" + [guid]::NewGuid())

New-Item -ItemType Directory -Path $TempDir | Out-Null

try {
    $Arch = [System.Runtime.InteropServices.RuntimeInformation]::OSArchitecture.ToString().ToLower()

    switch ($Arch) {
        "x64"   { $ArchName = "amd64" }
        "arm64" { $ArchName = "arm64" }
        default {
            throw "Unsupported architecture: $Arch"
        }
    }

    $ExeName = "rrh-windows-$ArchName.exe"
    $DownloadUrl = "https://github.com/$Repo/releases/latest/download/$ExeName"
    $ExePath = Join-Path $TempDir $ExeName

    Write-Host "Downloading: $DownloadUrl" -ForegroundColor Cyan
    Invoke-WebRequest -Uri $DownloadUrl -OutFile $ExePath -UseBasicParsing

    Write-Host "Starting Reality Route Helper..." -ForegroundColor Green
    & $ExePath
}
finally {
    Remove-Item -Recurse -Force $TempDir -ErrorAction SilentlyContinue
}
