# Paupahan — Quick Start for non-technical users

Thank you for trying Paupahan! This package contains a single executable that runs a local web server and opens the app in your default browser. No programming tools are required.

Files included
- `PaupahanApp.exe`  — The application executable (may be named `PaupahanApp.exe`).
- `start_installer.bat` — Double-click this to run the application.
- `README_DIST.md` — This file (what you're reading).

How to run
1. Double-click `start_installer.bat`.
2. The app will start a local web server and your browser should open automatically to:
   http://127.0.0.1:8000
3. When you are done, close the browser tab and then close the app window (if a console window stays open, you can close it).

Notes and troubleshooting
- Windows Firewall: the first time you run the EXE, Windows may show a firewall prompt asking to allow network access. Choose "Allow" for Private networks if you want to use the app locally. If you don't want to allow incoming network connections, that's fine; the app listens on the local interface only (127.0.0.1).
- If double-clicking does nothing, open the folder and confirm `PaupahanApp.exe` and `start_installer.bat` are in the same directory. Double-click `PaupahanApp.exe` directly.
- If the browser doesn't open automatically, open your browser and point it to: http://127.0.0.1:8000
- This is a local (development) server intended for local use only. Do not expose it to the public internet.

Common questions
- Q: Do I need to install Python or other software?
  A: No. The EXE bundles the necessary runtime.
- Q: How do I stop the app?
  A: Close the browser window, then close the open app window (or press Ctrl+C in the console if visible).
- Q: I see an antivirus warning. Is this safe?
  A: The EXE was built locally and contains a bundled Python runtime. Some antivirus tools may flag new unsigned executables; if you trust the sender, allow the app. For broad distribution, code signing is recommended.

If something doesn't work
- Contact the person who sent you the file and let them know the error message (or take a screenshot).

Enjoy Paupahan!
