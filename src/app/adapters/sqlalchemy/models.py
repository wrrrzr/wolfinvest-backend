from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    BigInteger,
    DateTime,
    Float,
    String,
)

from app.logic.models.user import USER_DEFAULT_ROLE


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Integer, nullable=False, default=USER_DEFAULT_ROLE)
    register_at = Column(DateTime(timezone=True), nullable=False)


class RefillModel(Base):
    __tablename__ = "refills"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    amount = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class SymbolActionModel(Base):
    __tablename__ = "symbol_action"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    ticker = Column(String, nullable=False)
    action = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class CurrenciesActionModel(Base):
    __tablename__ = "currencies_action"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    ticker = Column(String, nullable=False)
    action = Column(Integer, nullable=False)
    reason = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)
    price = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
