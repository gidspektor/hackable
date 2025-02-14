from pathlib import Path
import uvicorn

from fastapi import FastAPI
from fastapi.responses import UJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from hackable_api.api.router import api_router
from hackable_api.app.settings import settings
from hackable_api.api.middlewares.jwt_middleware import JWTMiddleware

APP_ROOT = Path(__file__).parent.parent

def get_app() -> FastAPI:
	"""Get the FastAPI application."""

	app = FastAPI(
		title="hackable-api",
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
	app.add_middleware(JWTMiddleware)

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
        "app.api.app.application:get_app",
        host=settings.HOST,
        port=settings.PORT,
        log_level=settings.LOG_LEVEL,
        reload=settings.RELOAD
    )