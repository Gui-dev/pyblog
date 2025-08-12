from sqlalchemy import create_engine, Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./src/database/blog.db'

engine = create_engine(
	SQLALCHEMY_DATABASE_URL, connect_args={ 'check_same_thread': False }
)

Base = declarative_base()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class User(Base):
	__tablename__ = 'users'
	
	id = Column(Integer, primary_key=True, index=True)
	email = Column(String, unique=True, index=True)
	hashed_password = Column(String)
	is_active = Column(Boolean, default=True)
	
	posts = relationship('Post', back_populates='owner')
	
	
class Post(Base):
	__tablename__ = 'posts'
	
	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True)
	content = Column(String)
	owner_id = Column(Integer, ForeignKey('users.id'))
	owner = relationship('User', back_populates='posts')