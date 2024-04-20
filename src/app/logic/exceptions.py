class LogicError(Exception):
    pass


class UsernameAlreadyTakenError(LogicError):
    pass


class IncorrectUsernameError(LogicError):
    pass


class IncorrectPasswordError(LogicError):
    pass
