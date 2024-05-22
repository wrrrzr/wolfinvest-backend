from dishka import Provider

from .adapters import AdaptersProvider
from .logic import LogicProvider


def all_providers() -> list[Provider]:
    return [AdaptersProvider(), LogicProvider()]


__all__ = ("all_providers",)
