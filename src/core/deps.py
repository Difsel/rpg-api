from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from src.core.database import SessionFactory

# Repositories
from src.repositories.userRepository import UserRepository
from src.repositories.characterRepository import CharacterRepository

#Services
from src.services.authService import AuthService
from src.services.userService import UserService
from src.services.characterService import CharacterService

#create Session
async def get_session() -> AsyncGenerator[AsyncSession, None]:
	async with SessionFactory() as session:
		yield session
# ----------

# ------------------- REPOSITORY SESSION RETURN ------------------------
async def get_user_repository(
		session: AsyncSession = Depends(get_session)
) -> UserRepository:
	return UserRepository(session)

async def get_character_repository(
		session: AsyncSession = Depends(get_session)
) -> CharacterRepository:
	return CharacterRepository(session)


# --------------------------------

# -------------------------------- SERVICE RETURNING WITH REPOSIROTY --------------------

async def get_auth_service(
		repo: UserRepository = Depends(get_user_repository)
) -> AuthService:
	return AuthService(repo)	

async def get_user_service(
		repo: UserRepository = Depends(get_user_repository)
) -> UserService:
	return UserService(repo)	

async def get_character_service(
		repo: CharacterRepository = Depends(get_character_repository)
) -> CharacterService:
	return CharacterService(repo)