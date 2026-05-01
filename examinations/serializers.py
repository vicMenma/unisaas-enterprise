from rest_framework import serializers
from .models import Grade

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = ('id', 'enrollment_course', 'score', 'grade_points', 'letter_grade', 'is_locked', 'created_at')
        read_only_fields = ('is_locked', 'created_at')
