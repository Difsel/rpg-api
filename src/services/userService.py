from src.repositories.userRepository import UserRepository

from src.schemas.userSchema import UserResponse
from src.exceptions.mainExceptions import UserNotFinded

class UserService:
	def __init__(self, userRepo: UserRepository):
		self.userRepo = userRepo

	async def get_user_by_id(self, id: int) -> UserResponse:
		user = await self.userRepo.get_by_id(id)

		if not user:
			raise UserNotFinded()
			
		return UserResponse.model_validate(user)