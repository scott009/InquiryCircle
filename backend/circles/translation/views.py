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
from django.http import JsonResponse

from authentication.views import get_key_from_request
from circles.models import Circle, CircleParticipant
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


def check_circle_access(request, circle_id):
    """
    Check if user has access to a translation circle.

    Returns: tuple (access_key, circle, error_response)
    - On success: (access_key, circle, None)
    - On failure: (None, None, JsonResponse with error)
    """
    # Verify authentication
    access_key, error = get_key_from_request(request)
    if not access_key:
        return None, None, JsonResponse({'error': error}, status=401)

    # Get circle and verify it's a translation circle
    try:
        circle = Circle.objects.get(id=circle_id, circle_type='translation')
    except Circle.DoesNotExist:
        return None, None, JsonResponse(
            {'error': 'Translation circle not found'},
            status=404
        )

    # Check membership
    if access_key.role == 'facilitator':
        if circle.facilitator_key != access_key:
            return None, None, JsonResponse(
                {'error': 'Access denied'},
                status=403
            )
    else:
        if not CircleParticipant.objects.filter(
            circle=circle,
            access_key=access_key
        ).exists():
            return None, None, JsonResponse(
                {'error': 'Access denied'},
                status=403
            )

    return access_key, circle, None


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

    # Check circle access
    circle_id = request.data.get('circle_id')
    access_key, circle, error_response = check_circle_access(request, circle_id)
    if error_response:
        return error_response

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
        # Use authenticated user
        started_by = access_key

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

    # Check circle access
    access_key, circle, error_response = check_circle_access(request, session.document.circle_id)
    if error_response:
        return error_response

    if session.status != 'active':
        return Response(
            {'error': f'Session is not active (status: {session.status})'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # Use authenticated user
        ended_by = access_key

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

    # Check circle access
    access_key, circle, error_response = check_circle_access(request, session.document.circle_id)
    if error_response:
        return error_response

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

    # Check circle access
    access_key, circle, error_response = check_circle_access(request, session.document.circle_id)
    if error_response:
        return error_response

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

    # Check circle access
    access_key, circle, error_response = check_circle_access(request, paragraph.session.document.circle_id)
    if error_response:
        return error_response

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

    # Check circle access
    access_key, circle, error_response = check_circle_access(request, paragraph.session.document.circle_id)
    if error_response:
        return error_response

    # Validate input
    update_serializer = ParagraphUpdateSerializer(data=request.data)
    if not update_serializer.is_valid():
        return Response(update_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Update paragraph
    paragraph.corrected_translation = update_serializer.validated_data['corrected_translation']
    paragraph.status = update_serializer.validated_data.get('status', 'in_progress')

    # Use authenticated user
    paragraph.last_modified_by = access_key
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

    # Check circle access and verify facilitator role
    access_key, circle, error_response = check_circle_access(request, paragraph.session.document.circle_id)
    if error_response:
        return error_response

    if access_key.role != 'facilitator':
        return JsonResponse(
            {'error': 'Only facilitators can approve paragraphs'},
            status=403
        )

    # Use authenticated user
    approved_by = access_key

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
        # Get authenticated user
        access_key, error = get_key_from_request(self.request)
        if not access_key:
            return TranslationDocument.objects.none()

        queryset = super().get_queryset()
        circle_id = self.request.query_params.get('circle')
        if circle_id:
            # Verify user has access to this circle
            _, _, error_response = check_circle_access(self.request, circle_id)
            if error_response:
                return TranslationDocument.objects.none()
            queryset = queryset.filter(circle_id=circle_id)
        else:
            # Return documents for circles the user has access to
            if access_key.role == 'facilitator':
                # Facilitators see their own circle documents
                user_circles = Circle.objects.filter(
                    facilitator_key=access_key,
                    circle_type='translation'
                ).values_list('id', flat=True)
            else:
                # Participants see documents from their circles
                user_circles = CircleParticipant.objects.filter(
                    access_key=access_key
                ).values_list('circle_id', flat=True)
            queryset = queryset.filter(circle_id__in=user_circles)

        return queryset
