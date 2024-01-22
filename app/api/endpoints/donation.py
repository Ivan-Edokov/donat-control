from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import User
from app.schemas.donation import DonationCreate, DonationDB, DonationDBSuper
from app.servies.investment import investment

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
    donation: DonationCreate,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user),
):
    new_donation = await donation_crud.create(
        donation, session, user
    )
    await investment(new_donation, session)
    await session.refresh(new_donation)
    return new_donation


@router.get(
    '/',
    response_model=list[DonationDBSuper],
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def get_all_donations(
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    db_donations = await donation_crud.get_multi(session)
    return db_donations


@router.get(
    '/{my}',
    response_model=list[DonationDB],
    response_model_exclude_none=True,
)
async def my_donations(
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_user)
):
    """Получает список всех донатов для текущего пользователя"""
    db_donations = await donation_crud.get_by_user(session, user)
    return db_donations


@router.delete(
    '/{id}',
    deprecated=True
)
async def donation_delete(id: str):
    """Запрещено удалять пожертвования"""
    raise HTTPException(
        status_code=404,
        detail='Удаление пожертвований запрещено!'
    )


@router.patch(
    '/{id}',
    deprecated=True
)
async def remove_donation(id: str):
    """Запрещено редактировать пожертвования"""
    raise HTTPException(
        status_code=404,
        detail='Редактировать пожертвований запрещено!'
    )
