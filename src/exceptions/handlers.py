from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.exceptions.mainExceptions import (
	DomainError, NotFoundError, InvalidCredentialsError,
	ValueMustBePositiveError, TypeMustBeArmorError, CharacterAlreadyExistsError
)

EXCEPTION_STATUS = {
	TypeMustBeArmorError: 422,
	ValueMustBePositiveError: 422, 
	CharacterAlreadyExistsError: 409,
	NotFoundError: 404,
	InvalidCredentialsError: 401,
	DomainError: 400,
}

def _make_handler(status_code: int):
	async def handler(request: Request, exc: Exception):
		return JSONResponse(status_code=status_code, content={"detail": str(exc)})
	return handler

def register_exception_handlers(app: FastAPI):
	for exc_class, status_code in EXCEPTION_STATUS.items():
		app.add_exception_handler(exc_class, _make_handler(status_code))