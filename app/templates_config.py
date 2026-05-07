"""Shared Jinja2Templates instance, instantiated once at app startup."""

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="app/templates")
