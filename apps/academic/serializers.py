from rest_framework import serializers

from apps.accounts.models import User
from apps.common.serializers import TenantScopedModelSerializer

from .models import (
    AcademicYear,
    Course,
    CourseAllocation,
    Department,
    Faculty,
    Programme,
    Semester,
)


class AcademicYearSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicYear
        fields = ("id", "name", "start_date", "end_date", "is_active", "created_at")
        read_only_fields = ("id", "created_at")


class ProgrammeSerializer(TenantScopedModelSerializer):
    tenant_related_fields = {"department": Department}

    class Meta:
        model = Programme
        fields = ("id", "name", "code", "department", "duration_years", "degree_type", "created_at")
        read_only_fields = ("id", "created_at")


class CourseSerializer(TenantScopedModelSerializer):
    tenant_related_fields = {"department": Department, "programme": Programme}

    class Meta:
        model = Course
        fields = ("id", "code", "name", "credits", "department", "programme", "created_at")
        read_only_fields = ("id", "created_at")


class DepartmentSerializer(TenantScopedModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)
    programmes = ProgrammeSerializer(many=True, read_only=True)
    tenant_related_fields = {"faculty": Faculty}

    class Meta:
        model = Department
        fields = ("id", "name", "code", "faculty", "programmes", "courses", "created_at")
        read_only_fields = ("id", "created_at")


class FacultySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = ("id", "name", "code", "departments", "created_at")
        read_only_fields = ("id", "created_at")


class SemesterSerializer(TenantScopedModelSerializer):
    tenant_related_fields = {"academic_year": AcademicYear}

    class Meta:
        model = Semester
        fields = ("id", "name", "academic_year", "start_date", "end_date", "is_active", "created_at")
        read_only_fields = ("id", "created_at")


class CourseAllocationSerializer(TenantScopedModelSerializer):
    tenant_related_fields = {
        "course": Course,
        "teacher": User,
        "semester": Semester,
        "academic_year": AcademicYear,
    }

    class Meta:
        model = CourseAllocation
        fields = ("id", "course", "teacher", "semester", "academic_year", "created_at")
        read_only_fields = ("id", "created_at")

    def validate_teacher(self, teacher):
        if teacher.role != "teacher":
            raise serializers.ValidationError("Course allocations require a teacher user.")
        return teacher
