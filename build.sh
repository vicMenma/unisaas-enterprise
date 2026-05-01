#!/usr/bin/env bash
# Render build script — runs on every deploy
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Create a default university + superuser if they don't exist
python manage.py shell -c "
from tenants.models import University
from accounts.models import User

uni, created = University.objects.get_or_create(
    slug='demo',
    defaults={
        'name': 'UniSaaS Demo University',
        'matricule_prefix': 'DEMO',
    }
)
if created:
    print('Created demo university')

if not User.objects.filter(email='admin@unisaas.com').exists():
    User.objects.create_superuser(email='admin@unisaas.com', password='UniSaaS2026!')
    print('Created superuser: admin@unisaas.com / UniSaaS2026!')
else:
    print('Superuser already exists')
"
