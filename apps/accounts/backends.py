from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q

User = get_user_model()

class TenantEmailBackend(ModelBackend):
    """
    Custom authentication backend that allows users to log in using their email.
    For the Admin panel (where we don't have a tenant context easily), it will 
    work for superusers or unique emails.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        if username is None:
            username = kwargs.get(User.REQUIRED_FIELDS[0]) # usually email
            
        try:
            # First, try to find a superuser by email (for Admin panel access)
            user = User.objects.get(email=username, is_superuser=True)
        except User.MultipleObjectsReturned:
            # If multiple users have the same email (non-superusers), we can't 
            # resolve without tenant context in the standard admin login.
            return None
        except User.DoesNotExist:
            # If not a superuser, try to find by the generated 'username' field
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None

        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
