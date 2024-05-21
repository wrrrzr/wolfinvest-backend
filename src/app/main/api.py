from dishka.integrations.fastapi import setup_dishka
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.presentation.api import register_routers
from .provider import create_async_container

origins = (
    "http://192.168.0.100:3000/",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
)


def create_app() -> None:
    app = FastAPI(title="wolfinvest")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    container = create_async_container()
    register_routers(app)
    setup_dishka(container, app)
    return app


app = create_app()
