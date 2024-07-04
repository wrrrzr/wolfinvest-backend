from dishka import Provider

from .adapters import AdaptersProvider
from .logic import LogicProvider
from .config import ConfigProvider
from .other import OtherProvider


def all_providers() -> list[Provider]:
    return [
        AdaptersProvider(),
        LogicProvider(),
        ConfigProvider(),
        OtherProvider(),
    ]


__all__ = ("all_providers",)
