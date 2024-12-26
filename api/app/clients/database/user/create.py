from collections.abc import Collection
from typing import Any, Mapping, Optional

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.errors.exception import UserNotFoundError
from app.models.user import User

from app.clients.database import dbutils


def create_user(
    db: Session,
    *,
    email: str,
    name: str,
    password_hash: str,
    avatar_seed: Optional[str] = None,
) -> User:
    """Create and insert user into database."""

    user = User(
        email=email,
        name=name,
        password=password_hash,
        avatar_seed=avatar_seed,
    )

    return insert_user(
        db=db,
        user=user,
    )


def insert_user(
    db: Session,
    user: User,
) -> User:
    """Insert user into database."""

    db.add(user)
    db.flush()
    db.refresh(user)
    return user