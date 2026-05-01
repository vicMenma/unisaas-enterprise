from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Grade
from .serializers import GradeSerializer
from .services import GPAService
from registration.models import Enrollment
from accounts.permissions import IsExaminationStaff

class GradeViewSet(viewsets.ModelViewSet):
    serializer_class = GradeSerializer
    permission_classes = [IsExaminationStaff]

    def get_queryset(self):
        # Strict tenant isolation
        return Grade.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)

    @action(detail=False, methods=['get'], url_path='gpa/(?P<enrollment_id>[^/.]+)')
    def gpa(self, request, enrollment_id=None):
        try:
            enrollment = Enrollment.objects.get(id=enrollment_id, university=request.tenant)
        except Enrollment.DoesNotExist:
            return Response({'error': 'Enrollment not found'}, status=status.HTTP_404_NOT_FOUND)
        
        gpa = GPAService.calculate_gpa(enrollment)
        return Response({'enrollment_id': enrollment.id, 'gpa': gpa})
