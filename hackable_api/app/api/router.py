from fastapi.routing import APIRouter

from app.api.v1.views import router as v1_router
from app.api.docs.views import router as docs_router
from app.api.views import router as monitoring
from app.api.users.views import router as users_router

api_router = APIRouter()
api_router.include_router(monitoring)
api_router.include_router(docs_router)
api_router.include_router(users_router)

api_router.include_router(
    v1_router,
    tags=["data v1"],
)
