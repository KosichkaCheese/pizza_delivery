from fastapi import APIRouter
from uuid import UUID
from api.models import Usercreate, Useredit
import user_service as user_service

user_router = APIRouter(prefix="/users", tags=["users"])


@user_router.post("/create_user")
async def create_user(user: Usercreate, password: str):
    result = await user_service.create_user_service(user, password)
    return result


@user_router.get("/get_user")
async def get_user(email: str):
    result = await user_service.get_user_service(email)
    return result


@user_router.delete("/delete_user")
async def delete_user(email: str):
    result = await user_service.delete_user_service(email)
    return result


@user_router.put("/update_user")
async def update_user(user: Useredit):
    result = await user_service.update_user_service(user)
    return result


@user_router.get("/check_auth")
async def check_auth(email: str, password: str):
    result = await user_service.check_auth_service(email, password)
    return result


@user_router.post("/add_to_cart")
async def add_to_cart(email: str, pizza_id: UUID, count: int):
    result = await user_service.add_to_cart_service(email, pizza_id, count)
    return result


@user_router.delete("/delete_from_cart")
async def delete_from_cart(email: str, pizza_id: UUID):
    result = await user_service.delete_from_cart_service(email, pizza_id)
    return result


@user_router.get("/get_user_orders")
async def get_user_orders(email: str):
    result = await user_service.get_user_orders_service(email)
    return result


@user_router.put("/place_order")
async def place_order(email: str, address: str = None, phone: str = None):
    result = await user_service.place_order_service(email, address, phone)
    return result
