from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, DateTime, Numeric
from sqlalchemy.orm import relationship

from .database import Base


class Price(Base):
    __tablename__ = "price"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    url = Column(String)
    datetime = Column(DateTime)
    price = Column(Integer)

    def __repr__(self):
        return f"{self.name} | {self.price}"

