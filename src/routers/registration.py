from fastapi import APIRouter, Depends

from src.core.deps import get_registration_service, get_user_service
from src.schemas.userSchema import RouterResponse, UserCreate


from src.services.registration import Registration


router = APIRouter()

@router.post('/register', response_model=RouterResponse)
async def register(
	data: UserCreate,
	service: Registration = Depends(get_registration_service)
	):

	user = await service.register(data)

	return {
		"message": "User created succesfully",
		"data": user,
	}
