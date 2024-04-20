import os

from dataclasses import dataclass


class ConfigParseError(Exception):
    pass


@dataclass
class SQLAlchemyConfig:
    db_uri: str


@dataclass
class CommonConfig:
    auth_secret_key: str


def getenv(key: str) -> str:
    val = os.getenv(key)
    if val is None:
        raise ConfigParseError(f"{key} is not set")
    return val


def load_common_config() -> CommonConfig:
    auth_secret_key = getenv("AUTH_SECRET_KEY")
    return CommonConfig(auth_secret_key=auth_secret_key)


def load_sqlalchemy_config() -> SQLAlchemyConfig:
    db_uri = getenv("DB_URI")
    return SQLAlchemyConfig(db_uri=db_uri)
