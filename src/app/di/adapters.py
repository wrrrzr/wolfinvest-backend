from typing import AsyncIterable

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dishka import (
    Provider,
    Scope,
    AnyOf,
    provide,
    decorate,
)

from app.logic.abstract.storages.users import (
    UsersAdder,
    UsersPasswordEditor,
    UsersOneSelector,
    UsersAllSelector,
    UsersChecker,
    UsersDeleter,
)
from app.logic.abstract.ticker_finder import TickerFinder
from app.logic.abstract.transaction import Transaction
from app.logic.abstract.symbols_getter import (
    SymbolsManyPriceGetter,
    SymbolsPriceGetter,
    SymbolsHistoryGetter,
)
from app.logic.abstract.storages.currency import (
    CurrencyUserAllSelector,
    CurrencyAmountSelector,
    CurrencyAdder,
    CurrencyRemover,
    CurrencyActionsManySelector,
    CurrencyChangesSelector,
    CurrencyUsersDeletor,
)
from app.logic.abstract.storages.symbols import (
    SymbolsAdder,
    SymbolsManySelector,
    SymbolsActionsManySelector,
    SymbolsRemover,
    SymbolsUsersDeletor,
    SymbolsAmountSelector,
)
from app.logic.abstract.storages.refills import (
    RefillsAdder,
    RefillsUsersSelector,
    RefillsUsersDeletor,
)
from app.logic.abstract.auth_manager import TokenManager, PasswordManager
from app.logic.abstract.currency_getter import CurrencyPriceGetter
from app.logic.abstract.clock import ClockCurrentTimeGetter
from app.logic.models import SQLAlchemyConfig
from app.adapters.sqlalchemy.transaction import SQLAlchemyTransaction
from app.adapters.symbols_getter import (
    YahooSymbolsGetter,
    MoexSymbolsGetter,
    MultiSymbolsGetter,
    MemoryCacheSymbolsGetter,
)
from app.adapters.auth import JWTTokenManager, PasslibPasswordManager
from app.adapters.ticker_finder import (
    TickersFileTickerFinder,
    MemoryCacheTickerFinder,
)
from app.adapters.currency_getter import (
    ExchangerateApiGetter,
    MemoryCacheCurrencyGetter,
)
from app.adapters.storages.users import (
    SQLAlchemyUsersStorage,
    MemoryCacheUsersStorage,
)
from app.adapters.storages.currency import SQLAlchemyCurrencyStorage
from app.adapters.storages.symbols import (
    SQLAlchemySymbolsStorage,
    MemoryCacheSymbolsStorage,
)
from app.adapters.storages.refills import (
    SQLAlchemyRefillsStorage,
    MemoryCacheRefillsStorage,
)
from app.adapters.clock import UTCClock

_memory_users = MemoryCacheUsersStorage.create_memory()
_memory_symbols = MemoryCacheSymbolsStorage.create_memory()
_memory_refills = MemoryCacheRefillsStorage.create_memory()
_memory_symbols_getter = MemoryCacheSymbolsGetter.create_memory()
_memory_ticker_finder = MemoryCacheTickerFinder.create_memory()
_memory_currency_getter = MemoryCacheCurrencyGetter.create_memory()


class AdaptersProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

    @provide
    async def session(
        self, config: SQLAlchemyConfig
    ) -> AsyncIterable[AsyncSession]:
        engine = create_async_engine(config.db_uri)
        async with AsyncSession(engine) as session:
            yield session

    @provide
    def sqlalchemy_transaction(self, session: AsyncSession) -> Transaction:
        return SQLAlchemyTransaction(session)

    ticker_finder = provide(TickersFileTickerFinder, provides=TickerFinder)
    token_manager = provide(JWTTokenManager, provides=TokenManager)
    password_manager = provide(
        PasslibPasswordManager, provides=PasswordManager
    )

    @provide
    def currency_storage(self, session: AsyncSession) -> AnyOf[
        CurrencyUserAllSelector,
        CurrencyAmountSelector,
        CurrencyAdder,
        CurrencyRemover,
        CurrencyActionsManySelector,
        CurrencyChangesSelector,
        CurrencyUsersDeletor,
    ]:
        return SQLAlchemyCurrencyStorage(session)

    @provide
    def clock(self) -> AnyOf[ClockCurrentTimeGetter]:
        return UTCClock()

    @provide
    def currency_getter(
        self, clock: ClockCurrentTimeGetter
    ) -> AnyOf[CurrencyPriceGetter]:
        return MemoryCacheCurrencyGetter(
            ExchangerateApiGetter(), _memory_currency_getter, clock
        )

    @provide
    def symbols_storage(self, session: AsyncSession) -> AnyOf[
        SymbolsAdder,
        SymbolsAmountSelector,
        SymbolsManySelector,
        SymbolsActionsManySelector,
        SymbolsRemover,
        SymbolsUsersDeletor,
    ]:
        return MemoryCacheSymbolsStorage(
            SQLAlchemySymbolsStorage(session), _memory_symbols
        )

    @provide
    def refills_storage(
        self, session: AsyncSession
    ) -> AnyOf[RefillsAdder, RefillsUsersSelector, RefillsUsersDeletor]:
        return MemoryCacheRefillsStorage(
            SQLAlchemyRefillsStorage(session), _memory_refills
        )

    @provide
    def users_storage(self, session: AsyncSession) -> AnyOf[
        UsersAdder,
        UsersPasswordEditor,
        UsersOneSelector,
        UsersAllSelector,
        UsersChecker,
        UsersDeleter,
    ]:
        return MemoryCacheUsersStorage(
            SQLAlchemyUsersStorage(session), _memory_users
        )

    @provide
    def symbols_getter(
        self, clock: ClockCurrentTimeGetter
    ) -> AnyOf[
        SymbolsPriceGetter, SymbolsManyPriceGetter, SymbolsHistoryGetter
    ]:
        return MemoryCacheSymbolsGetter(
            MultiSymbolsGetter(
                YahooSymbolsGetter(),
                MoexSymbolsGetter(clock),
            ),
            _memory_symbols_getter,
            clock,
        )

    @decorate
    def get_ticker_finder_cache(self, inner: TickerFinder) -> TickerFinder:
        return MemoryCacheTickerFinder(inner, _memory_ticker_finder)
