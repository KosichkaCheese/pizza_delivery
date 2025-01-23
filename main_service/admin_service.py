# import uuid
import httpx
from uuid import UUID
from api.models import Pizza, Pizzaedit
# from db.db import db_session
# from db.db_repository import OrderInteract, PizzaInteract, OrderContentInteract

ORDERS_SERVICE = "http://order-service:8000"
CATALOGUE_SERVICE = "http://catalogue-service:8000"
PROFILE_SERVICE = "http://profile-service:8000"


async def create_pizza_service(pizza: Pizza):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{CATALOGUE_SERVICE}/create_pizza", json=pizza.model_dump(), headers={"Content-Type": "application/json"})
        except Exception as e:
            print("error while creating pizza:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def delete_pizza_service(id: UUID):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.delete(f"{CATALOGUE_SERVICE}/delete_pizza/{id}")
        except Exception as e:
            print("error while deleting pizza:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def get_pizza_service(id: UUID):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CATALOGUE_SERVICE}/get_pizza/{id}")
        except Exception as e:
            print("error while getting pizza:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def get_pizza_list_service():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{CATALOGUE_SERVICE}/get_pizza_list")
        except Exception as e:
            print("error while getting pizza list:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def update_pizza_service(id: UUID, pizza_data: Pizzaedit):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{CATALOGUE_SERVICE}/update_pizza/{id}", json=pizza_data.model_dump(), headers={"Content-Type": "application/json"})
        except Exception as e:
            print("Error while updating pizza:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def get_order_list_service():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ORDERS_SERVICE}/get_order_list")
        except Exception as e:
            print("error while getting order list:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def get_orders_by_status_service(status: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ORDERS_SERVICE}/get_orders_by_status", params={"status": status})
        except Exception as e:
            print("error while getting orders by status:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def get_order_content_service(id: UUID):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{ORDERS_SERVICE}/get_order_content/{id}")
        except Exception as e:
            print("error while getting order content:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def update_order_status_service(id: UUID, status: int):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{ORDERS_SERVICE}/update_order_status/{id}", params={"status": status})
        except Exception as e:
            print("error while updating order status:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()


async def pizza_unavailable_service(id: UUID):
    async with httpx.AsyncClient() as client:
        try:
            response = await client.put(f"{CATALOGUE_SERVICE}/pizza_unavailable/{id}")
        except Exception as e:
            print("error while updating pizza status:", e)
            return {"status": 500, "message": "Internal server error"}
        return response.json()
