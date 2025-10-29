<#
build.ps1

PowerShell helper to build a single-file Windows EXE using PyInstaller.
Run this from the project root (where manage.py lives).

Usage (PowerShell):
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser  # only if activation blocked
  .\build.ps1

This script will:
 - ensure pyinstaller is installed in the active Python environment
 - run PyInstaller with sensible --add-data flags for this repo layout

Edit the $Adds array below if your project layout differs.
#>

param()

function Ensure-Package {
    param(
        [string]$pkg
    )
    Write-Host "Ensuring $pkg is installed..."
    python -m pip show $pkg > $null 2>&1
    if ($LASTEXITCODE -ne 0) {
        python -m pip install --upgrade pip
        python -m pip install $pkg
    }
}

try {
    python --version > $null 2>&1
} catch {
    Write-Error "Python is not found in PATH. Install Python 3.11+ and add to PATH."
    exit 1
}

Ensure-Package -pkg pyinstaller

# Files / directories to include. Format: "source;dest"
# On Windows PyInstaller expects a semicolon in the pair.
$projectRoot = (Get-Location).Path

# Adjust/add paths here if your static/templates live elsewhere.
$Adds = @(
    "db.sqlite3;.",
    "paupahan;./paupahan",
    "paupahan\static;./paupahan/static",
    "paupahan\tenants\templates;./paupahan/tenants/templates"
)

$addArgs = $Adds | ForEach-Object { "--add-data `"$_`"" } | Out-String
$addArgs = $addArgs -replace "\r\n"," "

Write-Host "Running PyInstaller. This may take a minute..."

$piCmd = "py -3 -m PyInstaller --onefile $addArgs --name PaupahanApp run_app.py"
Write-Host $piCmd

Invoke-Expression $piCmd

if ($LASTEXITCODE -eq 0) {
    Write-Host "Build finished. Dist executable is in the 'dist' folder: dist\PaupahanApp.exe"
} else {
    Write-Error "PyInstaller failed. Check the output above for errors and adjust --add-data paths if needed."
}
