"""FastAPI application factory."""

from fastapi import FastAPI
from src.api.routes import router
from src.config.settings import get_settings


def create_app() -> FastAPI:
    """Creates and configures the FastAPI application."""
    settings = get_settings()
    app = FastAPI(title=settings.app_name, debug=settings.debug)
    app.include_router(router, prefix=settings.api_prefix)
    return app
