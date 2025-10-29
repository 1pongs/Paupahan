<# internal/package_dist.ps1

Copy of the packaging helper. Run this after building the EXE and copying it into the package folder.

Usage (run from inside installer_package):
  .\internal\package_dist.ps1 -ExePath .\PaupahanApp.exe -OutZip ..\Paupahan-Installer.zip
#>

param(
    [string]$ExePath = ".\PaupahanApp.exe",
    [string]$OutZip = "..\Paupahan-Installer.zip"
)

if (-not (Test-Path $ExePath)) {
    Write-Error "Executable not found at: $ExePath"
    Write-Host "Copy the built EXE into the installer_package folder before running this script."
    exit 1
}

$tempDir = Join-Path -Path $env:TEMP -ChildPath ("paupahan_dist_" + [guid]::NewGuid().ToString())
New-Item -ItemType Directory -Path $tempDir | Out-Null

Copy-Item -Path $ExePath -Destination $tempDir -Force
Copy-Item -Path "..\start_installer.bat" -Destination $tempDir -Force
Copy-Item -Path "..\README_DIST.md" -Destination $tempDir -Force

if (Test-Path $OutZip) { Remove-Item $OutZip -Force }

Compress-Archive -Path (Join-Path $tempDir "*") -DestinationPath $OutZip -Force

Remove-Item -Recurse -Force $tempDir

Write-Host "Created $OutZip"
