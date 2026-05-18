from django.db import transaction
from rest_framework import serializers

from apps.academic.models import Course, Semester
from apps.common.serializers import TenantScopedModelSerializer, TenantScopedPrimaryKeyRelatedField
from apps.students.models import StudentProfile

from .models import Enrollment, EnrollmentCourse


class EnrollmentCourseSerializer(TenantScopedModelSerializer):
    course = TenantScopedPrimaryKeyRelatedField(queryset=Course.objects.all())
    tenant_related_fields = {"enrollment": Enrollment, "course": Course}

    class Meta:
        model = EnrollmentCourse
        fields = ("id", "enrollment", "course", "created_at")
        read_only_fields = ("id", "created_at")

    def validate(self, attrs):
        enrollment = attrs.get("enrollment")
        course = attrs.get("course")
        if enrollment and course and enrollment.university_id != course.university_id:
            raise serializers.ValidationError("Enrollment and course must belong to the same tenant.")
        return attrs


class EnrollmentSerializer(TenantScopedModelSerializer):
    student = TenantScopedPrimaryKeyRelatedField(queryset=StudentProfile.objects.all())
    semester = TenantScopedPrimaryKeyRelatedField(queryset=Semester.objects.all())
    courses = EnrollmentCourseSerializer(many=True, read_only=True)
    course_ids = TenantScopedPrimaryKeyRelatedField(
        queryset=Course.objects.all(),
        many=True,
        write_only=True,
        required=False,
    )

    class Meta:
        model = Enrollment
        fields = ("id", "student", "semester", "is_active", "courses", "course_ids", "created_at")
        read_only_fields = ("id", "created_at")

    def validate(self, attrs):
        student = attrs.get("student") or getattr(self.instance, "student", None)
        semester = attrs.get("semester") or getattr(self.instance, "semester", None)
        if student and semester and student.university_id != semester.university_id:
            raise serializers.ValidationError("Student and semester must belong to the same tenant.")
        exists = Enrollment.objects.filter(student=student, semester=semester)
        if self.instance:
            exists = exists.exclude(pk=self.instance.pk)
        if student and semester and exists.exists():
            raise serializers.ValidationError("Student is already registered for this semester.")
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        courses = validated_data.pop("course_ids", [])
        enrollment = Enrollment.objects.create(**validated_data)
        EnrollmentCourse.objects.bulk_create(
            [
                EnrollmentCourse(
                    university=enrollment.university,
                    enrollment=enrollment,
                    course=course,
                )
                for course in courses
            ],
            ignore_conflicts=True,
        )
        return enrollment
