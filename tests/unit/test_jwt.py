from src.tools.jwt import create_access_token
from datetime import datetime
from types import SimpleNamespace

from src.services.authService import AuthService
from src.services.userService import UserService
from src.schemas.userSchema import UserCreate
from src.exceptions.mainExceptions import UserNotFinded

import pytest

@pytest.mark.asyncio
async def test_login(mocker):
	fake_db_user = SimpleNamespace(
		id=67,
		email="test@example.com",
		password="hashed_password_from_bd_loool",
		created_at=datetime.now()
	)

	fake_user_repo = mocker.AsyncMock()
	fake_user_repo.get_by_email.return_value = fake_db_user

	mocker.patch("src.services.authService.verify_password", return_value=True)

	service = AuthService(user_repo=fake_user_repo)
	data = UserCreate(email="test@example.com", password="12345678")

	result = await service.login(data=data)

	assert result.email == "test@example.com"
	fake_user_repo.get_by_email.assert_awaited_once_with("test@example.com")


async def test_getById(mocker):
	fake_user_repo = mocker.AsyncMock()
	fake_user_repo.get_by_id.return_value = SimpleNamespace(
		id=67,
		email="test@example.com",
		password="hashed_password_from_bd_loool",
		created_at=datetime.now()
	)

	service = UserService(fake_user_repo)
	fake_user = await service.get_user_by_id(67)

	assert fake_user.email == "test@example.com"

async def test_getById_error(mocker):
	fake_user_repo = mocker.AsyncMock()
	fake_user_repo.get_by_id.return_value = None

	service = UserService(fake_user_repo)

	with pytest.raises(UserNotFinded):
		await service.get_user_by_id(67)