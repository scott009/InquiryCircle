"""
Translation Circle API Views

REST API endpoints for translation circle operations.

Endpoints:
- POST /api/translation/sessions/start/ - Start new translation session
- POST /api/translation/sessions/<id>/end/ - End session and save to JSON
- GET /api/translation/sessions/<id>/ - Get session details
- GET /api/translation/sessions/<id>/paragraphs/ - List all paragraphs in session
- GET /api/translation/paragraphs/<id>/ - Get single paragraph
- PATCH /api/translation/paragraphs/<id>/ - Update paragraph correction
- POST /api/translation/paragraphs/<id>/approve/ - Approve paragraph (facilitator)

Status: Phase 2 - Implementation
"""

from rest_framework import viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone

from .models import TranslationDocument, TranslationSession, ParagraphCorrection
from .serializers import (
    TranslationDocumentSerializer,
    TranslationSessionSerializer,
    ParagraphCorrectionSerializer,
    ParagraphUpdateSerializer,
    SessionStartSerializer,
    SessionEndSerializer,
)
from .services import JSONDocumentLoader, JSONDocumentWriter


@api_view(['POST'])
def start_session(request):
    """
    Start a new translation session.

    Loads JSON file into database and creates session.

    POST /api/translation/sessions/start/
    Body: {
        "document_id": 1,
        "circle_id": 1
    }
    """
    serializer = SessionStartSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    document = serializer.validated_data['document']

    # Check if there's already an active session
    existing_session = TranslationSession.objects.filter(
        document=document,
        status='active'
    ).first()

    if existing_session:
        return Response(
            {
                'error': 'An active session already exists for this document',
                'session_id': existing_session.id
            },
            status=status.HTTP_409_CONFLICT
        )

    # Create session using loader service
    try:
        # TODO: Get actual user from auth middleware
        # For now, use document.created_by as placeholder
        started_by = document.created_by

        loader = JSONDocumentLoader(document.file_path)
        session = loader.create_session(document, started_by)

        session_serializer = TranslationSessionSerializer(session)
        return Response(session_serializer.data, status=status.HTTP_201_CREATED)

    except FileNotFoundError as e:
        return Response(
            {'error': str(e)},
            status=status.HTTP_404_NOT_FOUND
        )
    except Exception as e:
        return Response(
            {'error': f'Failed to start session: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['POST'])
def end_session(request, session_id):
    """
    End translation session and save corrections to JSON.

    POST /api/translation/sessions/<id>/end/
    """
    session = get_object_or_404(TranslationSession, id=session_id)

    if session.status != 'active':
        return Response(
            {'error': f'Session is not active (status: {session.status})'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # TODO: Get actual user from auth middleware
        ended_by = session.started_by

        # Save to JSON using writer service
        writer = JSONDocumentWriter(session.document.file_path)
        writer.save_session(session, ended_by)

        session_serializer = TranslationSessionSerializer(session)
        return Response({
            'message': 'Session ended and corrections saved to JSON',
            'session': session_serializer.data
        })

    except Exception as e:
        return Response(
            {'error': f'Failed to end session: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
def get_session(request, session_id):
    """
    Get session details.

    GET /api/translation/sessions/<id>/
    """
    session = get_object_or_404(TranslationSession, id=session_id)
    serializer = TranslationSessionSerializer(session)
    return Response(serializer.data)


@api_view(['GET'])
def list_paragraphs(request, session_id):
    """
    List all paragraphs in a session.

    GET /api/translation/sessions/<id>/paragraphs/
    Query params:
    - status: Filter by status (unchecked, in_progress, approved)
    - chapter: Filter by chapter_id
    """
    session = get_object_or_404(TranslationSession, id=session_id)

    paragraphs = session.paragraphs.all()

    # Apply filters
    status_filter = request.query_params.get('status')
    if status_filter:
        paragraphs = paragraphs.filter(status=status_filter)

    chapter_filter = request.query_params.get('chapter')
    if chapter_filter:
        paragraphs = paragraphs.filter(chapter_id=chapter_filter)

    serializer = ParagraphCorrectionSerializer(paragraphs, many=True)
    return Response({
        'session_id': session_id,
        'total_paragraphs': paragraphs.count(),
        'paragraphs': serializer.data
    })


@api_view(['GET'])
def get_paragraph(request, paragraph_id):
    """
    Get single paragraph.

    GET /api/translation/paragraphs/<id>/
    """
    paragraph = get_object_or_404(ParagraphCorrection, id=paragraph_id)
    serializer = ParagraphCorrectionSerializer(paragraph)
    return Response(serializer.data)


@api_view(['PATCH'])
def update_paragraph(request, paragraph_id):
    """
    Update paragraph correction.

    PATCH /api/translation/paragraphs/<id>/
    Body: {
        "corrected_translation": "...",
        "status": "in_progress"  // optional
    }
    """
    paragraph = get_object_or_404(ParagraphCorrection, id=paragraph_id)

    # Validate input
    update_serializer = ParagraphUpdateSerializer(data=request.data)
    if not update_serializer.is_valid():
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update paragraph
    paragraph.corrected_translation = update_serializer.validated_data['corrected_translation']
    paragraph.status = update_serializer.validated_data.get('status', 'in_progress')

    # TODO: Get actual user from auth middleware
    # For now, use session.started_by as placeholder
    paragraph.last_modified_by = paragraph.session.started_by
    paragraph.save()

    # Update session statistics
    session = paragraph.session
    session.paragraphs_modified = session.paragraphs.exclude(
        status='unchecked'
    ).count()
    session.save()

    serializer = ParagraphCorrectionSerializer(paragraph)
    return Response(serializer.data)


@api_view(['POST'])
def approve_paragraph(request, paragraph_id):
    """
    Approve paragraph (facilitator only).

    POST /api/translation/paragraphs/<id>/approve/
    """
    paragraph = get_object_or_404(ParagraphCorrection, id=paragraph_id)

    # TODO: Add facilitator permission check
    # For now, anyone can approve

    # TODO: Get actual user from auth middleware
    approved_by = paragraph.session.started_by

    paragraph.status = 'approved'
    paragraph.approved_by = approved_by
    paragraph.approved_at = timezone.now()
    paragraph.save()

    serializer = ParagraphCorrectionSerializer(paragraph)
    return Response(serializer.data)


# ViewSet for TranslationDocument (optional - for document management)
class TranslationDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only viewset for translation documents.

    GET /api/translation/documents/ - List documents
    GET /api/translation/documents/<id>/ - Get document details
    """
    queryset = TranslationDocument.objects.all()
    serializer_class = TranslationDocumentSerializer

    def get_queryset(self):
        """Filter by circle if provided"""
        queryset = super().get_queryset()
        circle_id = self.request.query_params.get('circle')
        if circle_id:
            queryset = queryset.filter(circle_id=circle_id)
        return queryset
