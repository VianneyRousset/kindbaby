from collections.abc import Mapping
from typing import Any

from .base import ApiError, ConflictError, NotFoundError


class ItemSaveError(ApiError):
    """Exception related to a item save."""

    pass


class ItemSaveAlreadyExistsError(ItemSaveError, ConflictError):
    """Exception related to an already existing item save."""

    def __init__(self, *, user_id: int, item_id: int):
        message = f"Item #{item_id} is already saved by user #{user_id}."

        super().__init__(message)


class ItemSaveNotFoundError(ItemSaveError, NotFoundError):
    """Exception related to a non-existing item save."""

    def __init__(self, key: Mapping[str, Any], **kwargs):
        super().__init__(
            datatype="item save",
            key=key,
            **kwargs,
        )
