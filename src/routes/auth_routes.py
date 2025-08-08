from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from src.lib.auth import verify_password, create_access_token
from src.database.dependencies import get_db
from src.repositories.user import UserRepository
from src.schemas.token import Token

router = APIRouter(tags=['Auth'])


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
	return UserRepository(db)


@router.post('/token', response_model=Token)
async def login(
	form_data: OAuth2PasswordRequestForm = Depends(),
	repository: UserRepository = Depends(get_user_repository)):
	
	user = repository.get_user_by_email(email=form_data.username)
	
	if not user or not verify_password(form_data.password, user.hashed_password):
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail='Incorrect email or password',
			headers={ 'WWW_Authenticate': 'Bearer' }
		)
	
	access_token_expires = timedelta(minutes=30)
	access_token = create_access_token(
		data={ 'sub': user.email },
		expires_delta=access_token_expires
		)
	
	return { 'access_token': access_token, 'token_type': 'bearer' }
	
	
	
	
	