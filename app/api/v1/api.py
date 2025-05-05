from litestar import Router
from app.config import settings
from app.api.v1.endpoints.user_router import UserController

api_router = Router(
    path=f"/{settings.API_V1_STR}",
    route_handlers=[UserController]

)

