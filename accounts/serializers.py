from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import exceptions
from django.contrib.auth import get_user_model

User = get_user_model()

class TenantTokenObtainPairSerializer(TokenObtainPairSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # We only require email and password, not username
        self.fields['email'] = self.fields.pop(User.USERNAME_FIELD)

    def validate(self, attrs):
        request = self.context.get('request')
        tenant = getattr(request, 'tenant', None)
        email = attrs.get('email') or attrs.get(User.USERNAME_FIELD)
        password = attrs.get('password')

        if not tenant:
            raise exceptions.AuthenticationFailed('Tenant not resolved. Please provide X-Tenant-Slug header.')

        try:
            # Look up the user by the resolved tenant and email
            user = User.objects.get(university=tenant, email=email)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No active account found with the given credentials')

        if not user.check_password(password):
            raise exceptions.AuthenticationFailed('No active account found with the given credentials')

        if not user.is_active:
            raise exceptions.AuthenticationFailed('User account is disabled')

        # Since simplejwt generates tokens using the user object, we pass it to the token generation mechanism
        refresh = self.get_token(user)

        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Include role for UI convenience
        data['role'] = user.role

        return data
