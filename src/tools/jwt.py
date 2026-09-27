from src.core.config import settings
from datetime import datetime, timezone, timedelta

import jwt

def create_access_token(user_id: int) -> str:
	expire = datetime.now(timezone.utc) + timedelta(minutes=settings.jwt_expire_min)
	                      
	payload = {
		"sub": str(user_id),
		"exp": expire,
	}

	token = jwt.encode(
		payload,
		settings.jwt_secret,
		algorithm=settings.jwt_algorithm
	)

	return token

def decode_token(token: str) -> int | None:
	try:
		payload = jwt.decode(
			token,
			settings.jwt_secret,
			algorithms=[settings.jwt_algorithm]
		)

		user_id = payload.get("sub")

		if not user_id:
			return None

		return int(user_id)
	
	except jwt.PyJWTError:
		return None

# -----------------------

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

bearer_scheme = HTTPBearer()

def get_current_user_id(
		credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)
) -> int:
	token = credentials.credentials
	user_id = decode_token(token)

	if user_id is None:
		raise HTTPException(
			status_code=status.HTTP_401_UNAUTHORIZED,
			detail="Invalid token or expired token",
			headers={"WWW-Authenticate": "Bearer"}
		)

	return user_id