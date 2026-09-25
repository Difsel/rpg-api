from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.core.database import SessionFactory

# Repositories
from src.repositories.userRepository import UserRepository

#Services
from src.services.authService import AuthService
from src.services.userService import UserService

#create Session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
	async with SessionFactory() as session:
		yield session
# ----------

# return USER repository with session
async def get_user_repository(
		session: AsyncSession = Depends(get_session)
) -> UserRepository:
	return UserRepository(session)

# Return auth service with repo
async def get_auth_service(
		repo: UserRepository = Depends(get_user_repository)
) -> AuthService:
	return AuthService(repo)	

# Return user service with repo
async def get_user_service(
		repo: UserRepository = Depends(get_user_repository)
) -> UserService:
	return UserService(repo)	