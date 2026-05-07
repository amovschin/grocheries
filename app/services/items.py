"""Business logic for list and item creation, toggling, and deletion."""

import uuid

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.models import Item, List


def create_list(name: str, db: Session) -> List:
    """Create and persist a new List with a generated UUID."""
    grocery_list = List(id=str(uuid.uuid4()), name=name)
    db.add(grocery_list)
    db.commit()
    db.refresh(grocery_list)
    return grocery_list


def get_list_or_404(list_id: str, db: Session) -> List:
    """Return a List by id, or raise HTTP 404 if not found."""
    grocery_list = db.get(List, list_id)
    if grocery_list is None:
        raise HTTPException(status_code=404, detail="List not found")
    return grocery_list


def create_item(
    list_id: str,
    name: str,
    location: str | None,
    quantity: int | None,
    comment: str | None,
    added_by: str | None,
    priority: int | None,
    db: Session,
) -> Item:
    """Create and persist a new Item on the given list."""
    get_list_or_404(list_id, db)
    item = Item(
        list_id=list_id,
        name=name,
        location=location or None,
        quantity=quantity,
        comment=comment or None,
        added_by=added_by or None,
        priority=priority,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def delete_list(list_id: str, db: Session) -> None:
    """Permanently delete a list and all its items from the database."""
    grocery_list = get_list_or_404(list_id, db)
    db.delete(grocery_list)
    db.commit()


def rename_list(list_id: str, new_name: str, db: Session) -> List:
    """Update the name of an existing list and persist the change."""
    grocery_list = get_list_or_404(list_id, db)
    grocery_list.name = new_name
    db.commit()
    db.refresh(grocery_list)
    return grocery_list


def toggle_item(item_id: int, list_id: str, db: Session) -> Item:
    """Flip the checked state of an item and persist the change."""
    item = db.get(Item, item_id)
    if item is None or item.list_id != list_id:
        raise HTTPException(status_code=404, detail="Item not found")
    item.checked = not item.checked
    db.commit()
    db.refresh(item)
    return item


def delete_item(item_id: int, list_id: str, db: Session) -> None:
    """Permanently delete an item from the database."""
    item = db.get(Item, item_id)
    if item is None or item.list_id != list_id:
        raise HTTPException(status_code=404, detail="Item not found")
    db.delete(item)
    db.commit()
