from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession
from dishka import (
    Provider,
    Scope,
    AsyncContainer,
    provide,
    decorate,
    make_async_container,
)

from app.logic.abstract import UsersStorage, SymbolsPriceStorage
from app.logic.auth import RegisterUser, AuthUser
from app.logic.symbols import GetSymbol
from app.logic.users import GetMe
from app.adapters.sqlalchemy.db import async_session_maker
from app.adapters.sqlalchemy.users import SQLAlchemyUsersStorage
from app.adapters.cache import UsersCacheStorage, SymbolsPriceCacheStorage
from app.adapters.yahoo_symbols_price import YahooSymbolsPriceStorage


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

    @provide
    async def session(self) -> AsyncIterable[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    users = provide(SQLAlchemyUsersStorage, provides=UsersStorage)
    symbols = provide(YahooSymbolsPriceStorage, provides=SymbolsPriceStorage)

    @decorate
    def get_users_cache(self, inner: UsersStorage) -> UsersStorage:
        return UsersCacheStorage(inner)

    @decorate
    def get_symbols_cache(
        self, inner: SymbolsPriceStorage
    ) -> SymbolsPriceStorage:
        return SymbolsPriceCacheStorage(inner)


class LogicProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

    get_symbol = provide(GetSymbol)
    register_user = provide(RegisterUser)
    auth_user = provide(AuthUser)
    get_me = provide(GetMe)


def create_async_container() -> AsyncContainer:
    return make_async_container(AdaptersProvider(), LogicProvider())
