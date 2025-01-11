from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User
from sqlalchemy import String, ForeignKey, Integer
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy.dialects.postgresql.json import JSON

from ..config.db import db


class Strategy(db.Model):
    __tablename__ = "strategies"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(30))
    description: Mapped[str] = mapped_column(String(300))
    asset_type: Mapped[str] = mapped_column(String(30))
    buy_conditions: Mapped[JSON] = mapped_column(JSON())
    sell_conditions: Mapped[JSON] = mapped_column(JSON())
    status: Mapped[str] = mapped_column(String(30))
    # relationships
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    user: Mapped["User"] = relationship("User", back_populates="strategies", lazy="selectin")

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "asset_type": self.asset_type,
            "buy_conditions": self.buy_conditions,
            "sell_conditions": self.sell_conditions,
            "status": self.status,
        }
