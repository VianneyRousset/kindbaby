from typing import Optional

from sqlalchemy.orm import Session

from app.clients import database
from app.enums import LoanRequestState
from app.errors.loan import LoanRequestStateError
from app.schemas.chat.base import ChatId
from app.schemas.loan.query import LoanRequestQueryFilter
from app.schemas.loan.read import LoanRead, LoanRequestRead
from app.services.chat import (
    send_message_loan_request_created,
    send_message_loan_started,
)


def create_loan_request(
    db: Session,
    *,
    item_id: int,
    borrower_id: int,
) -> LoanRequestRead:
    """Create a loan request."""

    # create messages
    message = send_message_loan_request_created(
        db=db,
        chat_id=ChatId(
            item_id=item_id,
            borrower_id=borrower_id,
        ),
    )

    loan_request = database.loan.create_loan_request(
        db=db,
        borrower_id=borrower_id,
        item_id=item_id,
        creation_message_id=message.id,
    )

    return LoanRequestRead.from_orm(loan_request)


def execute_loan_request(
    db: Session,
    *,
    loan_request_id: int,
    query_filter: Optional[LoanRequestQueryFilter] = None,
    force: Optional[bool] = False,
) -> LoanRead:
    """Create a loan from an accepted loan request.

    Loan request state must be `pending` if `force` is `False`.

    The loan request state is changed to `executed`.

    If `borrower_id` is given, the loan request must have this user as
    borrower.
    """

    # get loan request from database
    loan_request = database.loan.get_loan_request(
        db=db,
        loan_request_id=loan_request_id,
        query_filter=query_filter,
    )

    # create messages
    message = send_message_loan_started(
        db=db,
        chat_id=ChatId(
            item_id=loan_request.item_id,
            borrower_id=loan_request.borrower_id,
        ),
    )

    # check loan request state
    if not force and loan_request.state != LoanRequestState.accepted:
        raise LoanRequestStateError(
            expected_state=LoanRequestState.accepted,
            actual_state=loan_request.state,
        )

    # create loan from loan request
    loan = database.loan.create_loan(
        db=db,
        item_id=loan_request.item_id,
        borrower_id=loan_request.borrower_id,
        creation_message_id=message.id,
    )

    database.loan.update_loan_request(
        db=db,
        loan_request=loan_request,
        attributes={
            "state": LoanRequestState.executed,
            "loan": loan,
        },
    )

    return LoanRead.from_orm(loan)
