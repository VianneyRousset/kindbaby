from typing import Optional

from pydantic import Field, field_validator

from app.schemas.base import ApiQueryBase


class ItemApiQuery(ApiQueryBase):
    # words
    q: Optional[list[str]] = Field(
        title="Words used for fuzzy search",
        description=(
            "An item is returned if any word in this list fuzzy-matches a word in the "
            "item's name or description. However, the more given words that do not "
            "match any word in the item's name or description, the higher the word "
            "matching distance is."
        ),
        examples=[
            ["chair"],
            ["dog", "cat"],
        ],
        default=None,
    )

    # targeted_age_months
    mo: Optional[str] = Field(
        alias="mo",
        title="Targeted age months",
        description=(
            "An item is returned if its targeted age months is included in this range. "
            "The values are the targeted age in months. A null value specify "
            "an infinite bound."
        ),
        examples=[
            "3-12",
            "8-",
        ],
        default=None,
        pattern=r"^\d*-\d*$",
    )

    @field_validator("mo")
    def validate_mo(cls, mo):  # noqa: N805
        mo_range = cls.parse_mo(mo)

        if len(mo_range) != 2:
            msg = "mo must have 2 values"
            raise ValueError(msg)

        if (
            mo_range[0] is not None
            and mo_range[1] is not None
            and mo_range[0] > mo_range[1]
        ):
            msg = "mo values must be in order"
            raise ValueError(msg)

        return mo

    @staticmethod
    def parse_mo(mo):
        if mo is None:
            return None

        lower, upper = mo.split("-")
        lower = int(lower) if lower else None
        upper = int(upper) if upper else None

        return [lower, upper]

    @property
    def parsed_mo(self) -> Optional[list[int | None]]:
        return self.parse_mo(self.mo)

    # regions
    reg: Optional[list[int]] = Field(
        title="Regions",
        description=(
            "An item is returned if it is available in any of these regions IDs."
        ),
        examples=[
            [4],
            [2, 4, 7, 8],
        ],
        default=None,
    )

    # limit
    n: Optional[int] = Field(
        title="Limit returned items count",
        description="Limit the number of items returned.",
        examples=[
            [42],
        ],
        gt=0,
        le=128,
        default=64,
    )

    # cursor item_id
    cid: Optional[int] = Field(
        title="Page cursor for item ID",
        gt=0,
        default=None,
    )

    # cursor words_match
    cwm: Optional[int] = Field(
        title="Page cursor for words match",
        le=0,
        default=None,
    )


class SavedItemApiQuery(ItemApiQuery):
    # cursor save_id
    sid: Optional[int] = Field(
        title="Page cursor for save ID",
        gt=0,
        default=None,
    )


class LikedItemApiQuery(ItemApiQuery):
    # cursor save_id
    lid: Optional[int] = Field(
        title="Page cursor for like ID",
        gt=0,
        default=None,
    )
