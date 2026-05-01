from rest_framework import serializers
from .models import FeeCategory, Invoice, Payment

class FeeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeCategory
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ('id', 'invoice', 'amount', 'payment_method', 'reference', 'date')
        read_only_fields = ('date',)

class InvoiceSerializer(serializers.ModelSerializer):
    payments = PaymentSerializer(many=True, read_only=True)
    balance_due = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    
    class Meta:
        model = Invoice
        fields = ('id', 'student', 'description', 'total_amount', 'paid_amount', 'balance_due', 'status', 'due_date', 'payments')
        read_only_fields = ('paid_amount', 'status')
