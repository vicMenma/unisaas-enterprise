from django.db import models
from tenants.models import TenantModel
from students.models import StudentProfile
from academic.models import Semester, Course

class Enrollment(TenantModel):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='enrollments')
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='enrollments')
    is_active = models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student', 'semester'], name='unique_tenant_student_semester_enrollment')
        ]

    def __str__(self):
        return f"{self.student.matricule} - {self.semester.name}"


class EnrollmentCourse(TenantModel):
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name='courses')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['enrollment', 'course'], name='unique_tenant_enrollment_course')
        ]

    def __str__(self):
        return f"{self.enrollment} -> {self.course.code}"
