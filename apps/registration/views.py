from apps.accounts.permissions import IsRegistrationStaff
from apps.common.viewsets import TenantModelViewSet

from .models import Enrollment, EnrollmentCourse
from .serializers import EnrollmentCourseSerializer, EnrollmentSerializer


class EnrollmentViewSet(TenantModelViewSet):
    queryset = Enrollment.objects.select_related("student", "semester").prefetch_related("courses__course")
    serializer_class = EnrollmentSerializer
    permission_classes = [IsRegistrationStaff]


class EnrollmentCourseViewSet(TenantModelViewSet):
    queryset = EnrollmentCourse.objects.select_related("enrollment", "course")
    serializer_class = EnrollmentCourseSerializer
    permission_classes = [IsRegistrationStaff]
