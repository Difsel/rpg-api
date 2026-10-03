from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from sqlalchemy.orm import selectinload

from src.models.character import Character
from src.models.inventory import InventoryItem

ALLOWED_FIELDS = {
	"health", "stamina", "mana", "level", "exp",
	"max_health", "max_stamina", "max_mana", "max_exp",
}

ALLOWED_SLOTS = {
	"helmet_id", "chestplate_id", "legging_id", "boot_id",
	"main_hand_id", "off_hand_id",
	"usage_id",
	"shell_id",
}

class CharacterRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	# ---------------------------- Transaction ----------------------------------

	async def commit(self):
		await self.session.commit()

	async def rollback(self):
		await self.session.rollback()

	# ---------------------------- Character ----------------------------------

	async def create_character(self, owner_id: int, name: str) -> Character:
		character = Character(owner_id=owner_id, name=name)
		self.session.add(character)
		await self.session.flush()
		return character

	async def _update(self, character_id: int, **fields) -> bool:
		await self.session.execute(
			update(Character).where(Character.id == character_id).values(**fields)
		)
		return True

	async def get_character_by_owner_id(self, owner_id: int):
		command = (
			select(Character)
			.where(Character.owner_id == owner_id)
			.options(selectinload(Character.items))
			.execution_options(populate_existing=True)
		)
		result = await self.session.execute(command)
		return result.scalar_one_or_none()

	async def get_character_for_update(self, owner_id: int):
		command = (
			select(Character)
			.where(Character.owner_id == owner_id)
			.options(selectinload(Character.items))
			.with_for_update(of=Character)
			.execution_options(populate_existing=True)
		)
		result = await self.session.execute(command)
		return result.scalar_one_or_none()

	async def get_character_by_character_id(self, character_id: int):
		command = select(Character).where(Character.id == character_id)
		result = await self.session.execute(command)
		return result.scalar_one_or_none()

	# ------------------ change stats -----------------------

	async def update_stats(self, character_id: int, **fields) -> bool:
		if not fields.keys() <= ALLOWED_FIELDS:
			raise ValueError(f"Unknown fields: {fields.keys() - ALLOWED_FIELDS}")
		return await self._update(character_id, **fields)

	# ---------------------------- Equipment ----------------------------------

	async def equip_equipment(self, character_id: int, **fields) -> bool:
		if not fields.keys() <= ALLOWED_SLOTS:
			raise ValueError(f"Unknown slots: {fields.keys() - ALLOWED_SLOTS}")
		return await self._update(character_id, **fields)

	# ---------------------------- Inventory ----------------------------------

	async def add_item_in_character(self, character_id: int, item_id: str) -> InventoryItem:
		item = InventoryItem(item_id=item_id, character_id=character_id)
		self.session.add(item)
		await self.session.flush()
		await self.session.refresh(item)
		return item

	async def get_all_items(self, character_id: int) -> list[InventoryItem]:
		command = select(InventoryItem).where(InventoryItem.character_id == character_id)
		result = await self.session.execute(command)
		return list(result.scalars().all())

	async def get_non_full_stack(self, character_id: int, item_id: str, max_stack: int):
		command = (
			select(InventoryItem)
			.where(
				InventoryItem.character_id == character_id,
				InventoryItem.item_id == item_id,
				InventoryItem.quantity < max_stack,
			)
			.order_by(InventoryItem.quantity.desc())
			.limit(1)
			.with_for_update()
		)
		result = await self.session.execute(command)
		return result.scalar_one_or_none()

	async def get_one_item(self, character_id: int, item_id: str):
		command = (
			select(InventoryItem)
			.where(
				InventoryItem.character_id == character_id,
				InventoryItem.item_id == item_id,
			)
			.order_by(InventoryItem.id)
			.limit(1)
		)
		result = await self.session.execute(command)
		return result.scalar_one_or_none()

	async def remove_one_item_from_character(self, character_id: int, id: int) -> bool:
		command = (
			update(InventoryItem)
			.where(
				InventoryItem.id == id,
				InventoryItem.character_id == character_id,
			)
			.values(quantity=InventoryItem.quantity - 1)
		)
		result = await self.session.execute(command)
		return result.rowcount > 0

	async def remove_all_stack_item_from_character(self, character_id: int, id: int) -> bool:
		command = delete(InventoryItem).where(
			InventoryItem.id == id,
			InventoryItem.character_id == character_id,
		)
		result = await self.session.execute(command)
		return result.rowcount > 0

	async def add_quantity(self, character_id: int, id: int, quantity: int):
		command = (
			update(InventoryItem)
			.where(
				InventoryItem.character_id == character_id,
				InventoryItem.id == id,
			)
			.values(quantity=InventoryItem.quantity + quantity)
			.returning(InventoryItem.quantity)
		)
		result = await self.session.execute(command)
		return result.scalar_one_or_none()