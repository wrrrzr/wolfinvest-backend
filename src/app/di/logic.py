from dishka import Provider, Scope, provide_all

from app.logic.use_cases.auth import RegisterUser, AuthUser
from app.logic.use_cases.symbols import (
    GetSymbol,
    GetSymbolHistory,
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
from app.logic.use_cases.currency import GetCurrencyPrice


class LogicProvider(Provider):
    scope = Scope.REQUEST

    use_cases = provide_all(
        GetSymbol,
        GetSymbolHistory,
        RegisterUser,
        AuthUser,
        GetMe,
        BuySymbol,
        GetMySymbols,
        SellSymbol,
        TakeRefill,
        GetMyRefills,
        ChangePassword,
        GetAllUsers,
        DeleteUser,
        ChangeUserPassword,
        SetUserBalance,
        FindTicker,
        GetMyBalanceHistory,
        GetCurrencyPrice,
    )
