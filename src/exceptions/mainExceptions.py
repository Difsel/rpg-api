class DomainError(Exception):
	pass

class NotFoundError(DomainError):
	pass

class InvalidCredentialsError(DomainError):
	def __init__(self, message: str = "Invalid email or password"):
		super().__init__(message)

class UserNotFinded(NotFoundError):
	pass

class ItemNotFoundedError(NotFoundError):
	pass

class CharacterNotFoundError(NotFoundError):
	pass

class ItemNotInInventoryError(NotFoundError):
	pass

class ValueMustBePositiveError(DomainError):
	pass

class TypeMustBeArmorError(DomainError):
	pass

class SlotIsEmptyError(DomainError):
	pass

class InvalidSlotError(DomainError):
	pass

class CharacterAlreadyExistsError(DomainError):
	pass