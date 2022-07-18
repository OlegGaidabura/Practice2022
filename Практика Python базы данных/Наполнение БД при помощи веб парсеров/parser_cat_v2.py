import requests
from bs4 import BeautifulSoup
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, Column, Integer, String, Numeric, DateTime
from sqlalchemy.ext.declarative import declarative_base

CATALOG_URL = "https://lemurrr.ru/catalog"
pages = []

headers = {
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

#Добавление в список всех продуктов на странице
catalog_page = requests.get(url=CATALOG_URL, headers=headers)
soup = BeautifulSoup(catalog_page.content, "lxml")
for link in soup.find_all('li',class_='catalog__entry catalog__entry_thumb'):
    pages.append('https://lemurrr.ru'+link.a.get('href'))

#---------------------------------
Base = declarative_base()

class Price(Base):
	__tablename__ = "price"

	id = Column(Integer, primary_key=True)
	name = Column(String)
	url = Column(String)
	datetime = Column(DateTime)
	price = Column(Integer)

	def __repr__(self):
		return f" {self.name} | {self.price}"

engine = create_engine("sqlite:///database.sqlite")
Base.metadata.create_all(engine)

session = Session(bind=engine)

def add_product(url,title,price): 
    is_exist = session.query(Price).filter(Price.name==title).order_by(Price.datetime.desc()).first()
    if not is_exist:
	    session.add(
		    Price(
				url=url,
			    name=title,
			    datetime=datetime.now(),
			    price=price
	    	)
	    )
	    session.commit()
    else:
        if is_exist.price != price:
	        session.add(
	            Price(
					url=url,
		            name=title,
		            datetime=datetime.now(),
		            price=price
	            )
            )
        session.commit()

#-------------------------------------
for page in pages:
    current_page = requests.get(url=page, headers=headers)
    soup = BeautifulSoup(current_page.content, "lxml")
    product_url = str(page)
    product_title = soup.find("h1").get_text()
    product_price = soup.find("span",class_="price__actual").get_text()
    product_price = int(''.join([i for i in product_price if i.isdigit()]))
    add_product(product_url,product_title,product_price)

items = session.query(Price).all()
for item in items:
	print(item)