@echo off
REM start_installer.bat
REM Simple launcher for Paupahan distributable EXE.

setlocal
set EXE=PaupahanApp.exe

REM Check if the EXE exists next to this batch file
if exist "%~dp0%EXE%" (
    echo Starting Paupahan...
    start "Paupahan" "%~dp0%EXE%"
    exit /b 0
) else (
    echo.
    echo ERROR: %EXE% not found in this folder.
    echo Please place %EXE% into the same folder as this batch file and try again.
    echo You can also double-click the EXE directly if present.
    echo.
    pause
    exit /b 1
)
