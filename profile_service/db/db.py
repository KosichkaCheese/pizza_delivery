from typing import AsyncGenerator
import settings as settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy import Column, String, Boolean, ForeignKey

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


class User(Base):
    __tablename__ = 'user'

    email = Column(String, nullable=False, unique=True, primary_key=True)
    role = Column(Boolean, nullable=False, default=USER)
    name = Column(String, default='')
    phone = Column(String, unique=True)
    address = Column(String, default='')


class Auth(Base):
    __tablename__ = 'auth'

    email = Column(String, ForeignKey('user.email'),
                   primary_key=True, nullable=False)
    password = Column(String, nullable=False)

    user = relationship("User")
