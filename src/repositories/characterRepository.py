from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete

from src.models.user import Character, InventoryItem

ALLOWED_FIELDS = {
    "health", "stamina", "mana", "level", "exp",
    "max_health", "max_stamina", "max_mana", "max_exp",
}

ALLOWED_SLOTS = {
    "helmet_id", "chestplate_id", "legging_id", "boot_id",
    "main_hand_id", "off_hand_id",
    "usage_id",
  	"shell_id"
}

class CharacterRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def create_character(self, owner_id: int, name: str):
		character = Character(
			owner_id = owner_id,
			name = name,
		)
		self.session.add(character)
		await self.session.commit()
		await self.session.refresh(character)
		return character

	async def _update(self, character_id: int, **fields):	
		await self.session.execute(
				update(Character).where(Character.id == character_id).values(**fields)
		)
		await self.session.commit()

	async def get_by_owner_id(self, owner_id: int):
		command = select(Character).where(owner_id == Character.owner_id)
		execute = await self.session.execute(command)
		result = execute.scalar_one_or_none()
		return result

	async def get_by_character_id(self, character_id: int):
		command = select(Character).where(character_id == Character.id)
		execute = await self.session.execute(command)
		result = execute.scalar_one_or_none()
		return result

	# ------------------change stats-----------------------
	
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

	async def create_item(self, character_id: int, item_id: str):
		item = InventoryItem(
			item_id=item_id,
			character_id=character_id
		)
		self.session.add(item)
		await self.session.commit()
		await self.session.refresh(item)
		return item

	async def get_all_items(self, character_id: int) -> list[InventoryItem]:
		command = select(InventoryItem).where(InventoryItem.character_id == character_id)
		result = await self.session.execute(command)
		return list(result.scalars().all())

	async def remove_item(self, character_id: int, item_id: str):
		command = delete(InventoryItem).where(
			item_id == InventoryItem.item_id,
			character_id == InventoryItem.character_id
		)
		result = await self.session.execute(command)
		await self.session.commit()
		return result.rowcount > 0

	async def add_quantity(self, character_id: int, item_id: str, quantity: int):
		command = (
			update(InventoryItem)
			.where(
				InventoryItem.character_id == character_id,
				InventoryItem.item_id == item_id
			)
			.values(quantity=InventoryItem.quantity + quantity)
		)
		result = await self.session.execute(command)
		await self.session.commit()
		return result.rowcount > 0