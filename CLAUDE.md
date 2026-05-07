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
