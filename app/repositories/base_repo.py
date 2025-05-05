
from abc import ABC
from typing import TypeVar, Generic, Optional, TYPE_CHECKING, List, Any
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from collections.abc import AsyncGenerator
from sqlalchemy import BigInteger, String, TIMESTAMP, func, select, and_
from advanced_alchemy.base import UUIDAuditBase
from advanced_alchemy.repository import ModelT



class BaseRepository(SQLAlchemyAsyncRepository[ModelT], Generic[ModelT]):
    """Базовый асинхронный репозиторий с общими CRUD-методами.

    Наследуется от SQLAlchemyAsyncRepository и предоставляет дополнительные методы
    для работы с моделями по указанным полям.

    Args:
        ModelT: Дженерик-тип модели SQLAlchemy.
    """

    async def get_by_field(
        self, 
        field_name: str, 
        value: Any
    ) -> ModelT | None:
        """Получить запись по значению указанного поля.

        Args:
            field_name: Название поля для фильтрации.
            value: Значение поля для поиска.

        Returns:
            Экземпляр модели или None, если запись не найдена.

        Examples:
            >>> repo = BaseRepository(User)
            >>> user = await repo.get_by_field("email", "test@example.com")
        """
        return await self.get_one_or_none(**{field_name: value})

    async def exists_by_field(
        self, 
        field_name: str, 
        value: Any
    ) -> bool:
        """Проверить существование записи с указанным значением поля.

        Args:
            field_name: Название поля для проверки.
            value: Значение поля.

        Returns:
            bool: True если запись существует, иначе False.

        Examples:
            >>> repo = BaseRepository(User)
            >>> exists = await repo.exists_by_field("username", "john_doe")
        """
        return await self.count(**{field_name: value}) > 0

