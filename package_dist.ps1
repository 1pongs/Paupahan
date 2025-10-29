<#
package_dist.ps1

Helper to build a distributable ZIP that contains:
 - PaupahanApp.exe (expects it at the provided path)
 - start_installer.bat
 - README_DIST.md

Usage (PowerShell, run from project root):
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser  # if needed
  .\package_dist.ps1 -ExePath .\dist\PaupahanApp.exe -OutZip .\Paupahan-Installer.zip

#>

param(
    [string]$ExePath = ".\dist\PaupahanApp.exe",
    [string]$OutZip = ".\Paupahan-Installer.zip"
)

if (-not (Test-Path $ExePath)) {
    Write-Error "Executable not found at: $ExePath"
    Write-Host "Build the EXE first (run build.ps1), or specify -ExePath to the correct EXE location."
    exit 1
}

$tempDir = Join-Path -Path $env:TEMP -ChildPath ("paupahan_dist_" + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $tempDir | Out-Null

Copy-Item -Path $ExePath -Destination $tempDir -Force
Copy-Item -Path ".\start_installer.bat" -Destination $tempDir -Force
Copy-Item -Path ".\README_DIST.md" -Destination $tempDir -Force

if (Test-Path $OutZip) { Remove-Item $OutZip -Force }

Compress-Archive -Path (Join-Path $tempDir "*") -DestinationPath $OutZip -Force

Remove-Item -Recurse -Force $tempDir

Write-Host "Created $OutZip"
