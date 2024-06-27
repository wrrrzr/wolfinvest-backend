from dishka import Provider

from .adapters import AdaptersProvider
from .logic import LogicProvider
from .other import OtherProvider


def all_providers() -> list[Provider]:
    return [AdaptersProvider(), LogicProvider(), OtherProvider()]


__all__ = ("all_providers",)
