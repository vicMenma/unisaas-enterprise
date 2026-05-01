from rest_framework import serializers
from .models import Enrollment, EnrollmentCourse
from academic.models import Semester, Course

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

class EnrollmentCourseSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    class Meta:
        model = EnrollmentCourse
        fields = ('id', 'course')

class EnrollmentSerializer(serializers.ModelSerializer):
    courses = EnrollmentCourseSerializer(many=True, read_only=True)
    semester = SemesterSerializer(read_only=True)
    
    class Meta:
        model = Enrollment
        fields = ('id', 'student', 'semester', 'is_active', 'courses', 'created_at')
