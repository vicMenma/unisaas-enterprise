from rest_framework import serializers
from .models import StudentProfile
from accounts.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'role', 'is_active', 'created_at')

class StudentProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = StudentProfile
        fields = ('id', 'user', 'matricule', 'program_id', 'status', 'entry_year', 'current_level', 'created_at')
        read_only_fields = ('matricule', 'created_at')
