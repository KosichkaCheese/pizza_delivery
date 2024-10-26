from fastapi import APIRouter, Depends
import uuid
from uuid import UUID
from models import Usercreate, Useredit, Pizza, Pizzaedit
# from sqlalchemy.ext.asyncio import AsyncSession
# from main import session
from db import UserInteract, db_session, AuthInteract, OrderInteract, PizzaInteract, OrderContentInteract
from datetime import datetime


admin_router = APIRouter(prefix="/admin", tags=["admin"])
@admin_router.post("/create_pizza")
async def create_pizza(pizza: Pizza):               
    
    async with db_session() as session:
        async with session.begin():
            try:
                pizza_interact = PizzaInteract(session)
                new_pizza = await pizza_interact.create_pizza(id=uuid.uuid4(), name=pizza.name, cost=pizza.cost, description=pizza.description, image=pizza.image)
            except Exception as e:
                print("error while creating pizza:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": new_pizza}
        
@admin_router.delete("/delete_pizza")
async def delete_pizza(id: UUID):
    async with db_session() as session:
        async with session.begin():
            try:
                pizza_interact = PizzaInteract(session)
                await pizza_interact.delete_pizza(id=id)
            except Exception as e:
                print("error while deleting pizza:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "message": "Pizza deleted successfully"}
        
@admin_router.get("/get_pizza")
async def get_pizza(id: UUID):
    async with db_session() as session:
        async with session.begin():
            try:
                pizza_interact = PizzaInteract(session)
                pizza = await pizza_interact.get_pizza(id=id)
            except Exception as e:
                print("error while getting pizza:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": pizza}
        
@admin_router.get("/get_pizza_list")
async def get_pizza_list():
    async with db_session() as session:
        async with session.begin():
            try:
                pizza_interact = PizzaInteract(session)
                pizzas = await pizza_interact.get_pizza_list()
            except Exception as e:
                print("error while getting pizza list:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": pizzas}
         
@admin_router.put("/update_pizza")               
async def update_pizza(id: UUID, pizza_data: Pizzaedit):
    async with db_session() as session:
        async with session.begin():
            pizza_data_interact = PizzaInteract(session)
            try:
                cur_pizza = await pizza_data_interact.get_pizza(id=id)
                if not cur_pizza:
                    return {"status": 404, "message": "Pizza not found"}

                updated_pizza = await pizza_data_interact.update_pizza(
                    id=id,
                    name=pizza_data.name,
                    cost=pizza_data.cost,
                    description=pizza_data.description,
                    image=pizza_data.image
                )
            except Exception as e:
                print("Error while updating pizza:", e)
                return {"status": 500, "message": "Internal server error"}
            
            return {"status": 200, "data": updated_pizza}             
                
@admin_router.post("/get_order_list")
async def get_all_orders():
    async with db_session() as session:
        async with session.begin():
            try:
                order_interact = OrderInteract(session)
                orders = await order_interact.get_order_list()
            except Exception as e:
                print("error while getting order list:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": orders}

@admin_router.get("/get_orders_by_status")
async def get_orders_by_status(status: int):
    async with db_session() as session:
        async with session.begin():
            try:
                order_interact = OrderInteract(session)
                orders = await order_interact.get_orders_by_status(status=status)
            except Exception as e:
                print("error while getting orders by status:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": orders}
        