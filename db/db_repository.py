from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import joinedload
from sqlalchemy import Boolean, select, delete
from datetime import datetime
from db.db import User, Auth, Order, Pizza, OrderContent


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

    async def update_order_status(self, id: UUID, status: int):
        order = await self.db_session.get(Order, id)
        order.status = status
        await self.db_session.commit()
        return True


class PizzaInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_pizza(self, id: UUID, available: Boolean, name: str, cost: float, description: str, image: str) -> Pizza:
        pizza = Pizza(id=id, available=available, name=name,
                      cost=cost, description=description, image=image)
        self.db_session.add(pizza)
        return pizza

    async def get_pizza(self, id: UUID) -> Pizza:
        pizza = await self.db_session.get(Pizza, id)
        return pizza

    async def delete_pizza(self, id: UUID) -> bool:
        pizza = await self.db_session.get(Pizza, id)
        if pizza:
            await self.db_session.execute(delete(OrderContent).where(OrderContent.pizza_id == id))
            await self.db_session.delete(pizza)
            await self.db_session.commit()
            return True
        return False

    async def get_pizza_list(self) -> list[Pizza]:
        res = await self.db_session.execute(select(Pizza))
        return res.scalars().all()

    async def update_pizza(self, id: UUID, available: Boolean, name: str, cost: float, description: str, image: str) -> Pizza:
        pizza = await self.db_session.get(Pizza, id)
        for attr, value in zip(["available", "name", "cost", "description", "image"], [available, name, cost, description, image]):
            if value is not None:
                setattr(pizza, attr, value)
        return pizza


class OrderContentInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_order_content(self, order_id: UUID, pizza_id: UUID, count: int, id: UUID) -> OrderContent:
        order_content = OrderContent(
            order_id=order_id, pizza_id=pizza_id, count=count, id=id)
        self.db_session.add(order_content)
        return order_content

    async def get_order_content(self, order_id: UUID) -> list[OrderContent]:
        order_contents = await self.db_session.execute(select(OrderContent).where(OrderContent.order_id == order_id).options(joinedload(OrderContent.pizza)))
        order_contents = order_contents.scalars().all()
        return [
            {
                "pizza_id": order_content.pizza.id,
                "pizza_name": order_content.pizza.name,
                "pizza_cost": order_content.pizza.cost,
                "count": order_content.count
            } for order_content in order_contents
        ]
