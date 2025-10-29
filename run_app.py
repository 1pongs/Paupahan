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
import logging
import time
import tempfile


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
    # Start Django's development server in-process. When packaged by
    # PyInstaller the normal autoreloader used by runserver can fork and
    # confuse the bundled binary; calling the command with
    # use_reloader=False avoids that and keeps the server running in
    # this thread.
    try:
        from django.core.management import call_command

        logging.info("Starting Django runserver on 127.0.0.1:8000")
        # Call runserver without the autoreloader so it stays in this process
        call_command("runserver", "127.0.0.1:8000", use_reloader=False)
    except Exception:
        logging.exception("Failed to start Django runserver")
        raise


def main():
    # Setup Django
    import django

    django.setup()

    # Configure a simple file logger so we can inspect errors when running
    # the bundled EXE (double-clicks don't show a console). Place the log
    # in the temp dir when frozen, otherwise next to the project.
    try:
        if getattr(sys, "frozen", False):
            log_dir = tempfile.gettempdir()
        else:
            log_dir = base_dir
        log_file = os.path.join(log_dir, "paupahan_run.log")
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(levelname)s %(message)s",
            handlers=[logging.FileHandler(log_file, encoding="utf-8"), logging.StreamHandler()],
        )
        logging.info("run_app started; logging to %s", log_file)
    except Exception:
        # If logging setup fails, continue without file logging
        pass

    # Ensure database migrations are applied so the bundled app has the
    # required tables (the release build doesn't include a pre-built
    # db.sqlite3). Running migrations here creates the sqlite DB if it
    # doesn't exist.
    try:
        from django.core.management import call_command

        logging.info("Applying database migrations...")
        call_command("migrate", "--noinput")
        logging.info("Migrations applied")
    except Exception:
        logging.exception("Failed to apply migrations")

    # Start Django in a background thread so we can open the browser from
    # the main thread. Because we disabled the autoreloader above, the
    # server will run in this thread until stopped.
    t = threading.Thread(target=start_django, daemon=True)
    t.start()

    # Give the server a short moment to start then open the browser
    try:
        # small wait to let the server bind
        time.sleep(1.0)
        webbrowser.open("http://127.0.0.1:8000")
    except Exception:
        logging.exception("Failed to open web browser")

    # Keep the main thread alive while the server thread runs
    try:
        t.join()
    except KeyboardInterrupt:
        logging.info("Interrupted by user, exiting")


if __name__ == "__main__":
    main()
