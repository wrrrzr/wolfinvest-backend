from dishka import Provider, Scope, provide

from app.logic.balance_editor import BalanceEditor


class OtherProvider(Provider):
    scope = Scope.REQUEST

    balance_editor = provide(BalanceEditor)
