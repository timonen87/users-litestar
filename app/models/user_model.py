from advanced_alchemy.base import  BigIntAuditBase,  BigIntBase
from advanced_alchemy.types import GUID

from sqlalchemy import String, func, BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime


class User(BigIntBase):
    """Модель пользователя в базе данных."""

    __tablename__ = "user"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50))
    surname: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now()
    )