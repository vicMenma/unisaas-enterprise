from django.contrib.auth import get_user_model
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    university = serializers.CharField(source="university.slug", read_only=True)
    university_name = serializers.CharField(source="university.name", read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "role",
            "university",
            "university_name",
            "is_active",
            "is_staff",
            "created_at",
        )
        read_only_fields = fields


class TenantTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = "email"

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, trim_whitespace=False)

    def validate(self, attrs):
        request = self.context.get("request")
        tenant = getattr(request, "tenant", None)
        email = attrs.get("email")
        password = attrs.get("password")

        if not tenant:
            raise exceptions.AuthenticationFailed(
                "Tenant not resolved. Provide X-Tenant-Slug or use a tenant subdomain.",
            )

        try:
            user = User.objects.get(university=tenant, email__iexact=email)
        except User.DoesNotExist as exc:
            raise exceptions.AuthenticationFailed(
                "No active account found with the given credentials",
            ) from exc

        if not user.check_password(password) or not user.is_active:
            raise exceptions.AuthenticationFailed(
                "No active account found with the given credentials",
            )

        refresh = self.get_token(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "role": user.role,
            "user": UserProfileSerializer(user).data,
        }
