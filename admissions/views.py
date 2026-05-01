from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.contrib.auth import get_user_model
from .models import Application
from students.models import StudentProfile
from students.services import MatriculeService
from finance.models import Invoice
from .services import AdmissionDocumentService
from datetime import date

User = get_user_model()

class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(university=self.request.tenant)

    @action(detail=True, methods=['post'], url_path='accept')
    def accept_application(self, request, pk=None):
        """
        ERP Workflow: Accept Application -> Create User -> Create Profile -> Generate ID -> Generate Invoice
        """
        application = self.get_object()
        
        if application.status != 'pending':
            return Response({"error": "Application already processed"}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            # 1. Create User Account
            user = User.objects.create_user(
                email=application.email,
                university=application.university,
                password=User.objects.make_random_password(),
                role='student'
            )
            
            # 2. Generate Atomic Matricule
            matricule = MatriculeService.generate_matricule(
                application.university, date.today().year, "GEN", 1
            )
            
            # 3. Create Student Profile
            student = StudentProfile.objects.create(
                user=user,
                university=application.university,
                matricule=matricule,
                current_level=1
            )
            
            # 4. Generate Registration Invoice
            Invoice.objects.create(
                university=application.university,
                student=student,
                description="Initial Registration Fee",
                total_amount=1000.00, # Base fee
                due_date=date.today()
            )
            
            # 5. Update Application Status
            application.status = 'accepted'
            application.save()

            # 6. Generate PDF Offer Letter (Simulated in buffer for now)
            # In production, we'd save this to a FileField
            AdmissionDocumentService.generate_offer_letter(application)

        return Response({
            "message": "Student admitted successfully",
            "matricule": matricule,
            "user_id": user.id
        })
