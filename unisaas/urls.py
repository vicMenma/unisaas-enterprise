"""
URL configuration for unisaas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from students.views import StudentProfileViewSet
from registration.views import EnrollmentViewSet
from examinations.views import GradeViewSet
from finance.views import FeeCategoryViewSet, InvoiceViewSet, PaymentViewSet
from .views import home_view, static_view, portal_view, portal_static_view, dean_portal_view

router = DefaultRouter()
router.register(r'students', StudentProfileViewSet, basename='student')
router.register(r'enrollments', EnrollmentViewSet, basename='enrollment')
router.register(r'grades', GradeViewSet, basename='grade')
router.register(r'fee-categories', FeeCategoryViewSet, basename='fee-category')
router.register(r'invoices', InvoiceViewSet, basename='invoice')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('', home_view, name='home'),
    path('style.css', static_view, name='static_css'),
    path('portal', portal_view, name='portal'),
    path('portal.css', portal_static_view, name='portal_css'),
    path('dean-portal', dean_portal_view, name='dean_portal'),
    path('admin/', admin.site.urls),
    path('api/', include('accounts.urls')),
    path('api/', include(router.urls)),
]
