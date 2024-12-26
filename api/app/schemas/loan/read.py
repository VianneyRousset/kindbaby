from datetime import datetime
from typing import Optional

from app import models
from app.enums import LoanRequestState
from app.schemas.base import ReadBase
from app.schemas.item.preview import ItemPreviewRead
from app.schemas.user.preview import UserPreviewRead

from .base import LoanBase, LoanRequestBase


class LoanRequestRead(LoanRequestBase, ReadBase):
    id: int
    item: ItemPreviewRead
    borrower: UserPreviewRead
    state: LoanRequestState

    @classmethod
    def from_orm(cls, loan_request: models.loan.LoanRequest):
        return cls(
            id=loan_request.id,
            item=ItemPreviewRead.from_orm(loan_request.item),
            borrower=UserPreviewRead.from_orm(loan_request.borrower),
            state=loan_request.state,
        )


class LoanRead(LoanBase, ReadBase):
    id: int
    item: ItemPreviewRead
    borrower: UserPreviewRead
    during: list[datetime | None]
    active: bool

    @classmethod
    def from_orm(cls, loan: models.loan.Loan):
        return cls(
            id=loan.id,
            item=ItemPreviewRead.from_orm(loan.item),
            borrower=UserPreviewRead.from_orm(loan.borrower),
            during=[loan.during.lower, loan.during.upper],
            active=loan.during.upper is None,
        )