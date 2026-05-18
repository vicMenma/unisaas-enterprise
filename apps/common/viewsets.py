from rest_framework import viewsets


class TenantQuerySetMixin:
    tenant_field = "university"

    def get_queryset(self):
        queryset = super().get_queryset()
        tenant = getattr(self.request, "tenant", None)
        if tenant is None:
            return queryset.none()
        return queryset.filter(**{self.tenant_field: tenant})

    def perform_create(self, serializer):
        serializer.save(**{self.tenant_field: self.request.tenant})


class TenantModelViewSet(TenantQuerySetMixin, viewsets.ModelViewSet):
    pass
