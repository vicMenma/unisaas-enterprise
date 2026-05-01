from django.db import models
from tenants.models import TenantModel
import uuid

class Application(TenantModel):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    program_applied = models.CharField(max_length=100) # e.g. "Computer Science"
    entry_year = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submission_date = models.DateTimeField(auto_now_add=True)
    
    # PDF Offer Letter Persistence
    offer_letter = models.FileField(upload_to='admission_letters/', null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.program_applied}"

class Document(TenantModel):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='documents')
    doc_type = models.CharField(max_length=50) # e.g. "Transcript", "ID Card"
    file = models.FileField(upload_to='application_docs/')
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.doc_type} for {self.application.id}"
