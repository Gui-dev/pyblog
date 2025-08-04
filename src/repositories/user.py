from sqlalchemy.orm import Session
from passlib.context import CryptContext

from ..schemas.user import UserCreate
from ..database.database import User

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


class UserRepository:
	def __init__(self, db: Session):
		self.db = db
		

	def get_user_by_id(self, user_id: int):
		"""Busca um usuário pelo ID"""
		return self.db.query(User).filter(User.id == user_id).first()


	def get_user_by_email(self, email: str):
		"""Busca um usuário pelo e-mail."""
		return self.db.query(User).filter(User.email == email).first()


	def get_users(self, skip: int = 0, limit: int = 10):
		"""Retorna uma lista de usuários com paginação"""
		return self.db.query(User).offset(skip).limit(limit).all()


	def delete_user(self, user_id: int):
		"""Deleta um usuário pelo ID e retorna o usuário deletado."""
		db_user = self.db.query(User).filter(User.id == user_id).first()
		
		if db_user:
			self.db.delete(db_user)
			self.db.commit()
			
		return db_user


	def create_user(self, user: UserCreate):
		"""Cria um novo usuário no banco de dados"""
		hashed_password = pwd_context.hash(user.password)
		db_user = User(email=user.email, hashed_password=hashed_password)
		
		self.db.add(db_user)
		self.db.commit()
		self.db.refresh(db_user)
		
		return db_user
