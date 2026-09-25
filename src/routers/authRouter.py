from fastapi import APIRouter, Depends, HTTPException, status

from src.core.deps import get_auth_service
from src.schemas.userSchema import RouterResponse, UserCreate

from src.services.authService import AuthService
from src.exceptions.mainExceptions import InvalidCredentialsError


router = APIRouter()

@router.post('/register', response_model=RouterResponse)
async def register(
	data: UserCreate,
	service: AuthService = Depends(get_auth_service)
	):

	user = await service.register(data)

	return {
		"message": "User created succesfully",
		"data": user,
	}

@router.post('/login', response_model=RouterResponse)
async def login(
	data: UserCreate,
	service: AuthService = Depends(get_auth_service)
):
	try:
		user = await service.login(data)
	except InvalidCredentialsError:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid email or password"
		)

	return {
		"message": "User sign in succesfully",
		"data": user,
	}