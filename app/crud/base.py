from typing import Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User


class CRUDBase:

    def __init__(self, model):
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession
    ):
        """Метод пулучения объекта по id из БД"""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession
    ):
        """Получение всех объектов из БД"""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in,
            session: AsyncSession,
            user: Optional[User] = None
    ):
        """Метод создания нового объекта"""
        new_obj_data = obj_in.dict()
        if user is not None:
            new_obj_data['user_id'] = user.id
        new_db_obj = self.model(**new_obj_data)
        session.add(new_db_obj)
        await session.commit()
        await session.refresh(new_db_obj)
        return new_db_obj

    async def update(
            self,
            db_obj,
            obj_in,
            session: AsyncSession
    ):
        """Метод изменения объекта в БД"""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj,
            session: AsyncSession
    ):
        """Метод удаления объекта из БД"""
        await session.delete(db_obj)
        await session.commit()
        return db_obj
