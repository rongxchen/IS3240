from general_config import db_path
from models.util import to_string
from sqlalchemy import create_engine, Column, Integer, String
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
    user_id = Column(String(100), nullable=False)
    password = Column(String(100), nullable=False)

    def __init__(self, username, user_id, password):
        self.username = username
        self.user_id = user_id
        self.password = password

# if __name__ == '__main__':
#     Base.metadata.create_all(engine)
