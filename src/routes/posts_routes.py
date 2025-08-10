from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing import List
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from src.database.database import Base, engine, SessionLocal
from src.repositories.post import PostRepository
from src.repositories.user import UserRepository
from src.schemas.post import PostCreate, Post, PostUpdate
from src.schemas.user import User
from src.database.dependencies import get_db
from src.lib.auth import ALGORITHM, SECRET_KEY


router = APIRouter(
	prefix='/posts',
	tags=['Posts'],
)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')


def get_post_repository(db: Session = Depends(get_db)) -> PostRepository:
	return PostRepository(db)


def get_user_repository(db: Session = Depends(get_db)) -> UserRepository:
	return UserRepository(get_db)


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
	credentials_exception = HTTPException(
		status_code=status.HTTP_401_UNAUTHORIZED,
		detail='Could not validate credentials',
		headers={ 'WWW-Authenticate': 'Bearer' },
	)
	
	try:
		payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
		username: str = payload.get('sub')
		
		if username is None:
			raise credentials_exception
	except JWTError:
		raise credentials_exception
	
	user_repository = UserRepository(db)
	user = user_repository.get_user_by_email(email=username)
	
	if user is None:
		raise credentials_exception
	
	return user
	


@router.post('/', response_model=Post, status_code=status.HTTP_201_CREATED)
def create_post(post: PostCreate, current_user: User = Depends(get_current_user), post_repository: PostRepository = Depends(get_post_repository)):
	"""Cria um novo post para um usuário existente"""
	user_id = current_user.id
	return post_repository.create_post(post=post, user_id=user_id)


@router.get('/{post_id}', response_model=Post)
def get_post(post_id: int, post_repository: PostRepository = Depends(get_post_repository)):
	"""Retorna um post específico pelo ID"""
	db_post = post_repository.get_post_by_id(post_id=post_id)
	
	if db_post is None:
		raise HTTPException(status_code=404, detail='Post not found')
	
	return db_post


@router.get('/', response_model=List[Post])
def get_posts(skip: int = 0, limit: int = 10, post_repository: PostRepository = Depends(get_post_repository)):
	"""Retorna todos os posts do blog"""
	posts = post_repository.get_posts(skip=skip, limit=limit)
	
	return posts


@router.put('/{post_id}', response_model=Post)
def update_post(post_id: int, post_update: PostUpdate, current_user: User = Depends(get_current_user), repository: PostRepository = Depends(get_post_repository)):
	"""Atualiza um post existente. Apenas o dono pode atualizar"""
	db_post = repository.get_post_by_id(post_id)
	
	if db_post is None:
		raise HTTPException(status_code=404, detail='Post not found')
	
	if db_post.owner_id != current_user.id:
		raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='You are not authorized to update this post')
	
	return repository.update_post(post_update, post_id)


@router.delete('/post_id', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, post_repository: PostRepository = Depends(get_post_repository)):
	"""Deleta um post específico pelo ID"""
	db_post = post_repository.delete_post(post_id=post_id)
	
	if db_post is None:
		raise HTTPException(status_code=404, detail='Post not found')
	
	return




