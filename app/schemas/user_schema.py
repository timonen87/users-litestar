
from datetime import datetime
from typing import Optional
from litestar.dto import MsgspecDTO, DTOConfig
import msgspec


class UserCreate(msgspec.Struct):
    """Схема для создания пользователя."""
    name: str
    surname: str
    password: str


class UserUpdate(msgspec.Struct):
    """Схема для обновления пользователя."""
    name: Optional[str] = None
    surname: Optional[str] = None
    password: Optional[str] = None


class UserOut(msgspec.Struct):
    """Схема для вывода данных пользователя."""
    id: int
    name: str
    surname: str
    created_at: datetime
    updated_at: datetime


class UserCreateDTO(MsgspecDTO[UserCreate]):
    """DTO для создания пользователя."""
    config = DTOConfig(
        # exclude={"password"},
        # max_nested_depth=1
    )


class UserOutDTO(MsgspecDTO[UserOut]):
    """DTO для вывода пользователя."""
    config = DTOConfig()