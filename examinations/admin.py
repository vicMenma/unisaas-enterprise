from django.contrib import admin
from .models import Grade

@admin.register(Grade)
class GradeAdmin(admin.ModelAdmin):
    list_display = ('enrollment_course', 'score', 'letter_grade', 'is_locked', 'university')
    list_filter = ('is_locked', 'letter_grade')
    search_fields = ('enrollment_course__enrollment__student__matricule',)
