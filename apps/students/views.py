import logging

from django.db import transaction
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.accounts.permissions import IsRegistrationStaff, IsStudent
from apps.common.viewsets import TenantModelViewSet
from unisaas.logging import EnterpriseLogger

from .models import StudentProfile
from .serializers import StudentProfileSerializer
from .services import MatriculeService
from .tasks import send_welcome_email_task

logger = logging.getLogger(__name__)


class StudentProfileViewSet(TenantModelViewSet):
    queryset = StudentProfile.objects.select_related("user", "programme")
    serializer_class = StudentProfileSerializer

    def get_permissions(self):
        if self.action == "me":
            return [IsStudent()]
        return [IsRegistrationStaff()]

    def perform_create(self, serializer):
        university = self.request.tenant
        entry_year = serializer.validated_data.get("entry_year")
        programme = serializer.validated_data.get("programme")
        program_code = (programme.code if programme else serializer.validated_data.get("program_id"))
        current_level = serializer.validated_data.get("current_level")

        matricule = MatriculeService.generate_matricule(university, entry_year, program_code, current_level)
        student = serializer.save(university=university, matricule=matricule)

        EnterpriseLogger.log_action(
            self.request,
            "Student Created",
            "StudentProfile",
            student.id,
            new_state={"matricule": student.matricule, "email": student.user.email},
        )
        transaction.on_commit(lambda: self._send_welcome_email(student.user.id))

    @action(detail=False, methods=["get"], url_path="me")
    def me(self, request):
        try:
            profile = StudentProfile.objects.select_related("user", "programme").get(
                university=request.tenant,
                user=request.user,
            )
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student profile not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(self.get_serializer(profile).data)

    def _send_welcome_email(self, user_id):
        try:
            send_welcome_email_task.delay(str(user_id))
        except Exception:
            logger.exception("Failed to enqueue welcome email for user %s", user_id)
