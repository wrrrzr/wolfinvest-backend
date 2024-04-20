from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.presentation.api import register_routers
from .provider import create_async_container


def create_app() -> None:
    app = FastAPI()
    container = create_async_container()
    register_routers(app)
    setup_dishka(container, app)
    return app


app = create_app()
