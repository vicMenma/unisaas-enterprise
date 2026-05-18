from rest_framework import serializers

from apps.common.serializers import TenantScopedModelSerializer, TenantScopedPrimaryKeyRelatedField
from apps.students.models import StudentProfile

from .models import FeeCategory, Invoice, Payment


class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = ("id", "name", "amount", "description", "created_at")
        read_only_fields = ("id", "created_at")


class PaymentSerializer(TenantScopedModelSerializer):
    invoice = TenantScopedPrimaryKeyRelatedField(queryset=Invoice.objects.all())

    class Meta:
        model = Payment
        fields = ("id", "invoice", "amount", "payment_method", "reference", "date")
        read_only_fields = ("id", "date")

    def validate_amount(self, amount):
        if amount <= 0:
            raise serializers.ValidationError("Payment amount must be positive.")
        return amount

    def validate(self, attrs):
        invoice = attrs.get("invoice")
        amount = attrs.get("amount")
        if invoice and amount and amount > invoice.balance_due:
            raise serializers.ValidationError("Payment amount cannot exceed invoice balance.")
        return attrs


class InvoiceSerializer(TenantScopedModelSerializer):
    student = TenantScopedPrimaryKeyRelatedField(queryset=StudentProfile.objects.all())
    payments = PaymentSerializer(many=True, read_only=True)
    balance_due = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Invoice
        fields = (
            "id",
            "student",
            "description",
            "total_amount",
            "paid_amount",
            "balance_due",
            "status",
            "due_date",
            "payments",
            "created_at",
        )
        read_only_fields = ("id", "paid_amount", "status", "created_at")
