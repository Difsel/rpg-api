from fastapi import APIRouter, Depends, HTTPException, status

from src.core.deps import get_auth_service
from src.schemas.userSchema import RouterResponse, UserCreate, LoginRouter_response

from src.services.authService import AuthService
from src.exceptions.mainExceptions import InvalidCredentialsError
from src.tools.jwt import create_access_token


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

@router.post('/login', response_model=LoginRouter_response)
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

	token = create_access_token(user.id)
	
	return {
		"message": "User sign in succesfully",
		"data": user,
		"token": token
	}