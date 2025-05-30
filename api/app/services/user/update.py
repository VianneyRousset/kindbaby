from sqlalchemy.orm import Session

from app.clients import database
from app.schemas.user.private import UserPrivateRead
from app.schemas.user.update import UserUpdate


def update_user(
    db: Session,
    user_id: int,
    user_update: UserUpdate,
) -> UserPrivateRead:
    """Update user with `user_id`."""

    # get user from database
    user = database.user.get_user(
        db=db,
        user_id=user_id,
    )

    # update user in database
    user = database.user.update_user(
        db=db,
        user=user,
        attributes=user_update.model_dump(exclude_none=True),
    )

    return UserPrivateRead.model_validate(user)
