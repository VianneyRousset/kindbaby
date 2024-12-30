from fastapi import Request, status
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import services
from app.database import get_db_session
from app.schemas.loan.read import LoanRequestRead

from .annotations import item_id_annotation
from .router import router


# CREATE


@router.post("/{item_id}/request", status_code=status.HTTP_201_CREATED)
def create_loan_request(
    request: Request,
    item_id: item_id_annotation,
    db: Session = Depends(get_db_session),
) -> LoanRequestRead:
    """Add a loan request of the item."""

    client_user_id = services.auth.check_auth(request)

    return services.loan.create_loan_request(
        db=db,
        item_id=item_id,
        borrower_id=client_user_id,
    )


# DELETE


@router.delete("/{item_id}/request", status_code=status.HTTP_200_OK)
def cancel_loan_request(
    request: Request,
    item_id: item_id_annotation,
    db: Session = Depends(get_db_session),
) -> LoanRequestRead:
    """Add a loan request of the item."""

    client_user_id = services.auth.check_auth(request)

    return services.loan.cancel_pending_loan_request(
        db=db,
        item_id=item_id,
        borrower_id=client_user_id,
    )
