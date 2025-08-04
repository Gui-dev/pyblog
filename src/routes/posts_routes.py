from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status
from typing import List

from src.database.database import Base, engine, SessionLocal
from src.repositories.post import PostRepository
from src.schemas.post import PostCreate, Post
from src.database.dependencies import get_db

router = APIRouter(
	prefix='/posts',
	tags=['Posts'],
)

def get_post_repository(db: Session = Depends(get_db)) -> PostRepository:
	return PostRepository(db)

@router.post('/', response_model=Post)
def create_post(post: PostCreate, user_id: int, post_repository: PostRepository = Depends(get_post_repository)):
	"""Cria um novo post para um usuário existente"""
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


@router.delete('/post_id', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, post_repository: PostRepository = Depends(get_post_repository)):
	"""Deleta um post específico pelo ID"""
	db_post = post_repository.delete_post(post_id=post_id)
	
	if db_post is None:
		raise HTTPException(status_code=404, detail='Post not found')
	
	return




