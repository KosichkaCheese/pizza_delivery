# import uuid
import httpx
from uuid import UUID
from api.models import Usercreate, Useredit
# from db.db import db_session
# from db.db_repository import AuthInteract, OrderInteract, PizzaInteract, OrderContentInteract, UserInteract
# from datetime import datetime

ORDERS_SERVICE = "http://order-service:8000"
CATALOGUE_SERVICE = "http://catalogue-service:8000"
PROFILE_SERVICE = "http://profile-service:8000"


async def create_user_service(user: Usercreate, password: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{PROFILE_SERVICE}/create_user", json=user.model_dump(), params={"password": password}, headers={"Content-Type": "application/json"})
        except Exception as e:
            print("error while creating user:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def get_user_service(email: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PROFILE_SERVICE}/get_user/{email}")
        except Exception as e:
            print("error while getting user:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def delete_user_service(email: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{PROFILE_SERVICE}/delete_user/{email}")
        except Exception as e:
            print("error while deleting user:", e)
            return {"status": 500, "message": "Internal server error"}
        return response


async def update_user_service(user: Useredit):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{PROFILE_SERVICE}/update_user", json=user.model_dump(), headers={"Content-Type": "application/json"})
        except Exception as e:
            print("error while updating user:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def check_auth_service(email: str, password: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{PROFILE_SERVICE}/check_auth", params={"email": email, "password": password})
        except Exception as e:
            print("error while checking auth:", e)
            return {"status": 500, "message": "Internal server error"}
        return response


async def add_to_cart_service(email: str, pizza_id: UUID, count: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{ORDERS_SERVICE}/add_to_cart", params={"email": email, "pizza_id": pizza_id, "count": count})
        except Exception as e:
            print("error while adding to cart:", e)
            return {"status": 500, "message": "Internal server error"}
        return response


async def get_user_orders_service(email: str):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ORDERS_SERVICE}/get_user_orders", params={"email": email})
        except Exception as e:
            print("error while getting orders:", e)
            return {"status": 500, "message": "Internal server error"}
        return response


async def place_order_service(email: str, address: str = None, phone: str = None):
    async with httpx.AsyncClient() as client:
        try:
            params = {"email": email, "address": address, "phone": phone}
            params = {k: v for k, v in params.items() if v is not None}
            response = await client.post(f"{ORDERS_SERVICE}/place_order", params=params)
        except Exception as e:
            print("error while placing order:", e)
        return response
