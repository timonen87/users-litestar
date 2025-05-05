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
    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_repository = UserRepository(session=session)

    async def create_user(self, data: UserCreate) -> UserOut:
        """Создание пользователя с бизнес-логикой"""

        user_data = data.as_builtins()  # Преобразуем в dict
        user = await self.user_repository.add(
            self.user_repository.model_type(
                name=user_data["name"],
                surname=user_data["surname"],
                password=hash_password(user_data["password"])  # Здесь должна быть реальная хеш-функция
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
        """Получение пользователя по ID"""
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
        """
        Получение списка пользователей с пагинацией
        
        Args:
            page: Номер страницы (начиная с 1)
            page_size: Количество записей на странице
            
        Returns:
            OffsetPagination[UserOut]: Объект пагинации с пользователями
        """
        users, total = await self.user_repository.list_paginated(page, page_size)
        
        
        return OffsetPagination(
            items=[UserOut( 
                id=int(user.id),
                name=user.name,
                surname=user.surname,
                created_at=user.created_at,
                updated_at=user.updated_at
                ) 
                for user in users],
            total=total,
            limit=page_size,
            offset=(page - 1) * page_size
        )

    async def update_user(self, user_id: int, update_data: UserUpdate) -> UserOut:
        """Обновление данных пользователя"""
        user = await self.user_repository.get(user_id)
        if not user:
            raise NotFoundException("User not found")
        
        

        # Обновление полей
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
        """Удаление пользователя"""
        user = await self.user_repository.get(user_id)
        print("delete user", user)
        if not user:
            raise NotFoundException("User not found")
            
        await self.user_repository.delete(user_id)
        await self.user_repository.session.commit()


