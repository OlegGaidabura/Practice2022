from datetime import datetime
from typing import List, Union

from pydantic import BaseModel


class PriceBase(BaseModel):
    name: str
    url: str = None
    price: int


class PriceCreate(PriceBase):
    pass


class Price(PriceBase):
    id: int
    datetime: datetime

    class Config:
        orm_mode = True
