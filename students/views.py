from django.db import transaction
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import StudentProfile
from .serializers import StudentProfileSerializer
from .services import MatriculeService
from .tasks import send_welcome_email_task
from accounts.permissions import IsRegistrationStaff
from unisaas.logging import EnterpriseLogger

class StudentProfileViewSet(viewsets.ModelViewSet):
    serializer_class = StudentProfileSerializer
    permission_classes = [IsRegistrationStaff]

    def get_queryset(self):
        # Strict tenant isolation
        return StudentProfile.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        # In a real scenario, the user would be created via a service or passed in.
        # For simplicity, we assume the user is created beforehand and passed, or we generate the matricule here.
        university = self.request.tenant
        entry_year = serializer.validated_data.get('entry_year')
        program_id = serializer.validated_data.get('program_id')
        current_level = serializer.validated_data.get('current_level')
        
        matricule = MatriculeService.generate_matricule(university, entry_year, program_id, current_level)
        student = serializer.save(university=university, matricule=matricule)
        
        # Enterprise Audit Log
        EnterpriseLogger.log_action(
            self.request, "Student Created", "StudentProfile", student.id,
            new_state=serializer.data
        )
        
        # Trigger async welcome email
        transaction.on_commit(lambda: send_welcome_email_task.delay(student.user.id))
