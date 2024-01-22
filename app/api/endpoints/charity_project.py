from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (check_charity_project_exists,
                                check_charity_project_not_closed,
                                check_charity_project_not_invested,
                                check_full_amount_not_less_invested_amount,
                                chek_name_dublicate)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.servies.investment import investment

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)],
)
async def create_new_charity_project(
    charity_project: CharityProjectCreate,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    await chek_name_dublicate(charity_project.name, session)
    new_project = await charity_project_crud.create(charity_project, session)
    await investment(new_project, session)
    await session.refresh(new_project)
    return new_project


@router.get(
    '/',
    response_model=list[CharityProjectDB],
    response_model_exclude_none=True,
)
async def get_all_charity_project(
    session: AsyncSession = Depends(get_async_session)
):
    all_project = await charity_project_crud.get_multi(session)
    return all_project


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)],
)
async def partially_update_charity_project(
    project_id: int,
    obj_in: CharityProjectUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Только для суперюзеров."""

    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_not_closed(charity_project)
    if obj_in.full_amount is not None:
        await check_full_amount_not_less_invested_amount(
            charity_project, obj_in.full_amount
        )
    if obj_in.name is not None:
        await chek_name_dublicate(obj_in.name, session)
    charity_project = await charity_project_crud.update(
        charity_project, obj_in, session
    )
    await investment(charity_project, session)
    await session.refresh(charity_project)

    return charity_project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_charity_project(
    project_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    """Только для суперюзеров."""

    charity_project = await check_charity_project_exists(
        project_id, session
    )
    await check_charity_project_not_invested(charity_project)
    charity_project = await charity_project_crud.remove(
        charity_project, session
    )
    return charity_project
