from typing import Annotated

from fastapi import APIRouter, Query, Request, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import services
from app.database import get_db_session
from app.schemas.user import UserRead

router = APIRouter()

user_id_annotation = Annotated[
    int,
    Query(
        title="The ID of the user.",
        ge=0,
    ),
]


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(
    request: Request,
    user_id: user_id_annotation,
    db: Session = Depends(get_db_session),
) -> UserRead:
    """Get user from id."""

    services.auth.check_auth(request)

    return await services.users.get_user_by_id(
        db=db,
        user_id=user_id,
    )


@router.post("/{user_id}/report", status_code=status.HTTP_201_CREATED)
async def report_user(
    request: Request,
    user_id: user_id_annotation,
    db: Session = Depends(get_db_session),
):
    """Report user with `user_id`."""

    client_user_id = services.auth.check_auth(request)

    return await services.users.report_user(
        db=db,
        user_id=user_id,
        client_user_id=client_user_id,
    )