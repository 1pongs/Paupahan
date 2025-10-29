@echo off
REM start_installer.bat (packaged copy)
setlocal
set EXE=PaupahanApp.exe
if exist "%~dp0%EXE%" (
    echo Starting Paupahan...
    start "Paupahan" "%~dp0%EXE%"
    exit /b 0
) else (
    echo.
    echo ERROR: %EXE% not found in this folder.
    echo Please copy the built PaupahanApp.exe into this folder before sending to recipients.
    echo.
    pause
    exit /b 1
)
