from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=r"C:\Users\s\Desktop\apivenv\.env.secret")

DATABASE_URL = os.getenv("DATABASE_URL")
DEBUG_MODE = os.getenv("DEBUG", "False") == "True"


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush = False, bind=engine, expire_on_commit= False)
Base = declarative_base()
