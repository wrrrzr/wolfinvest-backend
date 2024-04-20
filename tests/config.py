import os

from dataclasses import dataclass


class ConfigParseError(Exception):
    pass


@dataclass
class SQLAlchemyConfig:
    db_uri: str


def getenv(key: str) -> str:
    val = os.getenv(key)
    if val is None:
        raise ConfigParseError(f"{key} is not set")
    return val


def load_test_sqlalchemy_config() -> SQLAlchemyConfig:
    db_uri = getenv("TEST_DB_URI")
    return SQLAlchemyConfig(db_uri=db_uri)
