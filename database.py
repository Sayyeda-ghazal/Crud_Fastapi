from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql://postgres:ghazaldb1@localhost:5432/Book'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine, expire_on_commit= False)
Base = declarative_base()
