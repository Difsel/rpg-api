from src.schemas.userSchema import UserCreate, UserResponse

from src.repositories.userRepository import UserRepository
from src.tools.pass_hash import hash_password

class Registration:
	def __init__(self, user_repo: UserRepository):
		self.user_repo = user_repo

	async def register(self, data: UserCreate) -> UserResponse:
		pass_hash = hash_password(data.password)
		user = await self.user_repo.create(data.email, pass_hash)

		return UserResponse.model_validate(user)