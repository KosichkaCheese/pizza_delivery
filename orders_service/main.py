from fastapi import FastAPI
from fastapi import APIRouter
from uuid import UUID
import orders

app = FastAPI(title='Orders API', version='0.0.1')

main_router = APIRouter()
app.include_router(main_router)


@app.post("/add_to_cart/{pizza_id}")
async def add_to_cart(email: str, pizza_id: UUID, count: int):
    result = await orders.add_to_cart_service(email, pizza_id, count)
    return result


@app.get("/get_user_orders")
async def get_user_orders(email: str):
    result = await orders.get_user_orders_service(email)
    return result


@app.put("/place_order")
async def place_order(email: str, address: str = None, phone: str = None):
    result = await orders.place_order_service(email, address, phone)
    return result


@app.get("/get_order_list")
async def get_all_orders():
    result = await orders.get_order_list_service()
    return result


@app.get("/get_orders_by_status")
async def get_orders_by_status(status: int):
    result = await orders.get_orders_by_status_service(status)
    return result


@app.get("/get_order_content/{order_id}")
async def get_order_content(order_id: UUID):
    result = await orders.get_order_content_service(order_id)
    return result


@app.put("/update_order_status/{order_id}")
async def update_order_status(order_id: UUID, status: int):
    result = await orders.update_order_status_service(order_id, status)
    return result


@app.delete("/delete_from_cart/{pizza_id}")
async def delete_from_cart(email: str, pizza_id: UUID):
    result = await orders.delete_from_cart_service(email, pizza_id)
    return result
