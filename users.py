from fastapi import APIRouter
from models import Usercreate
# from main import session
from db import UserInteract, db_session

user_router = APIRouter(prefix="/users", tags=["users"])

@user_router.post("/create_user")
async def create_user(user: Usercreate):
    async with db_session() as session:
        async with session.begin():
            user_data = UserInteract(session)
            try:
                new_user = await user_data.create_user(
                    email=user.email,
                    role=user.role, 
                    name=user.name, 
                    phone=user.phone, 
                    address=user.address
                )
            except Exception as e:
                print("error while creating user:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "data": new_user}
