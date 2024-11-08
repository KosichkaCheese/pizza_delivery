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


class UserInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_user(self, email: str, role: bool, name: str, phone: str, address: str) -> User:
        new_user = User(email=email, role=role, name=name,
                        phone=phone, address=address)
        self.db_session.add(new_user)
        return new_user

    async def get_user(self, email: str) -> User:
        user = await self.db_session.get(User, email)
        return user

    async def delete_user(self, email: str) -> Boolean:
        user = await self.db_session.get(User, email)
        user_auth = await self.db_session.get(Auth, email)
        await self.db_session.delete(user_auth)
        await self.db_session.delete(user)
        await self.db_session.commit()
        return True

    async def update_user(self, email: str, name: Optional[str], phone: Optional[str], address: Optional[str]) -> User:
        user = await self.db_session.get(User, email)
        for attr, value in zip(["name", "phone", "address"], [name, phone, address]):
            if value is not None:
                setattr(user, attr, value)
        return user

    async def get_user_orders(self, email: str) -> list[Order]:
        user = await self.db_session.get(User, email)
        return user.orders


class AuthInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_auth(self, email: str, password: str) -> Boolean:
        auth = Auth(email=email, password=password)
        self.db_session.add(auth)
        return True

    async def check_auth(self, email: str, password: str) -> Boolean:
        auth = await self.db_session.get(Auth, email)
        if auth.password == password:
            return True
        return False


class OrderInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_order(self, id: UUID, user_email: str, time: datetime, summ: float, address: str, phone: str) -> Order:
        order = Order(id=id, user_email=user_email, time=time,
                      summ=summ, address=address, phone=phone)
        self.db_session.add(order)
        return order

    async def get_order(self, id: UUID) -> Order:
        order = await self.db_session.get(Order, id)
        return order

    async def current_order(self, email: str) -> Order:
        res = await self.db_session.execute(select(Order).where(Order.user_email == email, Order.status == 0))
        cur_order = res.scalars().first()
        return cur_order

    async def get_order_list(self) -> list[Order]:
        res = await self.db_session.execute(select(Order))
        orders = res.scalars().all()
        return orders

    async def get_orders_by_status(self, status: int) -> list[Order]:
        res = await self.db_session.execute(select(Order).where(Order.status == status))
        orders = res.scalars().all()
        return orders

    async def get_user_orders(self, u_email: str) -> list[Order]:
        res = await self.db_session.execute(select(Order).where((Order.user_email == u_email) & (Order.status != 0)))
        orders = res.scalars().all()
        return orders

    async def place_order(self, id: UUID, time: datetime, summ: float, address: str, phone: str) -> Order:
        order = await self.db_session.get(Order, id)
        order.time = time
        order.summ = summ
        order.status = 1
        order.address = address
        order.phone = phone
        await self.db_session.commit()
        return order
