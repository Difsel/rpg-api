from src.repositories.userRepository import UserRepository

from src.schemas.userSchema import UserResponse

class UserService:
	def __init__(self, userRepo: UserRepository):
		self.userRepo = userRepo

	async def get_user_by_id(self, id: int) -> UserResponse | None:
		user = await self.userRepo.get_by_id(id)

		if user is None:
			return None
			
		return UserResponse.model_validate(user)