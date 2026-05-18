#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-unisaas.settings.production}"

python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate --noinput

if [ "${SEED_DEMO_DATA:-false}" = "true" ]; then
  python scripts/seed_demo.py
fi

if [ "${DJANGO_SUPERUSER_CREATE:-false}" = "true" ]; then
  python manage.py shell -c "
import os
from apps.tenants.models import University
from apps.accounts.models import User

email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
tenant_slug = os.environ.get('DJANGO_SUPERUSER_TENANT', 'system')

if not email or not password:
    raise SystemExit('DJANGO_SUPERUSER_EMAIL and DJANGO_SUPERUSER_PASSWORD are required when DJANGO_SUPERUSER_CREATE=true')

university, _ = University.objects.get_or_create(
    slug=tenant_slug,
    defaults={'name': 'System Administration', 'matricule_prefix': 'SYS'},
)

if not User.objects.filter(university=university, email=email.lower()).exists():
    User.objects.create_superuser(email=email, password=password, university=university)
    print(f'Created superuser {email}')
else:
    print(f'Superuser {email} already exists')
"
fi
