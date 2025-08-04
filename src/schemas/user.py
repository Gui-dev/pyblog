from pydantic import BaseModel
from typing import List, Optional

from .post import Post


class UserBase(BaseModel):
	email: str
	
	
class UserCreate(UserBase):
	password: str
	

class User(UserBase):
	id: int
	is_active: bool
	posts: List[Post] = []
	
	class Config:
		from_attributes = True