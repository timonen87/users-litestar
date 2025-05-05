
from litestar.contrib.sqlalchemy.plugins import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar.plugins.sqlalchemy import (
    AsyncSessionConfig,
    SQLAlchemyAsyncConfig,
    SQLAlchemyInitPlugin,
    base,
    filters,
    repository,
    SQLAlchemyAsyncConfig,
    SQLAlchemyPlugin
)
import uuid
from sqlalchemy import ForeignKey, func, select, BigInteger
from app.repositories.user_repo import UserRepository
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User
from app.config  import settings


session_config = AsyncSessionConfig(expire_on_commit=False)
sqlalchemy_config = SQLAlchemyAsyncConfig(
        connection_string=settings.database_url,
        session_dependency_key="db_session",
        session_config=session_config,
        create_all=True,
)  
sqlalchemy_plugin = SQLAlchemyPlugin(config=sqlalchemy_config)


async def on_startup() -> None:
    """Adds some dummy data if no data is present."""
    async with sqlalchemy_config.get_session() as session:
        statement = select(func.count()).select_from(User)
        count = await session.execute(statement)
        if not count.scalar():
            session.add(
                User(name="user", surname="test", password="123456", id=1)
            )
            await session.commit()