from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, BigInteger, String


class Base(DeclarativeBase):
    pass


class UserModel(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=False)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
