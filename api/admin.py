from fastapi import APIRouter
from uuid import UUID
from api.models import Pizza, Pizzaedit
import services.admin_service as admin_service


admin_router = APIRouter(prefix="/admin", tags=["admin"])


@admin_router.post("/create_pizza")
async def create_pizza(pizza: Pizza):
    result = await admin_service.create_pizza_service(pizza)
    return result


@admin_router.delete("/delete_pizza")
async def delete_pizza(id: UUID):
    result = await admin_service.delete_pizza_service(id)
    return result


@admin_router.get("/get_pizza")
async def get_pizza(id: UUID):
    result = await admin_service.get_pizza_service(id)
    return result


@admin_router.get("/get_pizza_list")
async def get_pizza_list():
    result = await admin_service.get_pizza_list_service()
    return result


@admin_router.put("/update_pizza")
async def update_pizza(id: UUID, pizza_data: Pizzaedit):
    result = await admin_service.update_pizza_service(id, pizza_data)
    return result


@admin_router.post("/get_order_list")
async def get_all_orders():
    result = await admin_service.get_order_list_service()
    return result


@admin_router.get("/get_orders_by_status")
async def get_orders_by_status(status: int):
    result = await admin_service.get_orders_by_status_service(status)
    return result
