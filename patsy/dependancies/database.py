from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import Engine
from sqlalchemy.orm import sessionmaker

from patsy.settings import CONFIG, DATABASE

engine: Engine = create_async_engine(DATABASE.database_url, echo=CONFIG.debug, future=True)


async def get_session():
    """Yield an engine session, should used as a dependency."""
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session
