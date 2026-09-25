from pydantic import BaseModel, field_validator, Field
from datetime import datetime

class UserBase(BaseModel):
	email: str

class UserCreate(UserBase):
	@field_validator("email")
	@classmethod
	def check_mail(cls, v):
		if "@" not in v:
			raise ValueError("Некорректный email")
		return v
	
	password: str = Field(min_length=8)

class UserResponse(UserBase):
	id: int
	created_at: datetime

	class Config:
		from_attributes = True

# Route Response
class RouterResponse(BaseModel):
	message: str
	data: UserResponse