"""HTTP route handlers for grocery list operations."""

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.database import get_db
from app.services.broadcast import manager
from app.services.items import (
    create_item,
    delete_item,
    get_list_or_404,
    toggle_item,
)
from app.templates_config import templates

router = APIRouter()

_RELOAD = {"action": "reload"}


@router.get("/list/{list_id}")
async def get_list(list_id: str, request: Request, db: Session = Depends(get_db)):
    """Render the grocery list page for the given list_id."""
    grocery_list = get_list_or_404(list_id, db)
    return templates.TemplateResponse(
        "list.html",
        {"request": request, "list": grocery_list, "items": grocery_list.items},
    )


@router.post("/list/{list_id}/items")
async def add_item(
    list_id: str,
    name: str = Form(...),
    location: str = Form(default=""),
    quantity_raw: str = Form(default=""),
    comment: str = Form(default=""),
    added_by: str = Form(default=""),
    priority_raw: str = Form(default=""),
    db: Session = Depends(get_db),
):
    """Create a new item on the list and broadcast a reload event."""
    quantity = int(quantity_raw) if quantity_raw.strip() else None
    priority = int(priority_raw) if priority_raw.strip() else None
    create_item(list_id, name, location, quantity, comment, added_by, priority, db)
    await manager.broadcast(list_id, _RELOAD)
    return RedirectResponse(url=f"/list/{list_id}", status_code=303)


@router.patch("/list/{list_id}/items/{item_id}/toggle")
async def toggle_item_route(
    list_id: str, item_id: int, db: Session = Depends(get_db)
):
    """Toggle an item's checked state and broadcast a reload event."""
    toggle_item(item_id, list_id, db)
    await manager.broadcast(list_id, _RELOAD)
    return RedirectResponse(url=f"/list/{list_id}", status_code=303)


@router.delete("/list/{list_id}/items/{item_id}")
async def delete_item_route(
    list_id: str, item_id: int, db: Session = Depends(get_db)
):
    """Delete an item from the list and broadcast a reload event."""
    delete_item(item_id, list_id, db)
    await manager.broadcast(list_id, _RELOAD)
    return RedirectResponse(url=f"/list/{list_id}", status_code=303)
