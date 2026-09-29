from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime

class CharacterCreate(BaseModel):
	name: str

class CharacterRead(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	owner_id: int
	name: str

	health: int
	max_health: int
	stamina: int
	max_stamina: int
	mana: int 
	max_mana: int

	level: int
	exp: int
	max_exp: int

	inventory: dict

	created_at: datetime
	updated_at: datetime

class RouterResponse(BaseModel):
	message: str
	data: CharacterRead