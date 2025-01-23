from typing import AsyncGenerator
# from sqlalchemy.ext.declarative import declarative_base
import settings as settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, relationship, declarative_base
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, ForeignKey, DateTime, DECIMAL, Integer

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


class Order(Base):
    __tablename__ = 'order'

    id = Column(UUID, primary_key=True, nullable=False)
    user_email = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    summ = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Integer, default=0)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    order_content = relationship(
        "OrderContent", back_populates="order", cascade="all, delete-orphan")


class OrderContent(Base):
    __tablename__ = 'order_content'

    id = Column(UUID, primary_key=True, nullable=False)
    order_id = Column(UUID, ForeignKey('order.id'), nullable=False)
    pizza_id = Column(UUID, nullable=False)
    count = Column(Integer, default=1)

    order = relationship("Order", back_populates="order_content")
