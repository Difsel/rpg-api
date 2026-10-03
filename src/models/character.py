from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.user import User
    from src.models.inventory import InventoryItem

from src.core.database import Base
from src.models.timestamp import TimestampMixin

class Character(TimestampMixin, Base):
	__tablename__ = "characters"

	id: Mapped[int] = mapped_column(primary_key=True)
	owner_id: Mapped[int] = mapped_column(
		ForeignKey("users.id", ondelete="CASCADE"),
		index=True,
		unique=True
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