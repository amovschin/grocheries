# CLAUDE.md

## Project
This is the `grocheries` project. Always read SPEC.md before making
any change.

## Rules
- Never install dependencies not listed in SPEC.md without asking first
- Never modify the data model without explicit instruction
- Always write docstrings on service functions
- Never put business logic in route handlers — use service functions
- All config values must go through the Settings class, never hardcoded

## Code style
- Python: follow PEP8, use type hints everywhere
- Maximum function length: 30 lines — split if longer
- Use explicit variable names, no abbreviations

## Workflow
- After each task, summarize what was created and what to do next
- If something in SPEC.md is ambiguous, ask before implementing
- Prefer simple solutions over clever ones



## Lessons learned

### Dependencies
- Always pin exact versions in requirements.txt — version mismatches
  between FastAPI, Starlette, and Jinja2 can cause subtle runtime 
  errors (e.g. "unhashable type: dict")
- Required versions: fastapi==0.115.12, starlette==0.46.2, 
  jinja2==3.1.6

### Python
- Never use a variable named "location" in JavaScript — it conflicts
  with the browser's global window.location object
- Always use datetime.now(timezone.utc) instead of datetime.utcnow()
  (deprecated in Python 3.12)
- SQLAlchemy String columns must have explicit lengths (e.g. 
  String(255)) for PostgreSQL compatibility

### FastAPI
- Never instantiate Jinja2Templates inside a router file — 
  instantiate once in a shared templates_config.py and import it
- Form fields send empty string "" for optional fields, not None —
  always convert manually: value = int(raw) if raw.strip() else None
- PATCH and DELETE via HTML forms are not reliable in browsers —
  use POST with a dedicated route (/resource/action) instead

### Frontend
- HTML hidden attribute is overridden by CSS display properties —
  always add .item[hidden] { display: none !important } when using
  JS filtering with the hidden attribute
- Use DOMContentLoaded event listeners instead of inline onchange
  attributes to ensure JS functions are in scope when DOM loads
- HTMX is reliable for simple GET/POST — for PATCH/DELETE prefer
  standard HTML forms with dedicated POST routes

### Docker
- Always COPY alembic/ and alembic.ini into the Docker image —
  Alembic needs these files at runtime, not just at build time
- Always RUN mkdir -p /data in the Dockerfile for the SQLite
  volume mount point

### Security
- Always use fine-grained GitHub tokens scoped to a single repo
- Never hardcode secrets — use environment variables via 
  pydantic Settings class
- Always pass token through template context when using it in 
  forms — easy to forget and causes silent 403 errors