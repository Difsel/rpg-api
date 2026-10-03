from src.repositories.characterRepository import CharacterRepository
from sqlalchemy.exc import IntegrityError


from src.models.character import Character
from src.schemas.characterSchema import (
	CharacterCreate, CharacterRead, RecoveryRead, RecoveryCreate,
	ItemCreate, ItemRead, ExpCreate, ExpRead, UnequipCreate,
)

from src.tools import leveling
from src.items import get_item

from src.exceptions.mainExceptions import (
	ValueMustBePositiveError, TypeMustBeArmorError,
	CharacterNotFoundError, ItemNotInInventoryError,
	SlotIsEmptyError, InvalidSlotError, CharacterAlreadyExistsError
)

ARMOR_SLOT_TO_FIELD = {
	"helmet": "helmet_id",
	"chestplate": "chestplate_id",
	"legging": "legging_id",
	"boot": "boot_id",
}

class CharacterService:
	def __init__(self, characterRepository: CharacterRepository):
		self.characterRepository = characterRepository

	# ---------------------------- helpers ----------------------------------

	async def _get_character(self, owner_id: int) -> CharacterRead:
		character = await self.characterRepository.get_character_by_owner_id(owner_id)
		if character is None:
			raise CharacterNotFoundError(f"Character of user {owner_id} not found")
		return CharacterRead.model_validate(character)

	async def _get_character_locked(self, owner_id: int) -> Character:
		character = await self.characterRepository.get_character_for_update(owner_id)
		if character is None:
			raise CharacterNotFoundError(f"Character of user {owner_id} not found")
		return character

	@staticmethod
	def _check_positive(value: int, name: str):
		if value <= 0:
			raise ValueMustBePositiveError(f"{name} must be positive")

	async def _give_item(self, character_id: int, item_id: str):
		item = get_item(item_id)
		stack = await self.characterRepository.get_non_full_stack(
			character_id, item_id, item.max_stack
		)
		if stack:
			await self.characterRepository.add_quantity(character_id, stack.id, 1)
		else:
			await self.characterRepository.add_item_in_character(character_id, item_id)

	async def _take_item(self, character_id: int, item_id: str):
		stack = await self.characterRepository.get_one_item(character_id, item_id)
		if stack is None:
			raise ItemNotInInventoryError(f"Item {item_id} is not in inventory")
		if stack.quantity > 1:
			await self.characterRepository.remove_one_item_from_character(character_id, stack.id)
		else:
			await self.characterRepository.remove_all_stack_item_from_character(character_id, stack.id)

	# ---------------------------- character ----------------------------------

	async def create_character(self, owner_id: int, data: CharacterCreate) -> CharacterRead:
		existing = await self.characterRepository.get_character_by_owner_id(owner_id)
		if existing is not None:
			raise CharacterAlreadyExistsError("User already has a character")

		try:
			await self.characterRepository.create_character(owner_id, data.name)
			await self.characterRepository.commit()
		except IntegrityError:
			await self.characterRepository.rollback()
			raise CharacterAlreadyExistsError("User already has a character")

		return await self._get_character(owner_id)

	# ---------------------------- stats ----------------------------------

	async def heal_character(self, owner_id: int, data: RecoveryCreate) -> RecoveryRead:
		self._check_positive(data.recovery_value, "recovery_value")
		character = await self._get_character_locked(owner_id)

		old_health = character.health
		new_health = min(old_health + data.recovery_value, character.max_health)

		await self.characterRepository.update_stats(character.id, health=new_health)
		await self.characterRepository.commit()
		return RecoveryRead(old_recovery_value=old_health, new_recovery_value=new_health)

	async def recovery_mana_character(self, owner_id: int, data: RecoveryCreate) -> RecoveryRead:
		self._check_positive(data.recovery_value, "recovery_value")
		character = await self._get_character_locked(owner_id)

		old_mana = character.mana
		new_mana = min(old_mana + data.recovery_value, character.max_mana)

		await self.characterRepository.update_stats(character.id, mana=new_mana)
		await self.characterRepository.commit()
		return RecoveryRead(old_recovery_value=old_mana, new_recovery_value=new_mana)

	async def damage_character(self, owner_id: int, data: RecoveryCreate) -> RecoveryRead:
		self._check_positive(data.recovery_value, "recovery_value")
		character = await self._get_character_locked(owner_id)

		old_health = character.health
		new_health = max(0, old_health - data.recovery_value)

		await self.characterRepository.update_stats(character.id, health=new_health)
		await self.characterRepository.commit()
		return RecoveryRead(old_recovery_value=old_health, new_recovery_value=new_health)

	# ---------------------------- inventory ----------------------------------

	async def add_item_in_character(self, owner_id: int, data: ItemCreate) -> ItemRead:
		character = await self._get_character_locked(owner_id)
		item = get_item(data.item_id)

		stack = await self.characterRepository.get_non_full_stack(
			character.id, data.item_id, item.max_stack
		)

		if stack:
			quantity = await self.characterRepository.add_quantity(character.id, stack.id, 1)
		else:
			new_stack = await self.characterRepository.add_item_in_character(
				character.id, data.item_id
			)
			quantity = new_stack.quantity

		await self.characterRepository.commit()
		return ItemRead(**item.model_dump(), quantity=quantity)

	# ---------------------------- exp / level ----------------------------------

	async def add_exp_and_level_up_character(self, owner_id: int, data: ExpCreate) -> ExpRead:
		self._check_positive(data.exp_value, "exp_value")
		character = await self._get_character_locked(owner_id)

		old_level = character.level
		level = character.level
		exp = character.exp + data.exp_value
		max_exp = character.max_exp

		while exp >= max_exp and level < leveling.MAX_LEVEL:
			exp -= max_exp
			level += 1
			max_exp = leveling.calc_max_exp(level)

		if level >= leveling.MAX_LEVEL:
			exp = 0

		fields = {"level": level, "exp": exp, "max_exp": max_exp}

		if level > old_level:
			fields.update(
				max_health=leveling.calc_max_health(level),
				max_stamina=leveling.calc_max_stamina(level),
				max_mana=leveling.calc_max_mana(level),
			)

		await self.characterRepository.update_stats(character.id, **fields)
		await self.characterRepository.commit()

		return ExpRead(
			old_level=old_level,
			new_level=level,
			levels_gained=level - old_level,
			exp=exp,
			max_exp=max_exp,
		)

	# ---------------------------- equipment ----------------------------------

	async def equip_armor(self, owner_id: int, data: ItemCreate) -> CharacterRead:
		character = await self._get_character_locked(owner_id)
		armor = get_item(data.item_id)

		if armor.type != "armor":
			raise TypeMustBeArmorError(f"Item type is {armor.type}. Type must be 'armor'")

		field = ARMOR_SLOT_TO_FIELD.get(armor.slot)
		if field is None:
			raise InvalidSlotError(f"Unknown armor slot: {armor.slot}")

		old_item_id = getattr(character, field)  

		await self._take_item(character.id, data.item_id)    
		if old_item_id:
			await self._give_item(character.id, old_item_id)  
		await self.characterRepository.equip_equipment(character.id, **{field: data.item_id})

		await self.characterRepository.commit()
		return await self._get_character(owner_id)

	async def unequip_armor(self, owner_id: int, data: UnequipCreate) -> CharacterRead:
		character = await self._get_character_locked(owner_id)

		field = ARMOR_SLOT_TO_FIELD[data.slot]
		item_id = getattr(character, field)
		if item_id is None:
			raise SlotIsEmptyError(f"Slot '{data.slot}' is already empty")

		await self._give_item(character.id, item_id)
		await self.characterRepository.equip_equipment(character.id, **{field: None})

		await self.characterRepository.commit()
		return await self._get_character(owner_id)