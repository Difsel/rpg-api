from fastapi import APIRouter, Depends, HTTPException, status

from src.services.userService import UserService
from src.core.deps import get_user_service
from src.schemas.userSchema import RouterResponse

router = APIRouter()

@router.get("/user/{user_id}", response_model=RouterResponse)
async def get_user_by_id(
	user_id: int,
	service: UserService = Depends(get_user_service)
):
	user = await service.get_user_by_id(user_id)

	if user is None:
		raise HTTPException(
			status_code=status.HTTP_404_NOT_FOUND,
			detail="User not found"
		)
	
	return {
		"message": "User succesfull finded!",
		"data": user
	}