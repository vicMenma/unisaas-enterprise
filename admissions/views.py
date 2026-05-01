from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Application, Document
from .serializers import ApplicationSerializer, DocumentSerializer
from students.models import StudentProfile
from students.services import MatriculeService
from finance.models import Invoice
from .services import AdmissionDocumentService
from unisaas.logging import EnterpriseLogger
from datetime import date
from django.core.files.base import ContentFile

User = get_user_model()


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Application.objects.filter(university=self.request.tenant)
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)

    @action(detail=True, methods=['post'], url_path='accept')
    def accept_application(self, request, pk=None):
        """
        ERP Workflow: Accept Application -> Create User -> Create Profile
                      -> Generate Matricule -> Generate Invoice -> Persist PDF
        """
        application = self.get_object()

        if application.status != 'pending':
            return Response(
                {"error": "Application already processed"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        with transaction.atomic():
            # 1. Create User Account
            user = User.objects.create_user(
                email=application.email,
                university=application.university,
                password=User.objects.make_random_password(),
                role='student',
            )

            # 2. Generate Atomic Matricule
            matricule = MatriculeService.generate_matricule(
                application.university,
                application.entry_year,
                application.program_applied[:3].upper(),
                1,
            )

            # 3. Create Student Profile
            student = StudentProfile.objects.create(
                user=user,
                university=application.university,
                matricule=matricule,
                program_id=application.program_applied,
                entry_year=application.entry_year,
                current_level=1,
            )

            # 4. Generate Registration Invoice
            Invoice.objects.create(
                university=application.university,
                student=student,
                description=f"Initial Registration Fee — {application.program_applied}",
                total_amount=1000.00,
                due_date=date.today(),
            )

            # 5. Update Application Status
            application.status = 'accepted'
            application.save()

            # 6. Generate and Persist PDF Offer Letter
            pdf_buffer = AdmissionDocumentService.generate_offer_letter(application)
            application.offer_letter.save(
                f"Offer_Letter_{application.id}.pdf",
                ContentFile(pdf_buffer.read()),
                save=True,
            )

            # 7. Audit Trail
            EnterpriseLogger.log_action(
                request, "Application Accepted", "Application",
                str(application.id),
                prev_state={"status": "pending"},
                new_state={"status": "accepted", "matricule": matricule},
            )

        return Response({
            "message": "Student admitted successfully",
            "matricule": matricule,
            "user_id": str(user.id),
            "invoice_generated": True,
            "offer_letter": application.offer_letter.url if application.offer_letter else None,
        })

    @action(detail=True, methods=['post'], url_path='reject')
    def reject_application(self, request, pk=None):
        application = self.get_object()
        if application.status != 'pending':
            return Response(
                {"error": "Application already processed"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        application.status = 'rejected'
        application.save()
        EnterpriseLogger.log_action(
            request, "Application Rejected", "Application",
            str(application.id),
        )
        return Response({"message": "Application rejected"})


class DocumentViewSet(viewsets.ModelViewSet):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Document.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)

    @action(detail=True, methods=['post'], url_path='verify')
    def verify_document(self, request, pk=None):
        doc = self.get_object()
        doc.is_verified = True
        doc.save()
        EnterpriseLogger.log_action(
            request, "Document Verified", "Document", str(doc.id),
        )
        return Response({"message": "Document verified"})
