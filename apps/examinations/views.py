from django.http import FileResponse
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from apps.accounts.permissions import IsExaminationStaff
from apps.common.viewsets import TenantModelViewSet
from apps.registration.models import Enrollment
from apps.students.models import StudentProfile
from unisaas.logging import EnterpriseLogger

from .models import Grade
from .serializers import GradeSerializer
from .services import GPAService
from .transcript import TranscriptService


class GradeViewSet(TenantModelViewSet):
    queryset = Grade.objects.select_related("enrollment_course", "enrollment_course__course")
    serializer_class = GradeSerializer
    permission_classes = [IsExaminationStaff]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == "teacher" and not self.request.user.is_superuser:
            qs = qs.filter(enrollment_course__course__allocations__teacher=self.request.user).distinct()
        return qs

    def perform_create(self, serializer):
        enrollment_course = serializer.validated_data["enrollment_course"]
        if not self._can_access_enrollment_course(enrollment_course):
            raise PermissionDenied("You are not allocated to this course.")
        instance = serializer.save(university=self.request.tenant)
        EnterpriseLogger.log_action(
            self.request,
            "Grade Created",
            "Grade",
            str(instance.id),
            new_state={"score": str(instance.score), "letter_grade": instance.letter_grade},
        )

    def perform_update(self, serializer):
        old = self.get_object()
        if old.is_locked:
            raise PermissionDenied("This grade is locked and cannot be modified.")
        previous = {"score": str(old.score), "letter_grade": old.letter_grade}
        instance = serializer.save()
        EnterpriseLogger.log_action(
            self.request,
            "Grade Updated",
            "Grade",
            str(instance.id),
            prev_state=previous,
            new_state={"score": str(instance.score), "letter_grade": instance.letter_grade},
        )

    def perform_destroy(self, instance):
        if instance.is_locked:
            raise PermissionDenied("This grade is locked and cannot be deleted.")
        EnterpriseLogger.log_action(
            self.request,
            "Grade Deleted",
            "Grade",
            str(instance.id),
            prev_state={"score": str(instance.score), "letter_grade": instance.letter_grade},
        )
        instance.delete()

    @action(detail=True, methods=["post"], url_path="approve")
    def approve(self, request, pk=None):
        grade = self.get_object()
        if not grade.is_locked:
            grade.is_locked = True
            grade.save(update_fields=["is_locked", "updated_at"])
            EnterpriseLogger.log_action(
                request,
                "Grade Approved",
                "Grade",
                str(grade.id),
                new_state={"is_locked": True},
            )
        return Response(self.get_serializer(grade).data)

    @action(detail=False, methods=["get"], url_path="gpa/(?P<enrollment_id>[^/.]+)")
    def gpa(self, request, enrollment_id=None):
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id, university=request.tenant)
        except Enrollment.DoesNotExist:
            return Response({"error": "Enrollment not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role == "teacher" and not enrollment.courses.filter(
            course__allocations__teacher=request.user,
            university=request.tenant,
        ).exists():
            raise PermissionDenied("You are not allocated to this enrollment.")
        gpa = GPAService.calculate_gpa(enrollment)
        return Response({"enrollment_id": str(enrollment.id), "gpa": str(gpa)})

    @action(detail=False, methods=["get"], url_path="transcript/(?P<student_id>[^/.]+)")
    def transcript(self, request, student_id=None):
        try:
            student = StudentProfile.objects.get(id=student_id, university=request.tenant)
        except StudentProfile.DoesNotExist:
            return Response({"error": "Student not found"}, status=status.HTTP_404_NOT_FOUND)
        if request.user.role == "teacher" and not student.enrollments.filter(
            courses__course__allocations__teacher=request.user,
            university=request.tenant,
        ).exists():
            raise PermissionDenied("You are not allocated to this student.")
        pdf = TranscriptService.generate_transcript(student)
        return FileResponse(pdf, as_attachment=True, filename=f"Transcript_{student.matricule}.pdf")

    def _can_access_enrollment_course(self, enrollment_course):
        user = self.request.user
        if user.is_superuser or user.role in {"owner", "university_admin", "examination"}:
            return True
        return enrollment_course.course.allocations.filter(
            teacher=user,
            university=self.request.tenant,
        ).exists()
