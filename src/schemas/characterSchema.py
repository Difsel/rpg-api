from pydantic import BaseModel, ConfigDict, field_validator, Field
from datetime import datetime
from typing import Literal

class InventoryItemRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    item_id: str
    quantity: int

class CharacterCreate(BaseModel):
	name: str

class CharacterRead(BaseModel):
	model_config = ConfigDict(from_attributes=True)

	id: int
	owner_id: int
	name: str

	helmet_id: str | None = None
	chestplate_id: str | None = None
	legging_id: str | None = None
	boot_id: str | None = None
	main_hand_id: str | None = None
	off_hand_id: str | None = None
	usage_id: str | None = None
	shell_id: str | None = None

	health: int
	max_health: int
	stamina: int
	max_stamina: int
	mana: int 
	max_mana: int

	level: int
	exp: int
	max_exp: int

	items: list[InventoryItemRead]

	created_at: datetime
	updated_at: datetime

class RouterResponse(BaseModel):
	message: str
	data: CharacterRead

class RecoveryCreate(BaseModel):
	recovery_value: int

class RecoveryRead(BaseModel):
	old_recovery_value: int
	new_recovery_value: int

class ItemCreate(BaseModel):
	item_id: str

# Without linked SQL
class ItemInfo(BaseModel):
	item_id: str
	name: str
	type: str
	description: str
	max_stack: int

	# Armor
	slot: str | None = None
	defense: int | None = None

	# Weapon
	damage: int | None = None
	two_hands: bool | None = None
	shell_type: str | None = None

	# Consumables
	recovery_type: str | None = None
	recovery_value: int | None = None

class ItemRead(ItemInfo):
	quantity: int

class UnequipCreate(BaseModel):
	slot: Literal["helmet", "chestplate", "legging", "boot"]

class ExpCreate(BaseModel):
	exp_value: int

class ExpRead(BaseModel):
	old_level: int
	new_level: int
	levels_gained: int
	exp: int
	max_exp: int