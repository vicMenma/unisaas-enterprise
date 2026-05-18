# UniSaaS Enterprise

UniSaaS Enterprise is a multi-tenant Django 6 university ERP for admissions, academics, student registration, examinations, finance, audit logs, and notifications.

## Local Setup

1. Create a Python 3.12 virtual environment.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and adjust values.
4. Run migrations and seed optional demo data:

```bash
python manage.py migrate
python scripts/seed_demo.py
```

5. Start the app:

```bash
python manage.py runserver
```

The API is available under `/api/v1/`. Pass `X-Tenant-Slug: demo` for local demo requests.

## Verification

```bash
python manage.py check
python manage.py makemigrations --check --dry-run
python manage.py test
```

## Deployment

Render deployment is configured in `render.yaml`. Production must set `DJANGO_SETTINGS_MODULE=unisaas.settings.production`, `SECRET_KEY`, `ALLOWED_HOSTS`, and any CORS/CSRF origins.

Superuser creation is opt-in:

```bash
DJANGO_SUPERUSER_CREATE=true
DJANGO_SUPERUSER_EMAIL=admin@example.edu
DJANGO_SUPERUSER_PASSWORD=...
```
