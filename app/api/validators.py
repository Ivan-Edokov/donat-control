from http import HTTPStatus

from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models.charity_project import CharityProject


async def chek_name_dublicate(
        project_name: str,
        session: AsyncSession
) -> None:
    """
    Корутина, проверяющая уникальность полученного
    имени переговорки.
    """

    project_id = await charity_project_crud.get_project_id_by_name(project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    """
    Корутина проверяет что объект с таким id есть в БД.
    """
    charity_project = await charity_project_crud.get(
        project_id, session
    )
    if charity_project is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail='Проект не найден!'
        )
    return charity_project


async def check_charity_project_not_invested(
        db_project: CharityProject
) -> None:
    """Корутина проверяет что в проект не было внесено средств."""

    if db_project.invested_amount != 0:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


async def check_charity_project_not_closed(
        db_project: CharityProject
) -> None:
    """Корутина проверяет что проект не закрыт."""

    if db_project.fully_invested:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!'
        )


async def check_full_amount_not_less_invested_amount(
    db_project: CharityProject,
    new_full_amount: int
) -> None:
    """
    Корутина проверяет что при изменении полной суммы проекта
    она была не менее уже внесенной.
    """
    if new_full_amount < db_project.invested_amount:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=('Новая требуемая сумма не может быть мене уже инвестированной, '
                    f'инвестированно на данный момент {db_project.invested_amount}')
        )
