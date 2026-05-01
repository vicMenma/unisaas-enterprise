from django.contrib import admin
from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('action', 'resource_type', 'resource_id', 'user', 'ip_address', 'timestamp')
    list_filter = ('action', 'resource_type')
    search_fields = ('action', 'resource_id')
    readonly_fields = (
        'user', 'action', 'resource_type', 'resource_id',
        'previous_state', 'new_state', 'ip_address', 'timestamp',
    )

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
