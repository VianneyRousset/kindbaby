from typing import Optional

from sqlalchemy.dialects.postgresql import Range
from sqlalchemy.orm import Session

from app.clients.database.image import get_image_by_name
from app.clients.database.region import get_region
from app.clients.database.user import get_user
from app.models.item import Item


def create_item(
    db: Session,
    *,
    name: str,
    description: str,
    targeted_age_months: list[int],
    owner_id: int,
    images: list[str],
    regions: list[int],
    blocked: Optional[bool] = False,
) -> Item:
    """Create and insert item into database."""

    item = Item(
        name=name,
        description=description,
        targeted_age_months=Range(*targeted_age_months, bounds="[]"),
        blocked=blocked,
        owner_id=owner_id,
    )

    # add images to item
    item.images.extend([get_image_by_name(db, name) for name in images])

    # add regions to item
    for region_id in regions:
        region = get_region(db, region_id)
        region.items.append(item)

    return insert_item(
        db=db,
        item=item,
    )


def insert_item(
    db: Session,
    item: Item,
) -> Item:
    """Insert item into the database."""

    # check owner exists
    get_user(
        db=db,
        user_id=item.owner_id,
    )

    db.flush()
    db.refresh(item)

    return item
