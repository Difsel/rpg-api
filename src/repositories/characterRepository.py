from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from src.models.user import Character

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

	async def change_health(self, character_id: int, health_value: int):
		command = update(Character).where(character_id == Character.id).values(health=health_value)
		await self.session.execute(command)
		await self.session.commit()
		return True

	async def change_stamina(self, character_id: int, stamina_value: int):
		command = update(Character).where(character_id == Character.id).values(stamina=stamina_value)
		await self.session.execute(command)
		await self.session.commit()
		return True

	async def change_mana(self, character_id: int, mana_value: int):
		command = update(Character).where(character_id == Character.id).values(mana=mana_value)
		await self.session.execute(command)
		await self.session.commit()
		return True

	async def change_level(self, character_id: int, level_value: int):
		command = update(Character).where(character_id == Character.id).values(level=level_value)
		await self.session.execute(command)
		await self.session.commit()
		return True
	
	async def change_exp(self, character_id: int, exp_value: int):
		command = update(Character).where(character_id == Character.id).values(exp=exp_value)
		await self.session.execute(command)
		await self.session.commit()
		return True

  # ---------------- Max stats ------------------

	async def change_max_health(self, character_id: int, max_health_value: int):
		command = update(Character).where(character_id == Character.id).values(max_health=max_health_value)
		await self.session.execute(command)
		await self.session.commit()
		return True

	async def change_max_stamina(self, character_id: int, max_stamina_value: int):
		command = update(Character).where(character_id == Character.id).values(max_stamina=max_stamina_value)
		await self.session.execute(command)
		await self.session.commit()
		return True

	async def change_max_mana(self, character_id: int, max_mana_value: int):
		command = update(Character).where(character_id == Character.id).values(max_mana=max_mana_value)
		await self.session.execute(command)
		await self.session.commit()
		return True
	
	async def change_max_exp(self, character_id: int, max_exp_value: int):
		command = update(Character).where(character_id == Character.id).values(max_exp=max_exp_value)
		await self.session.execute(command)
		await self.session.commit()
		return True

	# ---------------------------- Inventory ----------------------------------

	async def add_item_in_inventory(self):
		# TODO Реализация добавления предмета
		raise NotImplementedError

	async def remove_item_from_inventory(self):
		# TODO Реализация удаление предмета из инвентаря
		raise NotImplementedError

	async def change_item_from_inventory(self):
		# TODO Реализация изменения значения предмета из инвентаря
		raise NotImplementedError