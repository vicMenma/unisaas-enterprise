from django.db import models
from tenants.models import TenantModel
from registration.models import EnrollmentCourse

class Grade(TenantModel):
    enrollment_course = models.OneToOneField(EnrollmentCourse, on_delete=models.CASCADE, related_name='grade')
    score = models.DecimalField(max_digits=5, decimal_places=2) # e.g., 85.50
    grade_points = models.DecimalField(max_digits=4, decimal_places=2) # e.g., 4.0 for A, 3.0 for B
    letter_grade = models.CharField(max_length=5) # e.g., 'A', 'B+'
    is_locked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.enrollment_course} - {self.letter_grade}"
