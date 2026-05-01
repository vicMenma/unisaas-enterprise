from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.http import FileResponse
from .models import Grade
from .serializers import GradeSerializer
from .services import GPAService
from .transcript import TranscriptService
from registration.models import Enrollment
from students.models import StudentProfile
from accounts.permissions import IsExaminationStaff
from unisaas.logging import EnterpriseLogger


class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsExaminationStaff]

    def get_queryset(self):
        return Grade.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        instance = serializer.save(university=self.request.tenant)
        EnterpriseLogger.log_action(
            self.request, "Grade Created", "Grade", str(instance.id),
            new_state={
                "score": str(instance.score),
                "letter_grade": instance.letter_grade,
            },
        )

    def perform_update(self, serializer):
        old = self.get_object()
        if old.is_locked:
            raise permissions.PermissionDenied("This grade is locked and cannot be modified.")
        prev = {"score": str(old.score), "letter_grade": old.letter_grade}
        instance = serializer.save()
        EnterpriseLogger.log_action(
            self.request, "Grade Updated", "Grade", str(instance.id),
            prev_state=prev,
            new_state={"score": str(instance.score), "letter_grade": instance.letter_grade},
        )

    @action(detail=False, methods=['get'], url_path='gpa/(?P<enrollment_id>[^/.]+)')
    def gpa(self, request, enrollment_id=None):
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id, university=request.tenant)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Enrollment not found'}, status=status.HTTP_404_NOT_FOUND)
        gpa = GPAService.calculate_gpa(enrollment)
        return Response({'enrollment_id': str(enrollment.id), 'gpa': str(gpa)})

    @action(detail=False, methods=['get'], url_path='transcript/(?P<student_id>[^/.]+)')
    def transcript(self, request, student_id=None):
        """Download a PDF transcript for a student."""
        try:
            student = StudentProfile.objects.get(id=student_id, university=request.tenant)
        except StudentProfile.DoesNotExist:
            return Response({'error': 'Student not found'}, status=status.HTTP_404_NOT_FOUND)
        pdf = TranscriptService.generate_transcript(student)
        return FileResponse(pdf, as_attachment=True, filename=f"Transcript_{student.matricule}.pdf")
