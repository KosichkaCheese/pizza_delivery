from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import select
from datetime import datetime
from db.db import Order, OrderContent
import httpx


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


class OrderContentInteract:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def add_order_content(self, order_id: UUID, pizza_id: UUID, count: int, id: UUID) -> OrderContent:
        order_content = OrderContent(
            order_id=order_id, pizza_id=pizza_id, count=count, id=id)
        self.db_session.add(order_content)
        return order_content

    async def get_order_content(self, order_id: UUID) -> list[OrderContent]:
        order_contents = await self.db_session.execute(select(OrderContent).where(OrderContent.order_id == order_id))
        order_contents = order_contents.scalars().all()
        res = []
        for order_content in order_contents:
            async with httpx.AsyncClient() as client:
                pizza = await client.get(f"http://catalogue-service:8000/get_pizza/{order_content.pizza_id}")
                pizza = pizza.json()["data"]
            res.append({
                "pizza_id": pizza["id"],
                "pizza_name": pizza["name"],
                "pizza_cost": pizza["cost"],
                "count": order_content.count
            })
        return res
