from django.db import models
from django.db import transaction
from django.core.exceptions import ValidationError
from apps.tenants.models import TenantModel
from apps.students.models import StudentProfile

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
    payment_method = models.CharField(max_length=50)  # e.g., 'Bank Transfer', 'Mobile Money'
    reference = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        if not is_new:
            super().save(*args, **kwargs)
            return

        with transaction.atomic():
            invoice = Invoice.objects.select_for_update().get(pk=self.invoice_id)
            if invoice.university_id != self.university_id:
                raise ValidationError("Payment and invoice must belong to the same tenant.")
            if self.amount <= 0:
                raise ValidationError("Payment amount must be positive.")
            if self.amount > invoice.balance_due:
                raise ValidationError("Payment amount cannot exceed invoice balance.")

            super().save(*args, **kwargs)
            invoice.paid_amount += self.amount
            if invoice.paid_amount >= invoice.total_amount:
                invoice.status = 'paid'
            elif invoice.paid_amount > 0:
                invoice.status = 'partially_paid'
            else:
                invoice.status = 'unpaid'
            invoice.save(update_fields=['paid_amount', 'status', 'updated_at'])
