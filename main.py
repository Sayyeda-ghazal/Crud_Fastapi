from fastapi import FastAPI, Depends, Path, HTTPException, Request
import schemas
import models
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import auth
import random
import string
from auth import get_current_user, get_db
from starlette import status
from typing import Annotated

app = FastAPI()
app.include_router(auth.router)  

Base.metadata.create_all(engine)

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[str, Depends(get_current_user)]  

def getsession():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

fakeBOOKdata = {
    1: {'book': 'English'},
    2: {'book': 'Urdu'},
    3: {'book': 'Maths'}
}

@app.get("/books")
def book(session: Session = Depends(getsession), user: str = Depends(get_current_user)):
    books = session.query(models.Book).all()
    if not books:
        raise HTTPException(status_code=404, detail="No books found")
    return books

@app.get("/books/{id}")
def getbook(id: int = Path(title='The ID of the book', gt=0), session: Session = Depends(getsession), user: str = Depends(get_current_user)):
    book = session.query(models.Book).get(id)
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with ID {id} not found")
    return book

@app.post("/books")
def addbook(item: schemas.Book, session: Session = Depends(getsession), user: str = Depends(get_current_user)):
    existing_book = session.query(models.Book).filter(models.Book.task == item.task).first()
    if existing_book:
        raise HTTPException(status_code=400, detail=f"Book with name {item.task} already exists")
    book = models.Book(task=item.task)
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

@app.put("/books/{id}")
def updatebook(id: int, item: schemas.Book, session: Session = Depends(getsession), user: str = Depends(get_current_user)):
    bookobj = session.query(models.Book).get(id)
    if not bookobj:
        raise HTTPException(status_code=404, detail="Book not found")
    bookobj.task = item.task
    session.commit()
    session.refresh(bookobj)
    return bookobj

@app.delete("/books/{id}")
def deletebook(id: int, session: Session = Depends(getsession), user: str = Depends(get_current_user)):
    bookobj = session.query(models.Book).get(id)
    if not bookobj:
        raise HTTPException(status_code=404, detail="Book not found")
    session.delete(bookobj)
    session.commit()
    session.close()
    return {"detail": "Book was deleted"}

@app.middleware("http")
async def request_id_logging(request: Request, call_next):
    response = await call_next(request)
    random_letters = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    print(f'Log {random_letters}')
    response.headers["X-Request-ID"] = random_letters
    return response

@app.get("/user", status_code=status.HTTP_200_OK)
async def user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication failed')
    return {"user": user}
