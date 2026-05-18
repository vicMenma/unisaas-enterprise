# Deployment

Production uses `unisaas.settings.production`.

Required environment variables:

- `SECRET_KEY`
- `ALLOWED_HOSTS`
- `DATABASE_URL`
- `DJANGO_SETTINGS_MODULE=unisaas.settings.production`

Recommended:

- `CORS_ALLOWED_ORIGINS`
- `CSRF_TRUSTED_ORIGINS`
- `CELERY_BROKER_URL`
- `CELERY_RESULT_BACKEND`

Render runs `./build.sh`, which installs dependencies, collects static files, runs migrations, optionally seeds demo data, and optionally creates a superuser from environment variables. It does not contain hardcoded production credentials.
