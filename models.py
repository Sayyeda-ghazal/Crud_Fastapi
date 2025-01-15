from sqlalchemy import  Column, Integer, String
from database import Base


class Book(Base):
    __tablename__ ="book"

    id = Column(Integer, primary_key=True, index=True)
    task:str = Column(String(255), nullable=False)
    

class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True)
    password = Column(String)
    email = Column(String, unique=True, nullable=False)

