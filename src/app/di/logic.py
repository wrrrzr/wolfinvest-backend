from dishka import (
    Provider,
    Scope,
    provide,
)

from app.logic.use_cases.auth import RegisterUser, AuthUser
from app.logic.use_cases.symbols import (
    GetSymbol,
    GetDailySymbolHistory,
    BuySymbol,
    GetMySymbols,
    SellSymbol,
    FindTicker,
)
from app.logic.use_cases.users import GetMe
from app.logic.use_cases.refills import TakeRefill, GetMyRefills
from app.logic.use_cases.settings import ChangePassword
from app.logic.use_cases.admin import (
    GetAllUsers,
    DeleteUser,
    ChangeUserPassword,
    SetUserBalance,
)
from app.logic.use_cases.balance_history import GetMyBalanceHistory


class LogicProvider(Provider):
    scope = Scope.REQUEST

    get_symbol = provide(GetSymbol)
    get_daily_symbol_history = provide(GetDailySymbolHistory)
    register_user = provide(RegisterUser)
    auth_user = provide(AuthUser)
    get_me = provide(GetMe)
    buy_symbol = provide(BuySymbol)
    get_my_symbols = provide(GetMySymbols)
    sell_symbol = provide(SellSymbol)
    take_refill = provide(TakeRefill)
    get_my_refills = provide(GetMyRefills)
    change_password = provide(ChangePassword)
    get_all_users = provide(GetAllUsers)
    delete_user = provide(DeleteUser)
    change_user_password = provide(ChangeUserPassword)
    set_user_balance = provide(SetUserBalance)
    find_ticker = provide(FindTicker)
    get_my_balance_history = provide(GetMyBalanceHistory)
