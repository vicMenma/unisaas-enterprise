from decimal import Decimal

from django.test import TestCase
from rest_framework.test import APIClient

from apps.academic.models import Course, CourseAllocation, Department, Faculty, Semester
from apps.accounts.models import User
from apps.admissions.models import Application
from apps.audit.models import AuditLog
from apps.examinations.models import Grade
from apps.finance.models import Invoice, Payment
from apps.notifications.models import Notification
from apps.registration.models import Enrollment, EnrollmentCourse
from apps.students.models import StudentProfile
from apps.tenants.models import University


class UniSaaSApiTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.uni = University.objects.create(name="Demo University", slug="demo", matricule_prefix="DMO")
        self.other_uni = University.objects.create(name="Other University", slug="other", matricule_prefix="OTH")
        self.admin = User.objects.create_user(
            email="admin@example.edu",
            university=self.uni,
            password="pass12345",
            role="university_admin",
        )
        self.registration = User.objects.create_user(
            email="reg@example.edu",
            university=self.uni,
            password="pass12345",
            role="registration",
        )
        self.examiner = User.objects.create_user(
            email="exam@example.edu",
            university=self.uni,
            password="pass12345",
            role="examination",
        )
        self.teacher = User.objects.create_user(
            email="teacher@example.edu",
            university=self.uni,
            password="pass12345",
            role="teacher",
        )
        self.student_user = User.objects.create_user(
            email="student@example.edu",
            university=self.uni,
            password="pass12345",
            role="student",
        )
        self.student = StudentProfile.objects.create(
            university=self.uni,
            user=self.student_user,
            matricule="DMO-2026-CS-1-0001",
            program_id="CS",
            entry_year=2026,
            current_level="1",
        )
        self.faculty = Faculty.objects.create(university=self.uni, name="Science", code="SCI")
        self.department = Department.objects.create(
            university=self.uni,
            faculty=self.faculty,
            name="Computer Science",
            code="CS",
        )
        self.semester = Semester.objects.create(
            university=self.uni,
            name="Fall 2026",
            start_date="2026-09-01",
            end_date="2026-12-20",
        )
        self.course = Course.objects.create(
            university=self.uni,
            department=self.department,
            code="CS101",
            name="Programming",
            credits=4,
        )

    def tenant_headers(self, slug="demo"):
        return {"HTTP_X_TENANT_SLUG": slug}

    def authenticate(self, user):
        self.client.force_authenticate(user=user)

    def test_jwt_login_and_me_are_tenant_scoped(self):
        response = self.client.post(
            "/api/v1/auth/login/",
            {"email": "admin@example.edu", "password": "pass12345"},
            format="json",
            **self.tenant_headers(),
        )
        self.assertEqual(response.status_code, 200)
        token = response.data["access"]

        me = self.client.get(
            "/api/v1/auth/me/",
            HTTP_AUTHORIZATION=f"Bearer {token}",
            **self.tenant_headers(),
        )
        self.assertEqual(me.status_code, 200)
        self.assertEqual(me.data["email"], "admin@example.edu")

        wrong_tenant = self.client.get(
            "/api/v1/auth/me/",
            HTTP_AUTHORIZATION=f"Bearer {token}",
            **self.tenant_headers("other"),
        )
        self.assertEqual(wrong_tenant.status_code, 403)

    def test_cross_tenant_foreign_key_is_rejected(self):
        other_user = User.objects.create_user(
            email="otherstudent@example.edu",
            university=self.other_uni,
            password="pass12345",
            role="student",
        )
        other_student = StudentProfile.objects.create(
            university=self.other_uni,
            user=other_user,
            matricule="OTH-001",
            program_id="CS",
            entry_year=2026,
            current_level="1",
        )
        self.authenticate(self.registration)
        response = self.client.post(
            "/api/v1/enrollments/",
            {"student": str(other_student.id), "semester": str(self.semester.id)},
            format="json",
            **self.tenant_headers(),
        )
        self.assertEqual(response.status_code, 400)

    def test_application_acceptance_creates_student_finance_audit_notification(self):
        application = Application.objects.create(
            university=self.uni,
            first_name="Ada",
            last_name="Lovelace",
            email="ada@example.edu",
            program_applied="Computer Science",
            entry_year=2026,
        )
        self.authenticate(self.registration)
        response = self.client.post(
            f"/api/v1/applications/{application.id}/accept/",
            {},
            format="json",
            **self.tenant_headers(),
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(StudentProfile.objects.filter(user__email="ada@example.edu", university=self.uni).exists())
        self.assertTrue(Invoice.objects.filter(student__user__email="ada@example.edu", university=self.uni).exists())
        self.assertTrue(Notification.objects.filter(recipient__email="ada@example.edu", university=self.uni).exists())
        self.assertTrue(AuditLog.objects.filter(action="Application Accepted", university=self.uni).exists())

    def test_duplicate_enrollment_is_prevented(self):
        self.authenticate(self.registration)
        payload = {
            "student": str(self.student.id),
            "semester": str(self.semester.id),
            "course_ids": [str(self.course.id)],
        }
        first = self.client.post("/api/v1/enrollments/", payload, format="json", **self.tenant_headers())
        second = self.client.post("/api/v1/enrollments/", payload, format="json", **self.tenant_headers())
        self.assertEqual(first.status_code, 201)
        self.assertEqual(second.status_code, 400)

    def test_grade_approval_locks_future_changes(self):
        enrollment = Enrollment.objects.create(university=self.uni, student=self.student, semester=self.semester)
        enrollment_course = EnrollmentCourse.objects.create(
            university=self.uni,
            enrollment=enrollment,
            course=self.course,
        )
        self.authenticate(self.examiner)
        created = self.client.post(
            "/api/v1/grades/",
            {"enrollment_course": str(enrollment_course.id), "score": "91.00"},
            format="json",
            **self.tenant_headers(),
        )
        self.assertEqual(created.status_code, 201)
        grade_id = created.data["id"]
        approved = self.client.post(f"/api/v1/grades/{grade_id}/approve/", {}, format="json", **self.tenant_headers())
        self.assertEqual(approved.status_code, 200)
        self.assertTrue(Grade.objects.get(id=grade_id).is_locked)
        changed = self.client.patch(
            f"/api/v1/grades/{grade_id}/",
            {"score": "72.00"},
            format="json",
            **self.tenant_headers(),
        )
        self.assertEqual(changed.status_code, 403)

    def test_teacher_can_only_grade_allocated_courses(self):
        enrollment = Enrollment.objects.create(university=self.uni, student=self.student, semester=self.semester)
        enrollment_course = EnrollmentCourse.objects.create(
            university=self.uni,
            enrollment=enrollment,
            course=self.course,
        )
        self.authenticate(self.teacher)
        denied = self.client.post(
            "/api/v1/grades/",
            {"enrollment_course": str(enrollment_course.id), "score": "88.00"},
            format="json",
            **self.tenant_headers(),
        )
        self.assertEqual(denied.status_code, 403)

        CourseAllocation.objects.create(
            university=self.uni,
            course=self.course,
            teacher=self.teacher,
            semester=self.semester,
        )
        allowed = self.client.post(
            "/api/v1/grades/",
            {"enrollment_course": str(enrollment_course.id), "score": "88.00"},
            format="json",
            **self.tenant_headers(),
        )
        self.assertEqual(allowed.status_code, 201)

    def test_payment_updates_invoice_and_receipt_downloads(self):
        invoice = Invoice.objects.create(
            university=self.uni,
            student=self.student,
            description="Tuition",
            total_amount=Decimal("500.00"),
            due_date="2026-10-01",
        )
        self.authenticate(self.registration)
        response = self.client.post(
            "/api/v1/payments/",
            {
                "invoice": str(invoice.id),
                "amount": "500.00",
                "payment_method": "Bank",
                "reference": "PAY-API-001",
            },
            format="json",
            **self.tenant_headers(),
        )
        self.assertEqual(response.status_code, 201)
        invoice.refresh_from_db()
        self.assertEqual(invoice.status, "paid")
        receipt = self.client.get(f"/api/v1/payments/{response.data['id']}/receipt/", **self.tenant_headers())
        self.assertEqual(receipt.status_code, 200)
        self.assertEqual(receipt["Content-Type"], "application/pdf")

    def test_notifications_are_limited_to_recipient(self):
        Notification.objects.create(university=self.uni, recipient=self.student_user, title="Mine", message="Hello")
        Notification.objects.create(university=self.uni, recipient=self.admin, title="Admin", message="Secret")
        self.authenticate(self.student_user)
        response = self.client.get("/api/v1/notifications/", **self.tenant_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["count"], 1)
        self.assertEqual(response.data["results"][0]["title"], "Mine")
