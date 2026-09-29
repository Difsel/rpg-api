from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, Integer, ForeignKey
from sqlalchemy.types import JSON
from sqlalchemy.ext.mutable import MutableDict

from datetime import datetime

from src.core.database import Base

class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
	password: Mapped[str] = mapped_column(String(255))

	characters: Mapped[list["Character"]] = relationship(
		back_populates="owner",
		cascade="all, delete-orphan",
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime,
		server_default=func.now(),
	)


class Character(Base):
	__tablename__ = "characters"

	id: Mapped[int] = mapped_column(primary_key=True)
	owner_id: Mapped[int] = mapped_column(
		ForeignKey("users.id", ondelete="CASCADE"),
		index=True
	)

	# Biography
	name: Mapped[str] = mapped_column(String(50))

	# health stats
	health: Mapped[int] = mapped_column(default=100)
	max_health: Mapped[int] = mapped_column(default=100)
	stamina: Mapped[int] = mapped_column(default=100)
	max_stamina: Mapped[int] = mapped_column(default=100)
	mana: Mapped[int] = mapped_column(default=100)
	max_mana: Mapped[int] = mapped_column(default=100)

	# Inventory
	inventory: Mapped[dict] = mapped_column(
		MutableDict.as_mutable(JSON),
		default=dict
	)

	# Progression
	level: Mapped[int] = mapped_column(default=1)
	exp: Mapped[int] = mapped_column(default=0)
	max_exp: Mapped[int] = mapped_column(default=300)

	owner: Mapped["User"] = relationship(back_populates="characters")

	created_at: Mapped[datetime] = mapped_column(
		DateTime,
		server_default=func.now(),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime,
		server_default=func.now(),
		onupdate=func.now()
	)