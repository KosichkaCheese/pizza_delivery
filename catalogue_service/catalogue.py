import uuid
from uuid import UUID
from api.models import Pizza, Pizzaedit
from db.db import db_session
from db.db_repository import PizzaInteract


async def create_pizza_service(pizza: Pizza):
    async with db_session() as session:
        async with session.begin():
            try:
                pizza_interact = PizzaInteract(session)
                new_pizza = await pizza_interact.create_pizza(id=uuid.uuid4(), available=pizza.available, name=pizza.name, cost=pizza.cost, description=pizza.description, image=pizza.image)
            except Exception as e:
                print("error while creating pizza:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": new_pizza}


async def delete_pizza_service(id: UUID):
    async with db_session() as session:
        async with session.begin():
            try:
                pizza_interact = PizzaInteract(session)
                pizza = await pizza_interact.get_pizza(id=id)
                if not pizza:
                    return {"status": 404, "message": "Pizza not found"}
                await pizza_interact.delete_pizza(id=id)
            except Exception as e:
                print("error while deleting pizza:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "message": "Pizza deleted successfully"}


async def get_pizza_service(id: UUID):
    async with db_session() as session:
        async with session.begin():
            try:
                pizza_interact = PizzaInteract(session)
                pizza = await pizza_interact.get_pizza(id=id)
            except Exception as e:
                print("error while getting pizza:", e)
                return {"status": 500, "message": "Internal server error"}
            if not pizza:
                return {"status": 404, "message": "Pizza not found"}
            return {"status": 200, "data": pizza}


async def get_pizza_list_service():
    async with db_session() as session:
        async with session.begin():
            try:
                pizza_interact = PizzaInteract(session)
                pizzas = await pizza_interact.get_pizza_list()
            except Exception as e:
                print("error while getting pizza list:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": pizzas}


async def update_pizza_service(id: UUID, pizza_data: Pizzaedit):
    async with db_session() as session:
        async with session.begin():
            pizza_data_interact = PizzaInteract(session)
            try:
                cur_pizza = await pizza_data_interact.get_pizza(id=id)
                if not cur_pizza:
                    return {"status": 404, "message": "Pizza not found"}

                updated_pizza = await pizza_data_interact.update_pizza(
                    id=id,
                    available=pizza_data.available,
                    name=pizza_data.name,
                    cost=pizza_data.cost,
                    description=pizza_data.description,
                    image=pizza_data.image
                )
            except Exception as e:
                print("Error while updating pizza:", e)
                return {"status": 500, "message": "Internal server error"}

            return {"status": 200, "data": updated_pizza}


async def pizza_unavailable_service(id: UUID):
    async with db_session() as session:
        async with session.begin():
            try:
                pizza_interact = PizzaInteract(session)
                pizza = await pizza_interact.get_pizza(id=id)
                if not pizza:
                    return {"status": 404, "message": "Pizza not found"}
                new_pizza = await pizza_interact.update_pizza(id=id, available=False, name=None, cost=None, description=None, image=None)
            except Exception as e:
                print("error while updating pizza status:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": new_pizza}
