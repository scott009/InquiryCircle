<!-- Document Version: 1.5 -->
<!-- Last Updated: 2025-08-02 -->

# InquiryCircle v1.1.0 - Blackboard

*Document: `InquiryCircle1.1.Blackboard.md`*

## What's New in v1.1.0

### CircleMessage1 Feature
- **Purpose**: Allow circle facilitators to set an HTML message displayed to all visitors of a circle
- **Key Features**:
  - Facilitators can enter and approve messages via the control panel
  - Messages are displayed to all circle visitors in a clean, readable house style
  - Uses VueJS and Tailwind CSS for consistent UI
  - Messages are persisted in storage and displayed outside the debug window

### UI Improvements
- Jitsi video frame resized to 75% of original height
- Participant message box moved below Jitsi window for better layout
- Removed "Message from Circle Facilitator" header for cleaner display

## System Overview
- **Type**: Web-based video conferencing platform
- **Purpose**: Facilitate inquiry groups with role-based access control
- **Core Concept**: "Circles" as dedicated web pages with embedded Jitsi video conferencing

## Technical Stack
- **Frontend**: Vue.js v3 + Tailwind CSS
- **Backend**: Django (Python)
- **Video Solution**: Jitsi Meet (iframe embed)
- **Web Server**: Caddy
- **Process Manager**: Gunicorn + systemd
- **Hosting**: VPS (Ubuntu 22.04)
- **Authentication**: Key-based (no traditional user accounts)

## Core Components

### 1. Circle Management
- **Purpose**: Create and manage video conference rooms
- **Key Features**:
  - Role-based access control (Facilitator/Participant)
  - Jitsi Meet integration
  - Key-based authentication
  - Facilitator message system (new in v1.1.0)

### 2. Role System
- **Facilitators**:
  - Elevated privileges
  - Meeting controls
  - Participant management
  - Message management (new in v1.1.0)
- **Participants**:
  - Standard access
  - Basic meeting functions
  - View facilitator messages (new in v1.1.0)

### 3. Technical Architecture
```
InquiryCircle/
├── backend/          # Django application
│   ├── inquirycircle/  # Main project settings
│   └── circles/       # Circles app (models, views, storage)
├── frontend/         # Vue.js application
│   ├── src/          # Source files
│   └── public/       # Static assets
├── config/           # Server configurations
│   ├── caddy/        # Caddy web server configs
│   └── gunicorn/     # Gunicorn service files
├── deployment/       # Deployment scripts
└── docs/            # Documentation
```

## Key Configuration Files

### Backend Configuration
- `backend/.env` - Environment variables (copy from `.env.example`)
  ```
  DEBUG=True
  SECRET_KEY=your-secret-key
  JITSI_APP_ID=your-jitsi-app-id
  ```

### Frontend Configuration
- `frontend/.env` - Frontend environment variables
  ```
  VUE_APP_API_URL=http://localhost:8000
  VUE_APP_JITSI_DOMAIN=meet.jit.si
  ```

### Circle Message Feature (New in v1.1.0)
- Messages are stored in `backend/data/circles.json`
- Facilitators can update messages via the control panel
- Messages are sanitized for security before display

## Setup Instructions

### Backend (Django)
1. Environment setup:
   ```bash
   cd backend
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Unix/Mac: source venv/bin/activate
   pip install -r requirements.txt
   cp .env.example .env
   ```

2. Run development server:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### Frontend (Vue.js)
```bash
cd frontend
npm install
npm run dev
```

## Data Model

### Circle
- `id`: Unique identifier
- `name`: Display name
- `jitsi_room`: Jitsi room name
- `facilitator_key`: Secret key for facilitators
- `participant_key`: Secret key for participants
- `message`: HTML message from facilitator (new in v1.1.0)

### Session
- `circle`: ForeignKey to Circle
- `start_time`: Session start timestamp
- `end_time`: Session end timestamp
- `active`: Boolean status

## API Endpoints

### Circle Management
- `GET /api/circles/`: List all circles
- `POST /api/circles/`: Create new circle
- `GET /api/circles/<id>/`: Get circle details
- `POST /api/circles/<id>/join/`: Join a circle

### Facilitator API (New in v1.1.0)
- `POST /facilitator-api/`: Update circle message
  - Requires `circle_id` and `message` parameters
  - Requires valid facilitator key in session

## Security Considerations
- All keys should be securely hashed
- Use HTTPS in production
- Regular security audits recommended
- Messages are sanitized before storage/display

## Demo Credentials
- Admin: `admin-master-key`
- Facilitator: `facilitator-demo` (for demo-circle)
- Participant: `participant-demo` (for demo-circle)

