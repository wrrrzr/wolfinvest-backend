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
