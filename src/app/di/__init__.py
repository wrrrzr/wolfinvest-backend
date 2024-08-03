from dishka import Provider

from .adapters import AdaptersProvider
from .logic import LogicProvider
from .config import ConfigProvider


def all_providers() -> list[Provider]:
    return [
        AdaptersProvider(),
        LogicProvider(),
        ConfigProvider(),
    ]


__all__ = ("all_providers",)
