
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from litestar.params import Parameter, Dependency
from litestar.di import Provide


async def provide_user_service(db_session: AsyncSession) -> UserService:
    """Создает и возвращает экземпляр UserService с переданной асинхронной сессией БД.

    Args:
        db_session (AsyncSession): Асинхронная сессия SQLAlchemy для подключения к БД.

    Returns:
        UserService: Сервис для работы с пользователями.
    """
    return UserService(session=db_session)

