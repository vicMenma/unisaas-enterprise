from django.db import models
from django.conf import settings
from apps.tenants.models import TenantModel

class Faculty(TenantModel):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class Department(TenantModel):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='departments')
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class AcademicYear(TenantModel):
    name = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["university", "name"], name="unique_tenant_academic_year")
        ]
        ordering = ["-start_date"]

    def __str__(self):
        return self.name


class Programme(TenantModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name="programmes")
    name = models.CharField(max_length=150)
    code = models.CharField(max_length=20)
    duration_years = models.PositiveIntegerField(default=3)
    degree_type = models.CharField(max_length=80, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["university", "code"], name="unique_tenant_programme_code")
        ]
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class Semester(TenantModel):
    name = models.CharField(max_length=50) # e.g., "Fall 2026"
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="semesters",
        null=True,
        blank=True,
    )
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Course(TenantModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    programme = models.ForeignKey(
        Programme,
        on_delete=models.SET_NULL,
        related_name="courses",
        null=True,
        blank=True,
    )
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    credits = models.PositiveIntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["university", "code"], name="unique_tenant_course_code")
        ]
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} - {self.name}"


class CourseAllocation(TenantModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="allocations")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="course_allocations")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name="course_allocations")
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name="course_allocations",
        null=True,
        blank=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["university", "course", "teacher", "semester"],
                name="unique_tenant_course_allocation",
            )
        ]

    def __str__(self):
        return f"{self.course.code} -> {self.teacher.email}"
