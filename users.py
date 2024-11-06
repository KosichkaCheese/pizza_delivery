from fastapi import APIRouter, Depends
import uuid
from uuid import UUID
from models import Usercreate, Useredit, Pizza
# from sqlalchemy.ext.asyncio import AsyncSession
# from main import session
from db import UserInteract, db_session, AuthInteract, OrderInteract, PizzaInteract, OrderContentInteract
from datetime import datetime

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/create_user")
async def create_user(user: Usercreate, password: str):
    async with db_session() as session:
        async with session.begin():
            user_data = UserInteract(session)
            auth = AuthInteract(session)
            try:
                new_user = await user_data.create_user(
                    email=user.email,
                    role=user.role, 
                    name=user.name, 
                    phone=user.phone, 
                    address=user.address
                )
                new_auth = await auth.create_auth(email=user.email, password=password)
                if new_auth:
                    print(password)
            except Exception as e:
                print("error while creating user:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": new_user}
    
@user_router.get("/get_user")
async def get_user(email: str):
    async with db_session() as session:
        async with session.begin():
            user_data = UserInteract(session)
            try:
                user = await user_data.get_user(email=email)
            except Exception as e:
                print("error while getting user:", e)
                return {"status": 500, "message": "Internal server error"}
            if user:
                return {"status": 200, "data": user}
            else:
                return {"status": 404, "message": "User not found"}

@user_router.delete("/delete_user")
async def delete_user(email: str):
    async with db_session() as session:
        async with session.begin():
            user_data = UserInteract(session)
            try:
                user = await user_data.get_user(email=email)
                if user:
                    res = await user_data.delete_user(email=email)
                else:
                    return {"status": 404, "message": "User not found"}
            except Exception as e:
                print("error while deleting user:", e)
                return {"status": 500, "message": "Internal server error"}
            if res:
                return {"status": 200, "message": "User deleted successfully"}
            else:
                return {"status": 500, "message": "Internal server error"}
        
@user_router.put("/update_user")
async def update_user(user: Useredit):
    async with db_session() as session:
        async with session.begin():
            user_data = UserInteract(session)
            try:
                cur_user = await user_data.get_user(email=user.email)
                if not cur_user:
                    return {"status": 404, "message": "User not found"}
                
                updated_user = await user_data.update_user(
                    email=user.email,
                    name=user.name, 
                    phone=user.phone, 
                    address=user.address
                )
            except Exception as e:
                print("error while updating user:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": updated_user}
        
@user_router.get("/check_auth")
async def check_auth(email: str, password: str):
    async with db_session() as session:
        async with session.begin():
            auth = AuthInteract(session)
            try:
                auth_result = await auth.check_auth(email=email, password=password)
            except Exception as e:
                print("error while checking auth:", e)
                return {"status": 500, "message": "Internal server error"}
            if auth_result:
                return {"status": 200, "message": "Authentication successful"}
            else:
                return {"status": 401, "message": "Authentication failed"}
            
@user_router.post("/add_to_cart")
async def add_to_cart(email: str, pizza_id: UUID, count: int):
    async with db_session() as session:
        async with session.begin():
            try:
                order = OrderInteract(session)
                pizza_interact = PizzaInteract(session)
                user_interact = UserInteract(session)
                user = await user_interact.get_user(email=email)
                pizza = await pizza_interact.get_pizza(id=pizza_id)
                cur_order = await order.current_order(email=email)
                if not cur_order:
                    await order.create_order(id=uuid.uuid4(), user_email=email, time=datetime.now(), summ=(pizza.cost*count), address=user.address, phone=user.phone)
                    cur_order = await order.current_order(email=email)
                order_content = OrderContentInteract(session)
                await order_content.add_order_content(order_id=cur_order.id, pizza_id=pizza_id, count=count, id=uuid.uuid4())
            except Exception as e:
                print("error while adding to cart:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "message": "Pizza added to cart"}

@user_router.get("/get_user_orders")
async def get_user_orders(email: str):
    async with db_session() as session:
        async with session.begin():
            try:
                order_interact = OrderInteract(session)
                orders = await order_interact.get_user_orders(email)
            except Exception as e:
                print("error while getting orders:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": orders}

@user_router.put("/place_order")
async def place_order(email: str, address: str=None, phone: str=None):
    async with db_session() as session:
        async with session.begin():
            try:
                order = OrderInteract(session)
                cur_order = await order.current_order(email=email)
                if not cur_order:
                    return {"status": 404, "message": "cart is empty"}
                if not address or not phone:
                    user_interact = UserInteract(session)
                    user = await user_interact.get_user(email=email)
                    if not phone:
                        phone = user.phone
                    if not address:
                        address = user.address
                order_content_interact = OrderContentInteract(session)
                order_content = await order_content_interact.get_order_content(order_id=cur_order.id)
                new_summ = 0
                for order_content in order_content:
                    new_summ += order_content["pizza_cost"] * order_content["count"]
                cur_time = datetime.now()
                res = await order.place_order(id=cur_order.id, time=cur_time, summ=new_summ, address=address, phone=phone)
                return {"status": 200, "data": res}
            except Exception as e:
                print("error while placing order:", e)

