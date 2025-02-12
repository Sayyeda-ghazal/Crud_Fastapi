from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends, Path, Request
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users, Book
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import models, schemas
from schemas import createuserrequest, login
from dotenv import load_dotenv
import os

router = APIRouter(prefix='/auth', tags=['auth'])

load_dotenv(dotenv_path=".env")


SECRET_KEY = os.getenv("SECRET_KEY")
DEBUG_MODE = os.getenv("DEBUG", "False") == "True"

ALGORITHM = os.getenv("ALGORITHM")




bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
outh2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')
ACCESS_TOKEN_EXPIRE_MINUTES=30

def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def hash_password(password: str) -> str:

    return bcrypt_context.hash(password)

def get_current_user(token: str = Depends(outh2_bearer), session: Session = Depends(get_db)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
    
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid authentication credentials")
        user = session.query(models.Users).filter(models.Users.username == username).first()
    
        if user is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="User not found")
        return user
    
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token" )



db_dependency = Annotated[Session, Depends(get_db)]

def create_access_token(data: dict):
    
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

@router.post("/signup", status_code=status.HTTP_201_CREATED)

def create_user( user: createuserrequest, session: Session = Depends(get_db)):

    new_user = models.Users()
    existing_user = session.query(models.Users).filter(models.Users.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail=f"User with name {user.username} already exists")

    new_user.username = user.username
    new_user.password = bcrypt_context.hash(user.password)
    new_user.email = user.email
    session.add(new_user)
    session.commit()

    return new_user

@router.get("/login")

def login_user(user: login, session: Session = Depends(get_db)):

    db_user = session.query(models.Users).filter(models.Users.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "User not found")

    if not bcrypt_context.verify(user.password,db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= "Incorrect password")

    access_token = create_access_token(data={"sub": db_user.username})

    return { "access_token": access_token, "token_type": "bearer", "username": db_user.username, "email": db_user.email}


@router.get("/")

def book(session: Session = Depends(get_db),current_user: Users = Depends(get_current_user)): 

    books = session.query(models.Book).all()

    if not books:
        raise HTTPException(status_code=404, detail="No books found")

    return books


@router.get("/books/{id}")

def getbook(id: int = Path(title='The ID of the book', gt=0), session: Session = Depends(get_db),current_user: Users = Depends(get_current_user)): 
 
    book = session.query(models.Book).get(id)

    if not book:
        raise HTTPException(status_code=404, detail=f"Book with ID {id} not found")

    return book

@router.post("/books")

def addbook(item: schemas.Book, session: Session = Depends(get_db),current_user: Users = Depends(get_current_user)): 
 
    existing_book = session.query(models.Book).filter(models.Book.task == item.task).first()

    if existing_book:
        raise HTTPException(status_code=400, detail=f"Book with name {item.task} already exists")

    book = models.Book(task=item.task)
    session.add(book)
    session.commit()
    session.refresh(book)

    return book

@router.put("/books/{id}")

def updatebook(id: int, item: schemas.Book, session: Session = Depends(get_db),current_user: Users = Depends(get_current_user)): 
 
    bookobj = session.query(models.Book).get(id)

    if not bookobj:
        raise HTTPException(status_code=404, detail="Book not found")

    bookobj.task = item.task
    session.commit()
    session.refresh(bookobj)

    return bookobj

@router.delete("/books/{id}")

def deletebook(id: int, session: Session = Depends(get_db),current_user: Users = Depends(get_current_user)): 
 
    bookobj = session.query(models.Book).get(id)

    if not bookobj:
        raise HTTPException(status_code=404, detail="Book not found")

    session.delete(bookobj)
    session.commit()
    session.close()

    return {"detail": "Book was deleted"}

model_map = {
    "Users": models.Users,
    "Book": models.Book,
   
}

def get_model_query(model_name: str, session: Session):
 
    model = model_map.get(model_name)

    if not model:
        raise HTTPException(status_code=404, detail=f"Model {model_name} not found")

    query_result = session.query(model).all()

    return query_result

@router.get("/query/{model_name}")
def query_model(model_name: str, session: Session = Depends(get_db)):
    
    result = get_model_query(model_name, session)
    
    return result
