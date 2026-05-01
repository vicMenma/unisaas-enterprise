from rest_framework import viewsets
from accounts.permissions import IsUniversityAdmin
from .models import Faculty, Department, Semester, Course
from .serializers import FacultySerializer, DepartmentSerializer, SemesterSerializer, CourseSerializer


class FacultyViewSet(viewsets.ModelViewSet):
    serializer_class = FacultySerializer
    permission_classes = [IsUniversityAdmin]

    def get_queryset(self):
        return Faculty.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)


class DepartmentViewSet(viewsets.ModelViewSet):
    serializer_class = DepartmentSerializer
    permission_classes = [IsUniversityAdmin]

    def get_queryset(self):
        return Department.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)


class SemesterViewSet(viewsets.ModelViewSet):
    serializer_class = SemesterSerializer
    permission_classes = [IsUniversityAdmin]

    def get_queryset(self):
        return Semester.objects.filter(university=self.request.tenant)

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)


class CourseViewSet(viewsets.ModelViewSet):
    serializer_class = CourseSerializer
    permission_classes = [IsUniversityAdmin]

    def get_queryset(self):
        qs = Course.objects.filter(university=self.request.tenant)
        dept = self.request.query_params.get('department')
        if dept:
            qs = qs.filter(department_id=dept)
        return qs

    def perform_create(self, serializer):
        serializer.save(university=self.request.tenant)
