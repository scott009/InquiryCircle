# InquiryCircle Work Order System

## Overview
This directory contains YAML work order specifications for AI-assisted development. Work orders provide detailed specifications that can be handed off to AI assistants (particularly Claude Haiku) for implementation.

## Directory Structure

```
work-orders/
├── backend/
│   ├── domain/          # Domain logic classes (reactions, etc.)
│   ├── api/             # REST API endpoints
│   └── database/        # Schema changes, migrations
├── frontend/
│   ├── components/      # Vue component implementations
│   ├── routes/          # Route and navigation tasks
│   └── styling/         # CSS/Tailwind styling tasks
├── infrastructure/
│   ├── docker/          # Container configuration tasks
│   ├── deployment/      # Deploy scripts and automation
│   └── networking/      # Caddy routing, networking
├── integration/
│   ├── api-integration/ # Frontend-backend connections
│   └── e2e-testing/     # End-to-end test scenarios
└── templates/           # Reusable work order templates
```

## Workflow

### 1. Create Work Order
- Copy appropriate template from `templates/`
- Customize with specific requirements
- Save to appropriate category directory

### 2. Development Phase
- Assign to AI assistant (typically Claude Haiku)
- AI implements in `sandbox/` directory
- AI creates unit tests and validates implementation

### 3. Testing Phase
- Run unit tests in sandbox environment
- Validate against work order acceptance criteria
- Document any issues or modifications needed

### 4. Integration Phase
- Move validated components to `integration/` directory
- Stage for integration into main project
- Final integration testing

### 5. Production Integration
- Merge tested components into main project folders
- Update documentation and deployment configs

## Work Order Format

Each work order YAML file should include:

- **Metadata**: ID, priority, estimated effort
- **Technical Specs**: Class/component specifications
- **Implementation Requirements**: Detailed requirements and constraints
- **Test Requirements**: Unit tests and acceptance criteria
- **Quality Standards**: Code quality and documentation requirements
- **Deliverables**: Expected output files and locations

## Example Usage

```bash
# Create a new reaction class work order
cp templates/reaction-template.yaml backend/domain/love-reaction.yaml

# Edit the work order with specific requirements
# Then assign to Claude Haiku for implementation

# After implementation, validate in sandbox
cd ../../sandbox/backend
python -m pytest tests/domain/reactions/test_love_reaction.py

# Move to integration staging when ready
mv domain/reactions/love_reaction.py ../../integration/backend/validated/
```

## Current Work Orders

### Backend Domain
- `like-reaction.yaml` - LikeReaction class implementation

### Templates
- `reaction-template.yaml` - Template for reaction class work orders

## Safety Notes

- Work orders operate in isolated `sandbox/` environment
- No changes to production code (`backend/`, `frontend/`, `caddy/`, `compose/`)
- All development isolated until explicit integration decision
- Full testing required before integration approval