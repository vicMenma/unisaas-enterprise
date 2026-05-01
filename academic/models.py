from django.db import models
from tenants.models import TenantModel

class Semester(TenantModel):
    name = models.CharField(max_length=100) # e.g., "Fall 2026"
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['university', 'name'], name='unique_tenant_semester_name')
        ]

    def __str__(self):
        return f"{self.name} ({self.university.slug})"


class Course(TenantModel):
    code = models.CharField(max_length=20) # e.g., "CS101"
    title = models.CharField(max_length=255)
    credits = models.IntegerField(default=3)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['university', 'code'], name='unique_tenant_course_code')
        ]

    def __str__(self):
        return f"{self.code} - {self.title}"
