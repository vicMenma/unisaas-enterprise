from django.contrib import admin
from .models import Enrollment, EnrollmentCourse

class EnrollmentCourseInline(admin.TabularInline):
    model = EnrollmentCourse
    extra = 1

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'semester', 'is_active', 'university')
    list_filter = ('is_active',)
    search_fields = ('student__matricule',)
    inlines = [EnrollmentCourseInline]
