from datetime import date
from decimal import Decimal
import secrets

from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.permissions import IsRegistrationStaff
from apps.common.viewsets import TenantModelViewSet
from apps.finance.models import Invoice
from apps.notifications.models import Notification
from apps.students.models import StudentProfile
from apps.students.services import MatriculeService
from unisaas.logging import EnterpriseLogger

from .models import Application, Document
from .serializers import ApplicationSerializer, DocumentSerializer
from .services import AdmissionDocumentService

User = get_user_model()


class ApplicationViewSet(TenantModelViewSet):
    queryset = Application.objects.select_related("programme")
    serializer_class = ApplicationSerializer
    permission_classes = [IsRegistrationStaff]

    def get_queryset(self):
        qs = super().get_queryset()
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    @action(detail=True, methods=["post"], url_path="accept")
    def accept_application(self, request, pk=None):
        application = self.get_object()
        if application.status != "pending":
            return Response({"error": "Application already processed"}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(university=application.university, email=application.email.lower()).exists():
            return Response({"error": "A user with this email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            user = User.objects.create_user(
                email=application.email,
                university=application.university,
                password=secrets.token_urlsafe(18),
                role="student",
            )
            program_code = application.programme.code if application.programme else application.program_applied[:3].upper()
            matricule = MatriculeService.generate_matricule(
                application.university,
                application.entry_year,
                program_code,
                "1",
            )
            student = StudentProfile.objects.create(
                user=user,
                university=application.university,
                matricule=matricule,
                program_id=program_code,
                programme=application.programme,
                entry_year=application.entry_year,
                current_level="1",
            )
            invoice = Invoice.objects.create(
                university=application.university,
                student=student,
                description=f"Initial Registration Fee - {application.program_applied}",
                total_amount=Decimal("1000.00"),
                due_date=date.today(),
            )
            application.status = "accepted"
            application.save(update_fields=["status", "updated_at"])

            pdf_buffer = AdmissionDocumentService.generate_offer_letter(application)
            application.offer_letter.save(
                f"Offer_Letter_{application.id}.pdf",
                ContentFile(pdf_buffer.read()),
                save=True,
            )
            Notification.objects.create(
                university=application.university,
                recipient=user,
                title="Admission accepted",
                message=f"Your admission has been accepted. Matricule: {matricule}",
                priority="high",
            )
            EnterpriseLogger.log_action(
                request,
                "Application Accepted",
                "Application",
                str(application.id),
                prev_state={"status": "pending"},
                new_state={"status": "accepted", "matricule": matricule, "invoice": str(invoice.id)},
            )

        return Response(
            {
                "message": "Student admitted successfully",
                "matricule": matricule,
                "user_id": str(user.id),
                "student_id": str(student.id),
                "invoice_id": str(invoice.id),
                "offer_letter": application.offer_letter.url if application.offer_letter else None,
            }
        )

    @action(detail=True, methods=["post"], url_path="reject")
    def reject_application(self, request, pk=None):
        application = self.get_object()
        if application.status != "pending":
            return Response({"error": "Application already processed"}, status=status.HTTP_400_BAD_REQUEST)
        application.status = "rejected"
        application.save(update_fields=["status", "updated_at"])
        EnterpriseLogger.log_action(
            request,
            "Application Rejected",
            "Application",
            str(application.id),
            prev_state={"status": "pending"},
            new_state={"status": "rejected"},
        )
        return Response({"message": "Application rejected"})


class DocumentViewSet(TenantModelViewSet):
    queryset = Document.objects.select_related("application")
    serializer_class = DocumentSerializer
    permission_classes = [IsRegistrationStaff]

    @action(detail=True, methods=["post"], url_path="verify")
    def verify_document(self, request, pk=None):
        doc = self.get_object()
        doc.is_verified = True
        doc.save(update_fields=["is_verified", "updated_at"])
        EnterpriseLogger.log_action(request, "Document Verified", "Document", str(doc.id))
        return Response({"message": "Document verified"})
