from app import domain
from app.schemas.base import ReadBase
from app.schemas.item.base import ItemBase
from app.schemas.loan.read import LoanRead
from app.schemas.region.read import RegionRead
from app.schemas.user.preview import UserPreviewRead
from app.schemas.utils import integer_range_to_inclusive


class ItemPrivateRead(ItemBase, ReadBase):
    id: int
    name: str
    description: str
    targeted_age_months: list[int | None]
    images: list[str]
    available: bool
    owner_id: int

    owner: UserPreviewRead
    regions: list[RegionRead]
    likes_count: int

    blocked: bool
    loans: list[LoanRead]

    @classmethod
    def from_orm(cls, item):
        # get targeted_age_months as an inclusive [lower, upper] range
        targeted_age_months = integer_range_to_inclusive(item.targeted_age_months)
        targeted_age_months = [targeted_age_months.lower, targeted_age_months.upper]

        return cls(
            id=item.id,
            name=item.name,
            description=item.description,
            targeted_age_months=targeted_age_months,
            images=[img.name for img in item.images],
            available=domain.item.compute_item_available(
                is_blocked=item.blocked,
                active_loans_count=item.active_loans_count,
            ),
            owner_id=item.owner_id,
            owner=UserPreviewRead.from_orm(item.owner),
            regions=[RegionRead.from_orm(region) for region in item.regions],
            likes_count=item.likes_count,
            blocked=item.blocked,
            loans=[LoanRead.from_orm(loan) for loan in item.loans],
        )
