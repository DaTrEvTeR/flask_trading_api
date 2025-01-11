from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.models import Strategy

from app.config.db import db

from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    password: Mapped[str] = mapped_column(String(), nullable=False)
    username: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)

    strategies: Mapped[list["Strategy"]] = relationship("Strategy", back_populates="user", lazy="joined")
