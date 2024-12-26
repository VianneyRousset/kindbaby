from typing import Optional

from pydantic import Field, field_validator
from typing_extensions import Annotated

from app import config
from app.schemas.base import CreateBase
from app.schemas.item.base import ItemBase


class ItemCreate(ItemBase, CreateBase):
    name: Annotated[
        str,
        Field(
            min_length=config.ITEM_NAME_MIN_LENGTH,
            max_length=config.ITEM_NAME_MAX_LENGTH,
        ),
    ]
    description: Annotated[
        str,
        Field(
            min_length=config.ITEM_DESCRIPTION_MIN_LENGTH,
            max_length=config.ITEM_DESCRIPTION_MAX_LENGTH,
        ),
    ]
    images: list[str]
    targeted_age_months: list[int | None]
    regions: list[int]
    blocked: Optional[bool] = False

    @field_validator("targeted_age_months")
    def validate_targeted_age_months(cls, v):  # noqa: N805
        if len(v) != 2:
            msg = "targeted_age_months must have 2 values"
            raise ValueError(msg)

        if v[0] is not None and v[1] is not None and v[0] > v[1]:
            msg = "targeted_age_months values must be in order"
            raise ValueError(msg)

        return v
