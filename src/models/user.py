from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func
from datetime import datetime

from src.core.database import Base

class User(Base):
	__tablename__ = "users"

	id: Mapped[int] = mapped_column(primary_key=True)
	email: Mapped[str] = mapped_column(String(50), unique=True)
	password: Mapped[str] = mapped_column(String(255))

	created_at: Mapped[datetime] = mapped_column(
		DateTime,
		server_default=func.now(),
	)