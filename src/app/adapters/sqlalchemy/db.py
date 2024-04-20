from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.main.config import load_sqlalchemy_config

DB_URI = load_sqlalchemy_config().db_uri

engine = create_async_engine(DB_URI)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False)
