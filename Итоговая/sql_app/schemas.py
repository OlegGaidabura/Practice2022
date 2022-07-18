from typing import List, Union

from pydantic import BaseModel


class PriceBase(BaseModel):
    name: str
    url: str = None
    price: int


class PriceCreate(PriceBase):
    datetime: str


class Price(PriceBase):
    id: int

    class Config:
        orm_mode = True
