
from litestar import Litestar
from litestar.openapi import OpenAPIConfig

from litestar.openapi.spec import Server
from litestar.config.cors import CORSConfig

from app.config import settings
from app.api.v1.api import api_router
from litestar.status_codes import HTTP_500_INTERNAL_SERVER_ERROR
from litestar.di import Provide
from app.db.session import sqlalchemy_config,  on_startup
from litestar.plugins.sqlalchemy import SQLAlchemyAsyncConfig, SQLAlchemyPlugin
from litestar import Litestar, Request, Response
from litestar.exceptions import HTTPException


def get_cors_config() -> CORSConfig:
    """Конфигурация CORS."""
    return CORSConfig(
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
    )


def get_openapi_config() -> OpenAPIConfig:
    """Конфигурация OpenAPI."""
    return OpenAPIConfig(
        title="User API",
        version="1.0.0",
        description="REST API для управления пользователями на LiteStar",
 
        servers=[
            Server(
                url=f"http://{settings.APP_HOST}:{settings.APP_PORT}",  # Основной URL сервера
                description="Local server development"
            ),
            Server(
                url=f"https://{settings.APP_DOMAIN}",  # Production URL
                description="Production URL"
            )
        ]
    )

# Обработчик общих исключений
def exception_handler(request: Request, exc: Exception) -> Response:

    if isinstance(exc, HTTPException):
        status_code = exc.status_code
        detail = exc.detail
    else:
        status_code = HTTP_500_INTERNAL_SERVER_ERROR
        detail = "Внутренняя ошибка сервера"
        
        if settings.MODE == "development":
            detail = str(exc)
    
    return Response(
        content={"detail": detail},
        status_code=status_code,
    )


def create_app() -> Litestar:
    """Создать приложение Litestar."""
    return Litestar(
        route_handlers=[api_router],
        plugins=[SQLAlchemyPlugin(config=sqlalchemy_config)],
        on_startup=[on_startup],
        cors_config=get_cors_config(),
        openapi_config=get_openapi_config(),
        exception_handlers={Exception: exception_handler},

    )


app = create_app()


