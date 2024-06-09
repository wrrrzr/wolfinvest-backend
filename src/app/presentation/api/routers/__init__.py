from fastapi import FastAPI

from . import symbols
from . import auth
from . import users
from . import refills
from . import settings

routers = (
    symbols.router,
    auth.router,
    users.router,
    refills.router,
    settings.router,
)


def register_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router, prefix="/api")
