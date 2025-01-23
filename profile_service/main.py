from fastapi import FastAPI
from fastapi import APIRouter
from api.models import Usercreate, Useredit
import user_service as user_service

app = FastAPI(title='Profile API', version='0.0.1')
main_router = APIRouter()
app.include_router(main_router)


@app.post("/create_user")
async def create_user(user: Usercreate, password: str):
    result = await user_service.create_user_service(user, password)
    return result


@app.get("/get_user/{email}")
async def get_user(email: str):
    result = await user_service.get_user_service(email)
    return result


@app.delete("/delete_user/{email}")
async def delete_user(email: str):
    result = await user_service.delete_user_service(email)
    return result


@app.put("/update_user")
async def update_user(user: Useredit):
    result = await user_service.update_user_service(user)
    return result


@app.get("/check_auth")
async def check_auth(email: str, password: str):
    result = await user_service.check_auth_service(email, password)
    return result
