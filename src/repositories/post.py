from sqlalchemy.orm import Session

from src.schemas.post import PostCreate, PostUpdate
from ..database.database import Post


class PostRepository:
	def __init__(self, db: Session):
		self.db = db


	def get_post_by_id(self, post_id: int):
		"""Busca um post pelo ID"""
		return self.db.query(Post).filter(Post.id == post_id).first()


	def get_posts(self, skip: int = 0, limit: int = 10):
		"""Retorna uma lista de posts com paginação"""
		return self.db.query(Post).offset(skip).limit(limit).all()


	def create_post(self, post: PostCreate, user_id: int):
		"""Cria um novo post no banco de dados"""
		db_post = Post(title=post.title, content=post.content, owner_id=user_id)
		self.db.add(db_post)
		self.db.commit()
		self.db.refresh(db_post)
		return db_post
	
	
	def update_post(self, post_update: PostUpdate, post_id: int):
		db_post = self.db.query(Post).filter(Post.id == post_id).first()
		
		if db_post:
			db_post.title = post_update.title
			db_post.content = post_update.content
			self.db.commit()
			self.db.refresh(db_post)
		
		return db_post
		


	def delete_post(self, post_id: int):
		"""Deleta um post pelo ID e retorna o post deletado"""
		db_post = self.db.query(Post).filter(Post.id == post_id).first()
		
		if db_post:
			self.db.delete(db_post)
			self.db.commit()
			
		return db_post
