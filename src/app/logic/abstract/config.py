from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class JWTConfig:
    auth_secret_key: str


@dataclass
class SQLAlchemyConfig:
    db_uri: str


@dataclass
class TickersConfig:
    file_path: str


class JWTConfigLoader(ABC):
    @abstractmethod
    async def load_jwt_config(self) -> JWTConfig:
        raise NotImplementedError


class SQLAlchemyConfigLoader(ABC):
    @abstractmethod
    async def load_sqlalchemy_config(self) -> SQLAlchemyConfig:
        raise NotImplementedError


class TickersConfigLoader(ABC):
    @abstractmethod
    async def load_tickers_config(self) -> TickersConfig:
        raise NotImplementedError


class ConfigLoader(
    JWTConfigLoader, SQLAlchemyConfigLoader, TickersConfigLoader, ABC
):
    pass
