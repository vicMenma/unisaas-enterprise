from rest_framework import serializers
from .models import Application, Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'doc_type', 'file', 'is_verified', 'created_at')
        read_only_fields = ('id', 'created_at')


class ApplicationSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Application
        fields = (
            'id', 'first_name', 'last_name', 'email',
            'program_applied', 'entry_year', 'status',
            'submission_date', 'offer_letter', 'documents',
        )
        read_only_fields = ('id', 'status', 'submission_date', 'offer_letter')
