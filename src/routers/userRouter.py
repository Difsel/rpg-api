from fastapi import APIRouter, Depends, HTTPException, status

from src.services.userService import UserService
from src.core.deps import get_user_service
from src.schemas.userSchema import RouterResponse
from src.tools.jwt import get_current_user_id

from src.exceptions.mainExceptions import UserNotFinded

router = APIRouter()

@router.get("/me", response_model=RouterResponse)
async def get_user(
	user_id: int = Depends(get_current_user_id),
	service: UserService = Depends(get_user_service)
):
	user = await service.get_user_by_id(user_id)
	return {
		"message": "Succesfull",
		"data": user
	}

@router.get("/user/{user_id}", response_model=RouterResponse)
async def get_user_by_id(
	user_id: int,
	service: UserService = Depends(get_user_service)
):
	user = await service.get_user_by_id(user_id)
	
	return {
		"message": "User succesfull finded!",
		"data": user
	}