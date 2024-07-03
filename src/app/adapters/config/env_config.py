import os

from app.logic.abstract.config import (
    ConfigLoader,
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


class EnvConfigLoader(ConfigLoader):
    async def load_jwt_config(self) -> JWTConfig:
        auth_secret_key = getenv("AUTH_SECRET_KEY")
        return JWTConfig(auth_secret_key=auth_secret_key)

    async def load_sqlalchemy_config(self) -> SQLAlchemyConfig:
        db_uri = getenv("DB_URI")
        return SQLAlchemyConfig(db_uri=db_uri)

    async def load_tickers_config(self) -> TickersConfig:
        file_path = getenv("TICKERS_FILE_PATH")
        return TickersConfig(file_path=file_path)
