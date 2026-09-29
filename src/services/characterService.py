from src.repositories.characterRepository import CharacterRepository

from src.schemas.characterSchema import CharacterCreate, CharacterRead

class CharacterService:
	def __init__(self, characterRepository: CharacterRepository):
		self.characterRepository = characterRepository

	async def create_character(self, owner_id: int, data: CharacterCreate) -> CharacterRead:
		character = await self.characterRepository.create_character(owner_id, data.name)

		return CharacterRead.model_validate(character)