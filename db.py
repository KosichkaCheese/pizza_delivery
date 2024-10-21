from typing import AsyncGenerator, Optional
from sqlalchemy.ext.declarative import declarative_base
import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime, DECIMAL, Integer, Text, select
from datetime import datetime

ADMIN=True
USER=False

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
    
    orders = relationship("Order", back_populates="user")

class Order(Base):
    __tablename__ = 'order'
    
    id = Column(UUID, primary_key=True, nullable=False)
    user_email = Column(String, ForeignKey('user.email'), nullable=False)
    time = Column(DateTime, nullable=False)
    summ = Column(DECIMAL(10, 2), nullable=False)
    status = Column(Integer, default=0)
    
    user = relationship("User", back_populates="orders")
  
class Auth(Base):
    __tablename__ = 'auth'
    
    email = Column(String, ForeignKey('user.email'), primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    
    user=relationship("User")

class Pizza(Base):
    __tablename__ = 'pizza'
    
    id = Column(UUID, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    cost = Column(DECIMAL(10, 2), nullable=False)
    description = Column(Text)
    image = Column(String)

class OrderContent(Base):
    __tablename__ = 'order_content'
    
    order_id = Column(UUID, ForeignKey('order.id'), nullable=False, primary_key=True)
    pizza_id = Column(UUID, ForeignKey('pizza.id'), nullable=False)
    count = Column(Integer, default=1)
  
class UserInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def create_user(self, email: str, role: bool, name: str, phone: str, address: str) -> User:
        new_user = User(email=email, role=role, name=name, phone=phone, address=address)
        self.db_session.add(new_user)
        return new_user
    
    async def get_user(self, email: str) -> User:
        user = await self.db_session.get(User, email)
        return user
    
    async def delete_user(self, email: str)->Boolean:
        user = await self.db_session.get(User, email)
        self.db_session.delete(user)
        return True
    
    async def update_user(self, email: str, name: Optional[str], phone: Optional[str], address: Optional[str])->User:
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
        auth=Auth(email=email, password=password)
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

    async def create_order(self, id: UUID, user_email: str, time: datetime, summ: float) -> Order:
        order = Order(id=id, user_email=user_email, time=time, summ=summ)
        self.db_session.add(order)
        return order
    
    async def get_order(self, id: UUID) -> Order:
        order = await self.db_session.get(Order, id)
        return order
    
    async def current_order(self, email: str) -> Order:
        res = await self.db_session.execute(select(Order).where(Order.user_email == email, Order.status == 0))
        cur_order = res.scalars().first()
        return cur_order
    
    #изменить сумму
    #изменить статус + поменять время на актуальное
    
class PizzaInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def create_pizza(self, id: UUID, name: str, cost: float, description: str, image: str) -> Pizza:
        pizza = Pizza(id=id, name=name, cost=cost, description=description, image=image)
        self.db_session.add(pizza)
        return pizza

    async def get_pizza(self, id: UUID) -> Pizza:
        pizza = await self.db_session.get(Pizza, id)
        return pizza

class OrderContentInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
    
    async def add_order_content(self, order_id: UUID, pizza_id: UUID, count: int) -> OrderContent:
        order_content = OrderContent(order_id=order_id, pizza_id=pizza_id, count=count)
        self.db_session.add(order_content)
        return order_content
    
    async def get_order_content(self, order_id: UUID) -> list[OrderContent]:
        order_content = await self.db_session.get(OrderContent, order_id)
        return order_content
    