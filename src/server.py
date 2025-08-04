from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing import List

from src.database.database import Base, engine, SessionLocal
from src.database.dependencies import get_db

from src.repositories import user as user_repository
from src.schemas import user as schemas_user
from src.routes import users_routes, posts_routes

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(users_routes.router)
app.include_router(posts_routes.router)


@app.get('/')
async def root():
	return { "message": "Hello, World"}


@app.get('/health')
def health_check(db: Session = Depends(get_db)):
	return { 'status': 'ok', 'message': 'Database connection successful' }

