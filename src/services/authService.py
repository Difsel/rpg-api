from src.schemas.userSchema import UserCreate, UserResponse

from src.repositories.userRepository import UserRepository
from src.tools.pass_hash import hash_password, verify_password

from src.exceptions.mainExceptions import InvalidCredentialsError

class AuthService:
	def __init__(self, user_repo: UserRepository):
		self.user_repo = user_repo

	async def register(self, data: UserCreate) -> UserResponse:
		pass_hash = hash_password(data.password)
		user = await self.user_repo.create(data.email, pass_hash)

		return UserResponse.model_validate(user)

	async def login(self, data: UserCreate) -> UserResponse:

		isUser = await self.user_repo.get_by_email(data.email)
		if not isUser:
			raise InvalidCredentialsError() 
		
		verify_pass = verify_password(data.password, isUser.password)
		if not verify_pass:
			raise InvalidCredentialsError()

		return UserResponse.model_validate(isUser)