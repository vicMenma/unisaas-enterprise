from rest_framework import viewsets, permissions
from .models import FeeCategory, Invoice, Payment
from .serializers import FeeCategorySerializer, InvoiceSerializer, PaymentSerializer

class FeeCategoryViewSet(viewsets.ModelViewSet):
    serializer_class = FeeCategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return FeeCategory.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)

class InvoiceViewSet(viewsets.ModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)
