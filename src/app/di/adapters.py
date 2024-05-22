from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession
from dishka import (
    Provider,
    Scope,
    provide,
    decorate,
)

from app.logic.abstract import (
    UsersStorage,
    SymbolsStorage,
    RefillsStorage,
    SymbolsGetter,
    AuthManager,
)
from app.adapters.sqlalchemy.db import async_session_maker
from app.adapters.sqlalchemy.users import SQLAlchemyUsersStorage
from app.adapters.sqlalchemy.symbols import SQLAlchemySymbolsStorage
from app.adapters.sqlalchemy.refills import SQLAlchemyRefillsStorage
from app.adapters.cache import (
    UsersCacheStorage,
    SymbolsCacheStorage,
    RefillsCacheStorage,
    SymbolsGetterCache,
)
from app.adapters.symbols_getter import YahooSymbolsGetter
from app.adapters.auth import JWTAuthManager


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

    @provide
    async def session(self) -> AsyncIterable[AsyncSession]:
        async with async_session_maker() as session:
            yield session

    users = provide(SQLAlchemyUsersStorage, provides=UsersStorage)
    symbols = provide(SQLAlchemySymbolsStorage, provides=SymbolsStorage)
    refills = provide(SQLAlchemyRefillsStorage, provides=RefillsStorage)
    symbols_getter = provide(YahooSymbolsGetter, provides=SymbolsGetter)
    auth_manager = provide(JWTAuthManager, provides=AuthManager)

    @decorate
    def get_users_cache(self, inner: UsersStorage) -> UsersStorage:
        return UsersCacheStorage(inner)

    @decorate
    def get_symbols_cache(self, inner: SymbolsStorage) -> SymbolsStorage:
        return SymbolsCacheStorage(inner)

    @decorate
    def get_refills_cache(self, inner: RefillsStorage) -> RefillsStorage:
        return RefillsCacheStorage(inner)

    @decorate
    def get_symbols_getter_cache(self, inner: SymbolsGetter) -> SymbolsGetter:
        return SymbolsGetterCache(inner)
