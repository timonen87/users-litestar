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
    path = "/users"
    tags = ["Users"]
    dependencies = {"user_service": Provide(provide_user_service)}

    @post(dto=UserCreateDTO)
    async def create_user(
        self,
        user_service: UserService,
        data: DTOData[UserCreate]
    ) -> UserOut:
        return await user_service.create_user(data)
    
    @get(dto=UserOutDTO)
    async def get_all_users(
        self,
        user_service: UserService,
        page: int = Parameter(ge=1, default=1),
        page_size: int = Parameter(ge=1, le=1000, default=100),

    ) -> OffsetPagination[UserOut]:
        print("Received data:", page)
        return await user_service.get_list(
            page,
            page_size,
        )

    @get("/{user_id:int}")
    async def get_user(
        self,
        user_service: UserService,
        user_id: int
    ) -> UserOut:
        return await user_service.get_user(user_id)

    @put("/{user_id:int}")
    async def update_user(
        self,
        user_service: UserService,
        user_id: int,
        data: UserUpdate
    ) -> UserOut:
        return await user_service.update_user(user_id, data)

    @delete("/{user_id:int}")
    async def delete_user(
        self,
        user_service: UserService,
        user_id: int
    ) -> None:
        await user_service.delete_user(user_id)
        return Response(
                status_code=HTTP_200_OK,
                content={"status": "success", "message": "OK"},
                media_type=MediaType.JSON
            )

