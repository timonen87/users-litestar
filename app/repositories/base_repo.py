
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
    """Базовый репозиторий с общими методами CRUD"""

    async def get_by_field(
        self, 
        field_name: str, 
        value: Any
    ) -> ModelT | None:
        """Получить запись по значению поля"""
        return await self.get_one_or_none(**{field_name: value})

    async def exists_by_field(
        self, 
        field_name: str, 
        value: Any
    ) -> bool:
        """Проверить существование записи по полю"""
        return await self.count(**{field_name: value}) > 0

    async def update_by_field(
        self,
        field_name: str,
        field_value: Any,
        update_data: dict[str, Any]
    ) -> ModelT:
        """Обновить запись по значению поля"""
        obj = await self.get_one(**{field_name: field_value})
        return await self.update(obj, update_data)