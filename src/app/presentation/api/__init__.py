from dishka import make_async_container
from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI

from app.presentation.api.routers import register_routers
from app.presentation.api.di import AuthProvider
from app.di import all_providers


def create_app() -> None:
    app = FastAPI(title="wolfinvest")
    container = make_async_container(*all_providers(), AuthProvider())
    register_routers(app)
    setup_dishka(container, app)
    return app


app = create_app()
