from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings

FORMAT = "%Y/%m/%d %H:%M:%S"
PERMISSIONS_BODY = {'type': 'user',
                    'role': 'writer',
                    'emailAddress': settings.email}
SPREADSHEET_BODY = {
    'properties': {'title': 'Отчёт на {}',
                   'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': 'Лист1',
                               'gridProperties': {'rowCount': 100,
                                                  'columnCount': 11}}}]
}
TABLE_VALUES = [
    ['Отчёт от, {}'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    """
    Функция создания таблицы.
    """
    spreadsheet_body = deepcopy(SPREADSHEET_BODY)
    now_date_time = datetime.now().strftime(FORMAT)
    spreadsheet_body['properties']['title'] = (
        spreadsheet_body['properties']['title'].format(now_date_time)
    )
    service = await wrapper_services.discover('sheets', 'v4')
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    """Функция предоставления прав доступа
    личному аккаунту к созданному документу"""
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=PERMISSIONS_BODY,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        charity_projects: list,
        wrapper_services: Aiogoogle
) -> None:
    """
    Функция записывает полученную из базы данных информацию
    в документ с таблицами.
    """
    table_values = deepcopy(TABLE_VALUES)
    now_date_time = datetime.now().strftime(FORMAT)
    table_values[0][0] = table_values[0][0].format(now_date_time)
    service = await wrapper_services.discover('sheets', 'v4')
    for project in charity_projects[::-1]:
        new_row = [project.name,
                   str(project.close_date - project.create_date),
                   project.description]
        table_values.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
