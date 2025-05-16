from pathlib import Path
import uvicorn

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from app.api.router import api_router
from app.app.settings import settings

APP_ROOT = Path(__file__).parent.parent


def get_app() -> FastAPI:
    """Get the FastAPI application."""

    app = FastAPI(
        title="hackable_api",
        docs_url=None,
        redoc_url=None,
        openapi_url="/api/openapi.json",
        default_response_class=UJSONResponse,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )

    app.include_router(router=api_router, prefix="/api")

    # Adds static directory.
    # This directory is used to access swagger files.
    app.mount(
        "/static",
        StaticFiles(directory=APP_ROOT / "static"),
        name="static",
    )

    return app


def run_app() -> None:
    """Run the FastAPI app."""

    uvicorn.run(
        "app.app.application:get_app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )
