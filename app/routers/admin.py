"""Admin route handlers for privileged operations."""

import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import List

router = APIRouter()


@router.post("/admin/lists")
def create_list(
    token: str,
    name: str,
    list_id: str = "",
    db: Session = Depends(get_db),
) -> dict:
    """Create a new grocery list, generating a UUID if list_id is not provided."""
    if token != settings.admin_token:
        raise HTTPException(status_code=403, detail="Forbidden")
    resolved_id = list_id.strip() or str(uuid.uuid4())
    grocery_list = List(id=resolved_id, name=name)
    db.add(grocery_list)
    db.commit()
    return {"id": resolved_id, "name": name, "url": f"/list/{resolved_id}"}
