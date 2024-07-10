from fastapi import FastAPI

from . import symbols
from . import auth
from . import users
from . import refills
from . import settings
from . import admin
from . import balance_history
from . import currency
from . import symbols_actions

routers = (
    symbols.router,
    auth.router,
    users.router,
    refills.router,
    settings.router,
    admin.router,
    balance_history.router,
    currency.router,
    symbols_actions.router,
)


def register_routers(app: FastAPI) -> None:
    for router in routers:
        app.include_router(router, prefix="/api")
