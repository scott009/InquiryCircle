"""
Translation Circle Serializers

DRF serializers for translation circle data.

Serializers:
- TranslationDocumentSerializer: Document metadata
- TranslationSessionSerializer: Active session info
- ParagraphCorrectionSerializer: Paragraph data and corrections
- ParagraphUpdateSerializer: For updating corrections

Status: Phase 2 - Implementation
"""

from rest_framework import serializers
from .models import TranslationDocument, TranslationSession, ParagraphCorrection


class TranslationDocumentSerializer(serializers.ModelSerializer):
    """Serialize translation document metadata"""

    circle_name = serializers.CharField(source='circle.name', read_only=True)
    created_by_key = serializers.CharField(source='created_by.key', read_only=True)

    class Meta:
        model = TranslationDocument
        fields = [
            'id',
            'circle',
            'circle_name',
            'file_path',
            'language',
            'status',
            'title',
            'edition',
            'json_version',
            'created_by',
            'created_by_key',
            'created_at',
            'last_loaded_at',
            'last_saved_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'last_loaded_at',
            'last_saved_at',
        ]


class TranslationSessionSerializer(serializers.ModelSerializer):
    """Serialize translation session data"""

    document_title = serializers.CharField(source='document.title', read_only=True)
    document_language = serializers.CharField(source='document.language', read_only=True)
    circle_name = serializers.CharField(source='circle.name', read_only=True)
    started_by_key = serializers.CharField(source='started_by.key', read_only=True)
    ended_by_key = serializers.CharField(source='ended_by.key', read_only=True, allow_null=True)

    class Meta:
        model = TranslationSession
        fields = [
            'id',
            'document',
            'document_title',
            'document_language',
            'circle',
            'circle_name',
            'status',
            'started_by',
            'started_by_key',
            'started_at',
            'ended_at',
            'ended_by',
            'ended_by_key',
            'total_paragraphs',
            'paragraphs_modified',
        ]
        read_only_fields = [
            'id',
            'started_at',
            'ended_at',
            'total_paragraphs',
        ]


class ParagraphCorrectionSerializer(serializers.ModelSerializer):
    """Serialize paragraph correction data"""

    last_modified_by_key = serializers.CharField(
        source='last_modified_by.key',
        read_only=True,
        allow_null=True
    )
    approved_by_key = serializers.CharField(
        source='approved_by.key',
        read_only=True,
        allow_null=True
    )

    class Meta:
        model = ParagraphCorrection
        fields = [
            'id',
            'session',
            'paragraph_id',
            'chapter_id',
            'section_id',
            'text',
            'original_translation',
            'corrected_translation',
            'status',
            'last_modified_by',
            'last_modified_by_key',
            'last_modified_at',
            'approved_by',
            'approved_by_key',
            'approved_at',
        ]
        read_only_fields = [
            'id',
            'session',
            'paragraph_id',
            'chapter_id',
            'section_id',
            'text',
            'original_translation',
            'last_modified_at',
        ]


class ParagraphUpdateSerializer(serializers.Serializer):
    """Serializer for updating paragraph corrections"""

    corrected_translation = serializers.CharField(required=True)
    status = serializers.ChoiceField(
        choices=['unchecked', 'in_progress', 'approved'],
        required=False,
        default='in_progress'
    )

    def validate_corrected_translation(self, value):
        """Ensure corrected translation is not empty"""
        if not value or not value.strip():
            raise serializers.ValidationError("Corrected translation cannot be empty")
        return value


class SessionStartSerializer(serializers.Serializer):
    """Serializer for starting a translation session"""

    document_id = serializers.IntegerField(required=True)
    circle_id = serializers.IntegerField(required=True)

    def validate(self, data):
        """Validate that document belongs to circle"""
        from .models import TranslationDocument
        try:
            document = TranslationDocument.objects.get(
                id=data['document_id'],
                circle_id=data['circle_id']
            )
            data['document'] = document
        except TranslationDocument.DoesNotExist:
            raise serializers.ValidationError(
                "Document not found or does not belong to this circle"
            )
        return data


class SessionEndSerializer(serializers.Serializer):
    """Serializer for ending a translation session"""

    session_id = serializers.IntegerField(required=True)

    def validate_session_id(self, value):
        """Validate that session exists and is active"""
        try:
            session = TranslationSession.objects.get(id=value, status='active')
            return value
        except TranslationSession.DoesNotExist:
            raise serializers.ValidationError("Active session not found")
