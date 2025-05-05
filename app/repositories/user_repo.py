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
        """Получает список пользователей с пагинацией.
        
        Возвращает кортеж из списка пользователей на указанной странице и общего количества пользователей.
        Сортировка по дате создания (новые сначала).

        Args:
            page (int, optional): Номер страницы (начинается с 1). По умолчанию 1.
            page_size (int, optional): Количество пользователей на странице. По умолчанию 100.

        Returns:
            tuple[list[User], int]: Кортеж из:
                - Список пользователей на текущей странице.
                - Общее количество пользователей (для расчета общего числа страниц).

        """
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