from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.character import Character

from src.core.database import Base
from src.models.timestamp import TimestampMixin

class User(TimestampMixin, Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
	password: Mapped[str] = mapped_column(String(255))

	characters: Mapped[list["Character"]] = relationship(
		back_populates="owner",
		cascade="all, delete-orphan",
	)