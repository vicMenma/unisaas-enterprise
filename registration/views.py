from rest_framework import viewsets, permissions
from .models import Enrollment
from .serializers import EnrollmentSerializer
from accounts.permissions import IsRegistrationStaff

class EnrollmentViewSet(viewsets.ModelViewSet):
    serializer_class = EnrollmentSerializer
    permission_classes = [IsRegistrationStaff]

    def get_queryset(self):
        # Strict tenant isolation
        return Enrollment.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)
