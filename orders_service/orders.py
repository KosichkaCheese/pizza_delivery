import uuid
from uuid import UUID
from db.db import db_session
from db.db_repository import OrderInteract, OrderContentInteract
from datetime import datetime
import httpx

CATALOGUE_SERVICE = "http://catalogue-service:8000"
PROFILE_SERVICE = "http://profile-service:8000"


async def add_to_cart_service(email: str, pizza_id: UUID, count: int):
    async with db_session() as session:
        async with session.begin():
            try:
                order = OrderInteract(session)
                # pizza_interact = PizzaInteract(session)
                # user_interact = UserInteract(session)
                # user = await user_interact.get_user(email=email)
                # pizza = await pizza_interact.get_pizza(id=pizza_id)

                async with httpx.AsyncClient() as client:
                    response = await client.get(f"{CATALOGUE_SERVICE}/get_pizza/{pizza_id}")
                    response = response.json()
                    if response["status"] != 200:
                        return response
                    pizza = response["data"]

                    response = await client.get(f"{PROFILE_SERVICE}/get_user/{email}")
                    response = response.json()
                    if response["status"] != 200:
                        return response
                    user = response["data"]

                cur_order = await order.current_order(email=email)
                if not cur_order:
                    await order.create_order(id=uuid.uuid4(), user_email=email, time=datetime.now(), summ=(pizza["cost"]*count), address=user["address"], phone=user["phone"])
                    cur_order = await order.current_order(email=email)
                else:
                    summ = float(cur_order.summ) + (pizza["cost"]*count)
                    await order.change_summ(id=cur_order.id, summ=summ)
                order_content = OrderContentInteract(session)
                await order_content.add_order_content(order_id=cur_order.id, pizza_id=pizza_id, count=count, id=uuid.uuid4())
            except Exception as e:
                print("error while adding to cart:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "message": "Pizza added to cart"}


async def delete_from_cart_service(email: str, pizza_id: UUID):
    async with db_session() as session:
        async with session.begin():
            try:
                order = OrderInteract(session)
                cur_order = await order.current_order(email=email)
                if not cur_order:
                    return {"status": 404, "message": "cart is empty"}
                order_content_interact = OrderContentInteract(session)
                res = await order_content_interact.delete_from_cart(order_id=cur_order.id, pizza_id=pizza_id)

                order_content = await order_content_interact.get_order_content(order_id=cur_order.id)
                new_summ = 0
                for order_content in order_content:
                    new_summ += order_content["pizza_cost"] * \
                        order_content["count"]
                await order.change_summ(id=cur_order.id, summ=new_summ)

            except Exception as e:
                print("error while deleting from cart:", e)
                return {"status": 500, "message": "Internal server error"}
            if res:
                return {"status": 200, "message": "Pizza deleted from cart"}
            else:
                return {"status": 404, "message": "Pizza not found in cart"}


async def get_user_orders_service(email: str):
    async with db_session() as session:
        async with session.begin():
            try:
                order_interact = OrderInteract(session)
                orders = await order_interact.get_user_orders(email)
            except Exception as e:
                print("error while getting orders:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": orders}


async def place_order_service(email: str, address: str = None, phone: str = None):
    async with db_session() as session:
        async with session.begin():
            try:
                order = OrderInteract(session)
                cur_order = await order.current_order(email=email)
                if not cur_order:
                    return {"status": 404, "message": "cart is empty"}
                if not address or not phone:
                    # user_interact = UserInteract(session)
                    # user = await user_interact.get_user(email=email)

                    async with httpx.AsyncClient() as client:
                        response = await client.get(f"{PROFILE_SERVICE}/get_user/{email}")
                        response = response.json()
                        if response["status"] != 200:
                            return response
                        user = response["data"]

                    if not phone:
                        phone = user["phone"]
                    if not address:
                        address = user["address"]
                order_content_interact = OrderContentInteract(session)
                order_content = await order_content_interact.get_order_content(order_id=cur_order.id)
                new_summ = 0
                for order_content in order_content:
                    new_summ += order_content["pizza_cost"] * \
                        order_content["count"]
                cur_time = datetime.now()
                res = await order.place_order(id=cur_order.id, time=cur_time, summ=new_summ, address=address, phone=phone)
                return {"status": 200, "data": res}
            except Exception as e:
                print("error while placing order:", e)


async def get_order_list_service():
    async with db_session() as session:
        async with session.begin():
            try:
                order_interact = OrderInteract(session)
                orders = await order_interact.get_order_list()
            except Exception as e:
                print("error while getting order list:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": orders}


async def get_orders_by_status_service(status: int):
    async with db_session() as session:
        async with session.begin():
            try:
                order_interact = OrderInteract(session)
                orders = await order_interact.get_orders_by_status(status=status)
            except Exception as e:
                print("error while getting orders by status:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": orders}


async def get_order_content_service(id: UUID):
    async with db_session() as session:
        async with session.begin():
            try:
                orderc_interact = OrderContentInteract(session)
                content = await orderc_interact.get_order_content(order_id=id)
            except Exception as e:
                print("error while getting order content:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": content}


async def update_order_status_service(id: UUID, status: int):
    async with db_session() as session:
        async with session.begin():
            try:
                if status < 0 or status > 4:
                    return {"status": 400, "message": "Invalid status"}
                order_interact = OrderInteract(session)
                await order_interact.update_order_status(id=id, status=status)
            except Exception as e:
                print("error while updating order status:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "message": "Order status updated successfully"}
