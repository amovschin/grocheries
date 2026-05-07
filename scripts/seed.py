"""Seed the database with a test grocery list."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.database import Base, SessionLocal, engine  # noqa: E402
from app.models import List  # noqa: E402

LIST_ID = "test-liste-123"
LIST_NAME = "Courses de la semaine"


def seed() -> None:
    """Create tables and insert the test list if it does not exist."""
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = db.get(List, LIST_ID)
        if existing is None:
            db.add(List(id=LIST_ID, name=LIST_NAME))
            db.commit()
            print(f"Created list '{LIST_NAME}' with id '{LIST_ID}'.")
        else:
            print(f"List '{LIST_ID}' already exists, skipping.")
    finally:
        db.close()

    print(f"Access it at: http://localhost:8000/list/{LIST_ID}")


if __name__ == "__main__":
    seed()
