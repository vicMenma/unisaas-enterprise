from apps.accounts.permissions import IsUniversityAdmin
from apps.common.viewsets import TenantModelViewSet

from .models import AcademicYear, Course, CourseAllocation, Department, Faculty, Programme, Semester
from .serializers import (
    AcademicYearSerializer,
    CourseAllocationSerializer,
    CourseSerializer,
    DepartmentSerializer,
    FacultySerializer,
    ProgrammeSerializer,
    SemesterSerializer,
)


class FacultyViewSet(TenantModelViewSet):
    queryset = Faculty.objects.all()
    serializer_class = FacultySerializer
    permission_classes = [IsUniversityAdmin]


class DepartmentViewSet(TenantModelViewSet):
    queryset = Department.objects.select_related("faculty")
    serializer_class = DepartmentSerializer
    permission_classes = [IsUniversityAdmin]


class AcademicYearViewSet(TenantModelViewSet):
    queryset = AcademicYear.objects.all()
    serializer_class = AcademicYearSerializer
    permission_classes = [IsUniversityAdmin]


class ProgrammeViewSet(TenantModelViewSet):
    queryset = Programme.objects.select_related("department", "department__faculty")
    serializer_class = ProgrammeSerializer
    permission_classes = [IsUniversityAdmin]


class SemesterViewSet(TenantModelViewSet):
    queryset = Semester.objects.select_related("academic_year")
    serializer_class = SemesterSerializer
    permission_classes = [IsUniversityAdmin]


class CourseViewSet(TenantModelViewSet):
    queryset = Course.objects.select_related("department", "programme")
    serializer_class = CourseSerializer
    permission_classes = [IsUniversityAdmin]

    def get_queryset(self):
        qs = super().get_queryset()
        department = self.request.query_params.get("department")
        programme = self.request.query_params.get("programme")
        if department:
            qs = qs.filter(department_id=department)
        if programme:
            qs = qs.filter(programme_id=programme)
        return qs


class CourseAllocationViewSet(TenantModelViewSet):
    queryset = CourseAllocation.objects.select_related("course", "teacher", "semester", "academic_year")
    serializer_class = CourseAllocationSerializer
    permission_classes = [IsUniversityAdmin]
