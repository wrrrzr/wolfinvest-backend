from dishka import (
    Provider,
    Scope,
    provide,
)

from app.logic.auth import RegisterUser, AuthUser
from app.logic.symbols import (
    GetSymbol,
    GetDailySymbolHistory,
    BuySymbol,
    GetMySymbols,
    SellSymbol,
    GetListSymbols,
    FindTicker,
)
from app.logic.users import GetMe
from app.logic.refills import TakeRefill, GetMyRefills
from app.logic.settings import ChangePassword
from app.logic.admin import (
    GetAllUsers,
    DeleteUser,
    ChangeUserPassword,
    SetUserBalance,
)


class LogicProvider(Provider):
    scope = Scope.REQUEST

    def __init__(self) -> None:
        super().__init__()

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
    get_list_symbols = provide(GetListSymbols)
    change_password = provide(ChangePassword)
    get_all_users = provide(GetAllUsers)
    delete_user = provide(DeleteUser)
    change_user_password = provide(ChangeUserPassword)
    set_user_balance = provide(SetUserBalance)
    find_ticker = provide(FindTicker)
