# Interactions App

## Purpose
Handles all user interactions during InquiryCircle meetings, including reactions, polls, Q&A, and other real-time engagement features.

## Architecture

This app follows **Clean Architecture** principles with clear separation between domain logic and infrastructure:

```
interactions/
├── domain/              # Pure Python business logic (no Django dependencies)
│   ├── __init__.py
│   └── reactions.py     # Reaction domain models, services, interfaces
│
├── infrastructure/      # Django/Channels adapters (implements domain interfaces)
│   ├── __init__.py
│   ├── repository.py    # Django ORM implementation of Repository interface
│   ├── broadcaster.py   # Django Channels implementation of Broadcaster interface
│   └── cache.py         # Cache-based implementation of JitsiDirectory interface
│
├── policies/            # Business rules and policy enforcement
│   ├── __init__.py
│   └── reaction_policy.py  # DefaultPolicy implementation
│
├── tests/               # Unit and integration tests
│   ├── __init__.py
│   └── test_reactions.py   # Pure unit tests for domain logic
│
├── models.py            # Django models for persistence (Phase 2)
├── admin.py             # Django admin configuration (Phase 2)
├── apps.py              # Django app configuration
└── README.md            # This file
```

## Development Phases

### Phase 1: Domain Layer (Current) ✅
**Goal:** Build and test pure Python domain logic independently

**Files to create:**
- `domain/reactions.py` - All reaction domain models
- `tests/test_reactions.py` - Comprehensive unit tests

**No Django dependencies** - Can be tested without database, channels, or web framework

**Workorders:**
- `workorder-reactions-domain.yml`
- `workorder-reactions-tests.yml`

**Validation:**
```bash
pytest backend/interactions/tests/test_reactions.py -v --cov
```

---

### Phase 2: Infrastructure Layer (Future) 📋
**Goal:** Connect domain logic to Django/Channels infrastructure

**Files to create:**
- `infrastructure/repository.py` - Save reactions to database
- `infrastructure/broadcaster.py` - Send reactions via WebSocket
- `infrastructure/cache.py` - Track participants in Redis/cache
- `models.py` - Django models for Reaction persistence
- `policies/reaction_policy.py` - Concrete policy implementation

**Workorders:**
- `workorder-django-models.yml`
- `workorder-repository-django.yml`
- `workorder-broadcaster-channels.yml`
- `workorder-directory-cache.yml`
- `workorder-policy-implementation.yml`

---

### Phase 3: Application Layer (Future) 📋
**Goal:** Expose reactions via HTTP and WebSocket APIs

**Files to create:**
- `consumers.py` - WebSocket consumer for real-time reactions
- `views.py` - HTTP API endpoints (optional fallback)
- `urls.py` - URL routing

**Workorders:**
- `workorder-websocket-consumer.yml`
- `workorder-http-views.yml`

---

### Phase 4: Frontend Integration (Future) 📋
**Goal:** Connect Vue components to backend APIs

**Frontend files already exist:**
- `frontend/src/components/reactions/ReactionBar1.vue`
- `frontend/src/components/reactions/ReactionBar2.vue`
- `frontend/public/data/element-descriptions.json`

**Workorder:**
- `workorder-frontend-reaction-integration.yml`

---

## Current Status

**Phase 1 Status:** Directory structure created, ready for workorder execution

**Next Steps:**
1. Execute `workorder-reactions-domain.yml` to build `domain/reactions.py`
2. Execute `workorder-reactions-tests.yml` to build `tests/test_reactions.py`
3. Run tests to validate domain logic
4. Commit domain layer to git

**Blocked:** Phase 2+ (waiting for domain layer completion)

---

## Design Principles

### 1. Clean Architecture
- **Domain layer** is pure Python with no external dependencies
- **Infrastructure layer** adapts domain interfaces to Django/Channels
- **Application layer** orchestrates use cases
- **Presentation layer** (Vue) consumes APIs

### 2. Interface-Driven
Domain defines interfaces (Protocols):
- `Repository` - Persistence abstraction
- `Broadcaster` - Event distribution abstraction
- `JitsiDirectory` - Participant lookup abstraction
- `Policy` - Business rules abstraction

Infrastructure provides concrete implementations.

### 3. Testable
- Domain logic tested with fakes (no real DB/cache/channels)
- Infrastructure tested with real services (integration tests)
- UI tested independently (component tests)

### 4. Extensible
`interactions` app name chosen to support future features:
- ✅ Reactions (Phase 1)
- 📋 Polls (Future)
- 📋 Q&A (Future)
- 📋 Hand-raising (Future)
- 📋 Annotations (Future)

---

## Related Documentation

- **Workorders:** `/home/scott/inquirycircle/workorders/`
- **Project Spec:** `/mnt/c/Users/scott/Documents/AIProjects/Markdown/docs-websystems/projects/inquirycircle/Documentation/project-spec.md`
- **GitHub Discussion:** [2025-09-22-jitsi-api-python](https://github.com/scott009/docs-websystems/tree/main/discussion/2025-09-22-jitsi-api-python)

---

**Created:** 2025-10-04
**Last Updated:** 2025-10-04
**Maintainer:** scott009
