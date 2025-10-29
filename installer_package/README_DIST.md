# Paupahan — Quick Start (package folder)

This folder is intended for distribution to non-technical users.

Files they need to use:
- `start_installer.bat` — Double-click this to run the application executable (PaupahanApp.exe).
- `PaupahanApp.exe` — (Not included here) Place the built executable in this folder before sending.
- `README_DIST.md` — This file (instructions for recipients).

Internal files (for the sender):
- `internal\build.ps1` — PowerShell script to build the EXE locally using PyInstaller.
- `internal\package_dist.ps1` — PowerShell script to produce a ZIP with the EXE and distribution files.

How to prepare the package (for the sender)
1. Build the EXE locally using `build.ps1` (see internal folder), it will produce `dist\PaupahanApp.exe`.
2. Copy `dist\PaupahanApp.exe` into this folder.
3. Optionally run `internal\package_dist.ps1 -ExePath .\PaupahanApp.exe -OutZip .\Paupahan-Installer.zip` to create a ZIP ready to send.

What recipients should do
1. Extract the ZIP to a folder.
2. Double-click `start_installer.bat` (or `PaupahanApp.exe`) to run the app.
