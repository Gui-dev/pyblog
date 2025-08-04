from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing import List

from src.database.database import Base, engine, SessionLocal
from src.repositories.user import UserRepository
from src.schemas import user as schemas_user
from src.database.dependencies import get_db

router = APIRouter(
	prefix='/users',
	tags=['Users'],
)

def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
	return UserRepository(db)


@router.get('/', response_model=List[schemas_user.User])
def get_users(skip: int = 0, limit: int = 10, user_repository: UserRepository = Depends(get_user_repository)):
	users = user_repository.get_users(skip=skip, limit=limit)
	return users


@router.get('/{user_id}', response_model=schemas_user.User)
def get_user(user_id: int, user_repository: UserRepository = Depends(get_user_repository)):
	db_user = user_repository.get_user_by_id(user_id=user_id)
	
	if db_user is None:
		raise HTTPException(status_code=404, detail='User not found')
	
	return db_user


@router.post('/', response_model=schemas_user.User, status_code=status.HTTP_201_CREATED)
def create_user_endpoint(user: schemas_user.UserCreate, user_repository: UserRepository = Depends(get_user_repository)):
	db_user = user_repository.get_user_by_email(email=user.email)
	
	if db_user:
		raise HTTPException(status_code=400, detail="Email already registered")
	
	return user_repository.create_user(user=user)


@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, user_repository: UserRepository = Depends(get_user_repository)):
	db_user = user_repository.delete_user(user_id=user_id)
	
	if db_user is None:
		raise HTTPException(status_code=404, detail='User not found')
	