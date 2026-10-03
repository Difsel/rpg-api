from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.models.character import Character

from src.core.database import Base
from src.models.timestamp import TimestampMixin

class InventoryItem(TimestampMixin, Base):
	__tablename__ = "inventory_items"

	id: Mapped[int] = mapped_column(primary_key=True)
	character_id: Mapped[int] = mapped_column(
		ForeignKey("characters.id", ondelete="CASCADE"),
		index=True
	)
	item_id: Mapped[str] = mapped_column(String(50))
	quantity: Mapped[int] = mapped_column(default=1)

	character: Mapped["Character"] = relationship(back_populates="items")