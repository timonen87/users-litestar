from typing import Generic, TypeVar
from litestar.plugins.sqlalchemy import repository
from app.models.user_model import User
from app.repositories.base_repo import BaseRepository
from sqlalchemy import func, select



class UserRepository(BaseRepository[User]):
    """Специализированный репозиторий для работы с пользователями"""

    model_type = User
    id_type = int


    async def list_paginated(
        self,
        page: int = 1,
        page_size: int = 100,
    ) -> tuple[list[User], int]:
        """Получение пользователей с пагинацией"""
        
        # Базовый запрос
        stmt = select(User).order_by(User.created_at.desc())
        
        # Пагинация
        paginated_stmt = (
            stmt
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
        
        # Получение результатов
        result = await self.session.execute(paginated_stmt)
        users = result.scalars().all()
        
        # Получение общего количества
        count_result = await self.session.execute(select(func.count()).select_from(stmt))
        total = count_result.scalar_one()
        
        return users, total

