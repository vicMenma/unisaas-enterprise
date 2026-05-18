from rest_framework import serializers
from .models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.CharField(source='user.email', read_only=True, default='System')

    class Meta:
        model = AuditLog
        fields = (
            'id', 'user', 'user_email', 'action', 'resource_type',
            'resource_id', 'previous_state', 'new_state',
            'ip_address', 'timestamp',
        )
        read_only_fields = fields
