"""
Translation Circle Services

Business logic for translation circle operations.

Services:
- JSONDocumentLoader: Load JSON and populate database
- JSONDocumentWriter: Save corrections back to JSON
- ParagraphNavigator: Navigate hierarchical JSON structure

Status: Phase 2 - Implementation
"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from django.utils import timezone
from .models import TranslationDocument, TranslationSession, ParagraphCorrection


class JSONDocumentLoader:
    """
    Load translation JSON files and populate database for active session.

    Reads hierarchical JSON structure and creates ParagraphCorrection records
    for each paragraph in the document.
    """

    def __init__(self, json_path: str):
        """
        Initialize loader with JSON file path.

        Args:
            json_path: Absolute or relative path to JSON file
        """
        self.json_path = Path(json_path)
        self.data = None
        self.metadata = None

    def load_json(self) -> Dict:
        """Load and parse JSON file"""
        if not self.json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {self.json_path}")

        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)

        self.metadata = self.data.get('metadata', {})
        return self.data

    def extract_paragraphs(self) -> List[Dict]:
        """
        Extract all paragraphs from hierarchical JSON structure.

        Returns:
            List of paragraph dictionaries with flattened structure
        """
        if not self.data:
            self.load_json()

        paragraphs = []
        content = self.data.get('content', [])

        for section in content:
            if section.get('type') == 'section':
                section_id = section.get('id')
                chapters = section.get('chapters', [])

                for chapter in chapters:
                    chapter_id = chapter.get('id')
                    self._extract_from_sections(
                        chapter.get('sections', []),
                        chapter_id,
                        section_id,
                        paragraphs
                    )

        return paragraphs

    def _extract_from_sections(self, sections: List, chapter_id, section_id, paragraphs: List):
        """Recursively extract paragraphs from sections"""
        for section in sections:
            for content_item in section.get('content', []):
                if content_item.get('type') == 'paragraph':
                    para = self._format_paragraph(content_item, chapter_id, section_id)
                    if para:
                        paragraphs.append(para)
                elif content_item.get('type') == 'subsection':
                    # Recurse into subsections
                    for sub_item in content_item.get('content', []):
                        if sub_item.get('type') == 'paragraph':
                            para = self._format_paragraph(sub_item, chapter_id, section_id)
                            if para:
                                paragraphs.append(para)

    def _format_paragraph(self, para: Dict, chapter_id, section_id) -> Optional[Dict]:
        """Format paragraph data for database storage"""
        paragraph_id = para.get('id')
        if not paragraph_id:
            return None

        # Get language from metadata
        language = self.metadata.get('language', 'thai')
        lang_text_field = f"{language}_text"
        corrected_field = f"corrected_{language}_text"

        return {
            'paragraph_id': paragraph_id,
            'chapter_id': str(chapter_id),
            'section_id': str(section_id),
            'text': para.get('text', ''),
            'original_translation': para.get(lang_text_field, ''),
            'corrected_translation': para.get(corrected_field, para.get(lang_text_field, '')),
            'status': para.get(f'{language}_status', 'unchecked'),
        }

    def create_session(self, document: TranslationDocument, started_by) -> TranslationSession:
        """
        Create a new translation session and load paragraphs into database.

        Args:
            document: TranslationDocument instance
            started_by: AccessKey of user starting session

        Returns:
            TranslationSession instance with loaded paragraphs
        """
        # Load JSON
        self.load_json()
        paragraphs = self.extract_paragraphs()

        # Create session
        session = TranslationSession.objects.create(
            document=document,
            circle=document.circle,
            started_by=started_by,
            total_paragraphs=len(paragraphs)
        )

        # Create ParagraphCorrection records
        corrections = []
        for para_data in paragraphs:
            correction = ParagraphCorrection(
                session=session,
                paragraph_id=para_data['paragraph_id'],
                chapter_id=para_data['chapter_id'],
                section_id=para_data['section_id'],
                text=para_data['text'],
                original_translation=para_data['original_translation'],
                corrected_translation=para_data['corrected_translation'],
                status=para_data['status']
            )
            corrections.append(correction)

        # Bulk create for performance
        ParagraphCorrection.objects.bulk_create(corrections)

        # Update document status
        document.status = 'in_session'
        document.last_loaded_at = timezone.now()
        document.save()

        return session


class JSONDocumentWriter:
    """
    Write corrections from database back to JSON file.

    Updates corrected_<language>_text fields and metadata in JSON file.
    """

    def __init__(self, json_path: str):
        """
        Initialize writer with JSON file path.

        Args:
            json_path: Absolute or relative path to JSON file
        """
        self.json_path = Path(json_path)
        self.data = None

    def load_json(self) -> Dict:
        """Load current JSON file"""
        with open(self.json_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        return self.data

    def update_paragraph(self, paragraph_id: str, corrected_text: str,
                        status: str, approved_by_name: Optional[str] = None,
                        approved_by_id: Optional[str] = None):
        """
        Update a single paragraph in the JSON data structure.

        Args:
            paragraph_id: Paragraph ID (e.g., 'p9-1')
            corrected_text: Human-corrected translation
            status: Paragraph status ('unchecked', 'in_progress', 'approved')
            approved_by_name: Name of approver (for approved status)
            approved_by_id: ID of approver (for approved status)
        """
        if not self.data:
            self.load_json()

        language = self.data.get('metadata', {}).get('language', 'thai')
        corrected_field = f"corrected_{language}_text"
        status_field = f"{language}_status"

        # Find and update paragraph
        found = self._find_and_update_paragraph(
            self.data.get('content', []),
            paragraph_id,
            corrected_field,
            status_field,
            corrected_text,
            status,
            approved_by_name,
            approved_by_id,
            language
        )

        if not found:
            raise ValueError(f"Paragraph {paragraph_id} not found in JSON")

    def _find_and_update_paragraph(self, content: List, paragraph_id: str,
                                   corrected_field: str, status_field: str,
                                   corrected_text: str, status: str,
                                   approved_by_name: Optional[str],
                                   approved_by_id: Optional[str],
                                   language: str) -> bool:
        """Recursively find and update paragraph in JSON structure"""
        for section in content:
            if section.get('type') == 'section':
                for chapter in section.get('chapters', []):
                    for sect in chapter.get('sections', []):
                        for item in sect.get('content', []):
                            # Check paragraph
                            if item.get('type') == 'paragraph' and item.get('id') == paragraph_id:
                                return self._update_paragraph_fields(
                                    item, corrected_field, status_field,
                                    corrected_text, status, approved_by_name,
                                    approved_by_id, language
                                )
                            # Check subsections
                            elif item.get('type') == 'subsection':
                                for sub_item in item.get('content', []):
                                    if sub_item.get('type') == 'paragraph' and sub_item.get('id') == paragraph_id:
                                        return self._update_paragraph_fields(
                                            sub_item, corrected_field, status_field,
                                            corrected_text, status, approved_by_name,
                                            approved_by_id, language
                                        )
        return False

    def _update_paragraph_fields(self, para: Dict, corrected_field: str,
                                status_field: str, corrected_text: str,
                                status: str, approved_by_name: Optional[str],
                                approved_by_id: Optional[str], language: str) -> bool:
        """Update paragraph fields"""
        para[corrected_field] = corrected_text
        para[status_field] = status

        if status == 'approved':
            para[f'{language}_approved_by_name'] = approved_by_name
            para[f'{language}_approved_by_id'] = approved_by_id
            para[f'{language}_approved_at'] = timezone.now().isoformat()

        return True

    def save_json(self):
        """Write updated data back to JSON file"""
        with open(self.json_path, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)

    def save_session(self, session: TranslationSession, ended_by):
        """
        Save all corrections from a session back to JSON file.

        Args:
            session: TranslationSession instance
            ended_by: AccessKey of user ending session
        """
        self.load_json()

        # Get all modified paragraphs
        paragraphs = session.paragraphs.all()

        for para in paragraphs:
            approved_by_name = None
            approved_by_id = None

            if para.approved_by:
                approved_by_name = para.approved_by.key
                approved_by_id = str(para.approved_by.id)

            self.update_paragraph(
                paragraph_id=para.paragraph_id,
                corrected_text=para.corrected_translation,
                status=para.status,
                approved_by_name=approved_by_name,
                approved_by_id=approved_by_id
            )

        # Save to file
        self.save_json()

        # Update session and document status
        session.status = 'completed'
        session.ended_at = timezone.now()
        session.ended_by = ended_by
        session.save()

        session.document.status = 'saved'
        session.document.last_saved_at = timezone.now()
        session.document.save()
