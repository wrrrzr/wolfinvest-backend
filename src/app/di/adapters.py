from typing import AsyncIterable

from sqlalchemy.ext.asyncio import AsyncSession
from dishka import (
    Provider,
    Scope,
    AnyOf,
    provide,
    decorate,
)

from app.logic.abstract import (
    UsersStorage,
    SymbolsStorage,
    RefillsStorage,
    SymbolsPriceGetter,
    SymbolsHistoryGetter,
    SymbolsGetter,
    AuthManager,
    TickerFinder,
    BalanceHistoryEditor,
    BalanceHistoryAllSelector,
)
from app.adapters.sqlalchemy.db import async_session_maker
from app.adapters.sqlalchemy.users import SQLAlchemyUsersStorage
from app.adapters.sqlalchemy.symbols import SQLAlchemySymbolsStorage
from app.adapters.sqlalchemy.refills import SQLAlchemyRefillsStorage
from app.adapters.sqlalchemy.balance_history import (
    SQLAlchemyBalanceHistoryStorage,
)
from app.adapters.cache import (
    UsersCacheStorage,
    create_users_memory,
    SymbolsCacheStorage,
    create_symbols_memory,
    RefillsCacheStorage,
    create_refills_memory,
    SymbolsGetterCache,
    create_symbols_getter_memory,
    TickerFinderCache,
    create_ticker_finder_memory,
)
from app.adapters.symbols_getter import YahooSymbolsGetter
from app.adapters.auth import JWTAuthManager
from app.adapters.ticker_finder import MemoryTickerFinder

_memory_users = create_users_memory()
_memory_symbols = create_symbols_memory()
_memory_refills = create_refills_memory()
_memory_symbols_getter = create_symbols_getter_memory()
_memory_ticker_finder = create_ticker_finder_memory()


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
    auth_manager = provide(JWTAuthManager, provides=AuthManager)
    ticker_finder = provide(MemoryTickerFinder, provides=TickerFinder)
    balance_history_editor = provide(
        SQLAlchemyBalanceHistoryStorage, provides=BalanceHistoryEditor
    )
    balance_history_selector = provide(
        SQLAlchemyBalanceHistoryStorage, provides=BalanceHistoryAllSelector
    )

    @provide
    def symbols_getter(
        self,
    ) -> AnyOf[SymbolsPriceGetter, SymbolsHistoryGetter]:
        return SymbolsGetterCache(YahooSymbolsGetter(), _memory_symbols_getter)

    @decorate
    def get_users_cache(self, inner: UsersStorage) -> UsersStorage:
        return UsersCacheStorage(inner, _memory_users)

    @decorate
    def get_symbols_cache(self, inner: SymbolsStorage) -> SymbolsStorage:
        return SymbolsCacheStorage(inner, _memory_symbols)

    @decorate
    def get_refills_cache(self, inner: RefillsStorage) -> RefillsStorage:
        return RefillsCacheStorage(inner, _memory_refills)

    @decorate
    def get_ticker_finder_cache(self, inner: TickerFinder) -> TickerFinder:
        return TickerFinderCache(inner, _memory_ticker_finder)
