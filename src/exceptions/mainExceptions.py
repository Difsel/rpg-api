class DomainError(Exception):
	pass

class InvalidCredentialsError(DomainError):
	pass

class UserNotFinded(DomainError):
	pass