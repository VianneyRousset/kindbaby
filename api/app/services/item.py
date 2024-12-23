from typing import Optional

from sqlalchemy.orm import Session

from app import domain
from app.clients import database
from app.enums import ReportType
from app.models.item import Item
from app.schemas.item.create import ItemCreate
from app.schemas.item.query import (
    ItemQueryPageResult,
    ItemQueryFilter,
    ItemQueryPageOptions,
)
from app.schemas.item.preview import ItemPreviewRead
from app.schemas.item.private import ItemPrivateRead
from app.schemas.item.read import ItemRead
from app.schemas.item.update import ItemUpdate
from app.schemas.report import ReportCreate


async def create_item(
    db: Session,
    owner_id: int,
    item_create: ItemCreate,
) -> ItemPreviewRead:
    """Create a new item in the database."""

    # TODO index data in search engine
    item = await database.item.create_item(
        db=db,
        name=item_create.name,
        description=item_create.description,
        regions=item_create.regions,
        owner_id=owner_id,
        images=item_create.images,
        targeted_age_months=item_create.targeted_age_months,
        blocked=item_create.blocked,
        load_attributes=[Item.images, Item.active_loans],
    )

    await database.user.add_stars_to_user(
        db=db,
        user_id=owner_id,
        added_stars_count=domain.star.get_stars_gain_when_adding_item(1),
    )

    return ItemPreviewRead.from_orm(item)


async def list_items(
    db: Session,
    *,
    query_filter: Optional[ItemQueryFilter] = None,
    page_options: Optional[ItemQueryPageOptions] = None,
) -> ItemQueryPageResult[ItemPreviewRead]:
    """List items matchings criteria in the database.

    Order
    -----
    The items are return sorted by:
    - Increasing words match distance (the most relevant items are given first)
      if query_filter.words is provided.
    - Then, by descreasing `save_id` (the items saved the most recently
      are given first) if query_filter.saved_by_user_id is provided.
    - Then, by descreasing `like_id` (the items liked the most recently
      are given first) if query_filter.liked_by_user_id is provided.
    - Finally, by descreasing `item_id` (the items created most recently
      are given first.
    """

    # search in db
    # TODO discard words shorter than 3 characters ?
    result = await database.item.list_items(
        db=db,
        query_filter=query_filter,
        page_options=page_options,
        load_attributes=[Item.images, Item.active_loans],
    )

    return ItemQueryPageResult[ItemPreviewRead](
        **{
            **result.dict(),
            "items": [ItemPreviewRead.from_orm(item) for item in result.items],
        }
    )


async def get_item(
    db: Session,
    item_id: int,
) -> ItemRead:
    """Get item by id."""

    # get item from databse
    # TODO replace client concept with a non-client concept
    item = await database.item.get_item(
        db=db,
        item_id=item_id,
        load_attributes=[
            Item.owner,
            Item.images,
            Item.regions,
            Item.likes_count,
            Item.active_loans,
        ],
    )

    return ItemRead.from_orm(item)


async def get_private_item(
    db: Session,
    item_id: int,
    owner_id: Optional[int] = None,
) -> ItemPrivateRead:
    """Get item by id.

    If `owner_id` is provided, the item must be owned by the user with this ID.
    """

    # get item from databse
    # TODO replace client concept with a non-client concept
    item = await database.item.get_item(
        db=db,
        item_id=item_id,
        owner_id=owner_id,
        load_attributes=[
            Item.owner,
            Item.images,
            Item.regions,
            Item.likes_count,
            Item.loans,
            Item.active_loans,
        ],
    )

    return ItemPrivateRead.from_orm(item)


async def update_item(
    db: Session,
    *,
    item_id: int,
    item_update: ItemUpdate,
    owner_id: Optional[int] = None,
) -> ItemPrivateRead:
    """Update item owned by `owner_id`."""

    # TODO check if images exists

    item = await database.item.update_item(
        db=db,
        item_id=item_id,
        owner_id=owner_id,
        attributes=item_update.dict(exclude_none=True),
        load_attributes=[
            Item.owner,
            Item.images,
            Item.regions,
            Item.likes_count,
            Item.loans,
            Item.active_loans,
        ],
    )

    return ItemPrivateRead.from_orm(item)


async def delete_item(
    db: Session,
    item_id: int,
    owner_id: Optional[int] = None,
):
    """Delete the item with ID `item_id`.

    If `owner_id` is provided, the item must be owned by the user with this ID.
    """

    await database.item.delete_item(
        db=db,
        owner_id=owner_id,
        item_id=item_id,
    )


async def report_item(
    db: Session,
    item_id: int,
    reported_by_user_id: int,
    report_create: ReportCreate,
):
    """Create a report for the item with `item_id`.

    A maximum of item infos are saved as well as the given client provided description
    and context.
    """

    item = await database.item.get_item_for_report()

    await database.report.insert_report(
        report_type=ReportType.item,
        reported_by_user_id=reported_by_user_id,
        saved_info=item.json(),
        description=report_create.description,
        context=report_create.context,
    )

    # TODO send an email to moderators
