from collections.abc import AsyncGenerator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.settings import settings

engine = create_async_engine(
    url=str(settings.postgres.DSN),
    echo=settings.postgres.ECHO_SQL,
    future=True,
    pool_pre_ping=True,
    pool_size=settings.postgres.POOL_SIZE,
    max_overflow=settings.postgres.MAX_OVERFLOW,
)

async_session_maker = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=True,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for getting async session."""
    try:
        async with async_session_maker() as session:
            yield session
    except SQLAlchemyError as e:
        raise e from None
    finally:
        await session.close()
