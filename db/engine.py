from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker
)
from typing import AsyncGenerator
from config import DATABASE, DB_NAME, AIO_DB


SQLALCHEMY_DATABASE_URL = f"{DATABASE}+{AIO_DB}:///./{DB_NAME}.db"

Base = declarative_base()


engine = create_async_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        await db.close()
