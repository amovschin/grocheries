"""FastAPI entry point for the Grocheries application."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from alembic import command
from alembic.config import Config
from fastapi import FastAPI
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles

from app.routers import admin, lists, ws
from app.templates_config import templates as _templates  # noqa: F401

alembic_cfg = Config("alembic.ini")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Run Alembic migrations to head on startup."""
    command.upgrade(alembic_cfg, "head")
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(admin.router)
app.include_router(lists.router)
app.include_router(ws.router)


@app.get("/favicon.ico", include_in_schema=False)
async def favicon() -> Response:
    return Response(status_code=204)
