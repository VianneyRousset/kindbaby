from typing import TYPE_CHECKING

from sqlalchemy import (
    CheckConstraint,
    Identity,
    Integer,
    String,
    func,
    select,
    text,
)
from sqlalchemy.orm import (
    Mapped,
    column_property,
    deferred,
    mapped_column,
    relationship,
)

from .base import Base, CreationDate
from .item import Item, ItemLike

if TYPE_CHECKING:
    from .chat import Chat
    from .loan import Loan, LoanRequest


class User(CreationDate, Base):
    __tablename__ = "user"

    # id is defined explicitly instead of using IntegerIdentifier subclassing
    # to be accessed by likes_count deferred query
    id: Mapped[int] = mapped_column(
        Integer,
        Identity(always=True),
        primary_key=True,
        index=True,
        autoincrement=True,
    )

    email: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
    )
    name: Mapped[str] = mapped_column(
        String,
    )
    password: Mapped[str] = mapped_column(
        String,
    )
    avatar_seed: Mapped[str] = mapped_column(
        String,
        server_default=func.md5(text("random()::text")),
    )

    items: Mapped[list["Item"]] = relationship(
        "Item",
        back_populates="owner",
        cascade="all, delete",
    )

    liked_items: Mapped[list["Item"]] = relationship(
        "Item",
        secondary="item_like",
        back_populates="liked_by",
    )

    saved_items: Mapped[list["Item"]] = relationship(
        "Item",
        secondary="item_save",
        back_populates="saved_by",
    )

    borrowings: Mapped[list["Loan"]] = relationship(
        "Loan",
        back_populates="borrower",
    )
    borrowing_requests: Mapped[list["LoanRequest"]] = relationship(
        "LoanRequest",
        back_populates="borrower",
        cascade="all, delete-orphan",
    )
    chats: Mapped[list["Chat"]] = relationship(
        "Chat",
        secondary="chat_participant",
        back_populates="participants",
    )

    stars_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
    )

    # total number of likes of the items owned by the user
    likes_count: Mapped[int] = deferred(
        column_property(
            select(func.count(ItemLike.item_id))
            .join(Item)
            .where(Item.owner_id == id)
            .scalar_subquery()
        )
    )

    # number of items owned by the user
    items_count: Mapped[int] = deferred(
        column_property(
            select(func.count(Item.id)).where(Item.owner_id == id).scalar_subquery()
        )
    )

    __table_args__ = (CheckConstraint(stars_count >= 0, name="positive_stars_count"),)

    def __repr__(self):
        return f"<{self.__class__.__name__} #{self.id!r} {self.email!r} {self.name!r}>"
