# SPEC.md — Grocheries

## Overview

Web application allowing a small group of users to share and edit a grocery
list in real time, accessible via a secret link from a smartphone.

---

## Tech stack

- **Backend**: Python 3.12, FastAPI
- **Real-time**: WebSockets (native FastAPI)
- **Database**: SQLite via SQLAlchemy (ORM)
- **Frontend**: HTML5, CSS (mobile-first), HTMX
- **Containerization**: Docker

---

## Data model

### List (`list`)
| Field | Type | Description |
|---|---|---|
| id | string (UUID) | Unique identifier — serves as the "secret link" |
| name | string | List name |
| created_at | datetime | Creation timestamp |

### Item (`item`)
| Field | Type | Constraint |
|---|---|---|
| id | integer | Primary key, auto-incremented |
| list_id | string (UUID) | Foreign key → list.id |
| name | string | Required |
| location | string | Optional — where to buy it |
| quantity | integer | Optional |
| comment | string | Optional |
| added_by | string | Optional — who added the item |
| priority | integer | Optional — 1 (high), 2 (medium), 3 (low) |
| checked | boolean | Default: false |
| created_at | datetime | Creation timestamp |

---

## Features

### Access
- URL `/list/{uuid}` gives access to the list
- No authentication — anyone with the UUID can access
- UUID is created manually (no sign-up flow)

### User actions
1. **Add an item**: form with name (required), location, quantity,
   comment, added_by, priority
2. **Check an item**: toggle checked/unchecked
3. **Delete an item**: permanent deletion with confirmation

### Filtering
Users can filter the item list by:
- **location** — dropdown of distinct locations present in the list
- **priority** — dropdown: all / high / medium / low
- **added_by** — dropdown of distinct names present in the list

Filters are combinable. Filtering is client-side (HTMX or plain JS),
no server round-trip needed.

### Real-time
- WebSocket connection to `/ws/{list_id}` on page load
- Every mutation (add, toggle, delete) is broadcast to all clients
  connected to the same list
- WebSocket message: `{ "action": "reload" }` → client reloads the list

---

## REST API

| Method | Endpoint | Description |
|---|---|---|
| GET | `/list/{list_id}` | HTML page for the list |
| POST | `/list/{list_id}/items` | Add an item |
| PATCH | `/list/{list_id}/items/{item_id}/toggle` | Toggle checked |
| DELETE | `/list/{list_id}/items/{item_id}` | Delete an item |
| WS | `/ws/{list_id}` | WebSocket connection |

---

## Technical constraints

- **Mobile-first**: UI must be usable on smartphones (touch-friendly, readable)
- **No frontend build step**: no Node.js, no bundler —
  everything is served statically or via Jinja2 templates
- **Single process**: FastAPI serves both the API and static files
- **Persistence**: SQLite file stored in a Docker-mounted volume at `/data/`

---

## Expected file structure
grocheries/
├── app/
│   ├── main.py           # FastAPI entry point
│   ├── models.py         # SQLAlchemy models
│   ├── database.py       # SQLite connection
│   ├── routers/
│   │   ├── lists.py      # HTTP routes
│   │   └── ws.py         # WebSocket handler
│   ├── templates/
│   │   └── list.html     # Jinja2 template
│   └── static/
│       └── style.css     # Mobile-first CSS
├── data/                 # Mounted Docker volume (SQLite file lives here)
├── Dockerfile
├── docker-compose.yml
└── SPEC.md

---

## Out of scope (for now)

- List creation via the UI (UUID is created manually)
- Edit history / audit log
- Push notifications
- User authentication

---

## Architecture decisions

### Designed for extensibility

The current version is intentionally minimal, but the codebase must remain
easy to extend. The following decisions reflect that constraint.

#### Dependency injection for database sessions
Use FastAPI's `Depends()` for database sessions in every route. This makes
it straightforward to swap SQLite for PostgreSQL later without rewriting
route logic.

#### Router-based structure
Each feature domain lives in its own router file (`routers/lists.py`,
`routers/ws.py`). Adding authentication, admin routes, or a new resource
means adding a new file — not modifying existing ones.

#### No business logic in route handlers
Route handlers only handle HTTP concerns (parse input, return response).
All business logic (create item, toggle item, broadcast event) lives in
dedicated service functions. This makes logic reusable and testable
independently of the web layer.

#### Auth-ready middleware slot
The app is structured so that an authentication middleware can be added
in `main.py` without touching any route. The secret-link access pattern
is implemented as a simple dependency (`get_list_or_404`), which can later
be replaced or wrapped with a proper auth check.

#### UUID as list identifier
Using a UUID (rather than an integer ID) as the list identifier means the
"secret link" pattern and a future authenticated access pattern can coexist:
the UUID remains the canonical identifier regardless of how access is
controlled.

#### Environment-based configuration
All environment-specific values (database path, app secret, allowed origins)
are read from environment variables via a `Settings` class (Pydantic
BaseSettings). No hardcoded values in the codebase.

#### Static files and templates are separate from logic
`static/` and `templates/` are cleanly separated from application logic.
If the frontend is later replaced by a React app or a mobile client,
the API layer requires no changes.



