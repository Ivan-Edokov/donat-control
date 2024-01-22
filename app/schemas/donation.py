from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra, Field, PositiveInt


class DonationBase(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationDB(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDBSuper(DonationDB):
    user_id: Optional[int] = Field(None)
    invested_amount: int = Field(0)
    fully_invested: bool = Field(False)
    close_date: Optional[datetime] = Field(None)
