"""
Translation Circle URL Configuration
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router for ViewSets
router = DefaultRouter()
router.register(r'documents', views.TranslationDocumentViewSet, basename='translation-document')

# URL patterns
urlpatterns = [
    # Session management
    path('sessions/start/', views.start_session, name='translation-session-start'),
    path('sessions/<int:session_id>/', views.get_session, name='translation-session-detail'),
    path('sessions/<int:session_id>/end/', views.end_session, name='translation-session-end'),
    path('sessions/<int:session_id>/paragraphs/', views.list_paragraphs, name='translation-session-paragraphs'),

    # Paragraph operations
    path('paragraphs/<int:paragraph_id>/', views.get_paragraph, name='translation-paragraph-detail'),
    path('paragraphs/<int:paragraph_id>/update/', views.update_paragraph, name='translation-paragraph-update'),
    path('paragraphs/<int:paragraph_id>/approve/', views.approve_paragraph, name='translation-paragraph-approve'),

    # Include router URLs (for documents)
    path('', include(router.urls)),
]
