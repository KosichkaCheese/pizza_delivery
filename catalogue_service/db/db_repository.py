
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Boolean, select
from db.db import Pizza


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
