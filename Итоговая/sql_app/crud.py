from datetime import datetime
from sqlalchemy.orm import Session

import models, schemas


def get_price(db: Session, price_id: int):
    return db.query(models.Price).filter(models.Price.id == price_id).first()

def del_price(db: Session, price_id: int):
    item = db.query(models.Price).filter(models.Price.id == price_id).delete() 
    db.commit()
    return

def get_price_by_name(db: Session, name: str):
    return db.query(models.Price).filter(
        models.Price.name == name
    ).order_by(models.Price.datetime.desc()).first()


def get_prices(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Price).offset(skip).limit(limit).all()


def create_price(db: Session, price: schemas.PriceCreate):
    dt = datetime.now()
    db_price = models.Price(
        name=price.name,
        url=price.url,
        price=price.price,
        datetime=dt
    )
    db.add(db_price)
    db.commit()
    db.refresh(db_price)
    return db_price

def update_price(db: Session, price_id: int, price: schemas.PriceCreate):
    item = db.query(models.Price).filter(models.Price.id == price_id).first()
    item.name = price.name
    item.url = price.url
    item.price = price.price
    db.add(item)
    db.commit()
    db.refresh(item)
    return item