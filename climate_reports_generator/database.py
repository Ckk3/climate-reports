import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_PATH = "sqlite:///" + os.path.abspath('./.dbdata/users.db')
engine = create_engine(DATABASE_PATH, echo=True)

Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

def setup_database():
    Base.metadata.create_all(engine)
