from general_config import db_path
from models.util import to_string
from sqlalchemy import create_engine, Column, Integer, String, Double
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine(db_path)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

@to_string
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100))
    user_id = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    def __init__(self, username, email, user_id, password):
        self.username = username
        self.email = email
        self.user_id = user_id
        self.password = password

@to_string
class News(Base):
    __tablename__ = "news"

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    url = Column(String(1000))
    publish_time = Column(String(59), nullable=False)
    timestamp = Column(Integer, nullable=False)
    category = Column(String(100))
    img_url = Column(String(1000))
    source = Column(String(100), nullable=False)

    def __init__(self, title, publish_time, timestamp, source, url="", category="", img_url=""):
        self.title = title
        self.publish_time = publish_time
        self.timestamp = timestamp
        self.source = source
        self.url = url
        self.category = category
        self.img_url = img_url

class Favourite(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True)
    user_id = Column(String(100), nullable=False)
    symbol = Column(String(100), nullable=False)
    market = Column(String(100), nullable=False)
    added_date = Column(String(100), nullable=False)
    timestamp = Column(Integer, nullable=False)
    cost = Column(Double, nullable=False)
    current_price = Column(Double)
    quantity = Column(Integer, nullable=False)

    def __init__(self, user_id, symbol, market, added_date, timestamp, cost, current_price=0.0, quantity=1):
        self.user_id = user_id
        self.symbol = symbol
        self.market = market
        self.added_date = added_date
        self.timestamp = timestamp
        self.cost = cost
        self.current_price = current_price
        self.quantity = quantity

# if __name__ == '__main__':
#     Base.metadata.create_all(engine)
