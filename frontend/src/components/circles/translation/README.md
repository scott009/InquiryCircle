# Translation Circle Components

Vue components for collaborative translation review interface.

## Components

### EnglishTextDisplay.vue (engtxt1)
Read-only display of English source text from JSON `text` field.

### AITranslationDisplay.vue (aitrans1)
Read-only display of AI-generated translation from JSON `<language>_text` field.

### CorrectedTextEditor.vue (corrected1)
Editable textarea for human-corrected translation (`corrected_<language>_text`).
Includes Save button to persist changes to backend.

### DocumentNavigator.vue (docnav1)
JSON-based navigation showing document structure (chapters, sections, paragraphs).
Allows jumping between paragraphs for review.

## Development Status
**Phase 1 (Current)**: Stub components created ✅
**Phase 3 (Next)**: Implement functional components with API integration
**Phase 5**: Add video integration to layout

## Usage
These components will be composed together in `TranslationCircle.vue` to create the 4-window translation editing interface.

## Related Documentation
See `/Documentation/project-spec.md` - Translation Circle Specification section
