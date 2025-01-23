from fastapi import FastAPI
from fastapi import APIRouter
from uuid import UUID
from api.models import Pizza, Pizzaedit
import catalogue as catalogue

app = FastAPI(title='Catalogue API', version='0.0.1')
main_router = APIRouter()
app.include_router(main_router)


@app.post("/create_pizza")
async def create_pizza(pizza: Pizza):
    result = await catalogue.create_pizza_service(pizza)
    return result


@app.delete("/delete_pizza/{id}")
async def delete_pizza(id: UUID):
    result = await catalogue.delete_pizza_service(id)
    return result


@app.get("/get_pizza/{id}")
async def get_pizza(id: UUID):
    result = await catalogue.get_pizza_service(id)
    return result


@app.get("/get_pizza_list")
async def get_pizza_list():
    result = await catalogue.get_pizza_list_service()
    return result


@app.put("/update_pizza/{id}")
async def update_pizza(id: UUID, pizza_data: Pizzaedit):
    result = await catalogue.update_pizza_service(id, pizza_data)
    return result


@app.put("/pizza_unavailable/{id}")
async def pizza_unavailable(id: UUID):
    result = await catalogue.pizza_unavailable_service(id)
    return result
