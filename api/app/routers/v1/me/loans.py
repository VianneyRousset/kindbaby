from typing import Annotated, Optional

from fastapi import Query, Request, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import services
from app.database import get_db_session
from app.schemas.loan.query import LoanQueryFilter
from app.schemas.loan.read import LoanRead
from app.schemas.query import QueryPageOptions

from .me import router


@router.get("/loans", status_code=status.HTTP_200_OK)
def list_client_loans(
    request: Request,
    page_options: Annotated[QueryPageOptions, Query()],
    active: Annotated[
        Optional[bool],
        Query(
            title="Select only active loans",
        ),
    ] = True,
    db: Session = Depends(get_db_session),
) -> list[LoanRead]:
    """List loans where the client is the owner."""

    client_user_id = services.auth.check_auth(request)

    result = services.loan.list_loans(
        db=db,
        query_filter=LoanQueryFilter(
            owner_id=client_user_id,
            active=active,
        ),
        page_options=page_options,
    )

    # TODO add pagination info in headers
    return result.data