## File Structure
```
InquiryCircle/
│
├── backend/                          # Django backend
│   ├── inquirycircle/                # Main project package
│   │   ├── __init__.py
│   │   ├── settings.py              # Main settings file
│   │   ├── urls.py                  # Root URL configuration
│   │   └── wsgi.py                  # WSGI config
│   │
│   ├── circles/                      # Circles app
│   │   ├── __init__.py
│   │   ├── admin.py                 # Admin interface config
│   │   ├── apps.py                  # App config
│   │   ├── models.py                # Data models
│   │   ├── storage.py               # Data storage implementation
│   │   ├── urls.py                  # App URL routing
│   │   └── views.py                 # Request handlers
│   │
│   ├── manage.py                    # Django management script
│   ├── requirements.txt             # Python dependencies
│   └── .env                         # Environment variables (gitignored)
│
├── frontend/                        # Vue.js frontend
│   ├── public/                      # Static files
│   │   ├── index.html               # Main HTML file
│   │   └── favicon.ico
│   │
│   ├── src/                         # Source files
│   │   ├── assets/                  # Static assets
│   │   ├── components/              # Vue components
│   │   ├── router/                  # Vue Router config
│   │   ├── views/                   # Page components
│   │   ├── App.vue                  # Root Vue component
│   │   └── main.js                  # Entry point
│   │
│   ├── package.json                 # NPM dependencies
│   └── vue.config.js                # Vue CLI config
│
├── config/                          # Server configurations
│   ├── caddy/                       # Caddy web server configs
│   └── gunicorn/                    # Gunicorn service files
│
├── deployment/                      # Deployment scripts
├── docs/                            # Documentation files
├── docfig/                          # Docfig documentation
│   ├── InquiryCircle1.0.Blackboard.md  # v1.0 Blackboard
│   ├── InquiryCircle1.1.Blackboard.md  # v1.1 Blackboard (this document)
│   └── readme1.1.md                 # v1.1 Human-readable docs
├── .gitignore                       # Git ignore rules
├── README.md                        # Main project documentation
└── readme1.1.md                     # Human-readable documentation
```

## Version Information
- **Version**: 1.1.0
- **Last Updated**: 2025-08-02
- **Compatibility**: Python 3.8+, Node.js 14+

## Cross-System Suggestions and Actions

This section facilitates communication between different AI systems (e.g., ChatGPT, Windsurf/Claude, etc.), enabling structured coordination of suggestions, actions, and implementation tracking across tools.

Each block has a unique ID and follows the naming convention:  
**`[Platform]/[Model] [Action Type]`** — e.g., `ChatGPT/ChatGPT4.0 Suggests`, `Windsurf/Claude4-Sonnet Did`

### 📄 Block Format

```markdown
<!-- [Platform/Model] [Action Type] -->
<!-- ID: [prefix]-[number] -->
<!-- Related To: [reference or topic] -->
<!-- Status: [Pending/In Progress/Completed/Rejected] -->
<!-- Priority: [High/Medium/Low] -->
<!-- Date: YYYY-MM-DD -->

[Description of suggestion, action, or response]
```

### 📌 Guidelines

1. **User Approval Required** – No actions may be implemented without explicit user confirmation.
2. **Capability Awareness** – Naming must reflect actual agent capabilities, not just platform or branding.
3. **Status Tracking** – Use `Status` field to follow implementation state.
4. **Priority Management** – Helps triage urgent vs. non-urgent coordination.
5. **Traceability** – Use `Related To` to maintain linked discussions across models and versions.
6. **Implementation Authority** – ChatGPT suggests and analyzes; Windsurf executes code changes (unless reconfigured).

### ✅ Example Blocks

```markdown
<!-- ChatGPT/ChatGPT4.0 Suggests -->
<!-- ID: cg-001 -->
<!-- Related To: CircleMessage1 Feature -->
<!-- Status: Pending -->
<!-- Priority: High -->
<!-- Date: 2025-08-02 -->

ChatGPT suggests creating a glossary section for new terms introduced in v1.1.0, particularly "CircleMessage1" and related concepts like "facilitator message" and "message persistence".
```

```markdown
<!-- Windsurf/Claude4-Sonnet Did -->
<!-- ID: wd-001 -->
<!-- Related To: CircleMessage1 Feature -->
<!-- Status: Completed -->
<!-- Priority: High -->
<!-- Date: 2025-08-02 -->

Windsurf/Claude4-Sonnet implemented the CircleMessage1 feature including backend persistence, frontend UI, and API endpoints. All functionality has been tested and verified.
```

```markdown
<!-- Windsurf/Claude4-Sonnet Suggests -->
<!-- ID: ws-001 -->
<!-- Related To: GitHub Integration -->
<!-- Status: User Considering -->
<!-- Priority: High -->
<!-- Date: 2025-08-02 -->

Windsurf/Claude4-Sonnet suggests implementing GitHub as the next major development step for the InquiryCircle project. Benefits include: controlled access via private repository (free GitHub accounts now support unlimited private repos), expedited feature development, proper version control, and enabling the cross-system AI communication framework. User expressed interest in GitHub implementation to control access while security features are still being developed.
```

```markdown
<!-- ChatGPT/ChatGPT4.0 Suggests -->
<!-- ID: cg-002 -->
<!-- Related To: Documentation -->
<!-- Status: Pending -->
<!-- Priority: Medium -->
<!-- Date: 2025-08-02 -->

ChatGPT suggests creating a migration guide for users upgrading from v1.0 to v1.1.0, particularly focusing on the new message field in circles.json and the updated circle.html template.
```

```markdown
<!-- Windsurf/Claude4-Sonnet Did -->
<!-- ID: wd-002 -->
<!-- Related To: Documentation -->
<!-- Status: Completed -->
<!-- Priority: Medium -->
<!-- Date: 2025-08-02 -->

Windsurf/Claude4-Sonnet created comprehensive documentation for v1.1.0 including this Blackboard file, human-readable documentation, and updated README. All new features are fully documented.
```
