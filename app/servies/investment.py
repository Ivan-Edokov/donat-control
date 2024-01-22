from datetime import datetime
from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import CharityProject, Donation


async def investment(
    obj_in: Union[CharityProject, Donation],
    session: AsyncSession,
) -> Union[CharityProject, Donation]:

    db_obj = (CharityProject if isinstance(obj_in, Donation) else Donation)

    db_objs = await session.execute(select(db_obj).where(
        db_obj.fully_invested == False # noqa
    ))
    db_objs = db_objs.scalars().all()

    incomming_amout = obj_in.full_amount

    for obj in db_objs:
        rest_amount = obj.full_amount - obj.invested_amount

        investment = (
            incomming_amout
            if incomming_amout < rest_amount else rest_amount
        )

        incomming_amout -= investment
        obj.invested_amount += investment
        obj_in.invested_amount += investment

        if obj.full_amount == obj.invested_amount:
            await close_object(obj)
        if not incomming_amout:
            await close_object(obj_in)
    await session.commit()
    return obj_in


async def close_object(
        obj: Union[CharityProject, Donation]
) -> None:
    obj.close_date = datetime.now()
    obj.fully_invested = True
