from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.academic.views import (
    AcademicYearViewSet,
    CourseAllocationViewSet,
    CourseViewSet,
    DepartmentViewSet,
    FacultyViewSet,
    ProgrammeViewSet,
    SemesterViewSet,
)
from apps.admissions.views import ApplicationViewSet, DocumentViewSet
from apps.audit.views import AuditLogViewSet
from apps.examinations.views import GradeViewSet
from apps.finance.views import FeeCategoryViewSet, InvoiceViewSet, PaymentViewSet
from apps.notifications.views import NotificationViewSet
from apps.registration.views import EnrollmentCourseViewSet, EnrollmentViewSet
from apps.students.views import StudentProfileViewSet

from .views import dean_portal_view, home_view, login_view, portal_view

router = DefaultRouter()
router.register(r"academic-years", AcademicYearViewSet, basename="academic-year")
router.register(r"faculties", FacultyViewSet, basename="faculty")
router.register(r"departments", DepartmentViewSet, basename="department")
router.register(r"programmes", ProgrammeViewSet, basename="programme")
router.register(r"semesters", SemesterViewSet, basename="semester")
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"course-allocations", CourseAllocationViewSet, basename="course-allocation")
router.register(r"students", StudentProfileViewSet, basename="student")
router.register(r"enrollments", EnrollmentViewSet, basename="enrollment")
router.register(r"enrollment-courses", EnrollmentCourseViewSet, basename="enrollment-course")
router.register(r"grades", GradeViewSet, basename="grade")
router.register(r"fee-categories", FeeCategoryViewSet, basename="fee-category")
router.register(r"invoices", InvoiceViewSet, basename="invoice")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"applications", ApplicationViewSet, basename="application")
router.register(r"documents", DocumentViewSet, basename="document")
router.register(r"audit-logs", AuditLogViewSet, basename="audit-log")
router.register(r"notifications", NotificationViewSet, basename="notification")

urlpatterns = [
    path("", home_view, name="home"),
    path("login/", login_view, name="login"),
    path("portal/", portal_view, name="portal"),
    path("dean-portal/", dean_portal_view, name="dean_portal"),
    path("admin/", admin.site.urls),
    path("api/v1/", include("apps.accounts.urls")),
    path("api/v1/", include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
