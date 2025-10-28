Paupahan
========

Lightweight Django app for managing tenants, charges, and payments.

Quick start (local, without Docker)

1. Clone the repo and enter it:

```bash
git clone <repo-url>
cd Paupahan
```

2. Create and activate a virtual environment (zsh/bash):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies and run migrations:

```bash
pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```

Using Docker (recommended for reproducibility)

Build and run the app with Docker Compose (requires Docker & Docker Compose v2+):

```bash
docker compose up --build
# then visit http://localhost:8000
```

Notes
- Project uses SQLite by default (db.sqlite3). If you want a separate DB, update
  `paupahan/settings.py` or provide environment variables and modify `docker-compose.yml`.
- Do not commit secrets. Use an environment file (`.env`) for SECRET_KEY and other private settings.

Files added to help sharing:
- `Dockerfile` and `docker-compose.yml` — reproducible environment
- `.gitignore` — excludes venv and common artifacts
- `paupahan/tenants/tests/test_formatters.py` — unit test for the custom template filter
Paupahan — Tenant Payments

Minimal Django app to monitor tenant rent, water, and electricity payments.

Quick start

1. Create virtualenv and install:

   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

2. Run migrations and create superuser:

   python manage.py migrate
   python manage.py createsuperuser

3. Run server:

   python manage.py runserver

4. Open http://127.0.0.1:8000/ to see tenant list, or /admin/ to manage data.

Notes

- Admin can create tenants, charges (per month) and payments.
- A `Charge` contains rent, water and electric amounts for a tenant and a year/month.
- `Payment` can be attached to a `Charge` or be general; tenant balance = sum(charges) - sum(payments).
