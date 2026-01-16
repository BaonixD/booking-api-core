from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from app.core.config import settings
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_async_engine(settings.DATABASE_URL, echo=False)

# Асинхронная фабрика сессий
async_session_maker = async_sessionmaker(bind=engine,
                                   expire_on_commit=False,
                                   class_=AsyncSession
                                   )


class Base(DeclarativeBase):
    pass

async def get_db():
    async with async_session_maker() as session:
        yield session



