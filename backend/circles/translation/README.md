# Translation Circle Backend

Backend support for collaborative translation review and correction.

## Purpose
Enables groups to collaboratively review and correct AI-generated translations through:
- JSON document loading and parsing
- Paragraph-level correction tracking
- Language selection and management
- Integration with circle membership and authentication

## Structure
```
translation/
├── __init__.py       # Module initialization
├── models.py         # Django models (TranslationDocument, ParagraphCorrection)
├── views.py          # REST API endpoints
├── serializers.py    # DRF serializers
├── services.py       # Business logic
└── README.md         # This file
```

## Development Status
**Phase 1 (Current)**: Folder structure and stubs ✅
**Phase 2 (Next)**: Models, services, and API implementation
**Phase 3+**: Integration with frontend

## Related Documentation
See `/Documentation/project-spec.md` - Translation Circle Specification section
