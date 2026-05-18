import io

from django.http import FileResponse
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from rest_framework import mixins, viewsets
from rest_framework.decorators import action

from apps.accounts.permissions import IsFinanceStaff
from apps.common.viewsets import TenantModelViewSet, TenantQuerySetMixin
from unisaas.logging import EnterpriseLogger

from .models import FeeCategory, Invoice, Payment
from .serializers import FeeCategorySerializer, InvoiceSerializer, PaymentSerializer


class FeeCategoryViewSet(TenantModelViewSet):
    queryset = FeeCategory.objects.all()
    serializer_class = FeeCategorySerializer
    permission_classes = [IsFinanceStaff]


class InvoiceViewSet(TenantModelViewSet):
    queryset = Invoice.objects.select_related("student")
    serializer_class = InvoiceSerializer
    permission_classes = [IsFinanceStaff]


class PaymentViewSet(
    TenantQuerySetMixin,
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Payment.objects.select_related("invoice", "invoice__student")
    serializer_class = PaymentSerializer
    permission_classes = [IsFinanceStaff]

    def perform_create(self, serializer):
        payment = serializer.save(university=self.request.tenant)
        EnterpriseLogger.log_action(
            self.request,
            "Payment Received",
            "Payment",
            str(payment.id),
            new_state={"amount": str(payment.amount), "invoice": str(payment.invoice_id)},
        )

    @action(detail=True, methods=["get"], url_path="receipt")
    def receipt(self, request, pk=None):
        payment = self.get_object()
        buffer = io.BytesIO()
        page = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4
        page.setFont("Helvetica-Bold", 18)
        page.drawCentredString(width / 2, height - inch, "Payment Receipt")
        page.setFont("Helvetica", 11)
        y = height - 1.7 * inch
        rows = [
            ("University", payment.university.name),
            ("Receipt No", str(payment.id)),
            ("Invoice", str(payment.invoice_id)),
            ("Student", payment.invoice.student.matricule),
            ("Amount", f"{payment.amount:.2f}"),
            ("Method", payment.payment_method),
            ("Reference", payment.reference),
            ("Date", payment.date.strftime("%Y-%m-%d %H:%M")),
        ]
        for label, value in rows:
            page.drawString(inch, y, f"{label}: {value}")
            y -= 0.25 * inch
        page.showPage()
        page.save()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename=f"Receipt_{payment.reference}.pdf")
