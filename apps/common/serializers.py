from rest_framework import serializers


class TenantScopedPrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    """Restrict related-object choices to the request tenant."""

    def get_queryset(self):
        queryset = super().get_queryset()
        request = self.context.get("request")
        tenant = getattr(request, "tenant", None)
        if queryset is None or tenant is None:
            return queryset.none() if queryset is not None else None
        model = queryset.model
        if hasattr(model, "university"):
            return queryset.filter(university=tenant)
        return queryset


class TenantScopedModelSerializer(serializers.ModelSerializer):
    tenant_related_fields = {}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get("request")
        tenant = getattr(request, "tenant", None)
        if tenant is None:
            return
        for field_name, model in self.tenant_related_fields.items():
            if field_name in self.fields:
                self.fields[field_name].queryset = model.objects.filter(university=tenant)
