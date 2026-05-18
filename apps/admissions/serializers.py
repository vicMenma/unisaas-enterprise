from apps.academic.models import Programme
from apps.common.serializers import TenantScopedModelSerializer, TenantScopedPrimaryKeyRelatedField

from .models import Application, Document


class DocumentSerializer(TenantScopedModelSerializer):
    application = TenantScopedPrimaryKeyRelatedField(queryset=Application.objects.all())

    class Meta:
        model = Document
        fields = ("id", "application", "doc_type", "file", "is_verified", "created_at")
        read_only_fields = ("id", "created_at")


class ApplicationSerializer(TenantScopedModelSerializer):
    programme = TenantScopedPrimaryKeyRelatedField(
        queryset=Programme.objects.all(),
        required=False,
        allow_null=True,
    )
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = (
            "id",
            "first_name",
            "last_name",
            "email",
            "program_applied",
            "programme",
            "entry_year",
            "status",
            "submission_date",
            "offer_letter",
            "documents",
        )
        read_only_fields = ("id", "status", "submission_date", "offer_letter")
        extra_kwargs = {"program_applied": {"required": False, "allow_blank": True}}

    def validate(self, attrs):
        programme = attrs.get("programme")
        if programme and not attrs.get("program_applied"):
            attrs["program_applied"] = programme.name
        return attrs
