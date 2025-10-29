<# internal/build.ps1

Copy of the build script for the sender; run this on your Windows dev machine to build the EXE.
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
