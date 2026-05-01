from rest_framework import viewsets, mixins
from accounts.permissions import IsUniversityAdmin
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    Read-only viewset for audit logs. Only university admins and owners
    can view audit trails. Append-only by design — no create/update/delete.
    """
    serializer_class = AuditLogSerializer
    permission_classes = [IsUniversityAdmin]

    def get_queryset(self):
        qs = AuditLog.objects.filter(university=self.request.tenant)
        action = self.request.query_params.get('action')
        resource = self.request.query_params.get('resource_type')
        if action:
            qs = qs.filter(action__icontains=action)
        if resource:
            qs = qs.filter(resource_type__icontains=resource)
        return qs
