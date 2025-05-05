from typing import Any
from litestar.exceptions import NotFoundException, ValidationException
from app.repositories.user_repo import UserRepository
from app.models.user_model import User
from sqlalchemy import select
from advanced_alchemy.repository import SQLAlchemyAsyncRepository
from sqlalchemy.ext.asyncio import AsyncSession
from litestar.pagination import OffsetPagination
from litestar.dto import DTOData
from app.schemas.user_schema import UserCreate, UserUpdate, UserOut
from app.services.security import hash_password
import msgspec

class UserService:
    """Сервис для работы с пользователями.
    
    Предоставляет методы для CRUD-операций с пользователями, включая пагинацию.
    """
    
    def __init__(self, session: AsyncSession):
        """Инициализация сервиса.
        
        Args:
            session: Асинхронная сессия SQLAlchemy для работы с БД.
        """
        self.session = session
        self.user_repository = UserRepository(session=session)

    async def create_user(self, data: UserCreate) -> UserOut:
        """Создает нового пользователя с хешированием пароля.
        
        Args:
            data: Данные для создания пользователя (Pydantic-схема UserCreate).
            
        Returns:
            UserOut: Схема с данными созданного пользователя.
            
        Raises:
            ValueError: Если данные не прошли валидацию.
            SQLAlchemyError: При ошибках работы с БД.
        """
        user_data = data.as_builtins()  # Преобразуем в dict
        user = await self.user_repository.add(
            self.user_repository.model_type(
                name=user_data["name"],
                surname=user_data["surname"],
                password=hash_password(user_data["password"])
            )
        )
        await self.user_repository.session.commit()
        return UserOut(
            id=int(user.id),
            name=user.name,
            surname=user.surname,
            created_at=user.created_at,
            updated_at=user.updated_at
        )

    async def get_user(self, user_id: int) -> UserOut:
        """Получает пользователя по ID.
        
        Args:
            user_id: Идентификатор пользователя.
            
        Returns:
            UserOut: Схема с данными пользователя.
            
        Raises:
            NotFoundException: Если пользователь не найден.
        """
        user = await self.user_repository.get(user_id)
        if not user:
            raise NotFoundException("User not found")
        return UserOut(
            id=int(user.id),
            name=user.name,
            surname=user.surname,
            created_at=user.created_at,
            updated_at=user.updated_at
        )
    
    async def get_list(
        self,
        page: int = 1,
        page_size: int = 100
    ) -> OffsetPagination[UserOut]:
        """Получает список пользователей с пагинацией.
        
        Args:
            page: Номер страницы (начиная с 1). Default: 1.
            page_size: Количество элементов на странице. Default: 100.
            
        Returns:
            OffsetPagination[UserOut]: Объект пагинации с пользователями.
        """
        users, total = await self.user_repository.list_paginated(page, page_size)
        return OffsetPagination(
            items=[UserOut(
                id=int(user.id),
                name=user.name,
                surname=user.surname,
                created_at=user.created_at,
                updated_at=user.updated_at
            ) for user in users],
            total=total,
            limit=page_size,
            offset=(page - 1) * page_size
        )

    async def update_user(self, user_id: int, update_data: UserUpdate) -> UserOut:
        """Обновляет данные пользователя.
        
        Args:
            user_id: Идентификатор пользователя.
            update_data: Данные для обновления (Pydantic-схема UserUpdate).
            
        Returns:
            UserOut: Схема с обновленными данными пользователя.
            
        Raises:
            NotFoundException: Если пользователь не найден.
            ValueError: Если данные не прошли валидацию.
        """
        user = await self.user_repository.get(user_id)
        if not user:
            raise NotFoundException("User not found")
            
        for field, value in msgspec.structs.asdict(update_data).items():
            if field == "password" and value:
                value = hash_password(value)
            setattr(user, field, value)

        updated_user = await self.user_repository.update(user)
        await self.user_repository.session.commit()
        return UserOut(
            id=int(user.id),
            name=updated_user.name,
            surname=updated_user.surname,
            created_at=updated_user.created_at,
            updated_at=updated_user.updated_at
        )

    async def delete_user(self, user_id: int) -> None:
        """Удаляет пользователя.
        
        Args:
            user_id: Идентификатор пользователя.
            
        Raises:
            NotFoundException: Если пользователь не найден.
            SQLAlchemyError: При ошибках удаления.
        """
        user = await self.user_repository.get(user_id)
        if not user:
            raise NotFoundException("User not found")
            
        await self.user_repository.delete(user_id)
        await self.user_repository.session.commit()