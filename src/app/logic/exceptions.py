class LogicError(Exception):
    pass


class UnfoundSymbolError(LogicError):
    pass


class NotEnoughBalanceError(LogicError):
    pass


class NotEnoughSymbolsError(LogicError):
    pass


class NotEnoughCurrencyError(LogicError):
    pass


class UsernameAlreadyTakenError(LogicError):
    pass


class IncorrectUsernameError(LogicError):
    pass


class IncorrectPasswordError(LogicError):
    pass


class PermissionDenied(LogicError):
    pass


class ConfigLoadError(LogicError):
    pass


class VerifyTokenError(LogicError):
    pass
