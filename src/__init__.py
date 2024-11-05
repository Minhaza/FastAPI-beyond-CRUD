from fastapi import FastAPI
from src.books.routes import book_router
from src.auth.routes import user_router
from contextlib import asynccontextmanager

from src.db.main import init_db

@asynccontextmanager
async def life_span(app:FastAPI):
    print(f"Server is starting ... ")
    await init_db()
    # Lines above this run at the start
    yield
    #Lines below this run when the server stop
    
    print(f"Server has been stopped")

version="v1"

app = FastAPI(
    title="Bookly",
    description="FastAPI beyond CRUD",
    version=version,
    lifespan=life_span    
)

app.include_router(router=book_router, prefix=f"/api/{version}/books", tags=["books"])
app.include_router(router=user_router, prefix=f"/api/{version}/auth", tags=["auth"])

