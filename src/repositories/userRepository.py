from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.user import User

class UserRepository:
	def __init__(self, session: AsyncSession):
		self.session = session

	async def get_by_id(self, user_id: int) -> User | None:
		command = select(User).where(User.id == user_id)
		result = await self.session.execute(command)
		user = result.scalar_one_or_none()
		return user

	async def get_by_email(self, user_email: str) -> User | None:
		command = select(User).where(User.email == user_email)
		result = await self.session.execute(command)
		user = result.scalar_one_or_none()
		return user

	async def create(self, user_email: str, hash_password: str) -> User:
		user = User(
			email = user_email,
			password = hash_password
		)
		self.session.add(user)
		await self.session.commit()
		await self.session.refresh(user)
		return user