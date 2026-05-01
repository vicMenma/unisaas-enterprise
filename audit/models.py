from django.db import models
from django.conf import settings
from tenants.models import TenantModel

class AuditLog(TenantModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=255) # e.g., "Grade Changed", "Payment Received"
    resource_type = models.CharField(max_length=100) # e.g., "Grade", "Invoice"
    resource_id = models.CharField(max_length=255)
    previous_state = models.JSONField(null=True, blank=True)
    new_state = models.JSONField(null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"
