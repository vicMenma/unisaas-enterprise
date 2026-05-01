from django.db import models
from tenants.models import TenantModel

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

class Semester(TenantModel):
    name = models.CharField(max_length=50) # e.g., "Fall 2026"
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Course(TenantModel):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='courses')
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=200)
    credits = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.code} - {self.name}"
