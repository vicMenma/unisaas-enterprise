import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unisaas.settings.local")

import django

django.setup()

from apps.tenants.models import University


def run():
    university, created = University.objects.get_or_create(
        slug="demo",
        defaults={
            "name": "UniSaaS Demo University",
            "matricule_prefix": "DEMO",
            "matricule_pattern": {
                "format": "{prefix}-{year}-{program}-{level}-{sequence}",
                "sequence_length": 4,
            },
        },
    )
    print(("Created" if created else "Found") + f" {university.name}")
    return university


if __name__ == "__main__":
    run()
