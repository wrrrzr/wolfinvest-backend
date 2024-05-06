from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, ForeignKey, BigInteger, String


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    balance = Column(BigInteger, default=0, nullable=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


class SymbolModel(Base):
    __tablename__ = "symbols"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    owner_id = Column(BigInteger, ForeignKey(UserModel.id), nullable=False)
    code = Column(String, nullable=False)
    amount = Column(BigInteger, nullable=False)
