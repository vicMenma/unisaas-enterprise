from django.db import models
from tenants.models import TenantModel

class Application(TenantModel):
    STATUS_CHOICES = (
        ('pending', 'Pending Review'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('enrolled', 'Enrolled'),
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    program_applied = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submission_date = models.DateTimeField(auto_now_add=True)
    review_notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program_applied}"

class Document(TenantModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=50) # e.g., "ID Card", "Transcript"
    file_path = models.CharField(max_length=255) # Placeholder for storage path
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doc_type} for {self.application.first_name}"
