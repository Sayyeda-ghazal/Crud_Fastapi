from datetime import timedelta, datetime
from typing import Annotated
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from starlette import status
from database import SessionLocal
from models import Users
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError

router = APIRouter(prefix='/auth', tags=['auth'])

SECRET_KEY = '7f9c2ba4b65e0c5ad3d4f8fae9c3e9f0f97db6bc1b43a9f9b321fd36a561cbd8'
ALGORITHM = 'HS256' 

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated = 'auto')
outh2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

class createuserrequest(BaseModel):
    username:str
    password:str

class Token(BaseModel):
    access_token: str
    token_type: str

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post("/", status_code=status.HTTP_201_CREATED)
async def get_current_user(token: str = Depends(outh2_bearer), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        user = db.query(Users).filter(Users.id == user_id).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found",
            )
        return user
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='incorrect username')
    token = create_access_token(user.username, user.id, timedelta(minutes=20))
    return{'access_token': token, 'token_type': 'bearer'}

def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user

def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {'sub':username, 'id': user_id}
    expires = datetime.utcnow() + expires_delta
    encode.update({'exp':expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)

async def get_current_user(token: Annotated[str, Depends(outh2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get('sub')
        user_id: str = payload.get('id')
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user.")
        return {'username': username, 'id': user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail= 'Could not validate user')

