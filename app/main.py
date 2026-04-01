from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager
from app.core.database import engine, Base
from app.models.article import Article
from app.routers import articles, auth, users
from app.core.dependencies import get_db
from sqlalchemy.orm import Session


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "ok"}

app.include_router(articles.router)
app.include_router(auth.router)
app.include_router(users.router)