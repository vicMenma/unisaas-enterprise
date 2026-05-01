from django.contrib import admin
from .models import StudentProfile, MatriculeSequence

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'matricule', 'program_id', 'status', 'current_level', 'university')
    search_fields = ('matricule', 'user__email')
    list_filter = ('status', 'current_level')
    readonly_fields = ('matricule', 'university')

@admin.register(MatriculeSequence)
class MatriculeSequenceAdmin(admin.ModelAdmin):
    list_display = ('university', 'year', 'program_code', 'level', 'current_sequence')
    readonly_fields = ('university', 'current_sequence')
