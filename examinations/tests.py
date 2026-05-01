from django.test import TestCase
from tenants.models import University
from accounts.models import User
from academic.models import Course, Semester, Faculty, Department
from students.models import StudentProfile
from registration.models import Enrollment, EnrollmentCourse
from .models import Grade
from .services import GPAService

class GPAServiceTest(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name="Exam Uni", slug="exam")
        self.user = User.objects.create_user(email="s1@test.com", university=self.uni, password="p")
        self.student = StudentProfile.objects.create(user=self.user, university=self.uni, matricule="S1", entry_year=2026)
        
        self.faculty = Faculty.objects.create(university=self.uni, name="Science", code="SCI")
        self.dept = Department.objects.create(university=self.uni, faculty=self.faculty, name="CS", code="CS")
        self.semester = Semester.objects.create(university=self.uni, name="Fall", start_date="2026-01-01", end_date="2026-06-01")
        
        self.c1 = Course.objects.create(university=self.uni, department=self.dept, code="CS101", name="P1", credits=4)
        self.c2 = Course.objects.create(university=self.uni, department=self.dept, code="CS102", name="P2", credits=3)
        
        self.enrollment = Enrollment.objects.create(university=self.uni, student=self.student, semester=self.semester)
        self.e1 = EnrollmentCourse.objects.create(university=self.uni, enrollment=self.enrollment, course=self.c1)
        self.e2 = EnrollmentCourse.objects.create(university=self.uni, enrollment=self.enrollment, course=self.c2)

    def test_gpa_calculation_logic(self):
        """
        Verify GPA calculation: (Grade * Credits) / Total Credits
        """
        Grade.objects.create(university=self.uni, enrollment_course=self.e1, score=90, grade_points=4.0, letter_grade='A')
        Grade.objects.create(university=self.uni, enrollment_course=self.e2, score=80, grade_points=3.0, letter_grade='B')
        
        gpa = GPAService.calculate_gpa(self.enrollment)
        
        # (4.0*4 + 3.0*3) / 7 = (16 + 9) / 7 = 25 / 7 = 3.57
        self.assertAlmostEqual(float(gpa), 3.57, places=2)
