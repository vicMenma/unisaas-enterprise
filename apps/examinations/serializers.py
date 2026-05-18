from rest_framework import serializers

from apps.common.serializers import TenantScopedPrimaryKeyRelatedField
from apps.registration.models import EnrollmentCourse

from .models import Grade
from .services import GradeScale


class GradeSerializer(serializers.ModelSerializer):
    enrollment_course = TenantScopedPrimaryKeyRelatedField(queryset=EnrollmentCourse.objects.all())

    class Meta:
        model = Grade
        fields = ("id", "enrollment_course", "score", "grade_points", "letter_grade", "is_locked", "created_at")
        read_only_fields = ("id", "grade_points", "letter_grade", "is_locked", "created_at")

    def validate_score(self, score):
        if score < 0 or score > 100:
            raise serializers.ValidationError("Score must be between 0 and 100.")
        return score

    def validate_enrollment_course(self, enrollment_course):
        if self.instance is None and hasattr(enrollment_course, "grade"):
            raise serializers.ValidationError("This enrollment course already has a grade.")
        return enrollment_course

    def create(self, validated_data):
        letter, points = GradeScale.from_score(validated_data["score"])
        validated_data["letter_grade"] = letter
        validated_data["grade_points"] = points
        return super().create(validated_data)

    def update(self, instance, validated_data):
        if "score" in validated_data:
            letter, points = GradeScale.from_score(validated_data["score"])
            validated_data["letter_grade"] = letter
            validated_data["grade_points"] = points
        return super().update(instance, validated_data)
