"""HTTP route handlers for grocery list operations."""

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import List
from app.services.broadcast import manager
from app.services.items import (
    create_item,
    create_list,
    delete_item,
    delete_list,
    get_list_or_404,
    rename_list,
    toggle_item,
)
from app.templates_config import templates

router = APIRouter()

_RELOAD = {"action": "reload"}


@router.get("/")
async def index(request: Request, token: str = "", db: Session = Depends(get_db)):
    """Render the admin home page listing all grocery lists."""
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Forbidden")
    all_lists = db.query(List).order_by(desc(List.created_at)).all()
    base_url = str(request.base_url).rstrip("/")
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "lists": all_lists, "base_url": base_url, "token": token},
    )


@router.get("/new")
async def new_list_page(request: Request):
    """Render the new-list creation form."""
    return templates.TemplateResponse("new.html", {"request": request})


@router.delete("/lists/{list_id}")
async def delete_list_route(
    list_id: str,
    token: str = "",
    db: Session = Depends(get_db),
):
    """Delete a list and all its items, then redirect to the home page."""
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Forbidden")
    delete_list(list_id, db)
    return RedirectResponse(url=f"/?token={token}", status_code=303)


@router.patch("/lists/{list_id}")
async def rename_list_route(
    list_id: str,
    token: str = "",
    new_name: str = Form(...),
    db: Session = Depends(get_db),
):
    """Rename a list, then redirect to the home page."""
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Forbidden")
    rename_list(list_id, new_name, db)
    return RedirectResponse(url=f"/?token={token}", status_code=303)


@router.post("/lists/{list_id}/delete")
async def delete_list_post(
    list_id: str,
    token: str = "",
    db: Session = Depends(get_db),
):
    """Delete a list via browser form POST, then redirect to the home page."""
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Forbidden")
    delete_list(list_id, db)
    return RedirectResponse(url=f"/?token={token}", status_code=303)


@router.post("/lists/{list_id}/rename")
async def rename_list_post(
    list_id: str,
    token: str = "",
    new_name: str = Form(...),
    db: Session = Depends(get_db),
):
    """Rename a list via browser form POST, then redirect to the home page."""
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Forbidden")
    rename_list(list_id, new_name, db)
    return RedirectResponse(url=f"/?token={token}", status_code=303)


@router.post("/lists")
async def create_list_route(
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    """Create a new list and redirect to its page."""
    grocery_list = create_list(name, db)
    return RedirectResponse(url=f"/list/{grocery_list.id}", status_code=303)


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
    quantity_raw: str = Form(default="", alias="quantity"),
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
