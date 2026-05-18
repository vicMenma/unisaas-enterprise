from rest_framework import serializers

from apps.academic.models import Programme
from apps.accounts.models import User
from apps.common.serializers import TenantScopedModelSerializer

from .models import StudentProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "role", "is_active", "created_at")
        read_only_fields = fields


class StudentProfileSerializer(TenantScopedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    user_detail = UserSerializer(source="user", read_only=True)
    tenant_related_fields = {"user": User, "programme": Programme}

    class Meta:
        model = StudentProfile
        fields = (
            "id",
            "user",
            "user_detail",
            "matricule",
            "program_id",
            "programme",
            "status",
            "entry_year",
            "current_level",
            "created_at",
        )
        read_only_fields = ("id", "matricule", "created_at")

    def validate_user(self, user):
        if user.role != "student":
            raise serializers.ValidationError("Student profiles require a user with the student role.")
        return user

    def validate(self, attrs):
        programme = attrs.get("programme")
        if programme and not attrs.get("program_id"):
            attrs["program_id"] = programme.code
        return attrs
