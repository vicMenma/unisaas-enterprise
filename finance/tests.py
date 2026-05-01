from decimal import Decimal
from django.test import TestCase
from tenants.models import University
from accounts.models import User
from students.models import StudentProfile
from .models import FeeCategory, Invoice, Payment


class FinanceModelTest(TestCase):
    def setUp(self):
        self.uni = University.objects.create(name="Fin Uni", slug="fin")
        self.user = User.objects.create_user(
            email="stu@fin.com", university=self.uni, password="pass",
        )
        self.student = StudentProfile.objects.create(
            user=self.user, university=self.uni,
            matricule="FIN-2026-001", entry_year=2026, current_level=1,
        )

    def test_fee_category_creation(self):
        cat = FeeCategory.objects.create(
            university=self.uni, name="Tuition", amount=Decimal("5000.00"),
        )
        self.assertEqual(str(cat), "Tuition - 5000.00")

    def test_invoice_balance(self):
        inv = Invoice.objects.create(
            university=self.uni, student=self.student,
            description="Tuition Q1", total_amount=Decimal("5000.00"),
            due_date="2026-06-01",
        )
        self.assertEqual(inv.balance_due, Decimal("5000.00"))
        self.assertEqual(inv.status, 'unpaid')

    def test_payment_updates_invoice_status(self):
        inv = Invoice.objects.create(
            university=self.uni, student=self.student,
            description="Tuition Q1", total_amount=Decimal("5000.00"),
            due_date="2026-06-01",
        )
        # Partial payment
        Payment.objects.create(
            university=self.uni, invoice=inv,
            amount=Decimal("2000.00"), payment_method="Mobile Money",
            reference="PAY-001",
        )
        inv.refresh_from_db()
        self.assertEqual(inv.paid_amount, Decimal("2000.00"))
        self.assertEqual(inv.status, 'partially_paid')

        # Full payment
        Payment.objects.create(
            university=self.uni, invoice=inv,
            amount=Decimal("3000.00"), payment_method="Bank Transfer",
            reference="PAY-002",
        )
        inv.refresh_from_db()
        self.assertEqual(inv.paid_amount, Decimal("5000.00"))
        self.assertEqual(inv.status, 'paid')
        self.assertEqual(inv.balance_due, Decimal("0.00"))
