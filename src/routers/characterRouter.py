from fastapi import APIRouter, Depends, HTTPException, status

from src.services.characterService import CharacterService
from src.core.deps import get_character_service
from src.schemas.characterSchema import RouterResponse, CharacterCreate
from src.tools.jwt import get_current_user_id

from src.exceptions.mainExceptions import UserNotFinded

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