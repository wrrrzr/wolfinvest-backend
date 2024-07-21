from typing import AsyncIterable

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from dishka import (
    Provider,
    Scope,
    AnyOf,
    provide,
    decorate,
)

from app.logic.abstract import (
    UsersAdder,
    UsersBalanceEditor,
    UsersPasswordEditor,
    UsersOneSelector,
    UsersAllSelector,
    UsersChecker,
    UsersDeleter,
    UsersIdGetter,
    SymbolsPriceGetter,
    SymbolsHistoryGetter,
    TickerFinder,
    BalanceHistoryEditor,
    BalanceHistoryAllSelector,
)
from app.logic.abstract.currency_storage import CurrencyUserAllSelector
from app.logic.abstract.symbols_storage import (
    SymbolsAdder,
    SymbolsManySelector,
    SymbolsRemover,
    SymbolsUsersDeletor,
    SymbolsAmountSelector,
)
from app.logic.abstract.refills_storage import (
    RefillsAdder,
    RefillsUsersSelector,
    RefillsUsersDeletor,
)
from app.logic.abstract.symbols_actions_storage import (
    SymbolsActionsAdder,
    SymbolsActionsManySelector,
    SymbolsActionsUsersDeletor,
)
from app.logic.abstract.auth_manager import TokenManager, PasswordManager
from app.logic.abstract.currency_getter import CurrencyPriceGetter
from app.logic.models import SQLAlchemyConfig
from app.adapters.sqlalchemy.users import SQLAlchemyUsersStorage
from app.adapters.sqlalchemy.symbols import SQLAlchemySymbolsStorage
from app.adapters.sqlalchemy.refills import SQLAlchemyRefillsStorage
from app.adapters.sqlalchemy.balance_history import (
    SQLAlchemyBalanceHistoryStorage,
)
from app.adapters.sqlalchemy.symbols_actions import (
    SQLAlchemySymbolsActionsStorage,
)
from app.adapters.sqlalchemy.currency import SQLAlchemyCurrencyStorage
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
    CacheCurrencyGetter,
    create_currency_getter_memory,
)
from app.adapters.symbols_getter import YahooSymbolsGetter
from app.adapters.auth import JWTTokenManager, PasslibPasswordManager
from app.adapters.ticker_finder import TickersFileTickerFinder
from app.adapters.currency_getter import ExchangerateApiGetter

_memory_users = create_users_memory()
_memory_symbols = create_symbols_memory()
_memory_refills = create_refills_memory()
_memory_symbols_getter = create_symbols_getter_memory()
_memory_ticker_finder = create_ticker_finder_memory()
_memory_currency_getter = create_currency_getter_memory()


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

    ticker_finder = provide(TickersFileTickerFinder, provides=TickerFinder)
    balance_history_editor = provide(
        SQLAlchemyBalanceHistoryStorage, provides=BalanceHistoryEditor
    )
    balance_history_selector = provide(
        SQLAlchemyBalanceHistoryStorage, provides=BalanceHistoryAllSelector
    )

    token_manager = provide(JWTTokenManager, provides=TokenManager)
    password_manager = provide(
        PasslibPasswordManager, provides=PasswordManager
    )

    @provide
    def currency_storage(
        self, session: AsyncSession
    ) -> AnyOf[CurrencyUserAllSelector]:
        return SQLAlchemyCurrencyStorage(session)

    @provide
    def currency_getter(self) -> AnyOf[CurrencyPriceGetter]:
        return CacheCurrencyGetter(
            ExchangerateApiGetter(), _memory_currency_getter
        )

    @provide
    def symbols_actions_storage(self, session: AsyncSession) -> AnyOf[
        SymbolsActionsAdder,
        SymbolsActionsManySelector,
        SymbolsActionsUsersDeletor,
    ]:
        return SQLAlchemySymbolsActionsStorage(session)

    @provide
    def symbols_storage(self, session: AsyncSession) -> AnyOf[
        SymbolsAdder,
        SymbolsAmountSelector,
        SymbolsManySelector,
        SymbolsRemover,
        SymbolsUsersDeletor,
    ]:
        return SymbolsCacheStorage(
            SQLAlchemySymbolsStorage(session), _memory_symbols
        )

    @provide
    def refills_storage(
        self, session: AsyncSession
    ) -> AnyOf[RefillsAdder, RefillsUsersSelector, RefillsUsersDeletor]:
        return RefillsCacheStorage(
            SQLAlchemyRefillsStorage(session), _memory_refills
        )

    @provide
    def users_storage(self, session: AsyncSession) -> AnyOf[
        UsersAdder,
        UsersBalanceEditor,
        UsersPasswordEditor,
        UsersOneSelector,
        UsersAllSelector,
        UsersChecker,
        UsersDeleter,
        UsersIdGetter,
    ]:
        return UsersCacheStorage(
            SQLAlchemyUsersStorage(session), _memory_users
        )

    @provide
    def symbols_getter(
        self,
    ) -> AnyOf[SymbolsPriceGetter, SymbolsHistoryGetter]:
        return SymbolsGetterCache(YahooSymbolsGetter(), _memory_symbols_getter)

    @decorate
    def get_ticker_finder_cache(self, inner: TickerFinder) -> TickerFinder:
        return TickerFinderCache(inner, _memory_ticker_finder)
