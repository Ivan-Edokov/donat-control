from typing import List, Optional

from sqlalchemy import select

from app.core.db import AsyncSession
from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
        self,
        project_name: str,
        session: AsyncSession,
    ) -> Optional[int]:
        """
        Функция принимает имя объекта и возвращает
        id проекта если такой есть в БД
        """

        db_project_id = await session.execute(
            select(CharityProject.id).where(
                CharityProject.name == project_name
            )
        )
        db_project_id = db_project_id.scalars().first()
        return db_project_id

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession,
    ) -> List[CharityProject]:
        """
        Функция отсортирует список со всеми закрытыми проектами
        по количеству времени, которое понадобилось на сбор средств,
        — от меньшего к большему.
        """
        charity_projects = await session.execute(
            select(CharityProject).where(
                CharityProject.fully_invested
            ).order_by(CharityProject.close_date - CharityProject.create_date)
        )
        charity_projects = charity_projects.scalars().all()
        return charity_projects


charity_project_crud = CRUDCharityProject(CharityProject)
