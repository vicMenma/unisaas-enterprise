import logging
from audit.models import AuditLog

class EnterpriseLogger:
    @staticmethod
    def log_action(request, action, resource_type, resource_id, prev_state=None, new_state=None):
        AuditLog.objects.create(
            university=request.tenant,
            user=request.user if request.user.is_authenticated else None,
            action=action,
            resource_type=resource_type,
            resource_id=str(resource_id),
            previous_state=prev_state,
            new_state=new_state,
            ip_address=request.META.get('REMOTE_ADDR')
        )
