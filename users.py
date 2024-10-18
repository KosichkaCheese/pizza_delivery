from fastapi import APIRouter
from models import Usercreate, Useredit
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
                    await session.delete(user)
                else:
                    return {"status": 404, "message": "User not found"}
            except Exception as e:
                print("error while deleting user:", e)
                return {"status": 500, "message": "Internal server error"}
            return {"status": 200, "message": "User deleted successfully"}
        
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
