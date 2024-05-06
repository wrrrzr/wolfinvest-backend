class LogicError(Exception):
    pass


class UnfoundSymbolError(LogicError):
    pass


class NotEnoughBalanceError(LogicError):
    pass


class UsernameAlreadyTakenError(LogicError):
    pass


class IncorrectUsernameError(LogicError):
    pass


class IncorrectPasswordError(LogicError):
    pass
