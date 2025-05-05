from litestar import Controller, get, post, put, delete
from litestar.dto import DTOData
from litestar.response import Response
from litestar.status_codes import HTTP_200_OK
from litestar.enums import MediaType
from app.schemas.user_schema import UserCreate, UserOut, UserUpdate, UserCreateDTO, UserOutDTO, UserCreate
from litestar import Controller, get, post, put, delete
from litestar.di import Provide
from app.deps.user_deps import provide_user_service
from app.services.user_service import UserService
from litestar.params import Parameter, Dependency
from litestar.pagination import OffsetPagination


class UserController(Controller):
    """Контроллер для управления пользователями.

    Обрабатывает CRUD-операции для сущности пользователя:
    - создание (create)
    - чтение (get, get_all)
    - обновление (update)
    - удаление (delete)

    Attributes:
        path (str): Базовый путь для маршрутов (`/users`).
        tags (list[str]): Теги для OpenAPI-документации.
        dependencies (dict): Зависимости контроллера (сервис пользователей).
    """
    path = "/users"
    tags = ["Users"]
    dependencies = {"user_service": Provide(provide_user_service)}

    @post(dto=UserCreateDTO)
    async def create_user(
        self,
        user_service: UserService,
        data: DTOData[UserCreate]
    ) -> UserOut:
        """Создает нового пользователя.

        Args:
            user_service (UserService): Сервис для работы с пользователями.
            data (DTOData[UserCreate]): Валидированные данные пользователя.

        Returns:
            UserOut: Данные созданного пользователя.

        Raises:
            HTTPException: 400 если данные невалидны, 409 если пользователь уже существует.
        """
        return await user_service.create_user(data)
    
    @get(dto=UserOutDTO)
    async def get_all_users(
        self,
        user_service: UserService,
        page: int = Parameter(ge=1, default=1),
        page_size: int = Parameter(ge=1, le=1000, default=100),
    ) -> OffsetPagination[UserOut]:
        """Возвращает список пользователей с пагинацией.

        Args:
            user_service (UserService): Сервис для работы с пользователями.
            page (int, optional): Номер страницы. Defaults to 1.
            page_size (int, optional): Размер страницы (1-1000). Defaults to 100.

        Returns:
            OffsetPagination[UserOut]: Пагинированный список пользователей.
        """
        return await user_service.get_list(page, page_size)

    @get("/{user_id:int}")
    async def get_user(
        self,
        user_service: UserService,
        user_id: int
    ) -> UserOut:
        """Возвращает данные пользователя по ID.

        Args:
            user_service (UserService): Сервис для работы с пользователями.
            user_id (int): Идентификатор пользователя.

        Returns:
            UserOut: Данные пользователя.

        Raises:
            HTTPException: 404 если пользователь не найден.
        """
        return await user_service.get_user(user_id)

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: int,
        data: UserUpdate
    ) -> UserOut:
        """Обновляет данные пользователя.

        Args:
            user_service (UserService): Сервис для работы с пользователями.
            user_id (int): Идентификатор пользователя.
            data (UserUpdate): Новые данные для обновления.

        Returns:
            UserOut: Обновленные данные пользователя.

        Raises:
            HTTPException: 404 если пользователь не найден, 400 если данные невалидны.
        """
        return await user_service.update_user(user_id, data)

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: int
    ) -> None:
        """Удаляет пользователя по ID.

        Args:
            user_service (UserService): Сервис для работы с пользователями.
            user_id (int): Идентификатор пользователя.

        Returns:
            Response: JSON-ответ с статусом операции.

        Raises:
            HTTPException: 404 если пользователь не найден.
        """
        await user_service.delete_user(user_id)
        return Response(
            status_code=HTTP_200_OK,
            content={"status": "success", "message": "OK"},
            media_type=MediaType.JSON
        )