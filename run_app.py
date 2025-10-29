"""run_app.py

Small wrapper to start the Django development server and open the default
web browser. Designed to be bundled into a single-file executable with
PyInstaller.

Place this file at the project root next to `manage.py`.
"""
import os
import sys
import threading
import webbrowser


# If frozen by PyInstaller, resources are extracted to _MEIPASS
if getattr(sys, "frozen", False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

# Ensure project root is importable (so 'paupahan' package imports work)
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

os.chdir(base_dir)

# Use the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "paupahan.settings")


def start_django():
    # Run Django's runserver management command
    from django.core.management import execute_from_command_line

    # Use 127.0.0.1 to avoid exposing to external interfaces by default
    execute_from_command_line(["manage.py", "runserver", "127.0.0.1:8000"])


def main():
    # Setup Django
    import django

    django.setup()

    # Start Django in a background thread so we can open the browser from main thread
    t = threading.Thread(target=start_django, daemon=True)
    t.start()

    # Open the default browser to the local site
    try:
        webbrowser.open("http://127.0.0.1:8000")
    except Exception:
        pass

    # Keep the main thread alive while the server thread runs
    try:
        t.join()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
