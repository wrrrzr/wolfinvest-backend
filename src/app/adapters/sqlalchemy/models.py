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


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    balance = Column(Float, default=0.0, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(Integer, nullable=False)


class SymbolModel(Base):
    __tablename__ = "symbols"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    code = Column(String, nullable=False)
    amount = Column(BigInteger, nullable=False)


class RefillModel(Base):
    __tablename__ = "refills"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    amount = Column(BigInteger, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class BalanceChangeModel(Base):
    __tablename__ = "balance_change"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    change_type = Column(Integer, nullable=False)
    reason = Column(Integer, nullable=False)
    user_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    amount = Column(Float, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)


class SymbolActionModel(Base):
    __tablename__ = "symbol_action"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    action = Column(Integer, nullable=False)
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False)
