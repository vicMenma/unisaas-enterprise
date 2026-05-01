from rest_framework import serializers
from .models import Faculty, Department, Semester, Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = ('id', 'code', 'name', 'credits', 'department', 'created_at')
        read_only_fields = ('id', 'created_at')


class DepartmentSerializer(serializers.ModelSerializer):
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = Department
        fields = ('id', 'name', 'code', 'faculty', 'courses', 'created_at')
        read_only_fields = ('id', 'created_at')


class FacultySerializer(serializers.ModelSerializer):
    departments = DepartmentSerializer(many=True, read_only=True)

    class Meta:
        model = Faculty
        fields = ('id', 'name', 'code', 'departments', 'created_at')
        read_only_fields = ('id', 'created_at')


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('id', 'name', 'start_date', 'end_date', 'is_active', 'created_at')
        read_only_fields = ('id', 'created_at')
