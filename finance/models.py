from django.db import models
from tenants.models import TenantModel
from students.models import StudentProfile

class FeeCategory(TenantModel):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.name} - {self.amount}"

class Invoice(TenantModel):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('unpaid', 'Unpaid'),
        ('partially_paid', 'Partially Paid'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    )
    
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE, related_name='invoices')
    description = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='unpaid')
    due_date = models.DateField()

    @property
    def balance_due(self):
        return self.total_amount - self.paid_amount

    def __str__(self):
        return f"INV-{self.id} for {self.student.matricule}"

class Payment(TenantModel):
    invoice = models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=50) # e.g., 'Bank Transfer', 'Mobile Money'
    reference = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Update the related invoice paid amount
            self.invoice.paid_amount += self.amount
            if self.invoice.paid_amount >= self.invoice.total_amount:
                self.invoice.status = 'paid'
            elif self.invoice.paid_amount > 0:
                self.invoice.status = 'partially_paid'
            self.invoice.save(update_fields=['paid_amount', 'status'])
