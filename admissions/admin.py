from django.contrib import admin
from .models import Application, Document


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'program_applied', 'entry_year', 'status', 'university')
    list_filter = ('status', 'entry_year', 'program_applied')
    search_fields = ('first_name', 'last_name', 'email')
    readonly_fields = ('offer_letter', 'submission_date')


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('doc_type', 'application', 'is_verified', 'university')
    list_filter = ('is_verified', 'doc_type')
