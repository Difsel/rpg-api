from fastapi import APIRouter, Depends, HTTPException, status

from src.services.userService import UserService
from src.core.deps import get_user_service
from src.schemas.userSchema import RouterResponse

from src.exceptions.mainExceptions import UserNotFinded

router = APIRouter()

@router.get("/user/{user_id}", response_model=RouterResponse)
async def get_user_by_id(
	user_id: int,
	service: UserService = Depends(get_user_service)
):
	try:
		user = await service.get_user_by_id(user_id)
	except UserNotFinded:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail=f"User with [id:{user_id}] not finded or not exists"
		)
	
	return {
		"message": "User succesfull finded!",
		"data": user
	}