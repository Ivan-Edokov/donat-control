from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt] = Field(None)

    class Config:
        extra = Extra.forbid


class CharityProjectUpdate(CharityProjectBase):

    @validator('name')
    def name_cannot_be_null(cls, value):
        """Функция проверяет что имя проекта не Null"""

        if value is None:
            raise ValueError('Название проекта не может быть пустым!')
        return value

    @validator('description')
    def description_cannot_be_null(cls, value):
        """Функция проверяет что имя проекта не Null"""

        if value is None:
            raise ValueError('Описание проекта не может быть пустым!')
        return value


class CharityProjectCreate(CharityProjectUpdate):
    name: str = Field(..., max_length=100, min_length=1)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    create_date: datetime
    close_date: Optional[datetime] = Field(None)

    class Config:
        orm_mode = True
