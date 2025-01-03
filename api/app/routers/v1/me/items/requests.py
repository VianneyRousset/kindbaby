from typing import Annotated

from fastapi import Query, Request, status, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app import services
from app.database import get_db_session
from app.schemas.loan.query import LoanRequestQueryFilter
from app.schemas.item.query import ItemQueryFilter
from app.schemas.loan.read import LoanRequestRead
from app.schemas.loan.api import LoanRequestApiQuery
from app.schemas.query import QueryPageOptions
from app.utils import set_query_param

from .annotations import item_id_annotation, loan_request_id_annotation
from .router import router


# READ


@router.get("/{item_id}/requests", status_code=status.HTTP_200_OK)
def list_client_item_loan_requests(
    request: Request,
    response: Response,
    item_id: item_id_annotation,
    query: Annotated[LoanRequestApiQuery, Query()],
    db: Session = Depends(get_db_session),
) -> list[LoanRequestRead]:
    """List loan requests of the item owned by the client."""

    client_user_id = services.auth.check_auth(request)

    # get item to check it is owned by the client
    item = services.item.get_item(
        db=db,
        item_id=item_id,
        query_filter=ItemQueryFilter(
            owner_id=client_user_id,
        ),
    )

    # get list of loan requests of the item
    result = services.loan.list_loan_requests(
        db=db,
        query_filter=LoanRequestQueryFilter(
            item_id=item.id,
            state=query.state,
        ),
        page_options=QueryPageOptions(
            limit=query.n,
            order=["loan_request_id"],
            cursor={"loan_request_id": query.cid},
            desc=True,
        ),
    )

    query_params = request.query_params
    for k, v in result.next_cursor().items():
        # rename query parameters
        k = {
            "loan_request_id": "cid",
        }[k]

        query_params = set_query_param(query_params, k, v)

    response.headers["Link"] = f'<{request.url.path}?{query_params}>; rel="next"'

    response.headers["X-Total-Count"] = str(result.total_count)

    return result.data


@router.get(
    "/{item_id}/requests/{loan_request_id}",
    status_code=status.HTTP_200_OK,
)
def get_client_item_loan_request(
    request: Request,
    item_id: item_id_annotation,
    loan_request_id: loan_request_id_annotation,
    db: Session = Depends(get_db_session),
) -> LoanRequestRead:
    """Get client's item loan request by id."""

    client_user_id = services.auth.check_auth(request)

    # get item to check it is owned by the client
    item = services.item.get_item(
        db=db,
        item_id=item_id,
        query_filter=ItemQueryFilter(
            owner_id=client_user_id,
        ),
    )

    return services.loan.get_loan_request(
        db=db,
        loan_request_id=loan_request_id,
        query_filter=LoanRequestQueryFilter(
            item_id=item.id,
        ),
    )


@router.post(
    "/{item_id}/requests/{loan_request_id}/accept",
    status_code=status.HTTP_200_OK,
)
def accept_client_item_loan_request(
    request: Request,
    item_id: item_id_annotation,
    loan_request_id: loan_request_id_annotation,
    db: Session = Depends(get_db_session),
) -> LoanRequestRead:
    """Accept client's item loan request."""

    client_user_id = services.auth.check_auth(request)

    return services.loan.accept_loan_request(
        db=db,
        loan_request_id=loan_request_id,
        query_filter=LoanRequestQueryFilter(
            item_id=item_id,
            owner_id=client_user_id,
        ),
    )


@router.post(
    "/{item_id}/requests/{loan_request_id}/reject",
    status_code=status.HTTP_200_OK,
)
def reject_client_item_loan_request(
    request: Request,
    item_id: item_id_annotation,
    loan_request_id: loan_request_id_annotation,
    db: Session = Depends(get_db_session),
) -> LoanRequestRead:
    """Reject client's item loan request."""

    client_user_id = services.auth.check_auth(request)

    return services.loan.reject_loan_request(
        db=db,
        loan_request_id=loan_request_id,
        query_filter=LoanRequestQueryFilter(
            item_id=item_id,
            owner_id=client_user_id,
        ),
    )
