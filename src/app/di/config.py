import os

from dishka import Provider, Scope, provide

from app.logic.models import (
    JWTConfig,
    SQLAlchemyConfig,
    TickersConfig,
)
from app.logic.exceptions import ConfigLoadError


def getenv(key: str) -> str:
    val = os.getenv(key)
    if val is None:
        raise ConfigLoadError(f"{key} is not set")
    return val


class ConfigProvider(Provider):
    scope = Scope.APP

    @provide
    def jwt(self) -> JWTConfig:
        auth_secret_key = getenv("AUTH_SECRET_KEY")
        return JWTConfig(auth_secret_key=auth_secret_key)

    @provide
    def sqlalchemy(self) -> SQLAlchemyConfig:
        db_uri = getenv("DB_URI")
        return SQLAlchemyConfig(db_uri=db_uri)

    @provide
    def tickers(self) -> TickersConfig:
        file_path = getenv("TICKERS_FILE_PATH")
        return TickersConfig(file_path=file_path)
