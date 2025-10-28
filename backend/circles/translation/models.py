"""
Translation Circle Models

Django models for translation circle functionality.

Storage Strategy (Hybrid):
- JSON files are the permanent source of truth
- During active sessions, content loaded into database for fast editing
- When session ends, corrections written back to JSON file
- Database tracks metadata and provides performance for active sessions

Models:
- TranslationDocument: Metadata about JSON translation files
- TranslationSession: Active editing sessions
- ParagraphCorrection: Paragraph-level edits (temporary, session-scoped)

Status: Phase 2 - Implementation
"""

from django.db import models
from django.utils import timezone
from circles.models import Circle
from authentication.models import AccessKey


class TranslationDocument(models.Model):
    """
    Metadata for translation JSON files.

    Links a JSON file to a circle and tracks when it was loaded/saved.
    The JSON file itself is the permanent storage for translations.
    """
    STATUS_CHOICES = [
        ('uploaded', 'Uploaded'),
        ('loaded', 'Loaded into DB'),
        ('in_session', 'Active Session'),
        ('saved', 'Saved to JSON'),
        ('archived', 'Archived'),
    ]

    circle = models.ForeignKey(
        Circle,
        on_delete=models.CASCADE,
        related_name='translation_documents'
    )
    file_path = models.CharField(
        max_length=512,
        help_text="Path to JSON file (relative or absolute)"
    )
    language = models.CharField(
        max_length=50,
        help_text="Target language (e.g., 'thai', 'vietnamese')"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='uploaded'
    )

    # Metadata from JSON
    title = models.CharField(max_length=255, blank=True)
    edition = models.CharField(max_length=50, blank=True)
    json_version = models.CharField(max_length=50, blank=True)

    # Tracking
    created_by = models.ForeignKey(
        AccessKey,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_documents'
    )
    created_at = models.DateTimeField(default=timezone.now)
    last_loaded_at = models.DateTimeField(null=True, blank=True)
    last_saved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} ({self.language}) - {self.circle.name}"

    class Meta:
        verbose_name = "Translation Document"
        verbose_name_plural = "Translation Documents"
        unique_together = ['circle', 'file_path']


class TranslationSession(models.Model):
    """
    Active translation editing session.

    When a session starts, paragraph data is loaded from JSON into ParagraphCorrection.
    When a session ends, corrections are written back to JSON.
    """
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('aborted', 'Aborted'),
    ]

    document = models.ForeignKey(
        TranslationDocument,
        on_delete=models.CASCADE,
        related_name='sessions'
    )
    circle = models.ForeignKey(
        Circle,
        on_delete=models.CASCADE,
        related_name='translation_sessions'
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='active'
    )

    # Session lifecycle
    started_by = models.ForeignKey(
        AccessKey,
        on_delete=models.SET_NULL,
        null=True,
        related_name='started_sessions'
    )
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    ended_by = models.ForeignKey(
        AccessKey,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='ended_sessions'
    )

    # Statistics
    total_paragraphs = models.IntegerField(default=0)
    paragraphs_modified = models.IntegerField(default=0)

    def __str__(self):
        return f"Session {self.id} - {self.document.title} ({self.status})"

    class Meta:
        verbose_name = "Translation Session"
        verbose_name_plural = "Translation Sessions"


class ParagraphCorrection(models.Model):
    """
    Temporary storage for paragraph corrections during active session.

    One record per paragraph in the JSON file.
    When session ends, corrected_translation is written back to JSON file.
    After save, these records can be archived or deleted.
    """
    STATUS_CHOICES = [
        ('unchecked', 'Unchecked'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
    ]

    session = models.ForeignKey(
        TranslationSession,
        on_delete=models.CASCADE,
        related_name='paragraphs'
    )

    # Paragraph identification
    paragraph_id = models.CharField(
        max_length=50,
        help_text="Paragraph ID from JSON (e.g., 'p9-1')"
    )
    chapter_id = models.CharField(max_length=50, blank=True)
    section_id = models.CharField(max_length=50, blank=True)

    # Content (read-only from JSON)
    text = models.TextField(
        help_text="Original English text (read-only)"
    )
    original_translation = models.TextField(
        help_text="AI-generated translation from JSON (read-only)"
    )

    # Editable correction
    corrected_translation = models.TextField(
        help_text="Human-corrected translation (editable)"
    )

    # Status tracking
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='unchecked'
    )

    # Attribution
    last_modified_by = models.ForeignKey(
        AccessKey,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='paragraph_edits'
    )
    last_modified_at = models.DateTimeField(auto_now=True)

    # Approval tracking (facilitator only)
    approved_by = models.ForeignKey(
        AccessKey,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_paragraphs'
    )
    approved_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.paragraph_id} - {self.session.document.title}"

    class Meta:
        verbose_name = "Paragraph Correction"
        verbose_name_plural = "Paragraph Corrections"
        unique_together = ['session', 'paragraph_id']
        ordering = ['paragraph_id']
