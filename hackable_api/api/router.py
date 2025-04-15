from fastapi.routing import APIRouter

from hackable_api.api.v1.views import router as v1_router
from hackable_api.api.docs.views import router as docs_router
from hackable_api.api.views import router as monitoring
from hackable_api.api.users.views import router as users_router

api_router = APIRouter()
api_router.include_router(monitoring)
api_router.include_router(docs_router)
api_router.include_router(users_router)

api_router.include_router(
    v1_router,
    tags=["data v1"],
)
