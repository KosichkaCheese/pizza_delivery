from typing import AsyncGenerator, Optional
from sqlalchemy.ext.declarative import declarative_base
import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, DECIMAL, Integer, Text, select
from datetime import datetime

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

    orders = relationship("Order", back_populates="user",
                          cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = 'order'

    id = Column(UUID, primary_key=True, nullable=False)
    user_email = Column(String, ForeignKey('user.email'), nullable=False)
    time = Column(DateTime, nullable=False)
    summ = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Integer, default=0)
    address = Column(String, nullable=False)
    phone = Column(String, nullable=False)

    user = relationship("User", back_populates="orders")
    order_content = relationship(
        "OrderContent", back_populates="order", cascade="all, delete-orphan")


class Auth(Base):
    __tablename__ = 'auth'

    email = Column(String, ForeignKey('user.email'),
                   primary_key=True, nullable=False)
    password = Column(String, nullable=False)

    user = relationship("User")


class Pizza(Base):
    __tablename__ = 'pizza'

    id = Column(UUID, primary_key=True, nullable=False)
    available = Column(Boolean, nullable=False, default=True)
    name = Column(String, nullable=False)
    cost = Column(DECIMAL(10, 2), nullable=False)
    description = Column(Text)
    image = Column(String)


class OrderContent(Base):
    __tablename__ = 'order_content'

    id = Column(UUID, primary_key=True, nullable=False)
    order_id = Column(UUID, ForeignKey('order.id'), nullable=False)
    pizza_id = Column(UUID, ForeignKey('pizza.id'), nullable=False)
    count = Column(Integer, default=1)

    order = relationship("Order", back_populates="order_content")
    pizza = relationship("Pizza")
