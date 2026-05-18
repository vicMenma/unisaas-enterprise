import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "unisaas.settings.local")

import django

django.setup()

from apps.academic.models import AcademicYear, Course, Department, Faculty, Programme, Semester
from apps.accounts.models import User
from apps.tenants.models import University


def run():
    university, _ = University.objects.get_or_create(
        slug="demo",
        defaults={"name": "UniSaaS Demo University", "matricule_prefix": "DEMO"},
    )
    admin, created = User.objects.get_or_create(
        university=university,
        email="admin@demo.edu",
        defaults={"role": "university_admin", "is_staff": True},
    )
    if created:
        admin.set_password("ChangeMe123!")
        admin.save()

    faculty, _ = Faculty.objects.get_or_create(university=university, code="SCI", defaults={"name": "Science"})
    department, _ = Department.objects.get_or_create(
        university=university,
        code="CS",
        defaults={"name": "Computer Science", "faculty": faculty},
    )
    year, _ = AcademicYear.objects.get_or_create(
        university=university,
        name="2026/2027",
        defaults={"start_date": "2026-09-01", "end_date": "2027-06-30", "is_active": True},
    )
    programme, _ = Programme.objects.get_or_create(
        university=university,
        code="BSC-CS",
        defaults={"name": "BSc Computer Science", "department": department, "duration_years": 4},
    )
    semester, _ = Semester.objects.get_or_create(
        university=university,
        name="Fall 2026",
        defaults={"academic_year": year, "start_date": "2026-09-01", "end_date": "2026-12-20", "is_active": True},
    )
    Course.objects.get_or_create(
        university=university,
        code="CS101",
        defaults={"name": "Introduction to Programming", "department": department, "programme": programme, "credits": 4},
    )
    print(f"Demo tenant ready: {university.slug} ({semester.name})")


if __name__ == "__main__":
    run()
