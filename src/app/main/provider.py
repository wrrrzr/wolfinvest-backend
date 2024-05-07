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

from app.logic.abstract import UsersStorage, SymbolsStorage, SymbolsGetter
from app.logic.auth import RegisterUser, AuthUser
from app.logic.symbols import GetSymbol, BuySymbol, GetMySymbols
from app.logic.users import GetMe
from app.adapters.sqlalchemy.db import async_session_maker
from app.adapters.sqlalchemy.users import SQLAlchemyUsersStorage
from app.adapters.sqlalchemy.symbols import SQLAlchemSymbolsStorage
from app.adapters.cache import UsersCacheStorage, SymbolsGetterCache
from app.adapters.symbols_getter import YahooSymbolsGetter


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

    @provide
    async def session(self) -> AsyncIterable[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    users = provide(SQLAlchemyUsersStorage, provides=UsersStorage)
    symbols = provide(SQLAlchemSymbolsStorage, provides=SymbolsStorage)
    symbols_getter = provide(YahooSymbolsGetter, provides=SymbolsGetter)

    @decorate
    def get_users_cache(self, inner: UsersStorage) -> UsersStorage:
        return UsersCacheStorage(inner)

    @decorate
    def get_symbols_getter_cache(self, inner: SymbolsGetter) -> SymbolsGetter:
        return SymbolsGetterCache(inner)


class LogicProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

    get_symbol = provide(GetSymbol)
    register_user = provide(RegisterUser)
    auth_user = provide(AuthUser)
    get_me = provide(GetMe)
    buy_symbol = provide(BuySymbol)
    get_my_symbols = provide(GetMySymbols)


def create_async_container() -> AsyncContainer:
    return make_async_container(AdaptersProvider(), LogicProvider())
