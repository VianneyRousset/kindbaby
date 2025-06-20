from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.errors.user import UserNotFoundError
from app.models.user import User
from app.schemas.user.query import UserQueryFilter


def get_user(
    db: Session,
    user_id: int,
) -> User:
    """Get user with `user_id` from database."""

    stmt = select(User).where(User.id == user_id)

    try:
        return db.execute(stmt).unique().scalars().one()

    except NoResultFound as error:
        raise UserNotFoundError({"id": user_id}) from error


def get_user_by_email(db: Session, email: str) -> User:
    """Get user with `email` from database."""

    stmt = select(User).where(User.email == email)

    try:
        return db.execute(stmt).unique().scalars().one()

    except NoResultFound as error:
        raise UserNotFoundError({"email": email}) from error


def get_user_by_validation_code(
    db: Session,
    validation_code: UUID,
) -> User:
    """Get user with `validation_code` from database."""

    stmt = select(User).where(User.validation_code == validation_code)

    try:
        return db.execute(stmt).unique().scalars().one()

    except NoResultFound as error:
        raise UserNotFoundError({"validation_code": validation_code}) from error


def list_users(
    db: Session,
) -> list[User]:
    """List users from database."""

    stmt = select(User)
    return list(db.scalars(stmt).all())


def get_user_exists(
    db: Session,
    query_filter: UserQueryFilter,
) -> bool:
    """Returns True if a user matching the `query_filter` exists."""

    stmt = query_filter.apply(select(User)).exists()
    return db.execute(select(stmt)).scalar_one()
