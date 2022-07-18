import requests
from bs4 import BeautifulSoup

PRODUCT_URL = "https://lemurrr.ru/product/00000036739"

headers = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}
page = requests.get(url=PRODUCT_URL, headers=headers)

soup = BeautifulSoup(page.content, "lxml")
product_title = soup.find("h1").get_text()
#print(product_title)
product_price = soup.find("span",class_="price__actual").get_text()
product_price = int(''.join([i for i in product_price if i.isdigit()]))
#print(product_price, type(product_price))

#-----------------------------
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Price(Base):
	__tablename__ = "price"

	id = Column(Integer, primary_key=True)
	name = Column(String)
	datetime = Column(DateTime)
	price_int = Column(Numeric(10,2))

	def __repr__(self):
		return f" {self.name} | {self.price_int}"

engine = create_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)

def add_record():
	session.add(
		Price(
			name=product_title,
			datetime=datetime.now(),
			price_int=product_price
		)
	)
	session.commit()

is_exist = session.query(Price).filter(Price.name==product_title).order_by(Price.datetime.desc()).first()
if not is_exist:
	add_record()
else:
	if is_exist.price_int != product_price:
		add_record()


items = session.query(Price).all()
for item in items:
	print(item)