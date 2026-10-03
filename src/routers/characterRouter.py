from fastapi import APIRouter, Depends

from src.services.characterService import CharacterService
from core.dependencies.deps import get_character_service
from src.schemas.characterSchema import RouterResponse, CharacterCreate, ItemCreate, UnequipCreate
from src.tools.jwt import get_current_user_id

router = APIRouter()

@router.post("/character/create", response_model=RouterResponse)
async def add_character(
	data: CharacterCreate,
	owner_id: int = Depends(get_current_user_id),
	service: CharacterService = Depends(get_character_service)
):
	character = await service.create_character(owner_id, data)

	return {
		"message": "Character succesfully created!",
		"data": character
	}

@router.post("/character/equip/armor", response_model=RouterResponse)
async def equip_armor(
	data: ItemCreate,
	owner_id: int = Depends(get_current_user_id),
	service: CharacterService = Depends(get_character_service)
):
	character = await service.equip_armor(owner_id, data)

	return {
		"message": "Armor succesfully equipped!",
		"data": character
	}

@router.post("/character/unequip/armor", response_model=RouterResponse)
async def unequip_armor(
	data: UnequipCreate,
	owner_id: int = Depends(get_current_user_id),
	service: CharacterService = Depends(get_character_service)
):
	character = await service.unequip_armor(owner_id, data)

	return {
		"message": "Armor succesfully unequipped!",
		"data": character
	}