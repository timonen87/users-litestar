
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories.user_repo import UserRepository
from app.services.user_service import UserService
from litestar.params import Parameter, Dependency
from litestar.di import Provide


async def provide_user_service(db_session: AsyncSession) -> UserService:
    return UserService(session=db_session)

