from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import Donation
from app.models.user import User


class CRUDDatation(CRUDBase):
    async def get_by_user(
        self,
        session: AsyncSession,
        user: User,
    ) -> list[Donation]:
        """Корутина возвращает список донатов текущего пользователя"""

        db_donations_user = await session.execute(
            select(Donation).where(
                Donation.user_id == user.id
            )
        )
        return db_donations_user.scalars().all()


donation_crud = CRUDDatation(Donation)
