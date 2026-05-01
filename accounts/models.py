import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from tenants.models import University

class CustomUserManager(BaseUserManager):
    def create_user(self, email, university, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not university:
            raise ValueError('The University field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, university=university, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'owner')
        
        # For superuser, we need a dummy university or a specific admin university
        # But since university is required, let's just get or create a default one
        university, _ = University.objects.get_or_create(
            slug='system',
            defaults={
                'name': 'System Admin University',
                'matricule_prefix': 'SYS'
            }
        )
        return self.create_user(email, university, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = (
        ('owner', 'Owner'),
        ('university_admin', 'University Admin'),
        ('registration', 'Registration'),
        ('examination', 'Examination'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='users')
    
    # Email is NOT globally unique, it is unique per tenant.
    email = models.EmailField(max_length=255)
    
    # Internal unique identifier for Django's auth system to work smoothly
    username = models.CharField(max_length=255, unique=True, editable=False)
    
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='student')
    
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['university', 'email'], name='unique_tenant_email')
        ]
        indexes = [
            models.Index(fields=['university', 'email']),
        ]

    def save(self, *args, **kwargs):
        # Generate globally unique username combining university ID and email
        if not self.username:
            self.username = f"{self.university_id}_{self.email}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.email} ({self.university.name})"
