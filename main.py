from fastapi import FastAPI,  Request
from database import Base, engine
import auth, random, string


app = FastAPI()
app.include_router(auth.router)  

Base.metadata.create_all(engine)


@app.middleware("http")
async def request_id_logging(request: Request, call_next):
    response = await call_next(request)
    random_letters = ''.join(random.choice(string.ascii_letters) for _ in range(10))
    print(f'Log {random_letters}')
    response.headers["X-Request-ID"] = random_letters
    return response

