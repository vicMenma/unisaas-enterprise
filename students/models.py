from django.db import models
from django.contrib.auth import get_user_model
from tenants.models import TenantModel

User = get_user_model()

class MatriculeSequence(TenantModel):
    """
    Keeps track of the sequence number for matricules, allowing atomic increments.
    We lock this row during generation to prevent race conditions.
    """
    year = models.IntegerField(help_text="Year of admission")
    program_code = models.CharField(max_length=50)
    level = models.CharField(max_length=20)
    current_sequence = models.IntegerField(default=0)

    class Meta:
        unique_together = ('university', 'year', 'program_code', 'level')


class StudentProfile(TenantModel):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
        ('withdrawn', 'Withdrawn'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    matricule = models.CharField(max_length=100)
    program_id = models.CharField(max_length=50) # In a real app, this would be a FK to a Program model
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    entry_year = models.IntegerField()
    current_level = models.CharField(max_length=20)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['university', 'matricule'], name='unique_tenant_matricule')
        ]
        indexes = [
            models.Index(fields=['university', 'matricule']),
        ]

    def __str__(self):
        return f"{self.matricule} - {self.user.email}"
