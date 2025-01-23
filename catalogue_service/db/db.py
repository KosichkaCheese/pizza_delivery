from typing import AsyncGenerator
# from sqlalchemy.ext.declarative import declarative_base
import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, DECIMAL, Text

ADMIN = True
USER = False

engine = create_async_engine(settings.DATABASE_URL)
db_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator:
    try:
        session: AsyncSession = db_session()
        yield session
    finally:
        await session.close()

Base = declarative_base()


class Pizza(Base):
    __tablename__ = 'pizza'

    id = Column(UUID, primary_key=True, nullable=False)
    available = Column(Boolean, nullable=False, default=True)
    name = Column(String, nullable=False)
    cost = Column(DECIMAL(10, 2), nullable=False)
    description = Column(Text)
    image = Column(String)
