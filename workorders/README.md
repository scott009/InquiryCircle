# InquiryCircle Workorders

## Purpose
This directory contains **YAML workorders** - structured specifications for AI assistants (especially Claude Haiku) to build components independently. Each workorder provides complete context, requirements, and acceptance criteria for implementing and testing code.

## Philosophy
- **Build tested, production-ready code BEFORE it's needed** in the UI
- **Lower-level AIs (Haiku)** can execute well-defined workorders efficiently
- **Tests verify correctness** independent of UI/framework integration
- **Domain logic stays pure** and reusable across different infrastructures

## Directory Structure
```
workorders/
├── README.md                          # This file
├── templates/
│   └── workorder-template.yml       # Template for new workorders
├── workorder-reactions-domain.yml   # Build reaction domain models
├── workorder-reactions-tests.yml    # Build reaction unit tests
└── [future workorders...]
```

## Workorder Naming Convention
**Format**: `workorder-[feature]-[component].yml`

**Examples**:
- `workorder-reactions-domain.yml` - Reaction domain models
- `workorder-reactions-tests.yml` - Reaction unit tests
- `workorder-policy-implementation.yml` - Policy enforcement logic
- `workorder-django-integration.yml` - Django models for reactions

**Why this format?**
- ✅ Descriptive - immediately understand purpose
- ✅ Sortable - alphabetically organized by feature
- ✅ Searchable - easy to find related workorders
- ✅ Simple - no complex numbering schemes

## Workorder Structure

Each workorder YAML file contains:

### 1. **Metadata**
- Title, assigned AI, stage, priority, dependencies, effort estimate

### 2. **Context**
- Business description
- Reference materials (docs, existing code)
- Business rules

### 3. **Deliverables**
- Output file path(s)
- Required components to build

### 4. **Specifications**
- Detailed class/function/test specifications
- Enums, value objects, interfaces, services
- Test cases with arrange-act-assert pattern

### 5. **Technical Requirements**
- Language, dependencies (allowed/forbidden)
- Code style, structure guidelines

### 6. **Acceptance Criteria**
- Functional requirements (what it must do)
- Technical requirements (how it must be built)

### 7. **Validation**
- Commands to verify correctness
- Expected outputs/exit codes

### 8. **Notes & Hints**
- Important context for AI
- Implementation suggestions
- Common pitfalls to avoid

## Workflow

### Creating a New Workorder
1. Copy template: `cp templates/workorder-template.yml workorder-[feature]-[component].yml`
2. Fill in all sections with detailed specifications
3. Review: Is it complete enough for Haiku to execute independently?
4. Commit to repo

### Executing a Workorder
1. Load workorder YAML into AI context (Haiku recommended for cost efficiency)
2. AI reads specification and implements code
3. AI writes unit tests (if separate workorder) or includes tests (if same workorder)
4. AI runs validation commands
5. Human reviews output and tests
6. If accepted, merge into codebase

### Tracking Progress
Update `metadata.status` in YAML file:
- `pending` - Not started
- `in_progress` - AI is working on it
- `completed` - Code written, tested, and merged
- `blocked` - Waiting on dependency or clarification

## Current Workorders

### ✅ Completed
None yet

### 🔄 In Progress
None yet

### 📋 Pending
1. **workorder-reactions-domain.yml** - Build reaction domain models (pure Python)
2. **workorder-reactions-tests.yml** - Build comprehensive unit tests for reactions

### 🔮 Future Workorders
- `workorder-policy-implementation.yml` - Implement DefaultPolicy class
- `workorder-repository-django.yml` - Django ORM repository adapter
- `workorder-broadcaster-channels.yml` - Django Channels broadcaster
- `workorder-directory-cache.yml` - Redis/cache-based participant directory
- `workorder-django-models.yml` - Django models for persisting reactions
- `workorder-websocket-consumer.yml` - Channels consumer for real-time reactions
- `workorder-http-views.yml` - REST API views for reactions
- `workorder-frontend-reaction-buttons.yml` - Vue components for reaction UI

## Best Practices

### For Workorder Writers (Humans)
- ✅ **Be specific** - Don't assume AI knows context
- ✅ **Include examples** - Show expected output/structure
- ✅ **Define interfaces first** - Before implementations
- ✅ **Test requirements** - Always include test specifications
- ✅ **Pure before integrated** - Domain logic before framework integration
- ✅ **Dependencies explicit** - List allowed/forbidden imports

### For Workorder Executors (AI)
- ✅ **Read entire workorder** - Don't skip sections
- ✅ **Follow specifications exactly** - Don't "improve" unless asked
- ✅ **Run validations** - Execute all validation commands
- ✅ **Ask if unclear** - Don't guess at requirements
- ✅ **Keep it pure** - Especially for domain models (no framework deps)

## Example Usage

### Assigning to Haiku
```
User: "Please execute workorder-reactions-domain.yml"
Haiku: [Reads YAML, implements reactions.py with all 12 reaction classes]
Haiku: [Runs validation: python -m py_compile reactions.py]
Haiku: "Completed. All 12 reaction types implemented and validated."
```

### Chaining Workorders
```
workorder-reactions-domain.yml (no dependencies)
    ↓
workorder-reactions-tests.yml (depends on reactions-domain)
    ↓
workorder-django-models.yml (depends on reactions-domain)
    ↓
workorder-websocket-consumer.yml (depends on reactions-domain, django-models)
```

## Integration with InquiryCircle

### Phase 1: Domain Layer (Current)
Build pure Python domain models and test them in isolation.
- **Workorders**: reactions-domain, reactions-tests
- **Output**: `/backend/interactions/domain/reactions.py`
- **Tests**: `/backend/interactions/tests/test_reactions.py`

### Phase 2: Infrastructure Layer (Next)
Build Django/Channels adapters that implement domain interfaces.
- **Workorders**: repository-django, broadcaster-channels, directory-cache
- **Output**: `/backend/interactions/infrastructure/*.py`

### Phase 3: Application Layer
Build Django views, consumers, and URL routing.
- **Workorders**: django-models, websocket-consumer, http-views
- **Output**: `/backend/interactions/models.py`, `consumers.py`, `views.py`

### Phase 4: Presentation Layer
Build Vue components that connect to WebSocket APIs.
- **Workorders**: frontend-reaction-buttons
- **Output**: `/frontend/src/components/reactions/*.vue`

## Version Control
- ✅ **Commit workorders** to Git (they're part of project documentation)
- ✅ **Update status** in YAML as work progresses
- ✅ **Reference in commits** - e.g., "Implements workorder-reactions-domain.yml"

## Related Documentation
- [Project Spec](/mnt/c/Users/scott/Documents/AIProjects/Markdown/docs-websystems/projects/inquirycircle/Documentation/project-spec.md)
- [Operations Guide](/mnt/c/Users/scott/Documents/AIProjects/Markdown/docs-websystems/projects/inquirycircle/Documentation/operations-guide.md)
- [Jitsi API Discussion](https://github.com/scott009/docs-websystems/tree/main/discussion/2025-09-22-jitsi-api-python)

---

**Last Updated**: 2025-10-04
**Maintainer**: scott009
