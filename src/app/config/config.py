import os

from dataclasses import dataclass


class ConfigParseError(Exception):
    pass


@dataclass
class SQLAlchemyConfig:
    db_uri: str


@dataclass
class JWTConfig:
    auth_secret_key: str


@dataclass
class TickersConfig:
    file_path: str


def getenv(key: str) -> str:
    val = os.getenv(key)
    if val is None:
        raise ConfigParseError(f"{key} is not set")
    return val


def load_jwt_config() -> JWTConfig:
    auth_secret_key = getenv("AUTH_SECRET_KEY")
    return JWTConfig(auth_secret_key=auth_secret_key)


def load_sqlalchemy_config() -> SQLAlchemyConfig:
    db_uri = getenv("DB_URI")
    return SQLAlchemyConfig(db_uri=db_uri)


def load_tickers_config() -> TickersConfig:
    file_path = getenv("TICKERS_FILE_PATH")
    return TickersConfig(file_path=file_path)
