"""
URL configuration for unisaas project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter

from students.views import StudentProfileViewSet
from registration.views import EnrollmentViewSet
from examinations.views import GradeViewSet
from finance.views import FeeCategoryViewSet, InvoiceViewSet, PaymentViewSet
from academic.views import FacultyViewSet, DepartmentViewSet, SemesterViewSet, CourseViewSet
from admissions.views import ApplicationViewSet, DocumentViewSet
from audit.views import AuditLogViewSet
from notifications.views import NotificationViewSet
from .views import home_view, static_view, portal_view, portal_static_view, dean_portal_view

router = DefaultRouter()
# Academic
router.register(r'faculties', FacultyViewSet, basename='faculty')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'semesters', SemesterViewSet, basename='semester')
router.register(r'courses', CourseViewSet, basename='course')
# Students
router.register(r'students', StudentProfileViewSet, basename='student')
# Registration
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
# Examinations
router.register(r'grades', GradeViewSet, basename='grade')
# Finance
router.register(r'fee-categories', FeeCategoryViewSet, basename='fee-category')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'payments', PaymentViewSet, basename='payment')
# Admissions
router.register(r'applications', ApplicationViewSet, basename='application')
router.register(r'documents', DocumentViewSet, basename='document')
# Audit
router.register(r'audit-logs', AuditLogViewSet, basename='audit-log')
# Notifications
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    # Frontend pages
    path('', home_view, name='home'),
    path('style.css', static_view, name='static_css'),
    path('portal', portal_view, name='portal'),
    path('portal.css', portal_static_view, name='portal_css'),
    path('dean-portal', dean_portal_view, name='dean_portal'),
    # Admin
    path('admin/', admin.site.urls),
    # API v1
    path('api/v1/', include('accounts.urls')),
    path('api/v1/', include(router.urls)),
    # Legacy (backward compat)
    path('api/', include('accounts.urls')),
    path('api/', include(router.urls)),
]

# Serve uploaded media in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
