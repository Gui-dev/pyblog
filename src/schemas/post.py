from pydantic import BaseModel
from typing import List, Optional

class PostBase(BaseModel):
	title: str
	content: str
	
	
class PostCreate(PostBase):
	pass


class PostUpdate(PostBase):
	pass


class Post(PostBase):
	id: int
	owner_id: int
	
	class Config:
		from_attributes = True