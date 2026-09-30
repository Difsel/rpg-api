from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, DateTime, func, ForeignKey, UniqueConstraint

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

	# Equipment
	helmet_id: Mapped[str | None] = mapped_column(String(50), default=None)
	chestplate_id: Mapped[str | None] = mapped_column(String(50), default=None)
	legging_id: Mapped[str | None] = mapped_column(String(50), default=None)
	boot_id: Mapped[str | None] = mapped_column(String(50), default=None)
	main_hand_id: Mapped[str | None] = mapped_column(String(50), default=None)
	off_hand_id: Mapped[str | None] = mapped_column(String(50), default=None)
	usage_id: Mapped[str | None] = mapped_column(String(50), default=None)
	shell_id: Mapped[str | None] = mapped_column(String(50), default=None)

	# Health stats
	health: Mapped[int] = mapped_column(default=100)
	max_health: Mapped[int] = mapped_column(default=100)
	stamina: Mapped[int] = mapped_column(default=100)
	max_stamina: Mapped[int] = mapped_column(default=100)
	mana: Mapped[int] = mapped_column(default=100)
	max_mana: Mapped[int] = mapped_column(default=100)

	# Progression
	level: Mapped[int] = mapped_column(default=1)
	exp: Mapped[int] = mapped_column(default=0)
	max_exp: Mapped[int] = mapped_column(default=300)

	owner: Mapped["User"] = relationship(back_populates="characters")

	items: Mapped[list["InventoryItem"]] = relationship(
		back_populates="character",
		cascade="all, delete-orphan",
	)

	created_at: Mapped[datetime] = mapped_column(
		DateTime,
		server_default=func.now(),
	)
	updated_at: Mapped[datetime] = mapped_column(
		DateTime,
		server_default=func.now(),
		onupdate=func.now()
	)

class InventoryItem(Base):
	__tablename__ = "inventory_items"
	__table_args__ = (
		UniqueConstraint("character_id", "item_id", name="uq_character_item"),
	)

	id: Mapped[int] = mapped_column(primary_key=True)
	character_id: Mapped[int] = mapped_column(
		ForeignKey("characters.id", ondelete="CASCADE"),
		index=True
	)
	item_id: Mapped[str] = mapped_column(String(50))
	quantity: Mapped[int] = mapped_column(default=1)

	character: Mapped["Character"] = relationship(back_populates="items")