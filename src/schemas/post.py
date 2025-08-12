from pydantic import BaseModel, ConfigDict
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
	
	model_config = ConfigDict(from_attributes=True)